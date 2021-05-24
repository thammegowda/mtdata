#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/17/21

from mtdata.index import Index, Entry


def load_all(index: Index):

    cite = index.ref_db.get_bibtex('ramesh2021samanantar')
    pairs = ('en-as en-bn en-gu en-hi en-kn en-ml en-mr en-or en-pa en-ta en-te as-bn as-gu as-hi'
             ' as-kn as-ml as-mr as-or as-pa as-ta as-te bn-gu bn-hi bn-kn bn-ml bn-mr bn-or bn-pa'
             ' bn-ta bn-te gu-hi gu-kn gu-ml gu-mr gu-or gu-pa gu-ta gu-te hi-kn hi-ml hi-mr hi-or'
             ' hi-pa hi-ta hi-te kn-ml kn-mr kn-or kn-pa kn-ta kn-te ml-mr ml-or ml-pa ml-ta ml-te'
             ' mr-or mr-pa mr-ta mr-te or-pa or-ta or-te pa-ta pa-te ta-te')
    BASE_v0_2 = 'https://storage.googleapis.com/samanantar-public/V0.2/data/{dirname}/{pair}.zip'
    for pair in pairs.strip().split(' '):
        l1, l2 = pair.split('-')
        dirname = 'en2indic' if l1 == 'en' else 'indic2indic'
        url = BASE_v0_2.format(dirname=dirname, pair=pair)
        ent = Entry(langs=(l1, l2), name='AI4B_Samananthar_v02', url=url, cite=cite,
              in_paths=[f'{pair}/train.{l1}', f'{pair}/train.{l2}'], in_ext='txt')
        index.add_entry(ent)
