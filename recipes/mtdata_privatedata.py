"""
Example for loading private data
"""

from mtdata.index import Entry, Index, DatasetId

def load_all(index: Index):
    group = 'PrivateOrg' # A placeholder
    for lang in 'cs de en'.split():
         index.add_entry(Entry(DatasetId(group, 'dataset', 'v1', (lang,)),
                url=f'https://www.statmt.org/europarl/v10/training-monolingual/europarl-v10.{lang}.tsv.gz',
                in_ext='tsv', cols=(0,)))
