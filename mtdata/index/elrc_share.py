#!/usr/bin/env python
# Parallel data scraped from ELRC-SHARE using https://github.com/kpu/elrc-scrape
# Author: Kenneth Heafield [mtdata (at) kheafield (dot) com] 

from pathlib import Path
from mtdata.index import Index, Entry, DatasetId
REFS_FILE = Path(__file__).parent / 'elrc_share.tsv'


def load_all(index: Index):
    with open(REFS_FILE, encoding='utf-8') as data:
        for line in data:
            l1, l2, num, short, name, info, download, licenses, in_paths = line.split('\t', maxsplit=8)
            dataset_name = short.lower().replace(':', '_').replace('__', '_').replace('__', '_')
            in_paths = in_paths.strip().split('\t')
            # Currently only two formats: .tmx and text files ending with a language code.
            in_ext = 'txt'
            for p in in_paths:
                if p.endswith('.tmx'):
                    in_ext = 'tmx'
            ent = Entry(did=DatasetId(group='ELRC', name=dataset_name, version='1', langs=(l1, l2)),
                    url=download, filename="ELRC_" + str(num) + ".zip", in_ext=in_ext, in_paths=in_paths)
            index.add_entry(ent)
