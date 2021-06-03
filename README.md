# MTData
MTData tool automates the dataset collection and preparation for machine translation research.
It provides CLI and python APIs, so it can be used as a standalone tool or embedded into
 python apps for preparing MT experiments.

This tool knows:
- From where to download data sets: WMT tests and devs for \[2014, 2015, ... 2020], Paracrawl, 
  Europarl, News Commentary, WikiTitles, Tilde Model corpus, OPUS ... 
- How to extract files : .tar, .tar.gz, .tgz, .zip, ... 
- How to parse .tmx, .sgm and such XMLs, or .tsv ... Checks if they have same number of segments.  
- Whether parallel data is in one .tsv file or two sgm files.
- Whether data is compressed in gz, xz or none at all.
- Whether the source-target is in the same order or is it swapped as target-source order.
- How to map code to ISO language codes! Using ISO 639_3 that has space for 7000+ languages of our planet.
- Download only once and keep the files in local cache.
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
pip install --editable .

# from pypi 
pip install mtdata  
```

# Current Status:

These are the summary of datasets from various sources (Updated: May 10 2020). 
The list is incomplete and meant to see as start. 
We have added some commonly used datasets - you are welcome to add more! 
 
| Source | # of datasets |
|---: | ---:|
| OPUS<sup>$1</sup> | 69,415 |
| JW300<sup>$2</sup> | 45,548 |
| Neulab_TEDTalksv1 | 4,455 |
| WikiMatrix | 1,617 |
| ELRC-SHARE | 1,297 |
| EU | 925 |
| Tilde | 519 |
| Statmt | 493 |
| OPUS100v1 | 302 |
| Paracrawl | 96 |
| AI4Bharath | 66 |
| UnitedNations<sup>$3</sup> | 30 |
| Joshua Indian Corpus | 29 |
| Other | 70 |
| ----|----|
| Total | 124,844 |

- <sup>$1</sup> - OPUS contains duplicate entries from other listed sources, but they are often older releases of corpus.
- <sup>$2</sup> - JW300 is also retrieved from OPUS, however handled differently due to the difference in the scale and internal format.
- <sup>$3</sup> - Only test sets are included

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
                        Language pairs; e.g.: deu-eng (default: None)
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
mtdata list -l deu-eng

# List a dataset by name(s)
mtdata list -n europarl_v9
mtdata list -n europarl_v9 news_commentary_v14

# list by both language pair and dataset name
mtdata list -l deu-eng -n europarl_v9 news_commentary_v14 newstest201{4,5,6,7,8,9}_deen

# get citation of a dataset (if available in index.py)
mtdata list -l deu-eng -n newstest2019_deen --full
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
                        Language pairs; e.g.: deu-eng 
  -tr [NAME [NAME ...]], --train [NAME [NAME ...]]
                        Names of datasets separated by space, to be used for *training*.
                          e.g. -tr news_commentary_v14 europarl_v9 .
                          To concatenate all these into a single train file, set --merge flag.
  -tt [NAME [NAME ...]], --test [NAME [NAME ...]]
                        Names of datasets separated by space, to be used for *testing*.
                          e.g. "-tt newstest2018_deen newstest2019_deen".
                        You may also use shell expansion if your shell supports it.
                          e.g. "-tt newstest201{8,9}_deen."
  --merge               Merge train into a single file (default: False)
  --no-merge            Do not Merge train into a single file (default: True)
                          
  -o OUT, --out OUT     Output directory name
```

# Example  
See what datasets are available for `deu-eng`
```bash
$ mtdata list -l deu-eng  # see available datasets
    europarl_v9	deu-eng	http://www.statmt.org/europarl/v9/training/europarl-v9.deu-eng.tsv.gz
    news_commentary_v14	deu-eng	http://data.statmt.org/news-commentary/v14/training/news-commentary-v14.deu-eng.tsv.gz
    wiki_titles_v1	deu-eng	http://data.statmt.org/wikititles/v1/wikititles-v1.deu-eng.tsv.gz
    wiki_titles_v2	deu-eng	http://data.statmt.org/wikititles/v2/wikititles-v2.deu-eng.tsv.gz
    newstest2014_deen	deu-eng	http://data.statmt.org/wmt20/translation-task/dev.tgz	dev/newstest2014-deen-src.de.sgm,dev/newstest2014-deen-ref.en.sgm
    newstest2015_ende	en-de	http://data.statmt.org/wmt20/translation-task/dev.tgz	dev/newstest2015-ende-src.en.sgm,dev/newstest2015-ende-ref.de.sgm
    newstest2015_deen	deu-eng	http://data.statmt.org/wmt20/translation-task/dev.tgz	dev/newstest2015-deen-src.de.sgm,dev/newstest2015-deen-ref.en.sgm
    ...[truncated]
```
Get these datasets and store under dir `deu-eng`
```bash
$ mtdata get --langs deu-eng --merge --train europarl_v10 wmt13_commoncrawl news_commentary_v14 --test newstest201{4,5,6,7,8,9}_deen --out deu-eng
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
    INFO:root:Dataset is ready at deu-eng
```
To reproduce this dataset again in the future or by others, please refer to `<out-dir>>/mtdata.signature.txt`:
```bash
$ cat deu-eng/mtdata.signature.txt
mtdat get -l deu-eng -tr europarl_v10 wmt13_commoncrawl news_commentary_v14 -ts newstest2014_deen newstest2015_deen newstest2016_deen newstest2017_deen newstest2018_deen newstest2019_deen -o <out-dir>
mtdata version 0.1.1
```

See what the above command has accomplished:
```bash 
$ find  deu-eng -type f | sort  | xargs wc -l
    3003 deu-eng/tests/newstest2014_deen.deu
    3003 deu-eng/tests/newstest2014_deen.eng
    2169 deu-eng/tests/newstest2015_deen.deu
    2169 deu-eng/tests/newstest2015_deen.eng
    2999 deu-eng/tests/newstest2016_deen.deu
    2999 deu-eng/tests/newstest2016_deen.eng
    3004 deu-eng/tests/newstest2017_deen.deu
    3004 deu-eng/tests/newstest2017_deen.eng
    2998 deu-eng/tests/newstest2018_deen.deu
    2998 deu-eng/tests/newstest2018_deen.eng
    2000 deu-eng/tests/newstest2019_deen.deu
    2000 deu-eng/tests/newstest2019_deen.eng
 1828521 deu-eng/train-parts/europarl_v10.deu
 1828521 deu-eng/train-parts/europarl_v10.eng
  338285 deu-eng/train-parts/news_commentary_v14.deu
  338285 deu-eng/train-parts/news_commentary_v14.eng
 2399123 deu-eng/train-parts/wmt13_commoncrawl.deu
 2399123 deu-eng/train-parts/wmt13_commoncrawl.eng
 4565929 deu-eng/train.deu
 4565929 deu-eng/train.eng
```

# ISO 639 3 
Internally all language codes are mapped to ISO-639 3 codes.
The mapping can be inspected with `python -m mtdata.iso ` or `mtdata-iso`
```bash
$  mtdata-iso -h
usage: python -m mtdata.iso [-h] [-b] [langs [langs ...]]

ISO 639-3 lookup tool

positional arguments:
  langs        Language code or name that needs to be looked up. When no
               language code is given, all languages are listed.

optional arguments:
  -h, --help   show this help message and exit
  -b, --brief  be brief; do crash on error inputs

# list all 7000+ languages and their 3 letter codes
$ mtdata-iso    # python -m mtdata.iso 
...

# lookup codes for some languages
$ mtdata-iso ka kn en de xx english german
Input   ISO639_3        Name
ka      kat     Georgian
kn      kan     Kannada
en      eng     English
de      deu     German
xx      -none-  -none-
english eng     English
german  deu     German

# Print no header, and crash on error; 
$ mtdata-iso xx -b
Exception: Unable to find ISO 639-3 code for 'xx'. Please run
python -m mtdata.iso | grep -i <name>
to know the 3 letter ISO code for the language.
```
To use Python API
```python
from mtdata.iso import iso3_code
print(iso3_code('en', fail_error=True))
print(iso3_code('eNgLIsH', fail_error=True))  # case doesnt matter
```

# How to extend, modify, or contribute:
Please help grow the datasets by adding any missing and new datasets to [`index`](mtdata/index/__init__.py) module.
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
from mtdata.index import INDEX as index, Entry
wmt_sets = {
    'newstest2014': [('de', 'en'), ('cs', 'en'), ('fr', 'en'), ('ru', 'en'), ('hi', 'en')],
    'newsdev2015': [('fi', 'en'), ('en', 'fi')]
}
for set_name, pairs in wmt_sets.items():
    for l1, l2 in pairs:
        src = f'dev/{set_name}-{l1}{l2}-src.{l1}.sgm'
        ref = f'dev/{set_name}-{l1}{l2}-ref.{l2}.sgm'
        name = f'{set_name}_{l1}{l2}'
        index.add_entry(Entry((l1, l2), name=name, filename='wmt20dev.tgz', in_paths=[src, ref],
                             url='http://data.statmt.org/wmt20/translation-task/dev.tgz'))
# filename='wmt20dev.tgz' -- is manually set, because url has dev.gz that can be confusing
# in_paths=[src, ref]  -- listing two sgm files inside the tarball
# in_ext='sgm' will be auto detected fropm path. set in_ext='txt' to explicitly set format as plain text 
```
Refer to [paracrawl](mtdata/index/paracrawl.py), [tilde](mtdata/index/tilde.py), or
 [statmt](mtdata/index/statmt.py) for examples.
 
If citation is available for a dataset, please add BibTeX entry to [mtdata/index/refs.bib](mtdata/index/refs.bib) 

```python
from mtdata.index import INDEX as index, Entry

cite = index.ref_db.get_bibtex('author-etal')
Entry(..., cite=cite)
```

When index is modified without incrementing version number, you will have to force refresh cache of index. The following command with `-ri` or `--reindex` flag helps reindex datasets. 

`python -m mtdata -ri list ` or `python -m mtdata --reindex list ` to refresh cache of index.  

For adding a custom parser, or file handler look into [`parser.read_segs()`](mtdata/parser.py) 
and [`cache`](mtdata/cache.py) for dealing with a new archive/file type that is not already supported.

## Change Cache Directory:

The default cache directory is `$HOME/.mtdata`. To change it, set the following environment variable
`export MTDATA=/path/to/new-cache-dir`


 
## Run tests
Tests are located in [tests/](tests) directory. To run all the tests:

    python -m pytest



## Developers and Contributor:
See - https://github.com/thammegowda/mtdata/graphs/contributors



--- 
# Disclaimer on Datasets

This tools downloads and prepares public datasets. We do not host or distribute these datasets, vouch for their quality or fairness, or make any claims regarding license to use these datasets. It is your responsibility to determine whether you have permission to use the dataset under the dataset's license.
We request all the users of this tool to cite the original creators of the datsets, which maybe obtained from  `mtdata list -n <NAME> -l <L1-L2> -full`.

If you're a dataset owner and wish to update any part of it (description, citation, etc.), or do not want your dataset to be included in this library, please get in touch through a GitHub issue. Thanks for your contribution to the ML community!
