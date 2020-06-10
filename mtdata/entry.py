#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20

from typing import Tuple, List, Optional, Set
from dataclasses import dataclass, field
from mtdata.parser import detect_extension
from mtdata.iso import iso3_code


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
    cols: Optional[Tuple[int, int]] = None

    def __post_init__(self):
        self.langs = tuple(iso3_code(l, fail_error=True) for l in self.langs)

        assert len(self.langs) == 2
        assert isinstance(self.langs, tuple)

        for ch in '.-/* ':
            assert ch not in self.name, f"Character '{ch}' is not permitted in name {self.name}"

        orig_name = self.url.split('/')[-1]
        self.ext = self.ext or detect_extension(self.filename or orig_name)
        langs = '_'.join(self.langs)
        self.filename = self.filename or f'{self.name}.{self.ext}'
        self.is_archive = self.ext in ('zip', 'tar', 'tar.gz', 'tgz')
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
    def make(cls, langs: Tuple[str, str], train: List[str], tests: List[str]):
        from mtdata.index import INDEX
        train = [INDEX.get_entry(name, langs) for name in train]
        tests = [INDEX.get_entry(name, langs) for name in tests]
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
