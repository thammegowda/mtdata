#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20

from typing import Optional, Union, Tuple, List
from dataclasses import dataclass
from pathlib import Path
from mtdata import log
from itertools import zip_longest

from mtdata.utils import IO

COMPRESS_EXT = ['gz', 'bz2', 'xz']


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
    langs: Tuple[str, str]
    ext: Optional[str] = None
    ent: Optional['Entry'] = None

    def __post_init__(self):
        if not isinstance(self.paths, list):
            self.paths = [self.paths]
        assert 1 <= len(self.paths) <= 3
        for p in self.paths:
            assert p.exists(), f'{p} not exists'

        if not self.ext:
            exts = [detect_extension(p.name) for p in self.paths]
            if len(exts) == 2 and set(exts) == set(self.langs):
                log.warning(f"Treating {' .'.join(exts)} as plain text. To override: in_ext=<ext>")
                exts = ['txt']  # treat that as plain text
            assert len(set(exts)) == 1, f'Expected a type of exts, but found: {exts}'
            self.ext = exts[0]

    def read_segs(self):
        readers = []
        if self.ext == 'opus_xces':
            align, lang1_dir, lang2_dir = self.paths
            from mtdata.opus_xces import OpusXcesParser
            reader = OpusXcesParser.read(align, lang1_dir, lang2_dir)
            readers.append(reader)
        else:
            for p in self.paths:
                if 'tsv' in self.ext:
                    cols = (0, 1) #extract first two columns
                    if self.ent and self.ent.cols:
                        cols = self.ent.cols
                    readers.append(self.read_tsv(p, cols=cols))
                elif 'raw' in self.ext or 'txt' in self.ext:
                    readers.append(self.read_plain(p))
                elif 'tmx' in self.ext:
                    from mtdata.tmx import read_tmx
                    readers.append(read_tmx(path=p, langs=self.langs))
                elif 'sgm' in self.ext:
                    from mtdata.sgm import read_sgm
                    readers.append(read_sgm(p))
                else:
                    raise Exception(f'Not supported {self.ext} : {p}')

        if len(readers) == 1:
            yield from readers[0]
        elif len(readers) == 2:
            for seg1, seg2 in zip_longest(*readers):
                if seg1 is None or seg2 is None:
                    raise Exception(f'{self.paths} have unequal number of segments')
                yield seg1, seg2
        else:
            raise Exception("This is an error")

    def read_plain(self, path):
        with IO.reader(path) as stream:
            for line in stream:
                yield line.strip()

    def read_tsv(self, path, delim='\t', cols=None):
        """
        Read data from TSV file
        :param path: path to TSV file
        :param delim: delimiter default is \\t
        :param cols: if certain columns are to be extracted;
            default is None, which returns all columns
        :return:
        """
        with IO.reader(path) as stream:
            for line in stream:
                row = [x.strip() for x in line.rstrip('\n').split(delim)]
                if cols:
                    row = [row[idx] for idx in cols]
                yield row
