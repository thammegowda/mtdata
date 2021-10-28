#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/13/20

from mtdata.index import Index, Entry, DatasetId
import itertools


def load_all(index: Index):
    cite = index.ref_db.get_bibtex('ziemski-etal-2016-united')
    url = "https://stuncorpusprod.blob.core.windows.net/corpusfiles/UNv1.0.testsets.tar.gz"
    url = "https://drive.google.com/uc?export=download&id=13GI1F1hvwpMUGBSa0QC6ov4eE57GC_Zx"  # they changed it!
    langs = ['en', 'ar', 'fr', 'es', 'ru', 'zh']
    for split in ['dev', 'test']:
        for l1, l2 in itertools.combinations(langs, 2):
            f1 = f'testsets/{split}set/UNv1.0.{split}set.{l1}'
            f2 = f'testsets/{split}set/UNv1.0.{split}set.{l2}'
            ent = Entry(did=DatasetId(group='UN', name=f'un_{split}', version='1', langs=(l1, l2)),
                 url=url, filename='UNv1.0.testsets.tar.gz', in_ext='txt', in_paths=[f1, f2], cite=cite)
            index.add_entry(ent)
