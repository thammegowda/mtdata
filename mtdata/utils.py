#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/13/20
import gzip
from mtdata import log
import shutil
from datetime import datetime
from pathlib import Path


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
        elif self.path.name.endswith(".xz"):
            import lzma
            self.fd = lzma.open(self.path, self.mode, encoding=self.encoding, errors=self.errors)
        else:
            if 'b' in self.mode:  # binary mode doesnt take encoding or errors
                self.fd = self.path.open(self.mode)
            else:
                self.fd = self.path.open(self.mode, encoding=self.encoding, errors=self.errors,
                                         newline='\n')
        return self.fd

    def __exit__(self, _type, value, traceback):
        self.fd.close()
        self.fd = None

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