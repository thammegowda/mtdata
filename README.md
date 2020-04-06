# MTData
MTData tool is written to reduce the burden of preparing the datasets for machine translation.
It provides commandline and python APIs that can be either used as a standalone tool, 
or call it from shell scripts or embed it in python application for preparing MT experiments.

With this you DON'T have to :
- Know where the URLs are for data sets: WMT tests and devs for \[2014, 2015, ... 2020], Paracrawl, 
  Europarl, News Commentary, WikiTitles ...
- Know how to extract files : .tar, .tar.gz, .tgz, .zip, .gz, ...
- Know how to parse .tmx, .sgm, .tsv
- Know if parallel data is in one .tsv file or two sgm files 
- (And more over the time. Create an issue discuss more of such "you dont have to" topics)

because, [MTData](https://github.com/thammegowda/mtdata) does all the above for you! 

## Installation
```bash
# from pypi
pip install mtdata 

# from the source on github 
git clone https://github.com/thammegowda/mtdata 
cd mtdata
pip install .  # add "--editable" flag for development mode 
```

## CLI Usage
- After pip installation, the CLI can be called using `mtdata` command  or `python -m mtdata`
- There are two sub commands: `list` for listing the datasets, and `get` for getting them   
### `mtdata list`
```bash
mtdata list -h
usage: mtdata list [-h] [-l LANGS] [-n [NAMES [NAMES ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -l LANGS, --langs LANGS
                        Language pairs; e.g.: de-en
  -n [NAMES [NAMES ...]], --names [NAMES [NAMES ...]]
                        Name of dataset set; eg europarl_v9.
``` 

```bash
# List everything
mtdata list

# List a lang pair 
mtdata list -l de-en

# List a dataset by name(s)
mtdata list -n europarl_v9
mtdata list -n europarl_v9 news_commentary_v14

# list by both language pair and dataset name
mtdata list -l de-en -n europarl_v9 news_commentary_v14 newstest201{4,5,6,7,8,9}_deen
```

## `mtdata get`
```bash
mtdata get -h
usage: mtdata get [-h] -l LANGS [-n [NAMES [NAMES ...]]] -o OUT

optional arguments:
  -h, --help            show this help message and exit
  -l LANGS, --langs LANGS
                        Language pairs; e.g.: de-en
  -n [NAMES [NAMES ...]], --names [NAMES [NAMES ...]]
                        Name of dataset set; eg europarl_v9.
  -o OUT, --out OUT     Output directory name
```
Here is an example showing collection and preparation of DE-EN datasets. 
```bash
mtdata get  -l de-en -n europarl_v9 news_commentary_v14 newstest201{4,5,6,7,8,9}_deen -o de-en
# It created a dir named `de-en`. And here are the contents
 1838557 42471404 de-en/parts/europarl_v9.de
 1838557 45547035 de-en/parts/europarl_v9.en
  338157 7399080 de-en/parts/news_commentary_v14.de
  338157 7212171 de-en/parts/news_commentary_v14.en
    3003   54865 de-en/parts/newstest2014_deen.de
    3003   59326 de-en/parts/newstest2014_deen.en
    2169   38160 de-en/parts/newstest2015_deen.de
    2169   40771 de-en/parts/newstest2015_deen.en
    2999   53944 de-en/parts/newstest2016_deen.de
    2999   56789 de-en/parts/newstest2016_deen.en
    3004   52833 de-en/parts/newstest2017_deen.de
    3004   56435 de-en/parts/newstest2017_deen.en
    2998   54933 de-en/parts/newstest2018_deen.de
    2998   58628 de-en/parts/newstest2018_deen.en
    2000   31097 de-en/parts/newstest2019_deen.de
    2000   34386 de-en/parts/newstest2019_deen.en
```


## How to extend or contribute:
Please help grow the datasets by adding missing+new datasets to [`index.py`](mtdata/index.py) module.
Here is an example listing europarl-v9 corpus.
```python
from mtdata.index import entries, Entry
EUROPARL_v9 = 'http://www.statmt.org/europarl/v9/training/europarl-v9.%s-%s.tsv.gz'
for pair in ['de en', 'cs en', 'cs pl', 'es pt', 'fi en', 'lt en']:
    l1, l2 = pair.split()
    entries.append(Entry(langs=(l1, l2), name='europarl_v9', url=EUROPARL_v9 % (l1, l2)))
```
If a datset is inside an archive such as `zip` or `tar`
```python
from mtdata.index import entries, Entry
wmt_sets = {
    'newstest2014': [('de', 'en'), ('cs', 'en'), ('fr', 'en'), ('ru', 'en'), ('hi', 'en')],
    'newsdev2015': [('fi', 'en'), ('en', 'fi')]
}
for set_name, pairs in wmt_sets.items():
    for l1, l2 in pairs:
        src = f'dev/{set_name}-{l1}{l2}-src.{l1}.sgm'
        ref = f'dev/{set_name}-{l1}{l2}-ref.{l2}.sgm'
        name = f'{set_name}_{l1}{l2}'
        entries.append(Entry((l1, l2), name=name, filename='wmt20dev.tgz', in_paths=[src, ref],
                             url='http://data.statmt.org/wmt20/translation-task/dev.tgz'))
# filename='wmt20dev.tgz' -- is manually set, because url has dev.gz that can be confusing
# in_paths=[src, ref]  -- listing two sgm files inside the tarball
```
For adding a custom parser, or file handler look into [`parser.read_segs()`](mtdata/parser.py) 
and [`cache`](mtdata/cache.py) for dealing with a new archive/file type that is not already supported.
 

## Developers:
- [Thamme Gowda](https://twitter.com/thammegowda) 
