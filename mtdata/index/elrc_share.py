#!/usr/bin/env python
# Parallel data scraped from ELRC-SHARE using https://github.com/kpu/elrc-scrape
# Author: Kenneth Heafield [mtdata (at) kheafield (dot) com] 


from mtdata import resource_dir
from mtdata.index import Index, Entry, DatasetId
REFS_FILE = resource_dir / 'elrc_share.tsv'
ELRC_CEF = [
    'https://elrc-share.eu/repository/download/365a8b821aa011eb913100155d02670611118e05e423402bb729137ecf6ac864/',
    5192
    ]


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

    elrc_cef = {
        'TestSet': [('de', 'it'), ('en', 'cs'), ('en', 'de'), ('en', 'it'), ('en', 'lv')],
    }
    for set_name, pairs in elrc_cef.items():
        for l1, l2 in pairs:
            src = f'CEF-DM-Multilingual-Benchmark/data/{set_name}-{l1.upper()}-{l2.upper()}.tsv'
            ent = Entry(did=DatasetId(group='ELRC', name='cef_data_marketplace', version='1', langs=(l1, l2)), 
                        url=ELRC_CEF[0], ext='zip', in_ext='tsv', cols=(1,2), in_paths=[src],
                        filename="ELRC_" + str(ELRC_CEF[1]) + ".zip")
            index.add_entry(ent)
