#!/usr/bin/env python
# Parallel data scraped from ELRC-SHARE using https://github.com/kpu/elrc-scrape
# Author: Kenneth Heafield [mtdata (at) kheafield (dot) com] 

from pathlib import Path
from mtdata.index import Index, Entry
REFS_FILE = Path(__file__).parent / 'elrc_share.tsv'

def load_all(index: Index):
    with open(REFS_FILE) as data:
        for line in data:
            l1, l2, num, short, name, info, download, licenses, in_paths = line.split('\t', maxsplit=8)
            in_paths = in_paths.strip().split('\t')
            ent = Entry(langs=(l1, l2), url=download, name="ELRC_" + short, filename="ELRC_" + str(num) + ".zip", in_ext='tmx', in_paths=in_paths)
            index.add_entry(ent)
