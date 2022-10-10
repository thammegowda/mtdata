#!/usr/bin/env python

# Created by Thamme Gowda on Sept 7, 2022

import argparse
import logging as log
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict
from tqdm import tqdm
import time

from operator import add

log.basicConfig(level=log.INFO)



@dataclass
class Stats:
    n_lines: int = 0
    n_tokens: int = 0
    types: Counter = field(default_factory=Counter)
    lang: Optional[str] = None
    path: Optional[Path] = None
    meta: Optional[Dict] = None

    @property
    def n_types(self) -> int:
        return len(self.types)

    def update_line(self, line: str):
        if self.meta and self.meta.get('caseless'):
            line = line.lower()
        self.n_lines += 1
        toks = line.split()
        self.n_tokens += len(toks)
        self.types.update(toks)

    @classmethod
    def read(cls, path, lang=None, **meta) -> 'Stats':
        stats = cls(path=path, lang=lang, meta=meta)
        with open(path, encoding='utf8') as lines:
            for line in lines:
                stats.update_line(line)
        return stats

    @classmethod
    def spark_read(cls, path, spark, **meta) -> 'Stats':
        LINE_TAG = '<-[LINE]->'
        lines = spark.read.text(str(path)).rdd.map(lambda r: r[0])
        counts = lines.flatMap(lambda x: x.split() + [LINE_TAG]) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
        types = counts.collectAsMap()
        n_lines = types.pop(LINE_TAG)
        n_tokens = sum(types.values())
        return cls(path=path, n_lines=n_lines, n_tokens=n_tokens, types=types, meta=meta)

    def __repr__(self):
        meta = ''
        if self.meta:
            meta = ' '.join(f'{key}: {val}' for key, val in self.meta.items())
        stats = f'Lines: {self.n_lines:,} Tokens: {self.n_tokens:,} Types: {self.n_types:,} {meta}]'
        return f'Stats[{self.path and f"{self.path.name}" or ""} {stats}'

@dataclass
class AggreatedStats(Stats):
    name: str = ''

    def merge(self, stats: Stats):
        self.n_tokens += stats.n_tokens
        self.n_lines += stats.n_lines
        assert isinstance(self.types, Counter)
        self.types.update(stats.types)

def report_stats(path: Path, tok_ext=None, caseless=False):
    log.info(f'{path}')
    parts_dir = path / 'train-parts'
    assert parts_dir.exists(), f'{parts_dir} expected but not found'
    parts = list(parts_dir.glob('.valid.*'))
    log.info(f"{path} has {len(parts)} parts")
    for part in tqdm(parts, desc=f'{path}'):
        did = part.name.replace(".valid.", "")
        group, name, version, lang1, lang2 = did.split("-")
        l1_file = parts_dir / (f'{did}.{lang1}' + (tok_ext or ''))
        l2_file = parts_dir / (f'{did}.{lang2}'+ (tok_ext or ''))
        assert l1_file.exists(), f'{l1_file} not found'
        assert l2_file.exists(), f'{l2_file} not found'
        log.info(f'reading: {l1_file} || {l2_file}')
        l1_stats = Stats.read(l1_file, lang=lang1, caseless=caseless, did=did)
        l2_stats = Stats.read(l2_file, lang=lang2, caseless=caseless, did=did)
        yield (did, l1_stats, l2_stats)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('recipe_dirs', metavar='DIR', type=Path, help='Recipe or experiment directory', nargs='+')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug logs')
    parser.add_argument('-t', '--tok-ext', help='Tokenized files extension. Example .tok')
    parser.add_argument('-lc', '--caseless', action='store_true',
                        help='Case insesitive when counting number of types (i.e. unique words)')

    args = parser.parse_args()
    return vars(args)


def main(**args):
    args = args or parse_args()
    if args.pop('debug'):
        log.setLevel(log.DEBUG)
        log.debug('Debug mode enabled')
    recipe_dirs = args.pop('recipe_dirs')
    header = ['Directory', 'Pair', 'DatasetID', 'Sentences', 'L1 Tokens', 'L2 Tokens', 'L1 Types', 'L2 Types']
    DELIM = '\t'
    for path in recipe_dirs:
        tag = (args.get('tok_ext') or '' ) + (args.get('caseless') and '.lc' or '')
        stats_file: Path = path / f'dataset_stats{tag}.tsv'
        flag_file = path/ (stats_file.name + '._OK')
        if stats_file.exists() and flag_file.exists():
            log.info(f'{stats_file} found. Skipping')
            continue
        stats = report_stats(path, **args)
        aggregated = {} # agrregate by source, e.g. OPUS

        with stats_file.open('w') as out:
            out.write(DELIM.join(header) + '\n')
            langs = None
            for part_id, l1_stats, l2_stats in stats:
                l1, l2 = l1_stats.lang.split('_')[0], l2_stats.lang.split('_')[0]
                if langs is None: # store this order
                    langs = l1, l2
                    aggregated['Total'] = (
                        AggreatedStats(name='Total', lang=l1),
                        AggreatedStats(name='Total', lang=l2))
                else: # ensure the order is same
                    if l1 == langs[0]:
                        # correct order, no swapping needed
                        assert l2 == langs[1]
                    else: # maybe swapped?
                        assert l1 == langs[1]
                        assert l2 == langs[0]  # definitely swapped
                        l1, l2 = l2, l1 # here we swap
                        l1_stats, l2_stats = l2_stats, l1_stats
                assert l1_stats.n_lines == l2_stats.n_lines, f'{part_id} doesnt not have equal number of lines'
                row = [path, f'{l1_stats.lang}-{l2_stats.lang}', part_id,
                       l1_stats.n_lines, l1_stats.n_tokens, l2_stats.n_tokens,
                       l1_stats.n_types, l2_stats.n_types]
                out.write(DELIM.join(str(x) for x in row) + '\n')

                aggregated['Total'][0].merge(l1_stats)
                aggregated['Total'][1].merge(l2_stats)
                group = part_id.split('-')[0]
                if group not in aggregated:
                    aggregated[group] = (AggreatedStats(name=group, lang=l1),
                                         AggreatedStats(name=group, lang=l2))
                aggregated[group][0].merge(l1_stats)
                aggregated[group][1].merge(l2_stats)
            #
            for name, (l1_stats, l2_stats) in aggregated.items():
                assert l1_stats.n_lines == l2_stats.n_lines, f'{name} doesnt not have equal number of lines'
                row = [path, f'{l1_stats.lang}-{l2_stats.lang}', f'[{name}]',
                       l1_stats.n_lines, l1_stats.n_tokens, l2_stats.n_tokens,
                       l1_stats.n_types, l2_stats.n_types]
                out.write(DELIM.join(str(x) for x in row) + '\n')
        log.info(f'Stats file created: {stats_file}')
        flag_file.touch()


if '__main__' == __name__:
    start = time.time()
    main()
    end = time.time()
    log.info(f"All done. Time taken = {end-start} secs")
