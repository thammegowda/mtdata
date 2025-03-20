from pathlib import Path
from typing import List, Iterator, Tuple
from itertools import zip_longest
from pymarian import Evaluator
from pymarian.utils import get_model_path, get_vocab_path


from . import log, pbar_man, Defaults
from  .entry import LangPair
from .utils import IO


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
        src_lang, tgt_lang = self.langs
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


class PyMarianScorer:

    def __init__(self, metric:str, langs:Tuple[str,str], quiet=False, fp16=False, **kwargs):
        self.metric = metric
        self.langs = langs
        self.quiet = quiet
        self.fp16 = fp16
        self._evaluator = None  # lazy load
        self.width = kwargs.get('width', 4)
        self.eval_args = kwargs

    @property
    def evaluator(self):
        if self._evaluator is None:
            model = get_model_path(self.metric)
            vocab = get_vocab_path(self.metric)
            log.info(f'Loading {self.metric};  model={model} vocab={vocab}')
            if not model.exists() or not vocab.exists():
                raise ValueError(f'Model or vocab not found for {metric}.')
            eval_args = dict(like='comet-qe', quiet=self.quiet, fp16=self.fp16)
            eval_args.update(self.eval_args)
            self._evaluator = Evaluator.new(model_file=model, vocab_file=vocab, **eval_args)
        return self._evaluator

    def score_all(self, work_dir: Path):
        """
        Score the translations in the work_dir using the specified metric.
        """
        log.info(f'Scoring {work_dir} with {self.metric}')
        dataset = LocalDataset(work_dir, self.langs)
        parts = dataset.list_parallel_parts()
        fp16 = self.fp16 and ".fp16" or ""
        log.info(f'Found {len(parts)} parts')
        for part_num, (did, src_file, tgt_file) in enumerate(parts):
            out_file = src_file.parent / f'{did}.{self.metric}.score{fp16}.gz'
            if out_file.exists() and out_file.stat().st_size > 0:
                log.info(f'Skipping {src_file.name} {tgt_file.name} (already scored)')
                continue
            log.info(f"Scoring: {did} -> {out_file}")
            tmp_file = out_file.with_name(out_file.name + '.tmp.gz')
            log.info(f'Scoring {src_file.name} {tgt_file.name}')
            src_lines = IO.get_lines(src_file)
            tgt_lines = IO.get_lines(tgt_file)

            desc = f'[{part_num}/{len(parts)}] Scoring {did}'
            with pbar_man.counter(unit='it', desc=desc, leave=False, min_delta=Defaults.PBAR_REFRESH_INTERVAL,
                                    autorefresh=True) as pbar:
                if tmp_file.exists():
                    line_count = sum(1 for _ in IO.get_lines(tmp_file))
                    if line_count > 0:
                        log.warning(f"File {tmp_file} already exists. Seek input with {line_count} lines")
                        for i, _ in enumerate(zip_longest(src_lines, tgt_lines)):
                            pbar.update(1)
                            if i >= line_count:
                                break
                with IO.writer(tmp_file, 'a') as out:
                        for score in self.score(src_lines, tgt_lines):
                            out.write(f'{score:.{self.width}f}\n')
                            pbar.update(1)
                pbar.close()

            # move tmp_file to out_file
            tmp_file.rename(out_file)

    def score(self, srcs: Iterator[str], mts: Iterator[str]) -> Iterator[float]:
        mn = self.eval_args.get('mini_batch', 64)
        mx = self.eval_args.get('maxi_batch', 1024)
        buffer_size = mn * mx
        def make_maxi_batches(batch_size=buffer_size):
            batch = []
            for s, t in zip_longest(srcs, mts):
                batch.append(f"{s}\t{t}")
                if len(batch) >= batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch

        for batch in make_maxi_batches():
            yield from self.evaluator.evaluate(batch)
