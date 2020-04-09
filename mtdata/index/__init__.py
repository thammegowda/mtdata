#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20
from typing import List
from mtdata.entry import Entry

class Index(list):
    # TODO: actually create index with checks for duplicates

    def add(self, entry: Entry):
        self.__add__(entry)

    def __add__(self, other):

        assert isinstance(other, Entry)
        self.append(other)

entries: List[Entry] = Index()

def get_entries(langs=None, names=None, not_names=None):
    """
    :param langs: language pairs  to select eg ('en', 'de')
    :param names:  names to select
    :param not_names:  names to exclude
    :return: list of dataset entries that match the criteria
    """
    select = entries
    if names:
        if not isinstance(names, set):
            names = set(names)
        select = [e for e in select if e.name in names]
    if langs:
        assert len(langs) == 2
        langs = sorted(langs)
        select = [e for e in select if langs == sorted(e.langs)]
    if not_names:
        if not isinstance(not_names, set):
            not_names = set(not_names)
        select = [e for e in select if e.name not in not_names]
    return select

def load_all():
    from mtdata.index import statmt, paracrawl, tilde
    statmt.load(entries)
    paracrawl.load(entries)
    tilde.load(entries)

# eager load, as of now TODO: lazy load
load_all()
