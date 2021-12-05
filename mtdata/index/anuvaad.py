#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 11/21/21

"""
# Scrape URLs and store it into anuvaad.tsv by this command
curl https://raw.githubusercontent.com/project-anuvaad/anuvaad-parallel-corpus/master/README.md |
   grep -o 'http[^ ]*zip' > anuvad.tsv
"""
from pathlib import Path
from mtdata.index import Index, Entry, DatasetId, log
import collections as coll


data_file = Path(__file__).parent / 'anuvaad.tsv'


def load_all(index: Index):
    lines = data_file.read_text(encoding='utf-8').splitlines()
    langs = set('hi bn ta ml te kn mr pa gu as ur or'.split())       # other than en
    group_id = 'Anuvaad'
    cite_txt = index.ref_db.get_bibtex('project-anuvaad')
    for url in lines:
        url = url.strip()
        assert url.startswith('http') and url.endswith('.zip')
        file_name = url.split('/')[-1]
        file_name = file_name[:-4]  # .zip
        char_count = coll.Counter(list(file_name))
        n_hyps = char_count.get('-', 0)
        n_unders = char_count.get('_', 0)
        if n_hyps > n_unders:
            parts = file_name.split('-')
        else:
            assert '_' in file_name
            parts = file_name.split('_')
        name, version= '?', '?'
        l1, l2  = 'en', '?'
        if parts[-2] == l1 and parts[-1] in langs:
            l2 = parts[-1]
            version = parts[-3]
        elif parts[-3] == l1 and parts[-2] in langs:
            l2 = parts[-2]
            version = parts[-1]
        else:
            log.warn(f"Unable to parse {file_name} :: {parts}")
            continue
        name = '_'.join(parts[:-3])
        name = name.replace('-', '_')
        f1 = f'{l1}-{l2}/*.{l1}'
        f2 = f'{l1}-{l2}/*.{l2}'
        if name == 'wikipedia':
            f1 = f'{l1}-{l2}/{l1}.txt'
            f2 = f'{l1}-{l2}/{l2}.txt'

        ent = Entry(did=DatasetId(group=group_id, name=name, version=version, langs=(l1, l2)),
              url=url, ext='zip', in_ext='txt', in_paths=[f1, f2], cite=cite_txt)
        index.add_entry(ent)
