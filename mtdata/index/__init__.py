#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20
from mtdata import log
from mtdata.entry import Entry, Paper


class Index:

    def __init__(self):
        self.entries = {}  # uniq
        self.papers = {}  # uniq

    @property
    def n_entries(self) -> int:
        return len(self.entries)

    def add_entry(self, entry: Entry):
        assert isinstance(entry, Entry)
        key = (entry.name, entry.langs)
        assert key not in self.entries, f'{key} is a duplicate'
        self.entries[key] = entry

    def add_paper(self, paper: Paper):
        assert isinstance(paper, Paper)
        assert paper.name not in self.papers, f'{paper.name} is a duplicate'
        self.papers[paper.name] = paper

    def get_entries(self):
        return self.entries.values()

    def get_papers(self):
        return self.papers.values()

    def contains_entry(self, name, langs):
        key = (name, langs)
        return key in self.entries

    def contains_paper(self, name):
        return name in self.papers

    def get_entry(self, name, langs):
        assert isinstance(name, str)
        assert isinstance(langs, tuple)
        key = (name, langs)
        rev_key = (name, tuple(reversed(langs)))
        if key not in self.entries and rev_key in self.entries:
            key = rev_key
        return self.entries[key]

    def get_paper(self, name):
        return self.papers[name]

    def __len__(self):
        return len(self.entries)


INDEX: Index = Index()


def get_entries(langs=None, names=None, not_names=None):
    """
    :param langs: language pairs  to select eg ('en', 'de')
    :param names:  names to select
    :param not_names:  names to exclude
    :return: list of dataset entries that match the criteria
    """
    select = list(INDEX.get_entries())
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
    from mtdata.index import statmt, paracrawl, tilde, literature
    counts = [('init', 0)]
    statmt.load(INDEX)
    counts.append(('Statmt.org', len(INDEX) - counts[-1][-1]))
    paracrawl.load(INDEX)
    counts.append(('Paracrawl', len(INDEX) - counts[-1][-1]))
    tilde.load(INDEX)
    counts.append(('Tilde', len(INDEX) - counts[-1][-1]))

    from mtdata.index import joshua_indian
    joshua_indian.load_all(INDEX)
    counts.append(('JoshuaIndianCorpus', len(INDEX) - counts[-1][-1]))

    from mtdata.index import globalvoices
    globalvoices.load_all(INDEX)
    counts.append(('GlobalVoices', len(INDEX) - counts[-1][-1]))

    from mtdata.index import unitednations
    unitednations.load_all(INDEX)
    counts.append(('UnitedNations', len(INDEX) - counts[-1][-1]))

    from mtdata.index.opus import opus_index, jw300
    opus_index.load_all(INDEX)
    counts.append(('OPUS', len(INDEX) - counts[-1][-1]))
    jw300.load_all(INDEX)
    counts.append(('OPUS_JW300', len(INDEX) - counts[-1][-1]))



    del counts[0]
    counts = {n: c for n, c in counts}
    log.info(f"Loaded entries: {counts}")
    literature.load(INDEX)


# eager load, as of now TODO: lazy load
load_all()
