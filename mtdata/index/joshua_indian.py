#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/13/20
from mtdata.index import Index, Entry

def load_all(index: Index):

    cite="""@inproceedings{post-etal-2012-constructing,
    title = "Constructing Parallel Corpora for Six {I}ndian Languages via Crowdsourcing",
    author = "Post, Matt  and
      Callison-Burch, Chris  and
      Osborne, Miles",
    booktitle = "Proceedings of the Seventh Workshop on Statistical Machine Translation",
    month = jun,
    year = "2012",
    address = "Montr{\'e}al, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W12-3152",
    pages = "401--409",
}"""
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
            ent = Entry(langs=(l1, l2), url=url, name=f'JoshuaIndianCorpus_{split}',
                  filename='joshua-indian-parallel-corpora.tar.gz',
                  in_paths=[f1, f2], in_ext='txt', cite=cite)
            index.add_entry(ent)
