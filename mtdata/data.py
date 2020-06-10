#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu]
# Created: 4/5/20

from pathlib import Path
from mtdata import log
from mtdata.cache import Cache
from mtdata.index import Entry, get_entries
from mtdata.parser import Parser
from mtdata.utils import IO
from typing import Optional, List
from itertools import zip_longest
import collections as coll
import json


class Dataset:

    def __init__(self, dir: Path, langs, cache_dir: Path):
        self.dir = dir
        self.langs = langs
        assert len(langs) == 2, 'Only parallel datasets are supported for now and expect two langs'
        self.cache = Cache(cache_dir)

        self.train_parts_dir = dir / 'train-parts'  # will be merged later
        self.tests_dir = dir / 'tests'  # wont be merged
        self.train_parts_dir.mkdir(parents=True, exist_ok=True)
        self.tests_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def resolve_entries(cls, langs, names):
        inp_names = set(names)
        assert len(inp_names) == len(names), f'{names} are not unique.'
        entries = get_entries(langs=langs, names=inp_names)
        out_names = set(e.name for e in entries)
        if inp_names & out_names != inp_names | out_names:
            missed = inp_names - out_names
            assert missed
            raise Exception(f'Could not find: {missed} for languages: {langs}')
        return entries

    @classmethod
    def prepare(cls, langs, train_names: Optional[List[str]], test_names: Optional[List[str]],
                out_dir: Path, cache_dir: Path, merge_train=False):
        assert langs, 'langs required'
        assert train_names or test_names, 'Either train_names or test_names should be given'
        # First, resolve and check if they exist before going to process them.
        # Fail early for typos in name
        train_entries, test_entries = None, None
        if test_names:
            test_entries = cls.resolve_entries(langs, test_names)
        if train_names:
            train_entries = cls.resolve_entries(langs, train_names)

        dataset = cls(dir=out_dir, langs=langs, cache_dir=cache_dir)
        if test_entries: # tests are smaller so quicker; no merging needed
            dataset.add_test_entries(test_entries)

        if train_entries: # this might take some time
            dataset.add_train_entries(train_entries, merge_train=merge_train)
        return dataset

    def add_train_entries(self, entries, merge_train=False):
        self.add_parts(self.train_parts_dir, entries)
        if not merge_train:
            return
        # merge
        l1, l2 = self.langs
        l1_files = list(self.train_parts_dir.glob(f"*.{l1}"))
        assert l1_files and len(l1_files) >= len(entries)

        l2_files = [l1_f.with_suffix(f".{l2}") for l1_f in l1_files]
        assert all(l2_f.exists() for l2_f in l2_files)
        log.info(f"Going to merge {len(l1_files)} files as one train file")
        counts = coll.defaultdict(int)
        of1 = self.dir / f'train.{l1}'
        of2 = self.dir / f'train.{l2}'
        of3 = self.dir / f'train.meta.gz'
        with IO.writer(of1) as w1, IO.writer(of2) as w2, IO.writer(of3) as w3:
            for if1, if2 in zip(l1_files, l2_files):
                name = if1.name.rstrip(f'.{l1}')
                for seg1, seg2 in self.read_parallel(if1, if2):
                    w1.write(seg1 + '\n')
                    w2.write(seg2 + '\n')
                    w3.write(name + '\n')
                    counts[name] += 1
        total = sum(counts.values())
        counts = {'total': total, 'parts': counts}
        counts_msg = json.dumps(counts, indent=2)
        log.info('Train stats:\n' + counts_msg)
        IO.write_lines(self.dir /'train.stats.json', counts_msg)
        return counts

    @classmethod
    def read_parallel(cls, file1: Path, file2: Path):
        with IO.reader(file1) as r1, IO.reader(file2) as r2:
            for seg1, seg2 in zip_longest(r1, r2):
                if seg1 is None or seg2 is None:
                    raise Exception(f'{file1} {file2} have unequal num of lines. Thats an error')
                yield seg1.strip(), seg2.strip()

    def add_test_entries(self, entries):
        self.add_parts(self.tests_dir, entries)

    def add_parts(self, dir_path, entries):
        for ent in entries:
            n_good, n_bad = self.add_part(dir_path=dir_path, entry=ent)
            log.info(f"{ent.name} : found {n_good:} segments and {n_bad:} errors")

    def add_part(self, dir_path: Path, entry: Entry):
        path = self.cache.get_entry(entry)
        swap = entry.is_swap(self.langs)
        parser = Parser(path, langs=self.langs, ext=entry.in_ext or None, ent=entry)
        langs = '_'.join(self.langs)
        l1 = (dir_path / f'{entry.name}-{langs}').with_suffix(f'.{self.langs[0]}')
        l2 = (dir_path / f'{entry.name}-{langs}').with_suffix(f'.{self.langs[1]}')
        mode = dict(mode='w', encoding='utf-8', errors='ignore')
        with l1.open(**mode) as f1, l2.open(**mode) as f2:
            count, skips = 0, 0
            for rec in parser.read_segs():
                rec = rec[:2]  # get the first two recs
                if len(rec) != 2:
                    skips += 1
                    continue
                sent1, sent2 = [s.strip() for s in rec]
                if not sent1 or not sent2:
                    if len(rec) != 2:
                        skips += 1
                        continue
                if swap:
                    sent2, sent1 = sent1, sent2
                f1.write(f'{sent1}\n')
                f2.write(f'{sent2}\n')
                count += 1
            msg = f'Looks like an error. {count} segs are valid {skips} are invalid: {entry}'
            assert count > skips and count > 0, msg

        return count, skips
