#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/13/20
from mtdata.index import Index, Entry, DatasetId


def load_all(index: Index):

    cite = index.ref_db.get_bibtex(key='post-etal-2012-constructing')
    url = 'https://github.com/joshua-decoder/indian-parallel-corpora/archive/a2cd1a99.tar.gz'
    l2 = 'en'
    langs = ['ml', 'hi', 'ur', 'bn', 'te', 'ta']
    for l1 in langs:
        for split in ['training', 'dev', 'test', 'devtest', 'dict']:
            if l1 == 'hi' and split == 'dict':
                continue   # hindi dont have dict
            f1 = f'*/{l1}-{l2}/{split}.{l1}-{l2}.{l1}'
            f2 = f'*/{l1}-{l2}/{split}.{l1}-{l2}.{l2}'
            if split not in ('training', 'dict'):
                f2 += '.0'
            ent = Entry(did=DatasetId(group='JoshuaDec', name=f'indian_{split}', version='1', langs=(l1, l2)),
                  url=url, filename='joshua-indian-parallel-corpora.tar.gz',
                  in_paths=[f1, f2], in_ext='txt', cite=cite)
            index.add_entry(ent)
