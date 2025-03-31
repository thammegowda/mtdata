#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20

from typing import Optional, Union, Tuple, List
from dataclasses import dataclass
from pathlib import Path
from mtdata import log, pbar_man, Defaults
from mtdata.entry import Entry
from itertools import zip_longest

from mtdata.utils import IO

COMPRESS_EXT = ['gz', 'bz2', 'xz']
HF_EXT = 'hfds'  # huggingface dataset
WMT21XML = 'wmt21xml'


def detect_extension(name: Union[str, Path]):
    """
    detects file extension from file name
    :param filename: name or full path of file
    :return: extension of file
    """

    filename = name if isinstance(name, str) else name.name
    parts = filename.split('.')
    ext = parts[-1]
    if ext in COMPRESS_EXT:
        ext = '.'.join(parts[-2:])
    return ext


@dataclass
class Parser:
    paths: Union[Path, List[Path]]
    ext: Optional[str] = None
    ent: Optional['Entry'] = None

    def __post_init__(self):
        if not isinstance(self.paths, list):
            self.paths = [self.paths]
        for p in self.paths:
            if isinstance(p, Path):
                assert p.exists(), f'{p} not exists'
            # skip cheks on HF datasets

        if not self.ext:
            exts = [detect_extension(p.name) for p in self.paths]
            if len(exts) == 2:
                did = self.ent and self.ent.did or ''
                log.warning(f"{did} :: Treating {' .'.join(exts)} as plain text. To override: in_ext=<ext>")
                exts = ['txt']  # treat that as plain text
            assert len(set(exts)) == 1, f'Expected a type of exts, but found: {exts}'
            self.ext = exts[0]
        assert 1 <= len(self.paths)
        # tsv and tmx just concatenate all of them
        assert len(self.paths) <= 3 or self.ext == 'tmx' or self.ext == 'tsv'

    def read_segs(self):
        readers = []
        if self.ext == 'opus_xces':
            preprocessing = 'xml'
            if "/raw/" in self.ent.in_paths[0]:
                preprocessing = 'raw'
            align, lang1_dir, lang2_dir = self.paths
            from mtdata.opus_xces import OpusXcesParser
            reader = OpusXcesParser.read(align, lang1_dir, lang2_dir, preprocessing=preprocessing)
            readers.append(reader)
        else:
            meta_fields = self.ent.meta and self.ent.meta.get('fields') or None
            for p in self.paths:
                if 'tsv' in self.ext:
                    cols = (0, 1) #extract first two columns
                    if self.ent and self.ent.cols:
                        cols = self.ent.cols
                    readers.append(self.read_tsv(p, cols=cols, meta_fields=meta_fields))
                elif 'csvwithheader' in self.ext:
                    readers.append(self.read_tsv(p, delim=',', skipheader=True, meta_fields=meta_fields))
                elif 'raw' in self.ext or 'txt' in self.ext:
                    readers.append(self.read_plain(p))
                elif 'tmx' in self.ext:
                    from mtdata.tmx import read_tmx
                    readers.append(read_tmx(path=p, langs=self.ent.did.langs))
                elif 'sgm' in self.ext:
                    from mtdata.sgm import read_sgm
                    readers.append(read_sgm(p))
                elif WMT21XML in self.ext:
                    from mtdata.sgm import read_wmt21_xml
                    readers.append(read_wmt21_xml(p))
                elif HF_EXT in self.ext:
                    readers.append(self.read_hfds(p))
                else:
                    raise Exception(f'Not supported {self.ext} : {p}')

        if len(readers) == 1:
            data = readers[0]
        elif self.ext == 'tmx' or self.ext == 'tsv':
            data = (rec for reader in readers for rec in reader)  # flatten all readers
        elif len(readers) == 2:
            def _zip_n_check():
                for row in zip_longest(*readers):
                    seg1, seg2 = row[:2]
                    if seg1 is None or seg2 is None:
                        raise Exception(f'{self.paths} have unequal number of segments')
                    yield seg1, seg2
            data = _zip_n_check()
        else:
            raise Exception("This is an error")
        with pbar_man.counter(color='green', unit='seg', leave=False, desc=f"Reading {self.ent.did}", autoregresh=True, 
                              min_delta=Defaults.PBAR_REFRESH_INTERVAL) as pbar:
            for rec in data:
                yield rec
                pbar.update()

    def read_plain(self, path):
        try:
            with IO.reader(path) as stream:
                for line in stream:
                    yield line.strip()
        except:
            log.warning(f'Error reading file {path}')
            raise

    def read_tsv(self, path, delim='\t', cols=None, skipheader=False, meta_fields=None):
        """
        Read data from TSV file
        :param path: path to TSV file
        :param delim: delimiter default is \\t
        :param cols: if certain columns are to be extracted;
            default is None, which returns all columns
        :return:
        """
        with IO.reader(path) as stream:
            if skipheader:
                line = stream.readline()
            for line in stream:
                row = [x.strip() for x in line.rstrip('\n').split(delim)]
                out_row = row
                if cols:
                    out_row = [row[idx] for idx in cols]
                if meta_fields:
                    metadata = {}
                    for key, idx in meta_fields.items():
                        if key in ("source", "target") or idx >= len(row) or row[idx] in ("", None):
                            continue
                        metadata[key] = row[idx]
                    if metadata:
                        out_row.append(metadata)
                yield out_row

    def read_hfds(self, ds):
        """ Read data from huggingface Dataset
        :param ds: huggingface dataset
        :return: generator of segments
        """
        fields = self.ent.meta["fields"]  # expects dictionary
        src_field = fields['source']
        tgt_field = fields.get('target', None)
        rev_map = {v: k for k, v in fields.items()}
        # fields map is a forward map of "dest: orig", and meant to pick a subset of fields from the row
        # in the current version, I am going to retain all fields to see what all fields exist,
        # and map the subset of fields as per the dict; so, created rev_map.get(orig,orig)
        for row in ds:
            out_row = [row.pop(src_field)]
            if tgt_field is not None:
                out_row.append(row.pop(tgt_field))
            # remap meta fields if necessary
            metadata = {rev_map.get(k, k): v for k, v in row.items() if k not in (src_field, tgt_field)}
            out_row.append(metadata)
            yield out_row
