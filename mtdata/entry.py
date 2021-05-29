#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20

from typing import Tuple, List, Optional, Set
from dataclasses import dataclass, field
from mtdata.parser import detect_extension
from mtdata.iso import iso3_code


class Entry:
    __slots__ = ('langs', 'name', 'url', 'filename', 'ext', 'in_paths', 'in_ext', 'cite', 'cols',
                 'is_archive')

    def __init__(self, langs: Tuple[str, str],
        name: str,
        url: str,
        filename: Optional[str] = None ,
        ext: Optional[str] = None,
        in_paths: Optional[List[str]] = None,
        in_ext: Optional[str] = None,
        cite: Optional[str] = None,
        cols: Optional[Tuple[int, int]] = None):

        assert isinstance(langs, tuple)
        assert len(langs) == 2
        for ch in '-/* ':
            assert ch not in name, f"Character '{ch}' is not permitted in name {name}"

        self.langs = tuple(iso3_code(l, fail_error=True) for l in langs)
        self.name = name
        self.url = url
        self.filename = filename
        orig_name = self.url.split('/')[-1]
        self.ext = ext or detect_extension(filename or orig_name)
        self.filename = self.filename or f'{self.name}.{self.ext}'

        self.in_paths = in_paths
        self.in_ext = in_ext
        self.cite = cite
        self.cols = cols

        self.is_archive = self.ext in ('zip', 'tar', 'tar.gz', 'tgz')
        if self.is_archive:
            assert self.in_paths and len(self.in_paths) > 0, 'Archive entries must have in_paths'

    def is_swap(self, langs):
        if self.in_ext == 'tmx':
            return False
        return tuple(reversed(langs)) == tuple(self.langs)

    def __str__(self):
        return self.format(delim=' ')

    def format(self, delim: str = ' '):
        msg = f'{self.name}{delim}{"-".join(self.langs)}{delim}{self.url}{delim}' \
              f'{",".join(self.in_paths or [])}'
        return msg

    def is_noisy(self, seg1, seg2) -> bool:
        # None or Empty
        noisy = seg1 is None or seg2 is None or not seg1.strip() or not seg2.strip()
        return noisy


class JW300Entry(Entry):
    url: Tuple[str, str, str]  # (align.xml, src.xml, tgt.xml)


@dataclass
class Experiment:
    langs: Tuple[str, str]  # (lang1 , lang2)  lang1 -> lang2
    train: List[Entry]  # training should be merged from all these
    tests: List[Entry]  # multiple tests; one of them can be validation set
    papers: Set['Paper'] = field(default_factory=set)

    def __post_init__(self):
        self.langs = tuple(iso3_code(l, fail_error=True) for l in self.langs)
        for t in self.tests:
            assert t
        for t in self.train:
            assert t

    @classmethod
    def make(cls, index, langs: Tuple[str, str], train: List[str], tests: List[str]):
        train = [index.get_entry(name, langs) for name in train]
        tests = [index.get_entry(name, langs) for name in tests]
        return cls(langs, train=train, tests=tests)


@dataclass(eq=False)  # see for hash related issues: https://stackoverflow.com/a/52390734/1506477
class Paper:  # or Article

    name: str  # author1-etal-year
    title: str  # title
    url: str  # Paper url to be sure
    cite: str  # bibtex would be nice to display
    experiments: List[Experiment]

    langs: Set[Tuple[str, str]] = None

    def __post_init__(self):
        self.langs = self.langs or set(exp.langs for exp in self.experiments)
        for exp in self.experiments:
            exp.papers.add(self)
