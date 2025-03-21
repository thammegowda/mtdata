from pathlib import Path
from typing import List, Iterator, Tuple
from itertools import zip_longest
import subprocess as sp
import os

from pymarian import Evaluator
from pymarian.utils import get_model_path, get_vocab_path


from . import log, pbar_man, Defaults
from  .entry import LangPair
from .utils import IO
from .map import SubprocMapper, read_paths


class LocalDataset:

    def __init__(self, root, langs:LangPair, compress=True):
        self.langs = langs
        self.root = Path(root)
        self.compress = compress
        assert self.langs is not None, "Language pair must be specified"
        assert self.root.exists(), f"Dataset root {self.root} does not exist"
        assert self.root.is_dir(), f"Dataset root {self.root} is not a directory"

    def list_parallel_parts(self, subdir="train-parts") -> List[Tuple[Path, Path]]:
        """
        List the parallel parts of the dataset.
        """
        # * is added to match script or country tags
        src_ext = f'{self.langs[0]}*' + (self.compress and ".gz" or "")
        tgt_ext = f'{self.langs[1]}*' + (self.compress and ".gz" or "")
        parts = []
        for src_file in self.root.glob(f'{subdir}/*.{src_ext}'):
            n_exts_parts = len(src_ext.split('.'))
            did = '.'.join(src_file.name.split('.')[:-n_exts_parts])
            tgt_files = list(src_file.parent.glob(f'{did}.{tgt_ext}'))
            if len(tgt_files) != 1:
                log.warning(f"Expected 1 target file for {src_file.parent}/{did}.{tgt_ext}, found {len(tgt_files)}")
            tgt_file = tgt_files[0] if len(tgt_files) == 1 else None
            parts.append((did, src_file, tgt_file))
        if len(parts) == 0:
            log.warning(f"No parallel parts found in {subdir} for {self.langs}")
        else:
            log.info(f"Found {len(parts)} parallel parts in {subdir} for {self.langs}")
        return parts


class PyMarianScorer():

    def __init__(self, metric:str, langs:Tuple[str,str], quiet=False, fp16=False, **kwargs):
        self.metric = metric
        self.langs = langs
        self.quiet = quiet
        self.fp16 = fp16
        self.eval_args = kwargs

    def score_all(self, work_dir: Path):
        """
        Score the translations in the work_dir using the specified metric.
        """
        log.info(f'Scoring {work_dir} with {self.metric}')
        dataset = LocalDataset(work_dir, self.langs)
        parts = dataset.list_parallel_parts()
        fp16 = self.fp16 and ".fp16" or ""
        log.info(f'Found {len(parts)} parts')
        all_paths = []
        for part_num, (did, src_file, tgt_file) in enumerate(parts):
            out_file = src_file.parent / f'{did}.{self.metric}.score{fp16}.gz'
            if out_file.exists() and out_file.stat().st_size > 0:
                log.info(f'Skipping {src_file.name} {tgt_file.name} (already scored)')
                continue
            all_paths.append((src_file, tgt_file, out_file))

        cmdline = f"pymarian-eval --stdin -m {self.metric} -a skip"
        if not self.quiet:
            cmdline += " --debug"
        if self.fp16:
            cmdline += " --fp16"
        for k,v in self.eval_args.items():
            k = k.replace('_', '-')
            cmdline += f" --{k} {v}"
        if os.getenv('PYMARIAN_CACHE'):
            cmdline += f" --cache {os.getenv('PYMARIAN_CACHE')}"

        # get internal command which is purely c++ and a bit more efficient than python wrapper
        cmdline = sp.check_output(cmdline + " --print-cmd", text=True, shell=True).strip()
        if cmdline.startswith("marian "):
            # older version used "marian evaluate", make it "pymarian evaluate"
            cmdline = f"py{cmdline}"
        stream = read_paths(all_paths)
        mapper = SubprocMapper(cmdline=cmdline)
        try:
            out_stream = mapper(stream)
            out_path = None
            tmp_path = None
            writer = None
            desc = f'Scoring {len(all_paths)} parts with {self.metric}'
            with pbar_man.counter(unit='it', desc=desc, min_delta=Defaults.PBAR_REFRESH_INTERVAL,
                                    autorefresh=True) as pbar:
                for rec in out_stream:
                    if isinstance(rec, dict):
                        if writer is not None:
                            writer.close()  # close the previous writer
                            tmp_path.rename(out_path)  # rename the tmp file to the final output file
                            log.info(f"Renamed {tmp_path} to {out_path}")
                        out_path = rec['output']
                        tmp_path = out_path.with_name('.tmp.' + out_path.name)
                        log.info(f"Writing to {tmp_path}")
                        tmp_path.unlink(missing_ok=True)  # remove the tmp file if it exists
                        tmp_path.parent.mkdir(parents=True, exist_ok=True)
                        writer = IO.writer(tmp_path).__enter__()
                    else:
                        writer.write(rec + '\n')
                        pbar.update(1)
            if writer is not None:
                writer.close()
                tmp_path.rename(out_path)  # rename the tmp file to the final output file
        finally:
            mapper.close()
