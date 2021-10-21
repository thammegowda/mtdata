#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/17/21

from mtdata.index import Index, Entry, DatasetId


def load_all(index: Index):
    group = 'AI4Bharath'
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

        ent = Entry(did=DatasetId(group=group, name=f'samananthar', version='0.2', langs=(l1, l2)),
                    url=url, cite=cite, in_paths=[f'{pair}/train.{l1}', f'{pair}/train.{l2}'], in_ext='txt')
        index.add_entry(ent)

    URL = "https://storage.googleapis.com/samanantar-public/benchmarks.zip"
    filename = "samananthar-benchmarks.zip"
    for split in ('dev', 'test'):
        want20_langs = 'bn gu hi ml mr ta te'.split()
        for l2 in want20_langs:
            f1 = f'benchmarks/wat2020-devtest/en-{l2}/{split}.en'
            f2 = f'benchmarks/wat2020-devtest/en-{l2}/{split}.{l2}'
            ent = Entry(did=DatasetId(group=group, name=f'wat_{split}', version='2020', langs=('en', l2)),
                        filename=filename, url=URL, cite=cite, in_paths=[f1, f2], in_ext='txt')
            index.add_entry(ent)

        wat21_langs = 'bn en gu hi kn ml mr or pa ta te'.split()
        for i, l1 in enumerate(wat21_langs):
            for l2 in wat21_langs[i + 1:]:
                f1 = f'benchmarks/wat2021-devtest/{split}.{l1}'
                f2 = f'benchmarks/wat2021-devtest/{split}.{l2}'
                ent = Entry(did=DatasetId(group=group, name=f'wat_{split}', version='2021', langs=(l1, l2)),
                            filename=filename, url=URL, cite=cite, in_paths=[f1, f2], in_ext='txt')
                index.add_entry(ent)

        # PMI langs; en-as
        index.add_entry(Entry(
            did=DatasetId(group=group, name=f'pmi_{split}', version='2021', langs=('en', 'as')),
            filename=filename, url=URL, cite=cite, in_ext='txt',
            in_paths=[f'benchmarks/pmi/en-as/{split}.en', f'benchmarks/pmi/en-as/{split}.as']))
