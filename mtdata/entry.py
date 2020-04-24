#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20

from typing import Tuple, List, Optional, Mapping
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


@dataclass
class Experiment:

    name: str            # lang1->lang2
    train: List[Entry]   # training should be merged from all these
    tests: List[Entry]   # multiple tests; one of them can be validation set

    def __post_init__(self):
        for t in self.tests:
            assert t
        for t in self.train:
            assert t

@dataclass
class Paper:  # or Article

    name: str   # author1-etal-year
    title: str   # title
    url: str    # Paper url to be sure
    cite: str    # bibtex would be nice to display
    experiments: List[Experiment]
