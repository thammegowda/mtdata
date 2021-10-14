#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu]
# Created: 4/5/20

from pathlib import Path
from mtdata import log
from mtdata.cache import Cache
from mtdata.index import INDEX, Entry, DatasetId, LangPair
from mtdata.iso.bcp47 import bcp47, BCP47Tag
from mtdata.parser import Parser
from mtdata.utils import IO
from typing import Optional, List, Tuple
from itertools import zip_longest
import collections as coll
import json


class Dataset:

    def __init__(self, dir: Path, langs: LangPair, cache_dir: Path, drop_train_noise=True,
                 drop_test_noise=False):
        self.dir = dir
        self.langs = langs
        assert len(langs) == 2, 'Only parallel datasets are supported for now and expect two langs'
        self.cache = Cache(cache_dir)

        self.train_parts_dir = dir / 'train-parts'  # will be merged later
        self.tests_dir = dir / 'tests'  # wont be merged
        self.train_parts_dir.mkdir(parents=True, exist_ok=True)
        self.tests_dir.mkdir(parents=True, exist_ok=True)
        self.drop_train_noise = drop_train_noise
        self.drop_test_noise = drop_test_noise

    @classmethod
    def resolve_entries(cls, dids: List[DatasetId]):
        inp_dids = set(dids)
        assert len(inp_dids) == len(dids), f'{dids} are not unique.'
        entries = []
        for did in inp_dids:
            if did in INDEX:
                entries.append(INDEX[did])
            else:
                raise Exception(f'Could not find {did}; try "mtdata list | grep -i <name>" to locate it')
        return entries

    @classmethod
    def prepare(cls, langs, train_dids: Optional[List[DatasetId]], test_dids: Optional[List[DatasetId]],
                dev_did: Optional[DatasetId], out_dir: Path, cache_dir: Path, merge_train=False,
                drop_noise: Tuple[bool, bool] = (True, False)):
        drop_train_noise, drop_test_noise = drop_noise
        assert langs, 'langs required'
        assert train_dids or test_dids, 'Either train_names or test_names should be given'
        # First, resolve and check if they exist before going to process them.
        # Fail early for typos in name
        train_entries, test_entries = None, None
        if test_dids:
            test_entries = cls.resolve_entries(test_dids)
        if train_dids:
            train_entries = cls.resolve_entries(train_dids)

        dataset = cls(dir=out_dir, langs=langs, cache_dir=cache_dir,
                      drop_train_noise=drop_train_noise, drop_test_noise=drop_test_noise)
        if test_entries:  # tests are smaller so quicker; no merging needed
            dataset.add_test_entries(test_entries)
        if dev_did:
            dev_entry = cls.resolve_entries([dev_did])[0]
            dataset.add_dev_entry(dev_entry)

        if train_entries:  # this might take some time
            dataset.add_train_entries(train_entries, merge_train=merge_train)
        return dataset

    def add_train_entries(self, entries, merge_train=False):
        self.add_parts(self.train_parts_dir, entries, drop_noise=self.drop_train_noise)
        if not merge_train:
            return
        # merge
        lang1, lang2 = self.langs
        if lang1.is_compatible(lang2):
            raise Exception(f"Unable to merge for {lang1}-{lang2}; it can result in unpredictable behavior.")
        paired_files = {}
        for path in self.train_parts_dir.glob("*.*"):
            if path.name.startswith("."):
                continue
            parts = path.name.split(".")
            assert len(parts) == 2, f'Invalid file name {path.name}; Unable to merge parts'
            did, ext = path.name.split(".")
            ext = bcp47(ext)
            if did not in paired_files:
                paired_files[did] = [None, None]
            if lang1.is_compatible(ext):
                assert not lang2.is_compatible(ext)
                paired_files[did][0] = path
            elif lang2.is_compatible(ext):
                paired_files[did][1] = path
            else:
                raise Exception(f"Unable to decide the side of train-part {path}; ext={ext}: we have {lang1}-{lang2}")
        for did, (f1, f2) in paired_files.items():
            assert f1 and f1.exists(), f'Invalid state: part {did} does not have pair, or pair is are removed'

        log.info(f"Going to merge {len(paired_files)} files as one train file")
        counts = coll.defaultdict(int)
        of1 = self.dir / f'train.{lang1}'
        of2 = self.dir / f'train.{lang2}'
        of3 = self.dir / f'train.meta.gz'
        with IO.writer(of1) as w1, IO.writer(of2) as w2, IO.writer(of3) as w3:
            for name, (if1, if2) in paired_files.items():
                for seg1, seg2 in self.read_parallel(if1, if2):
                    w1.write(seg1 + '\n')
                    w2.write(seg2 + '\n')
                    w3.write(name + '\n')
                    counts[name] += 1
        total = sum(counts.values())
        counts = {'total': total, 'parts': counts}
        counts_msg = json.dumps(counts, indent=2)
        log.info('Train stats:\n' + counts_msg)
        IO.write_lines(self.dir / 'train.stats.json', counts_msg)
        return counts

    @classmethod
    def read_parallel(cls, file1: Path, file2: Path):
        with IO.reader(file1) as r1, IO.reader(file2) as r2:
            for seg1, seg2 in zip_longest(r1, r2):
                if seg1 is None or seg2 is None:
                    raise Exception(f'{file1} {file2} have unequal num of lines. Thats an error')
                yield seg1.strip(), seg2.strip()

    def add_test_entries(self, entries):
        self.add_parts(self.tests_dir, entries, drop_noise=self.drop_test_noise)
        if len(entries) <= 4:
            for i, entry in enumerate(entries, start=1):
                self.link_to_part(entry, self.tests_dir, f"test{i}")

    def link_to_part(self, entry, data_dir, link_name):
        """Create link such as test, dev"""
        l1_path, l2_path = self.get_paths(data_dir, entry)
        l1_path, l2_path = l1_path.relative_to(self.dir), l2_path.relative_to(self.dir)
        l1_link = self.dir / f'{link_name}.{self.langs[0]}'
        l2_link = self.dir / f'{link_name}.{self.langs[1]}'
        for lnk in [l1_link, l2_link]:
            lnk.unlink(missing_ok=True)
        if BCP47Tag.are_compatible(self.langs[0], entry.did.langs[0]):
            assert not BCP47Tag.are_compatible(self.langs[0], entry.did.langs[1])
            # cool! no swapping needed
        elif BCP47Tag.are_compatible(self.langs[0], entry.did.langs[1]):
            l1_path, l2_path = l2_path, l1_path  # swapped
        else:
            raise Exception("This should not be happening! :(")

        l1_link.symlink_to(l1_path)
        l2_link.symlink_to(l2_path)

    def add_dev_entry(self, entry):
        n_good, n_bad = self.add_part(self.tests_dir, entry, drop_noise=self.drop_test_noise)
        log.info(f"{entry.did} : found {n_good:} segments and {n_bad:} errors")
        # create a link
        self.link_to_part(entry, self.tests_dir, "dev")

    def add_parts(self, dir_path, entries, drop_noise=False):
        for ent in entries:
            n_good, n_bad = self.add_part(dir_path=dir_path, entry=ent, drop_noise=drop_noise)
            log.info(f"{ent.did} : found {n_good:} segments and {n_bad:} errors")

    @classmethod
    def get_paths(cls, dir_path: Path, entry: Entry) -> Tuple[Path, Path]:
        l1 = (dir_path / f'{entry.did}').with_suffix(f'.{entry.did.langs[0]}')
        l2 = (dir_path / f'{entry.did}').with_suffix(f'.{entry.did.langs[1]}')
        return l1, l2

    def add_part(self, dir_path: Path, entry: Entry, drop_noise=False):
        path = self.cache.get_entry(entry)
        swap = entry.is_swap(self.langs)
        parser = Parser(path, langs=self.langs, ext=entry.in_ext or None, ent=entry)
        # langs = '_'.join(str(lang) for lang in self.langs)
        # Check that files are written in correct order
        l1, l2 = self.get_paths(dir_path, entry)
        mode = dict(mode='w', encoding='utf-8', errors='ignore')
        with l1.open(**mode) as f1, l2.open(**mode) as f2:
            count, skips, noise = 0, 0, 0
            for rec in parser.read_segs():
                rec = rec[:2]  # get the first two recs
                if len(rec) != 2:
                    skips += 1
                    continue
                if drop_noise and entry.is_noisy(seg1=rec[0], seg2=rec[1]):
                    skips += 1
                    noise += 1
                    continue
                sent1, sent2 = [s.strip() for s in rec]
                if not sent1 or not sent2:
                    skips += 1
                    continue
                if swap:
                    sent2, sent1 = sent1, sent2
                sent1 = sent1.replace('\n', ' ').replace('\t', ' ')
                sent2 = sent2.replace('\n', ' ').replace('\t', ' ')
                f1.write(f'{sent1}\n')
                f2.write(f'{sent2}\n')
                count += 1
            msg = f'Looks like an error. {count} segs are valid {skips} are invalid: {entry}'
            assert count > 0, msg
            if skips > count:
                log.warning(msg)
            if noise > 0:
                log.info(f"{entry}: Noise : {noise:,}/{count:,} => {100 * noise / count:.4f}%")
            log.info(f"wrote {count} lines to {l1} == {l2}")
        return count, skips
