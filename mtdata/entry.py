#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20

from typing import Tuple, List, Optional
from dataclasses import dataclass
from mtdata.parser import detect_extension


@dataclass
class Entry:
    langs: Tuple[str, str]
    name: str
    url: str
    filename: Optional[str] = None  # optional local file name; tries to auto-decide iff missing
    ext: Optional[str] = None  # extension name; tries to auto-decide iff missing
    in_paths: Optional[List[str]] = None  # if URL is a tar or zip, specify inside paths
    in_ext: Optional[str] = None  # extension of in_paths inside archive
    cite: Optional[str] = None

    def __post_init__(self):
        assert len(self.langs) == 2
        assert isinstance(self.langs, tuple)
        for ch in '.-/* ':
            assert ch not in self.name, f"Character '{ch}' not supported in dataset name"

        orig_name = self.url.split('/')[-1]
        self.ext = self.ext or detect_extension(self.filename or orig_name)
        langs = '_'.join(self.langs)
        self.filename = self.filename or f'{self.name}-{langs}.{self.ext}'
        self.is_archive = self.ext in ['zip', 'tar', 'tar.gz', 'tgz']
        if self.is_archive:
            assert self.in_paths and len(self.in_paths) > 0, 'Archive entries must have in_paths'

    def is_swap(self, langs):
        return tuple(reversed(langs)) == tuple(self.langs)

    def __str__(self):
        return self.format(delim=' ')

    def format(self, delim: str = ' '):
        msg = f'{self.name}{delim}{"-".join(self.langs)}{delim}{self.url}{delim}' \
              f'{",".join(self.in_paths or [])}'
        return msg
