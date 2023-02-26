#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu]
# Created: 4/8/20
import collections
import pickle
from pathlib import Path
from typing import List, Dict, Union
import json
import importlib
import os

import portalocker
from pybtex.database import parse_file as parse_bib_file

from mtdata import log, cached_index_file, __version__, resource_dir
from mtdata.entry import Entry, DatasetId
from mtdata.iso.bcp47 import bcp47, BCP47Tag

REFS_FILE = resource_dir / "refs.bib"


class Index:

    obj = None  # singleton object

    def __init__(self):
        self.entries: Dict[DatasetId, Entry] = {}  # unique dids
        self.papers = {}  # unique
        self.ref_db = ReferenceDb()
        self.version = __version__

    @classmethod
    def get_instance(cls):
        if not cls.obj:
            if not cached_index_file.exists():
                log.info("Creating a fresh index object")
                cached_index_file.parent.mkdir(exist_ok=True)
                lock_file = cached_index_file.with_suffix("._lock")
                with portalocker.Lock(lock_file, "w", timeout=60) as fh:
                    # got lock, check cache is not created by parallel processes while we waited
                    if not cached_index_file.exists():
                        obj = Index()
                        log.info("Indexing all datasets...")
                        obj.load_all()
                        log.info(f"Caching my index file at {cached_index_file}")
                        with open(cached_index_file, "wb") as out:
                            pickle.dump(obj, out)
                        obj.store_index(cached_index_file.with_suffix('.jsonl'))

            assert cached_index_file.exists()
            log.debug(f"Loading index from cache {cached_index_file}")
            with open(cached_index_file, "rb") as inp:
                obj = pickle.load(inp)

            assert isinstance(obj, cls), f"{cached_index_file} isnt valid. please move or remove it"
            cls.obj = obj
        return cls.obj
    
    def store_index(self, path, format='jsonl'):
        assert format in ('jsonl',) #TODO support tsv
        with open(path, 'w', encoding='utf8') as out:
            count = 0
            for ent in self.entries.values():
                line = json.dumps(ent, cls=Entry.JSONEncoder) 
                out.write(line)
                out.write('\n')
                count += 1

        log.info(f'Wrote {count:,} entries to {path}')
            
    def load_all(self):
       
        sub_modules = [
            ".statmt",
            ".paracrawl",
            ".tilde",
            ".joshua_indian",
            ".unitednations",
            ".wikimatrix",
            ".other",
            ".neulab_tedtalks",
            ".elrc_share",
            ".ai4bharat",
            ".eu",
            ".linguatools",
            ".anuvaad",
            ".allenai_nllb",
            ".flores",
            ".opus.opus_index",
            ".opus.opus100",
            ".leipzig",
        ]
        # modules from CWD
        for p in Path('.').glob('mtdata*.py'):
            module = p.name.replace('.py', '')
            sub_modules.append(module)
        #sub_modules = ['.statmt']
        for mod_name in sub_modules:
            module = importlib.import_module(mod_name, package=__name__)
            log.info(f'Loading module {mod_name}' )
            if hasattr(module, 'load_all'):
                getattr(module, 'load_all')(self)
            else:
                log.warning(f'skipping {module}.. no load_all() found')

        counts = collections.defaultdict(int)
        for e in self.entries.values():
            counts[e.did.group] += 1
        items = list(sorted(counts.items(), key=lambda x: x[1], reverse=True))
        items += [("Total", len(self))]
        counts = "\n".join([f"| {n} | {c:,}|" for n, c in items])
        log.info(f"Index status:\n{counts}")

    @property
    def n_entries(self) -> int:
        return len(self.entries)

    def add_entry(self, entry: Entry):
        assert isinstance(entry, Entry)
        key = entry.did
        assert key not in self.entries, f"{key} is a duplicate"
        if entry.cite:
            assert isinstance(entry.cite, tuple), 'cite field expected to be a tuple of bib keys'
            for bib_key in entry.cite:
                assert bib_key in self.ref_db, f'Bib key "{bib_key}" not found in refs.bib database'
        self.entries[key] = entry

    def __add__(self, e):
        if isinstance(e, Entry):
            self.add_entry(e)
            return self
        else:
            raise Exception(f'Expected instance of Entry, but given {type(e)}')

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
            assert file.exists(), f"{file} does not exist"
            cls._instance.db = parse_bib_file(file, bib_format="bibtex")
            log.debug(f"loaded {len(cls._instance)} references from {file}")
        return cls._instance

    def __getitem__(self, item):
        return self.db.entries[item]

    def __contains__(self, item):
        return item in self.db.entries

    def __len__(self):
        return len(self.db.entries)

    def get_bibtex(self, key: str) -> str:
        return self[key].to_string(bib_format="bibtex")

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


def get_entries(langs=None, names=None, not_names=None, fuzzy_match=False, 
                groups=None, not_groups=None) -> List[Entry]:
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
        if len(langs) == 2:
            select = [e for e in select if 2 == len(e.did.langs)\
                and bitext_lang_match(langs, e.did.langs, fuzzy_match=fuzzy_match)]
        else: # monolingual
            assert len(langs) == 1
            lang: BCP47Tag = langs[0]
            select = [e for e in select if 1 == len(e.did.langs) and lang.is_compatible(e.did.langs[0])]

    if not_names:
        if not isinstance(not_names, set):
            not_names = set(not_names)
        select = [e for e in select if e.did.name not in not_names]
    return select


INDEX: Index = Index.get_instance()
