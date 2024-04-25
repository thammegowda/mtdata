#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu]
# Created: 4/5/20
import collections as coll
import concurrent.futures
import json
from itertools import zip_longest
from pathlib import Path
import random
from typing import Dict, List, Tuple, Union

import portalocker

from mtdata import Defaults
from mtdata import cache_dir as CACHE_DIR
from mtdata import log, pbar_man
from mtdata.cache import Cache
from mtdata.entry import DatasetId, Entry, LangPair
from mtdata.index import INDEX
from mtdata.iso.bcp47 import BCP47Tag, bcp47
from mtdata.parser import Parser
from mtdata.utils import IO

DEF_COMPRESS = 'gz'
DATA_FIELDS = ('train', 'dev', 'test', 'mono_train', 'mono_dev', 'mono_test')


class Dataset:

    def __init__(self, dir: Path, langs: LangPair, cache_dir: Path, drop_train_noise=True, n_jobs=1,
                 drop_test_noise=False, drop_dupes=False, drop_tests=False, compress=False, fail_on_error=False):
        self.dir = dir
        assert len(langs) == 2, f'Only parallel datasets are supported for now and expected two langs; {langs}'
        assert isinstance(langs[0], BCP47Tag)
        assert isinstance(langs[1], BCP47Tag)
        self.langs = langs
        self.cache = Cache(cache_dir)

        self.train_parts_dir = dir / 'train-parts'  # will be merged later
        self.tests_dir = dir / 'tests'  # wont be merged
        self.mono_train_parts_dir = dir / 'mono-train-parts'  # wil be merged
        self.mono_tests_dir = dir / 'mono-tests'        # wont be merged
        self.train_parts_dir.mkdir(parents=True, exist_ok=True)
        self.tests_dir.mkdir(parents=True, exist_ok=True)
        self.drop_train_noise = drop_train_noise
        self.drop_test_noise = drop_test_noise
        self.drop_dupes = drop_dupes  # in training only
        self.drop_tests = drop_tests  # in training only
        self.fail_on_error = fail_on_error
        self.compress = compress
        self.n_jobs = n_jobs
        self.errors_file = self.dir / 'errors.tsv'
        assert self.n_jobs > 0

    @classmethod
    def resolve_entries(cls, dids: List[DatasetId]):
        inp_dids = set(dids)
        if len(inp_dids) != len(dids):
            dupes = [(id, c) for id, c in coll.Counter(dids).items() if c > 1]
            assert len(inp_dids) == len(dids), f'Dupes found (unique expected): {dupes}'
        entries = []
        for did in inp_dids:
            if did in INDEX:
                entries.append(INDEX[did])
            else:
                raise Exception(f'Could not find {did}; try "mtdata list | grep -i {did}" to locate it')
        return entries

    @classmethod
    def parallel_download(cls, entries: List[Entry], cache: Cache, n_jobs=1):
        """Download entries in parallel. This is useful when there are many entries to download.
        :param entries: list of entries to download
        :param cache: cache object to download the entries
        :param n_jobs: number of parallel jobs to run
        :return: dictionary of entry -> paths. Failed entries will have None path.
        """
        if n_jobs == 1:
            return [cache.get_entry(ent) for ent in entries]
        log.info(f"Downloading {len(entries)} datasets in parallel with {n_jobs} jobs")
        result = {}
        entries = list(entries) # make a copy
        # shuffle to hit different servers at the same time
        random.seed(42)
        random.shuffle(entries)
        status = dict(total=len(entries), success=0, failed=0)
        with concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
            futures_to_entry = {executor.submit(cache.get_entry, entry): entry for entry in entries}
            for future in concurrent.futures.as_completed(futures_to_entry.keys()):
                entry:Entry = futures_to_entry[future]
                try:
                    paths = future.result()   # paths, ignore
                    result[entry] = paths
                    status['success'] += 1
                    log.info(f"[{status['success']}/{status['total']}] Downloaded {entry.did}")
                except Exception as exc:
                    result[entry] = None
                    status['failed'] += 1
                    log.warning(f"Failed to download {entry.did}: {exc} Total failed: {status['failed']}")
        log.info(f"Downloaded {status['success']} datasets. Failed to download {status['failed']}")
        return result

    @classmethod
    def prepare(cls, langs, out_dir: Path, dataset_ids=Dict[str, List[DatasetId]],
                cache_dir: Path = CACHE_DIR, merge_train=False, drop_noise: Tuple[bool, bool] = (True, False),
                compress=False, drop_dupes=False, drop_tests=False, fail_on_error=False, n_jobs=1):
        drop_train_noise, drop_test_noise = drop_noise
        assert langs, 'langs required'
        assert dataset_ids
        assert isinstance(dataset_ids, dict)
        err_keys = dataset_ids.keys() - set(DATA_FIELDS)
        assert not err_keys, f'{err_keys} are unknown. Supported fields: {DATA_FIELDS}'
        # First, resolve and check if they exist before going to process them.
        # Fail early for typos in name
        all_dids = [id for ids in dataset_ids.values() for id in (ids or [])]
        all_entries = cls.resolve_entries(all_dids)
        for ent in all_entries:
            if not ent.is_compatible(langs):
                raise Exception(f'Given languages: {langs} and dataset: {ent.did} are not compatible')
        if n_jobs > 1:
            cls.parallel_download(all_entries, Cache(cache_dir), n_jobs=n_jobs)

        dataset = cls(dir=out_dir, langs=langs, cache_dir=cache_dir, drop_train_noise=drop_train_noise,
                      drop_test_noise=drop_test_noise, drop_dupes=drop_dupes, drop_tests=drop_tests,
                      fail_on_error=fail_on_error, n_jobs=n_jobs)

        dev_entries, test_entries = [], []
        if dataset_ids.get('test'):  # tests are smaller so quicker; no merging needed
            test_entries = cls.resolve_entries(dataset_ids['test'])
            dataset.add_test_entries(test_entries)
        if dataset_ids.get('dev'):
            dev_entries = cls.resolve_entries(dataset_ids['dev'])
            dataset.add_dev_entries(dev_entries)
        if dataset_ids.get('train'):  # this might take some time
            train_entries = cls.resolve_entries(dataset_ids['train'])
            drop_hashes = None
            if drop_tests:
                pair_files = []
                for ent in dev_entries + test_entries:
                    p1, p2 = dataset.get_paths(dataset.tests_dir, ent)
                    if BCP47Tag.check_compat_swap(langs, ent.did.langs, fail_on_incompat=True)[1]:
                        p1, p2 = p2, p1  # swap
                    pair_files.append((p1, p2))
                test_pair_hash, test_seg_hash = dataset.hash_all_bitexts(pair_files)
                drop_hashes = test_pair_hash | test_seg_hash  # set union
            dataset.add_train_entries(train_entries, merge_train=merge_train, compress=compress,
                                      drop_hashes=drop_hashes)
        for key, dirpath in [('mono_train', dataset.mono_train_parts_dir),
                             ('mono_dev', dataset.mono_tests_dir),
                             ('mono_test', dataset.mono_tests_dir)]:
            if dataset_ids.get(key):
                dirpath.mkdir(exist_ok=True)
                entries = cls.resolve_entries(dataset_ids[key])
                for entry in entries:
                    dataset.add_mono_entry(dirpath, entry, compress=compress) 

        # citations
        refs_file = out_dir / 'references.bib'
        if refs_file.exists():
            refs_file.rename(refs_file.with_suffix('.bib.bak'))
        with refs_file.open('w', encoding='utf-8', errors='ignore') as fh:
            for ent in all_entries:
                cite = ent.cite
                if cite:
                    try:
                        if isinstance(cite, str):
                            cite = [cite]
                        cite = '\n'.join(INDEX.ref_db.get_bibtex(key) for key in cite)
                    except:
                        log.exception(f'Error reading citation for {ent.did}: {cite}', exc_info=True)
                cite = cite or '%% UNKNOWN'
                fh.write(f"%% {ent.did}\n{cite}\n\n")
        log.info(f"Created references at {refs_file}")
        return dataset

    def hash_all_bitexts(self, paired_files):
        paired_hashes = set()
        seg_hashes = set()
        for if1, if2 in paired_files:
            for seg1, seg2 in self.read_parallel(if1, if2):
                paired_hashes.add(hash((seg1, seg2)))
                paired_hashes.add(hash((seg2, seg1)))
                seg_hashes.add(hash(seg1))
                seg_hashes.add(hash(seg2))
        return paired_hashes, seg_hashes

    def add_train_entries(self, entries, merge_train=False, compress=False, drop_hashes=None):
        self.add_parts(self.train_parts_dir, entries, drop_noise=self.drop_train_noise,
                       compress=compress, desc='Training sets', fail_on_error=self.fail_on_error)
        if not merge_train:
            return
        lang1, lang2 = self.langs
        # paired_files = self.find_bitext_pairs(self.train_parts_dir, lang1, lang2)
        paired_files = {}
        for ent in entries:
            e1, e2 = self.get_paths(self.train_parts_dir, ent, compress=compress)
            _, swapped = BCP47Tag.check_compat_swap(self.langs, ent.did.langs, fail_on_incompat=True)
            if swapped:
                e1, e2 = e2, e1
            paired_files[str(ent.did)] = e1, e2

        log.info(f"Going to merge {len(paired_files)} files as one train file")
        compress_ext = f'.{DEF_COMPRESS}' if compress else ''
        l1_ext = f'{lang1}{compress_ext}'
        l2_ext = f'{lang2}{compress_ext}'
        of1 = self.dir / f'train.{l1_ext}'
        of2 = self.dir / f'train.{l2_ext}'
        of3 = self.dir / f'train.meta.{DEF_COMPRESS}'

        counts = dict(total=coll.defaultdict(int),
                      dupes_skips=coll.defaultdict(int),
                      test_overlap_skips=coll.defaultdict(int),
                      selected=coll.defaultdict(int))
        train_hashes = set()

        with IO.writer(of1) as w1, IO.writer(of2) as w2, IO.writer(of3) as w3:
            with pbar_man.counter(color='green', total=len(paired_files), unit='it', desc="Merging", leave=False,
                                  min_delta=Defaults.PBAR_REFRESH_INTERVAL, autorefresh=True) as pbar:
                for name, (if1, if2) in paired_files.items():
                    for seg1, seg2 in self.read_parallel(if1, if2):
                        counts['total'][name] += 1
                        if self.drop_dupes or self.drop_tests:
                            hash_val = hash((seg1, seg2))
                            if drop_hashes and (hash_val in drop_hashes or hash(seg1) in drop_hashes
                                                or hash(seg2) in drop_hashes):
                                counts['test_overlap_skips'][name] += 1
                                continue
                            if self.drop_dupes:
                                if hash_val in train_hashes:
                                    counts['dupes_skips'][name] += 1
                                    continue
                                train_hashes.add(hash_val)
                        w1.write(seg1 + '\n')
                        w2.write(seg2 + '\n')
                        w3.write(name + '\n')
                        counts['selected'][name] += 1
                    pbar.update()

        stats = dict(selected=sum(counts['selected'].values()),
                     total=sum(counts['total'].values()),
                     counts=counts)

        stats_msg = json.dumps(stats, indent=2)
        log.info('Train stats:\n' + stats_msg)
        IO.write_lines(self.dir / 'train.stats.json', stats_msg)
        return counts

    def add_mono_entry(self, dirpath, entry: Entry, compress=False):
        flag_file = dirpath / f'.valid.{entry.did}'
        assert len(entry.did.langs) == 1, f'Monolingual entry expected, given {entry.did}'
        if flag_file.exists():
            log.info(f"{flag_file} exits. Skipping")
            return -1, -1
        cache_path = self.cache.get_entry(entry)
        parser = Parser(cache_path, ext=entry.in_ext or None, ent=entry)
        out_path = self.get_paths(dirpath, entry, compress=compress)
        log.info("Writing %s to %s", entry.did, out_path)
        io_args = dict(encoding='utf-8', errors='ignore')
        with IO.writer(out_path, **io_args) as out:
            count, skips = 0, 0
            for sentence in parser.read_segs():
                if isinstance(sentence, (list, tuple)) and len(sentence) == 1:
                    sentence = sentence[0]   # flatten list
                assert isinstance(sentence, str), f'str sentence expected. found: {type(sentence)}; entry: {entry.did}'
                sentence = sentence and sentence.strip()
                if not sentence:
                    skips += 1
                    continue
                sentence = sentence.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
                out.write(f'{sentence}\n')
                count += 1
            msg = f'Looks like an error. {count} segs are valid {skips} are invalid: {entry}'
            assert count > 0, msg
            if skips > count:
                log.warning(msg)
                log.info(f"{entry}: Skips : {skips:,}/{count:,} => {100 * skips / count:.4f}%")
        flag_file.touch()
        return count, skips

    @classmethod
    def find_bitext_pairs(cls, dir_path: Path, lang1: BCP47Tag, lang2: BCP47Tag):
        if lang1.is_compatible(lang2):
            raise Exception(f"Unable to merge for {lang1}-{lang2}; it can result in unpredictable behavior.")
        paired_files = {}
        for path in dir_path.glob("*.*"):
            if path.name.startswith("."):
                continue
            parts = path.name.split(".")
            assert len(parts) >= 2, f'Invalid file name {path.name}; Unable to merge parts'
            if parts[-1] == DEF_COMPRESS:
                parts = parts[:-1]
            *did, ext = parts  # did can have a dot e.g. version 7.1
            did = '.'.join(did)
            # dids, ext = parts[:2]
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
        return paired_files

    @classmethod
    def read_parallel(cls, file1: Path, file2: Path):
        with IO.reader(file1) as r1, IO.reader(file2) as r2:
            for seg1, seg2 in zip_longest(r1, r2):
                if seg1 is None or seg2 is None:
                    raise Exception(f'{file1} {file2} have unequal num of lines. This is an error.')
                yield seg1.strip(), seg2.strip()

    def add_test_entries(self, entries):
        self.add_parts(self.tests_dir, entries, drop_noise=self.drop_test_noise, desc='Held-out sets',
                       fail_on_error=self.fail_on_error)
        if len(entries) <= 20:
            for i, entry in enumerate(entries, start=1):
                self.link_to_part(entry, self.tests_dir, f"test{i}")

    def link_to_part(self, entry, data_dir, link_name):
        """Create link such as test, dev"""
        l1, l2 = self.langs
        l1_path, l2_path = self.get_paths(data_dir, entry)
        l1_path, l2_path = l1_path.relative_to(self.dir), l2_path.relative_to(self.dir)
        l1_link = self.dir / f'{link_name}.{l1.lang}'
        l2_link = self.dir / f'{link_name}.{l2.lang}'
        for lnk in [l1_link, l2_link]:
            if lnk.exists():
                lnk.unlink()
        compat, swapped = BCP47Tag.check_compat_swap(self.langs, entry.did.langs)
        if not compat:
            raise Exception(f"Unable to unify language IDs: {self.langs} x {entry.did.langs}")
        if swapped:
            l1_path, l2_path = l2_path, l1_path
        l1_link.symlink_to(l1_path)
        l2_link.symlink_to(l2_path)

    def add_dev_entries(self, entries):
        assert entries
        self.add_parts(self.tests_dir, entries, drop_noise=self.drop_test_noise, fail_on_error=self.fail_on_error)

        if len(entries) == 1:
            # create a link to the only one
            self.link_to_part(entries[0], self.tests_dir, "dev")
        else:
            l1, l2 = self.langs
            out_paths = (self.dir / f'dev.{l1.lang}', self.dir / f'dev.{l2.lang}')
            in_paths = []
            for ent in entries:
                e1, e2 = self.get_paths(self.tests_dir, ent)
                compat, swapped = BCP47Tag.check_compat_swap(self.langs, ent.did.langs)
                if not compat:
                    raise Exception(f"Unable to unify language IDs {self.langs} x {ent.did.langs}")
                if swapped:
                    e1, e2 = e2, e1
                in_paths.append((e1, e2))
            self.cat_bitexts(in_paths=in_paths, out_paths=out_paths)

    def cat_bitexts(self, in_paths: List[Tuple[Path, Path]], out_paths: Tuple[Path, Path]):
        of1, of2 = out_paths
        of1.parent.mkdir(exist_ok=True)
        of2.parent.mkdir(exist_ok=True)
        with pbar_man.counter(color='green', total=len(in_paths), unit='it', desc="Merging", leave=False,
                              min_delta=Defaults.PBAR_REFRESH_INTERVAL, autorefresh=True) as pbar, \
                IO.writer(of1) as w1, IO.writer(of2) as w2:
            for if1, if2 in in_paths:
                assert if1.exists()
                assert if2.exists()
                for seg1, seg2 in self.read_parallel(if1, if2):
                    w1.write(seg1 + '\n')
                    w2.write(seg2 + '\n')
                pbar.update()

    def add_part_thread(self, args):
        fail_on_error = args.pop('fail_on_error', False)
        ent = args['entry']
        assert isinstance(ent, Entry)
        try:
            n_good, n_bad = self.add_part(**args)
            if max(n_good, n_bad) >= 0:  # -1 for skipped record because it is valid
                log.info(f"{ent.did.name} : found {n_good:} segments and {n_bad:} errors")
        except Exception as e:
            log.error(f"Unable to add {ent.did}: {e}")
            if fail_on_error:
                raise e
            msg = str(e).replace('\n', '\t')
            with portalocker.Lock(self.errors_file, 'a', timeout=Defaults.FILE_LOCK_TIMEOUT) as fh:
                # self.errors_file.open('a').write(f"{ent.did}\t{msg}\n")
                fh.write(f"{ent.did}\t{msg}\n")

    def add_parts(self, dir_path, entries, drop_noise=False, compress=False, desc=None, fail_on_error=False):
        assert isinstance(entries, list)
        if self.n_jobs == 1:
            return self.add_parts_sequential(dir_path=dir_path, entries=entries, drop_noise=drop_noise,
                                             compress=compress, desc=desc, fail_on_error=fail_on_error)

        tasks = [dict(dir_path=dir_path, entry=ent, drop_noise=drop_noise, compress=compress,
                      fail_on_error=fail_on_error) for ent in entries]
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.n_jobs) as executor:
            futures = [executor.submit(self.add_part_thread, task) for task in tasks]
            with pbar_man.counter(color='blue', leave=False, total=len(entries), unit='it', desc=desc,
                              autorefresh=True, min_delta=Defaults.PBAR_REFRESH_INTERVAL, position=3) as pbar:
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        log.error(f"Error in thread: {e}")
                        if fail_on_error:
                            raise e
                    finally:
                        pbar.update(force=True)

    def add_parts_sequential(self, dir_path, entries, drop_noise=False, compress=False, desc=None, fail_on_error=False):
        with pbar_man.counter(color='blue', leave=False, total=len(entries), unit='it', desc=desc,
                              min_interval=Defaults.PBAR_REFRESH_INTERVAL, autorefresh=True, position=3) as pbar:
            for ent in entries:
                try:
                    n_good, n_bad = self.add_part(dir_path=dir_path, entry=ent, drop_noise=drop_noise,
                                                  compress=compress)
                    if max(n_good, n_bad) >= 0:  # -1 for skipped record because it is valid
                        log.info(f"{ent.did.name} : found {n_good:} segments and {n_bad:} errors")
                    pbar.update(force=True)
                except Exception as e:
                    log.exception(f"Unable to add {ent.did}: {e}")

                    if fail_on_error:
                        raise e
                    msg = str(e).replace('\n', '\t')
                    self.errors_file.open('a').write(f"{ent.did}\t{msg}\n")

    @classmethod
    def get_paths(cls, dir_path: Path, entry: Entry, compress=False) -> Union[Path, Tuple[Path, Path]]:
        """
        Gets file path for entry in given directory. 
        Return single path for monolingual entry and tuple of two paths for bilingual entry.
        Paths may have compress extension such as .gz when compress=True
        """
        compress_ext = compress and f'.{DEF_COMPRESS}' or ''
        l1_ext = str(entry.did.langs[0]) + compress_ext
        l1 = dir_path / f'{entry.did}.{l1_ext}'
        if len(entry.did.langs) == 1: # monolingual
            return l1
        else: # biling
            l2_ext = str(entry.did.langs[1]) + compress_ext
            l2 = dir_path / f'{entry.did}.{l2_ext}'
            return l1, l2

    def add_part(self, dir_path: Path, entry: Entry, drop_noise=False, compress=False):
        flag_file = dir_path / f'.valid.{entry.did}'
        if flag_file.exists():
            log.info(f"{flag_file} exits. Skipping")
            return -1, -1
        path = self.cache.get_entry(entry)
        # swap = entry.is_swap(self.langs)
        parser = Parser(path, ext=entry.in_ext or None, ent=entry)
        # langs = '_'.join(str(lang) for lang in self.langs)
        # Check that files are written in correct order
        l1, l2 = self.get_paths(dir_path, entry, compress=compress)
        io_args = dict(encoding='utf-8', errors='ignore')
        with IO.writer(l1, **io_args) as f1, IO.writer(l2, **io_args) as f2:
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
                sent1 = sent1.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
                sent2 = sent2.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
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
        flag_file.touch()
        return count, skips


def rreplace(text: str, cut: str, place: str):
    """ right replace: https://stackoverflow.com/a/9943875/1506477
        >>> 'XXX'.join('mississippi'.rsplit('iss', 1))
        'missXXXippi'
    """
    return place.join(text.split(cut, 1))
