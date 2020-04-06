#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/5/20

from pathlib import Path
from mtdata import log
from mtdata.cache import Cache
from mtdata.index import Entry, get_entries
from mtdata.parser import Parser

class Dataset:

    def __init__(self, dir: Path, langs, cache_dir: Path):
        self.dir = dir
        self.langs = langs
        self.cache = Cache(cache_dir)
        self.parts_dir = dir / 'parts'
        self.parts_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def prepare(cls, langs, names, out_dir, cache_dir):
        log.info(f"Locating datasets for langs={langs} names={names}")
        entries = get_entries(langs=langs, names=names)
        log.info(f"Found {len(entries)}")
        dataset = cls(dir=out_dir, langs=langs, cache_dir=cache_dir)
        total = 0
        skips = 0
        for ent in entries:
            n_good, n_bad = dataset.add_part(ent)
            total += n_good
            skips += n_bad
            log.info(f"Found {n_good} lines in {n_bad}; So far, total={total} skips={skips}")
        return dataset

    def add_part(self, entry: Entry):
        path = self.cache.get_entry(entry)
        swap = entry.is_swap(self.langs)
        parser = Parser(path, langs=self.langs)
        l1 = (self.parts_dir / entry.name).with_suffix(f'.{self.langs[0]}')
        l2 = (self.parts_dir / entry.name).with_suffix(f'.{self.langs[1]}')
        mode = dict(mode='w', encoding='utf-8', errors='ignore')
        with l1.open(**mode) as f1, l2.open(**mode) as f2:
            count, skips = 0, 0
            for rec in parser.read_segs():
                if len(rec) != 2:
                    skips += 1
                    continue
                sent1, sent2 =[s.strip() for s in  rec]
                if not sent1 or not sent2:
                    if len(rec) != 2:
                        skips += 1
                        continue
                if swap:
                    sent2, sent1 = sent1, sent2
                f1.write(f'{sent1}\n')
                f2.write(f'{sent2}\n')
                count += 1
        return count, skips


