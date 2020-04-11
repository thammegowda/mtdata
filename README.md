# MTData
MTData tool automate the dataset collection and preparation for machine translation research.
It provides CLI and python APIs, so it can be used as a standalone tool or embedded into
 python apps for preparing MT experiments.

This tool knows:
- From where to download data sets: WMT tests and devs for \[2014, 2015, ... 2020], Paracrawl, 
  Europarl, News Commentary, WikiTitles, Tilde Model corpus ... 
- How to extract files : .tar, .tar.gz, .tgz, .zip, ... 
- How to parse .tmx, .sgm and such XMLs, or .tsv ... Checks if they have same number of segments.  
- Whether parallel data is in one .tsv file or two sgm files.
- Whether data is compressed in gz, xz or none at all.
- Whether the source-target is in the same order or is it swapped as target-source order.
- (And more of such tiny details over the time.)

[MTData](https://github.com/thammegowda/mtdata) is here to:
- Automate the MT training data creation by taking out human intervention. Inspired by [SacreBLEU](https://github.com/mjpost/sacreBLEU) that takes out human intervention in evaluation stage.
- A reusable tool instead of dozens of use-once shell scripts spread across multiple repos. 

Limitations (as of now):
- Only publicly available datasets that do not need login are supported. No LDC yet.
- No tokenizers are integrated. (It should be fairly easy to get those integrated) 

# Installation
```bash
# from the source code on github 
git clone https://github.com/thammegowda/mtdata 
cd mtdata
pip install . --editable

# from pypi ; do not do this yet, since the code is evolving faster than releases
pip install mtdata  
```

# CLI Usage
- After pip installation, the CLI can be called using `mtdata` command  or `python -m mtdata`
- There are two sub commands: `list` for listing the datasets, and `get` for getting them   

### `mtdata list`
Lists datasets that are known to this tool.
```bash
mtdata list -h
usage: mtdata list [-h] [-l L1-L2] [-n [NAME [NAME ...]]]
                   [-nn [NAME [NAME ...]]] [-f]

optional arguments:
  -h, --help            show this help message and exit
  -l L1-L2, --langs L1-L2
                        Language pairs; e.g.: de-en (default: None)
  -n [NAME [NAME ...]], --names [NAME [NAME ...]]
                        Name of dataset set; eg europarl_v9. (default: None)
  -nn [NAME [NAME ...]], --not-names [NAME [NAME ...]]
                        Exclude these names (default: None)
  -f, --full            Show Full Citation (default: False)
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

# get citation of a dataset (if available in index.py)
mtdata list -l de-en -n newstest2019_deen --full
```

## `mtdata get`
This command downloads datasets specified by names for languages to a directory.
You will have to make definite choice for `--train` and `--test` arguments 
```bash
mtdata get -h
usage: mtdata get [-h] -l L1-L2 [-tr [NAME [NAME ...]]]
                  [-tt [NAME [NAME ...]]] -o OUT

optional arguments:
  -h, --help            show this help message and exit
  -l L1-L2, --langs L1-L2
                        Language pairs; e.g.: de-en (default: None)
  -tr [NAME [NAME ...]], --train [NAME [NAME ...]]
                        Names of datasets separated by space, to be used for *training*.
                          e.g. -tr news_commentary_v14 europarl_v9 .
                          All these datasets gets concatenated into one big file.
                           (default: None)
  -tt [NAME [NAME ...]], --test [NAME [NAME ...]]
                        Names of datasets separated by space, to be used for *testing*.
                          e.g. "-tt newstest2018_deen newstest2019_deen".
                        You may also use shell expansion if your shell supports it.
                          e.g. "-tt newstest201{8,9}_deen."  (default: None)
  -o OUT, --out OUT     Output directory name (default: None)
```

# Example  
See what datasets are available for `de-en`
```bash
$ mtdata list -l de-en  # see available datasets
    europarl_v9	de-en	http://www.statmt.org/europarl/v9/training/europarl-v9.de-en.tsv.gz
    news_commentary_v14	de-en	http://data.statmt.org/news-commentary/v14/training/news-commentary-v14.de-en.tsv.gz
    wiki_titles_v1	de-en	http://data.statmt.org/wikititles/v1/wikititles-v1.de-en.tsv.gz
    wiki_titles_v2	de-en	http://data.statmt.org/wikititles/v2/wikititles-v2.de-en.tsv.gz
    newstest2014_deen	de-en	http://data.statmt.org/wmt20/translation-task/dev.tgz	dev/newstest2014-deen-src.de.sgm,dev/newstest2014-deen-ref.en.sgm
    newstest2015_ende	en-de	http://data.statmt.org/wmt20/translation-task/dev.tgz	dev/newstest2015-ende-src.en.sgm,dev/newstest2015-ende-ref.de.sgm
    newstest2015_deen	de-en	http://data.statmt.org/wmt20/translation-task/dev.tgz	dev/newstest2015-deen-src.de.sgm,dev/newstest2015-deen-ref.en.sgm
    ...[truncated]
```
Get these datasets and store under dir `de-en`
```bash
$ mtdata get --langs de-en --train europarl_v10 wmt13_commoncrawl news_commentary_v14 --test newstest201{4,5,6,7,8,9}_deen --out de-en
    # ...[truncated]   
    INFO:root:Train stats:
    {
      "total": 4565929,
      "parts": {
        "wmt13_commoncrawl": 2399123,
        "news_commentary_v14": 338285,
        "europarl_v10": 1828521
      }
    }
    INFO:root:Dataset is ready at de-en
    INFO:root:mtdata args for reproducing this dataset:
    mtdat get -l de-en -tr europarl_v10 wmt13_commoncrawl news_commentary_v14 -ts newstest2014_deen newstest2015_deen newstest2016_deen newstest2017_deen newstest2018_deen newstest2019_deen -o <out-dir>
    mtdata version: 0.1.1     
```
To reproduce this dataset again in future or by others, do :
```bash
mtdata get -l de-en -tr europarl_v10 wmt13_commoncrawl news_commentary_v14 -ts newstest2014_deen \
 newstest2015_deen newstest2016_deen newstest2017_deen newstest2018_deen newstest2019_deen -o <out-dir>
```

See what the above command has accomplished:
```bash 
$ find  de-en -type f | sort  | xargs wc -l
    3003 de-en/tests/newstest2014_deen.de
    3003 de-en/tests/newstest2014_deen.en
    2169 de-en/tests/newstest2015_deen.de
    2169 de-en/tests/newstest2015_deen.en
    2999 de-en/tests/newstest2016_deen.de
    2999 de-en/tests/newstest2016_deen.en
    3004 de-en/tests/newstest2017_deen.de
    3004 de-en/tests/newstest2017_deen.en
    2998 de-en/tests/newstest2018_deen.de
    2998 de-en/tests/newstest2018_deen.en
    2000 de-en/tests/newstest2019_deen.de
    2000 de-en/tests/newstest2019_deen.en
 1828521 de-en/train-parts/europarl_v10.de
 1828521 de-en/train-parts/europarl_v10.en
  338285 de-en/train-parts/news_commentary_v14.de
  338285 de-en/train-parts/news_commentary_v14.en
 2399123 de-en/train-parts/wmt13_commoncrawl.de
 2399123 de-en/train-parts/wmt13_commoncrawl.en
 4565929 de-en/train.de
 4565929 de-en/train.en
```

# How to extend, modify, or contribute:
Please help grow the datasets by adding missing+new datasets to [`index`](mtdata/index/__init__.py) module.
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
Refer to [paracrawl](mtdata/index/paracrawl.py), [tilde](mtdata/index/tilde.py), or
 [statmt](mtdata/index/statmt.py) for examples.
 
If citation is available for a dataset, please include
```python
cite = r"""bib tex here""
Entry(... cite=cite)
```

For adding a custom parser, or file handler look into [`parser.read_segs()`](mtdata/parser.py) 
and [`cache`](mtdata/cache.py) for dealing with a new archive/file type that is not already supported.
 

## Developers:
- [Thamme Gowda](https://twitter.com/thammegowda) 
