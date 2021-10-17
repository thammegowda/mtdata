# How to extend

Here is an example listing europarl-v9 corpus.
Note: the language codes such as `de` `en` etc will be mapped to 3 letter ISO codes `deu` `eng` internally

```python
from mtdata.index import INDEX as index, Entry
EUROPARL_v9 = 'http://www.statmt.org/europarl/v9/training/europarl-v9.%s-%s.tsv.gz'
for pair in ['de en', 'cs en', 'cs pl', 'es pt', 'fi en', 'lt en']:
    l1, l2 = pair.split()
    index.add_entry(Entry(langs=(l1, l2), name='europarl_v9', url=EUROPARL_v9 % (l1, l2)))
```

If a datset is inside an archive such as `zip` or `tar`
```python
from mtdata.index import INDEX as index, Entry, DatasetId
wmt_sets = {
    'newstest2014': [('de', 'en'), ('cs', 'en'), ('fr', 'en'), ('ru', 'en'), ('hi', 'en')],
    'newsdev2015': [('fi', 'en'), ('en', 'fi')]
}
for set_name, pairs in wmt_sets.items():
    for l1, l2 in pairs:
        src = f'dev/{set_name}-{l1}{l2}-src.{l1}.sgm'
        ref = f'dev/{set_name}-{l1}{l2}-ref.{l2}.sgm'
        name = f'{set_name}_{l1}{l2}'
        index.add_entry(Entry(did=DatasetId((l1, l2), name=name, 
                                            filename='wmt20dev.tgz', in_paths=[src, ref],
                             url='http://data.statmt.org/wmt20/translation-task/dev.tgz'))
# filename='wmt20dev.tgz' -- is manually set, because url has dev.gz that can be confusing
# in_paths=[src, ref]  -- listing two sgm files inside the tarball
# in_ext='sgm' will be auto detected fropm path. set in_ext='txt' to explicitly set format as plain text 
```
Refer to [paracrawl](mtdata/index/paracrawl.py), [tilde](mtdata/index/tilde.py), or
 [statmt](mtdata/index/statmt.py) for examples.
 
If citation is available for a dataset, please add BibTeX entry to [mtdata/index/refs.bib](mtdata/index/refs.bib) 

```python
from mtdata.index import INDEX as index, Entry,

cite = index.ref_db.get_bibtex('author-etal')
Entry(..., cite=cite)
```

When index is modified without incrementing version number, you will have to force refresh cache of index. The following command with `-ri` or `--reindex` flag helps reindex datasets. 

`python -m mtdata -ri list ` or `python -m mtdata --reindex list ` to refresh cache of index.  

For adding a custom parser, or file handler look into [`parser.read_segs()`](mtdata/parser.py) 
and [`cache`](mtdata/cache.py) for dealing with a new archive/file type that is not already supported.