# MTData
[![image](http://img.shields.io/pypi/v/mtdata.svg)](https://pypi.python.org/pypi/mtdata/)
![Travis (.com)](https://img.shields.io/travis/com/thammegowda/mtdata?style=plastic)

MTData automates the collection and preparation of machine translation (MT) datasets.
It provides CLI and python APIs, which can be used for preparing MT experiments.

* [Quickstart Example](#quickstart--example)
* [Docs](https://thammegowda.github.io/mtdata/)
* Search datasets: https://thammegowda.github.io/mtdata/search.html


This tool knows:
- From where to download data sets: WMT News Translation tests and devs for Paracrawl,
  Europarl, News Commentary, WikiTitles, Tilde Model corpus, OPUS ...
- How to extract files : .tar, .tar.gz, .tgz, .zip, ...
- How to parse .tmx, .sgm and such XMLs, or .tsv ... Checks if they have same number of segments.
- Whether parallel data is in one .tsv file or two sgm files.
- Whether data is compressed in gz, xz or none at all.
- Whether the source-target is in the same order or is it swapped as target-source order.
- How to map code to ISO language codes! Using ISO 639_3 that has space for 7000+ languages of our planet.
  - New in v0.3: BCP-47 like language ID: (language, script, region)
- Download only once and keep the files in local cache.
- (And more of such tiny details over the time.)

[MTData](https://github.com/thammegowda/mtdata) is here to:
- Automate machinbe translation training data creation by taking out human intervention. This is inspired by [SacreBLEU](https://github.com/mjpost/sacreBLEU) that takes out human intervention at the evaluation stage.
- A reusable tool instead of dozens of use-once shell scripts spread across multiple repos.


# Installation
```bash
# from pypi
pip install mtdata

# from the source code on github
git clone https://github.com/thammegowda/mtdata
cd mtdata
pip install --editable .

# from develop branch
```


# Current Status:

We have added some commonly used datasets - you are welcome to add more! 
These are the summary of datasets from various sources (Updated: Feb 2022).

|                         Source | Dataset Count |
|-------------------------------:|--------------:|
| OPUS | 120,465|
| Neulab | 4,455|
| Facebook | 1,617|
| ELRC | 1,489|
| EU | 1,178|
| Statmt | 752|
| Tilde | 519|
| LinguaTools | 253|
| Anuvaad | 196|
| AI4Bharath | 192|
| ParaCrawl | 127|
| Lindat | 56|
| UN | 30|
| JoshuaDec | 29|
| StanfordNLP | 15|
| ParIce | 8|
| Phontron | 4|
| NRC_CA | 4|
| IITB | 3|
| WAT | 3|
| KECL | 2|
| Masakhane | 2|
| **Total** | **131,399** |


# Usecases
* USC ISI's 500-to-English MT: http://rtg.isi.edu/many-eng/
* WMT 2022 General (News) Translation Task: https://www.statmt.org/wmt22/mtdata/ 
* Meta AI's 200-to-200 MT: [Whitepaper](https://research.facebook.com/file/585831413174038/No-Language-Left-Behind--Scaling-Human-Centered-Machine-Translation.pdf)

# CLI Usage
- After pip installation, the CLI can be called using `mtdata` command  or `python -m mtdata`
- There are two sub commands: `list` for listing the datasets, and `get` for getting them

### `mtdata list`
Lists datasets that are known to this tool.
```bash
mtdata list -h
usage: __main__.py list [-h] [-l L1-L2] [-n [NAME ...]] [-nn [NAME ...]] [-f] [-o OUT]

optional arguments:
  -h, --help            show this help message and exit
  -l L1-L2, --langs L1-L2
                        Language pairs; e.g.: deu-eng (default: None)
  -n [NAME ...], --names [NAME ...]
                        Name of dataset set; eg europarl_v9. (default: None)
  -nn [NAME ...], --not-names [NAME ...]
                        Exclude these names (default: None)
  -f, --full            Show Full Citation (default: False)
``` 

```bash
# List everything ; add | cut -f1  to see ID column only
mtdata list | cut -f1

# List a lang pair 
mtdata list -l deu-eng 

# List a dataset by name(s)
mtdata list -n europarl
mtdata list -n europarl news_commentary

# list by both language pair and dataset name
 mtdata list -l deu-eng -n europarl news_commentary newstest_deen  | cut -f1
    Statmt-europarl-9-deu-eng
    Statmt-europarl-7-deu-eng
    Statmt-news_commentary-14-deu-eng
    Statmt-news_commentary-15-deu-eng
    Statmt-news_commentary-16-deu-eng
    Statmt-newstest_deen-2014-deu-eng
    Statmt-newstest_deen-2015-deu-eng
    Statmt-newstest_deen-2016-deu-eng
    Statmt-newstest_deen-2017-deu-eng
    Statmt-newstest_deen-2018-deu-eng
    Statmt-newstest_deen-2019-deu-eng
    Statmt-newstest_deen-2020-deu-eng
    Statmt-europarl-10-deu-eng
    OPUS-europarl-8-deu-eng

# get citation of a dataset (if available in index.py)
mtdata list -l deu-eng -n newstest_deen --full
```

### Dataset ID
Dataset IDs are standardized to this format:  
`<Group>-<name>-<version>-<lang1>-<lang2>`

* `Group`: source or the website where we are obtaining this dataset
* `name`: name of the dataset
* `version`: version name
* `lang1` and `lang2` are BCP47-like codes. In simple case, they are ISO-639-3 codes, however, they might have script and language tags separated by underscores (`_`). 


### `mtdata get`
This command downloads datasets specified by names for languages to a directory.
You will have to make definite choice for `--train` and `--test` arguments 

```
mtdata get -h
python -m mtdata get -h
usage: __main__.py get [-h] -l L1-L2 [-tr [ID ...]] [-ts [ID ...]] [-dv ID] [--merge | --no-merge] [--compress] -o OUT_DIR

optional arguments:
  -h, --help            show this help message and exit
  -l L1-L2, --langs L1-L2
                        Language pairs; e.g.: deu-eng (default: None)
  -tr [ID ...], --train [ID ...]
                        Names of datasets separated by space, to be used for *training*.
                            e.g. -tr Statmt-news_commentary-16-deu-eng europarl_v9 .
                             To concatenate all these into a single train file, set --merge flag. (default: None)
  -ts [ID ...], --test [ID ...]
                        Names of datasets separated by space, to be used for *testing*.
                            e.g. "-ts Statmt-newstest_deen-2019-deu-eng Statmt-newstest_deen-2020-deu-eng ".
                            You may also use shell expansion if your shell supports it.
                            e.g. "-ts Statmt-newstest_deen-20{19,20}-deu-eng"  (default: None)
  -dv ID, --dev ID     Dataset to be used for development (aka validation).
                            e.g. "-dv Statmt-newstest_deen-2017-deu-eng" (default: None)
  --merge               Merge train into a single file (default: False)
  --no-merge            Do not Merge train into a single file (default: True)
  --compress            Keep the files compressed (default: False)
  -o OUT_DIR, --out OUT_DIR
                        Output directory name (default: None)
```

## Quickstart / Example  
See what datasets are available for `deu-eng`
```bash
$ mtdata list -l deu-eng | cut -f1  # see available datasets
    Statmt-commoncrawl_wmt13-1-deu-eng
    Statmt-europarl_wmt13-7-deu-eng
    Statmt-news_commentary_wmt18-13-deu-eng
    Statmt-europarl-9-deu-eng
    Statmt-europarl-7-deu-eng
    Statmt-news_commentary-14-deu-eng
    Statmt-news_commentary-15-deu-eng
    Statmt-news_commentary-16-deu-eng
    Statmt-wiki_titles-1-deu-eng
    Statmt-wiki_titles-2-deu-eng
    Statmt-newstest_deen-2014-deu-eng
    ....[truncated]
```
Get these datasets and store under dir `data/deu-eng`
```bash
 $ mtdata get -l deu-eng --out data/deu-eng --merge \
     --train Statmt-europarl-10-deu-eng Statmt-news_commentary-16-deu-eng \
     --dev Statmt-newstest_deen-2017-deu-eng  --test Statmt-newstest_deen-20{18,19,20}-deu-eng
    # ...[truncated]   
    INFO:root:Train stats:
    {
      "total": 2206240,
      "parts": {
        "Statmt-news_commentary-16-deu-eng": 388482,
        "Statmt-europarl-10-deu-eng": 1817758
      }
    }
    INFO:root:Dataset is ready at deu-eng
```
To reproduce this dataset again in the future or by others, please refer to `<out-dir>/mtdata.signature.txt`:
```bash
$ cat deu-eng/mtdata.signature.txt
mtdata get -l deu-eng -tr Statmt-europarl-10-deu-eng Statmt-news_commentary-16-deu-eng \
   -ts Statmt-newstest_deen-2018-deu-eng Statmt-newstest_deen-2019-deu-eng Statmt-newstest_deen-2020-deu-eng \
   -dv Statmt-newstest_deen-2017-deu-eng --merge -o <out-dir>
mtdata version 0.3.0-dev
```

See what the above command has accomplished:
```bash 
$ tree  data/deu-eng/
├── dev.deu -> tests/Statmt-newstest_deen-2017-deu-eng.deu
├── dev.eng -> tests/Statmt-newstest_deen-2017-deu-eng.eng
├── mtdata.signature.txt
├── test1.deu -> tests/Statmt-newstest_deen-2020-deu-eng.deu
├── test1.eng -> tests/Statmt-newstest_deen-2020-deu-eng.eng
├── test2.deu -> tests/Statmt-newstest_deen-2018-deu-eng.deu
├── test2.eng -> tests/Statmt-newstest_deen-2018-deu-eng.eng
├── test3.deu -> tests/Statmt-newstest_deen-2019-deu-eng.deu
├── test3.eng -> tests/Statmt-newstest_deen-2019-deu-eng.eng
├── tests
│   ├── Statmt-newstest_deen-2017-deu-eng.deu
│   ├── Statmt-newstest_deen-2017-deu-eng.eng
│   ├── Statmt-newstest_deen-2018-deu-eng.deu
│   ├── Statmt-newstest_deen-2018-deu-eng.eng
│   ├── Statmt-newstest_deen-2019-deu-eng.deu
│   ├── Statmt-newstest_deen-2019-deu-eng.eng
│   ├── Statmt-newstest_deen-2020-deu-eng.deu
│   └── Statmt-newstest_deen-2020-deu-eng.eng
├── train-parts
│   ├── Statmt-europarl-10-deu-eng.deu
│   ├── Statmt-europarl-10-deu-eng.eng
│   ├── Statmt-news_commentary-16-deu-eng.deu
│   └── Statmt-news_commentary-16-deu-eng.eng
├── train.deu
├── train.eng
├── train.meta.gz
└── train.stats.json
```

## Recipes

> Since v0.3.1

Recipe is a set of datasets nominated for train, dev, and tests, and are meant to improve reproducibility of experiments.
Recipes are loaded from 
1. Default:  [`mtdata/recipe/recipes.yml`](mtdata/recipe/recipes.yml) from source code
2. Cache dir: `$MTDATA/mtdata.recipes.yml` where `$MTDATA` has default of `~/.mtdata`
3. Current dir: All files matching the glob: `$PWD/mtdata.recipes*.yml` 
   * If current dir is not preferred, `export MTDATA_RECIPES=/path/to/dir`
   * Alternatively, `MTDATA_RECIPES=/path/to/dir mtdata list-recipe` 

See [`mtdata/recipe/recipes.yml`](mtdata/recipe/recipes.yml) for the format and examples.

```bash
mtdata list-recipe  # see all recipes
mtdata get-recipe -ri <recipe_id> -o <out_dir>  # get recipe, recreate dataset
```

## Language Name Standardization
### ISO 639 3 
Internally, all language codes are mapped to ISO-639 3 codes.
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

### BCP-47 

> Since v0.3.0

We used ISO 639-3 from the beginning, however, we soon faced the limitation that ISO 639-3 cannot distinguish script and region variants of language. So we have upgraded to BCP-47 like language tags in `v0.3.0`.

* BCP47 uses two-letter codes to some and three-letter codes to the rest, we use three-letter codes to all languages.
* BCP47 uses `-` hyphens we use `_` underscores, since hyphens are used by MT community to separate bitext pairs (e.g. en-de or eng-deu)


Our tags are of form `xxx_Yyyy_ZZ` where 
 
| Pattern | Purpose  | Standard   | Length        | Case      | Required  | 
|---------|----------|------------|---------------|-----------|-----------|
| `xxx`   | Language | ISO 639-3  | three-letters | lowercase | mandatory |
| `Yyyy`  | Script   | ISO 15924  | four-letters  | Titlecase | optional  |
| `ZZ`    | Region   | ISO 3166-1 | two-letters   | CAPITALS  | optional  |


Notes:
* Region is preserved when available and left blank when unavailable
* Script `Yyyy` is forcibly suppressed in obvious cases. E.g. `eng` is written using `Latn` script, writing `eng-Latn` is just awkward to read as `Latn` is default we suppress `Latn` script for English. On the other hand a language like `Kannada` is written using `Knda` script (`kan-Knda` -> `kan`), but occasionally written using `Latn` script, so `kan-Latn` is not suppressed. 
* The information about what is default script is obtained from IANA language code registry
* Language code `mul` stands for _multiple languages, and is used as a placeholder for multilingual datasets (See `mul-eng` to represent many-to-English dataset recipes in [(mtdata/recipe/recipes.yml](mtdata/recipe/recipes.yml))

#### Example:
To inspect parsing/mapping, use `python -m mtdata.iso.bcp47 <args>` 

```bash
python -m mtdata.iso.bcp47 eng English en-US en-GB eng-Latn kan Kannada-Deva hin-Deva kan-Latn
```

| INPUT	        | STD	      | LANG	 | SCRIPT	 | REGION |
|---------------|-----------|-------|---------|--------|
| eng	          | eng	      | eng	  | None	   | None   |
| English	      | eng	      | eng	  | None	   | None   |
| en-US	        | eng_US	   | eng	  | None	   | US     |
| en-GB	        | eng_GB	   | eng	  | None	   | GB     |
| eng-Latn	     | eng	      | eng	  | None	   | None   |
| kan	          | kan	      | kan	  | None	   | None   |
| Kannada-Deva	 | kan_Deva	 | kan	  | Deva	   | None   |
| hin-Deva	     | hin	      | hin	  | None	   | None   |
| kan-Latn	     | kan_Latn	 | kan	  | Latn	   | None   |
| kan-in	       | kan_IN	   | kan	  | None	   | IN     |
| kn-knda-in	   | kan_IN	   | kan	  | None	   | IN     |

**Python API for BCP47 Mapping**
```python
from mtdata.iso.bcp47 import bcp47
tag = bcp47("en_US")
print(*tag)  # tag is a tuple
print(f"{tag}")  # str(tag) gets standardized string
```

## How to Contribute:
* Please help grow the datasets by adding any missing and new datasets to [`index`](mtdata/index/__init__.py) module.
* Please create issues and/or pull requests at https://github.com/thammegowda/mtdata/ 

## Change Cache Directory:

The default cache directory is `$HOME/.mtdata`.
It can grow to a large size when you download a lot of datasets using this command.

To change it: 
*  set the following environment variable
`export MTDATA=/path/to/new-cache-dir`
* Alternatively, move `$HOME/.mtdata` to the desired place and create a symbolic link 
```bash
mv $HOME/.mtdata /path/to/new/place
ln -s /path/to/new/place $HOME/.mtdata
```

## Run tests
Tests are located in [tests/](tests) directory. To run all the tests:

    python -m pytest



## Developers and Contributor:
See - https://github.com/thammegowda/mtdata/graphs/contributors

## Citation

https://aclanthology.org/2021.acl-demo.37/ 


```
@inproceedings{gowda-etal-2021-many,
    title = "Many-to-{E}nglish Machine Translation Tools, Data, and Pretrained Models",
    author = "Gowda, Thamme  and
      Zhang, Zhao  and
      Mattmann, Chris  and
      May, Jonathan",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.acl-demo.37",
    doi = "10.18653/v1/2021.acl-demo.37",
    pages = "306--316",
}
```

---
## Disclaimer on Datasets

This tools downloads and prepares public datasets. We do not host or distribute these datasets, vouch for their quality or fairness, or make any claims regarding license to use these datasets. It is your responsibility to determine whether you have permission to use the dataset under the dataset's license.
We request all the users of this tool to cite the original creators of the datsets, which maybe obtained from  `mtdata list -n <NAME> -l <L1-L2> -full`.

If you're a dataset owner and wish to update any part of it (description, citation, etc.), or do not want your dataset to be included in this library, please get in touch through a GitHub issue. Thanks for your contribution to the ML community!
