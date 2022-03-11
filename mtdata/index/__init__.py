#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20
import collections
import pickle
from pathlib import Path
from typing import List, Dict, Union

import portalocker
from pybtex.database import parse_file as parse_bib_file

from mtdata import log, cached_index_file, __version__
from mtdata.entry import Entry, DatasetId
from mtdata.iso.bcp47 import bcp47, BCP47Tag

REFS_FILE = Path(__file__).parent / 'refs.bib'


class Index:

    obj = None   # singleton object

    def __init__(self):
        self.entries: Dict[DatasetId, Entry] = {}  # unique dids
        self.papers = {}                            # unique
        self.ref_db = ReferenceDb()
        self.version = __version__

    @classmethod
    def get_instance(cls):
        if not cls.obj:
            if not cached_index_file.exists():
                log.info("Creating a fresh index object")
                cached_index_file.parent.mkdir(exist_ok=True)
                lock_file = cached_index_file.with_suffix("._lock")
                with portalocker.Lock(lock_file, 'w', timeout=60) as fh:
                    # got lock, check cache is not created by parallel processes while we waited
                    if not cached_index_file.exists():
                        obj = Index()
                        log.info("Indexing all datasets...")
                        obj.load_all()
                        log.info(f"Caching my index file at {cached_index_file}")
                        with open(cached_index_file, 'wb') as out:
                            pickle.dump(obj, out)

            assert cached_index_file.exists()
            log.info(f"Loading index from cache {cached_index_file}")
            with open(cached_index_file, 'rb') as inp:
                obj = pickle.load(inp)

            assert isinstance(obj, cls), f'{cached_index_file} isnt valid. please move or remove it'
            cls.obj = obj
        return cls.obj

    def load_all(self):
        from mtdata.index import (
            statmt, paracrawl, tilde, joshua_indian, unitednations, wikimatrix, other, neulab_tedtalks,
            elrc_share, ai4bharat, eu, linguatools, anuvaad)
        from mtdata.index.opus import opus_index, jw300, opus100
        subsets = [
            ('Statmt.org', statmt.load),
            ('Paracrawl', paracrawl.load),
            ('Tilde', tilde.load),
            ('JoshuaIndianCoprus', joshua_indian.load_all),
            ('UnitedNations', unitednations.load_all),
            ('OPUS', opus_index.load_all),
            # ('OPUS_JW300', jw300.load_all), # JW300 is taken down
            ('OPUS100', opus100.load_all),
            ('WikiMatrix', wikimatrix.load_all),
            ('Other', other.load_all),
            ('Neulab_TEDTalksv1', neulab_tedtalks.load_all),
            ('ELRC-SHARE', elrc_share.load_all),
            ('AI4Bharat', ai4bharat.load_all),
            ('EU', eu.load_all),
            ('LinguaTools', linguatools.load_all),
            ('Anuvaad', anuvaad.load_all),
        ]
        for name, loader in subsets:
            loader(self)

        counts = collections.defaultdict(int)
        for e in self.entries.values():
            counts[e.did.group] += 1
        items = list(sorted(counts.items(), key=lambda x: x[1], reverse=True))
        items += [('Total', len(self))]
        counts = '\n'.join([f'| {n} | {c:,}|' for n, c in items])
        log.info(f"Index status:\n{counts}")

    @property
    def n_entries(self) -> int:
        return len(self.entries)

    def add_entry(self, entry: Entry):
        assert isinstance(entry, Entry)
        key = entry.did
        assert key not in self.entries, f'{key} is a duplicate'
        self.entries[key] = entry

    def get_entries(self):
        return self.entries.values()

    def get_papers(self):
        return self.papers.values()

    def __contains__(self, item):
        assert isinstance(item, DatasetId)
        return item in self.entries

    def __getitem__(self, item):
        assert isinstance(item, DatasetId)
        return self.entries[item]

    def contains_paper(self, name):
        return name in self.papers

    def get_entry(self, name, langs):
        assert isinstance(name, str)
        assert isinstance(langs, tuple)
        langs = tuple(lang if isinstance(lang, BCP47Tag) else bcp47(lang) for lang in langs)
        key = (name, langs)
        rev_key = (name, tuple(reversed(langs)))
        if key not in self.entries and rev_key in self.entries:
            key = rev_key
        return self.entries[key]

    def get_paper(self, name):
        return self.papers[name]

    def __len__(self):
        return len(self.entries)


class ReferenceDb:

    _instance = None  # singleton instance

    def __new__(cls, file=REFS_FILE):
        if cls._instance is None:
            cls._instance = super(ReferenceDb, cls).__new__(cls)
            assert file.exists(), f'{file} does not exist'
            cls._instance.db = parse_bib_file(file, bib_format='bibtex')
            log.debug(f"loaded {len(cls._instance)} references from {file}")
        return cls._instance

    def __getitem__(self, item):
        return self.db.entries[item]

    def __contains__(self, item):
        return item in self.db.entries

    def __len__(self):
        return len(self.db.entries)

    def get_bibtex(self, key: str) -> str:
        return self[key].to_string(bib_format='bibtex')

    def keys(self):
        return self.db.entries.keys()


def is_compatible(lang1: Union[str, BCP47Tag], lang2: Union[str, BCP47Tag]):
    lang1 = lang1 if isinstance(lang1, BCP47Tag) else bcp47(lang1)
    lang2 = lang2 if isinstance(lang2, BCP47Tag) else bcp47(lang2)
    return lang1.is_compatible(lang2)


def bitext_lang_match(pair1, pair2, fuzzy_match=False) -> bool:
    x1, y1 = sorted(pair1)
    x2, y2 = sorted(pair2)
    if fuzzy_match:
        return is_compatible(x1, x2) and is_compatible(y1, y2)
    else:
        return x1 == x2 and y1 == y2


def get_entries(langs=None, names=None, not_names=None, fuzzy_match=False, groups=None, not_groups=None) -> List[Entry]:
    """
    :param langs: language pairs  to select eg ('en', 'de')
    :param names:  names to select
    :param not_names:  names to exclude
    :param groups: groups to select
    :param not_groups: groups to exlcude
    :param fuzzy_match
    :return: list of dataset entries that match the criteria
    """
    # TODO: our index has grown too big; improve search with fuzzy matches
    select = list(INDEX.get_entries())
    if groups:
        groups = set(g.lower() for g in groups)
        select = [e for e in select if e.did.group.lower() in groups]
    if not_groups:
        not_groups = set(g.lower() for g in not_groups)
        select = [e for e in select if e.did.group.lower() not in not_groups]
    if names:
        names = set(n.lower() for n in names)
        select = [e for e in select if e.did.name in names]
    if langs:
        assert len(langs) == 2
        langs = sorted(langs)
        select = [e for e in select if bitext_lang_match(langs, e.did.langs, fuzzy_match=fuzzy_match)]
    if not_names:
        if not isinstance(not_names, set):
            not_names = set(not_names)
        select = [e for e in select if e.did.name not in not_names]
    return select


INDEX: Index = Index.get_instance()
