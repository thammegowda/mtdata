#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20

from typing import Optional, Union, Tuple, List
from dataclasses import dataclass
from pathlib import Path
from mtdata import log
import shutil
import gzip
from datetime import datetime
from itertools import zip_longest

CONTAINERS = ['tar', 'zip', 'tgz', 'txz']
COMPRESS_EXT = ['gz', 'bz2', 'xz']
PLAIN = ['txt', 'tsv',  'raw']


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

    def __post_init__(self):
        if not isinstance(self.paths, list):
            self.paths = [self.paths]
        assert  1 <= len(self.paths) <= 2
        for p in self.paths:
            p.exists(), f'{p} not exists'

        if not self.ext:
            exts = [detect_extension(p.name) for p in self.paths]
            assert len(set(exts)) == 1, f'Expected a type of exts, but found: {exts}'
            self.ext = exts[0]

    def read_segs(self):
        readers = []
        for p in self.paths:
            if 'tsv' in self.ext:
                readers.append(self.read_tsv(p))
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
        if len(readers)  == 1:
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

    def read_tsv(self, path, delim='\t'):
        with IO.reader(path) as stream:
            for line in stream:
                yield [x.strip() for x in line.split(delim)]

class IO:
    """File opener and automatic closer
    Copied from my other project https://github.com/isi-nlp/rtg/blob/master/rtg/utils.py
    """
    def __init__(self, path, mode='r', encoding=None, errors=None):
        self.path = path if type(path) is Path else Path(path)
        self.mode = mode
        self.fd = None
        self.encoding = encoding or 'utf-8' if 't' in mode else None
        self.errors = errors or 'replace'

    def __enter__(self):
        if self.path.name.endswith(".gz"):   # gzip mode
            self.fd = gzip.open(self.path, self.mode, encoding=self.encoding, errors=self.errors)
        else:
            if 'b' in self.mode:  # binary mode doesnt take encoding or errors
                self.fd = self.path.open(self.mode)
            else:
                self.fd = self.path.open(self.mode, encoding=self.encoding, errors=self.errors,
                                         newline='\n')
        return self.fd

    def __exit__(self, _type, value, traceback):
        self.fd.close()

    @classmethod
    def reader(cls, path, text=True):
        return cls(path, 'rt' if text else 'rb')

    @classmethod
    def writer(cls, path, text=True, append=False):
        return cls(path, ('a' if append else 'w') + ('t' if text else 'b'))

    @classmethod
    def get_lines(cls, path, col=0, delim='\t', line_mapper=None, newline_fix=True):
        with cls.reader(path) as inp:
            if newline_fix and delim != '\r':
                inp = (line.replace('\r', '') for line in inp)
            if col >= 0:
                inp = (line.split(delim)[col].strip() for line in inp)
            if line_mapper:
                inp = (line_mapper(line) for line in inp)
            yield from inp

    @classmethod
    def get_liness(cls, *paths, **kwargs):
        for path in paths:
            yield from cls.get_lines(path, **kwargs)

    @classmethod
    def write_lines(cls, path: Path, text):
        if isinstance(text, str):
            text = [text]
        with cls.writer(path) as out:
            for line in text:
                out.write(line)
                out.write('\n')

    @classmethod
    def copy_file(cls, src: Path, dest: Path, text=False):
        assert src.resolve() != dest.resolve()
        log.info(f"Copy {src} → {dest}")
        with IO.reader(src, text=text) as inp, IO.writer(dest, text=text) as out:
            shutil.copyfileobj(inp, out)

    @classmethod
    def maybe_backup(cls, file: Path):
        if file.exists():
            time = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            dest = file.with_suffix(f'.{time}')
            log.info(f"Backup {file} → {dest}")
            file.rename(dest)
