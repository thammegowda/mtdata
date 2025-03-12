# Change Log

## 0.4.3 - WIP
* Add preliminary support for huggingface datasets; currently wmt24++ is the only supported dataset
* Update setup.py -> pyproject.toml; hf datasets is optional dependency
* Add mtdata index subcommand. deprecate `mtdata --reindex <cmd>`
* Add meta, a dictionary field to Entry to store arbitrary key-vals which maybe useful for downloading and parsing datasets.
* Preliminary support for document id , (currently, one among the many in meta fields)


## v0.4.2
- minor fixes

## v0.4.1 - 20240425
* Better parallelization: parallel and mono data are scheduled at once (previously it was one after the other)
* `mtdata cache` added. Improves concurrency by supporting multiple recipes
* Added WMT general test 2022 and 2023
* mtdata-bcp47 : -p/--pipe to map codes from stdin -> stdout
* mtdata-bcp47 : --script {suppress-default,suppress-all,express}
* Uses`pigz` to read and write gzip files by default when pigz is in PATH. export `USE_PIGZ=0` to disable

## v0.4.0 - 20230326

* Fix: allenai_nllb.json is now included in MANIFEST.in [#137](https://github.com/thammegowda/mtdata/issues/137). Also fixed CI: Travis -> github actions
* Update ELRC datasets [#138](https://github.com/thammegowda/mtdata/pull/138). Thanks [@AlexUmnov](https://github.com/AlexUmnov)
* Add Jparacrawl Chinese-Japanese subset  [#143](https://github.com/thammegowda/mtdata/pull/143 ). Thanks [@BrightXiaoHan](https://github.com/BrightXiaoHan)
* Add Flores200 dev and devtests [#145](https://github.com/thammegowda/mtdata/pull/145). Thanks [@ZenBel](https://github.com/ZenBel)
* Add support for `mtdata echo <ID>`
* dataset entries only store bibtext keys and not full citation text
   * creates index cache as JSONLine file. (WIP towards dataset statistics)
* Simplified index loading 
* simplified  compression format handlers. Added support for opening .bz2 files without creating temp files.
* all resources are moved to `mtdata/resource` dir and any new additions to that dir are automatically included in python package (Fail proof for future issues like #137 ) 

**New and exciting features:**
* Support for adding new datasets at runtime (`mtdata*.py` from run dir). Note: you have to reindex by calling  `mtdata -ri list`
* Monolingual datasets support in progress (currently testing)
   * Dataset IDs are now `Group-name-version-lang1-lang2` for bitext and `Group-name-version-lang` for monolingual
   * `mtdata list` is updated.  `mtdata list -l eng-deu` for bitext and `mtdata list -l eng` for monolingual   
   * Added: Statmt Newscrawl, news-discussions, Leipzig corpus, ... 
   

> _skipped 0.3.9 because the chages are significant_ 

## v0.3.8 - 20221124

* CLI arg `--log-level` with default set to `WARNING`
* progressbar can be disabled from CLI `--no-pbar`; default is enabled `--pbar`
* `mtdata stats --quick` does HTTP HEAD and shows content length; e.g. `mtdata stats --quick Statmt-commoncrawl-wmt19-fra-deu`
* `python -m mtdata.scripts.recipe_stats` to read stats from output directory
* Security fix with tar extract | Thanks @TrellixVulnTeam
* Added NLLB datasets prepared by AllenAI | Thanks @AlexUmnov  
* Opus and ELRC datasets update | Thanks @ZenBel 


## v0.3.7 - 20220711
- Update ELRC data including EU acts which is used for wmt22 (thanks @kpu) 


## v0.3.6 - 20220708 
- fixes and additions for wmt22
- Fixed KECL-JParaCrawl
- added Paracrawl bonus for ukr-eng
- added Yandex rus-eng corpus
- added Yakut sah-eng
- update recipe for wmt22 constrained eval

## v0.3.5 - 20220310 

- Parallel download support `-j/--n-jobs` argument (with default `4`)
- Add histogram to web search interface (Thanks, @sgowdaks)
- Update OPUS index. Use OPUS API to download all datasets
  - A lot of new datasets are added. 
  - WARNING: Some OPUS IDs are not backward compatible (version number mismatch) 
- Fix: JESC dataset language IDs were wrong  
- New datasets:
   - jpn-eng: add paracrawl v3, and wmt19 TED
   - backtranslation datasets for en2ru ru2en en2ru
- Option to set `MTDATA_RECIPES` dir (default is $PWD). All files matching the glob `${MTDATA_RECIPES}/mtdata.recipes*.yml` are loaded
- WMT22 recipes added 
- JW300 is disabled [#77](https://github.com/thammegowda/mtdata/issues/77)
- Automatically create references.bib file based on datasets selected

## v0.3.4 - 20220206

- ELRC datasets updated
- Added docs, separate copy for each version (github pages)  
  - Dataset search via web interface. Support for regex match 
- Added two new datasets Masakane fon-fra
- Improved TMX files BCP47 lang ID matching: compatibility instead of exact match


## v0.3.3 - 20220127

- bug fix: xml reading inside tar: Element tree's compain about TarPath 
- `mtdata list` has `-g/--groups` and `-ng/--not-groups` as include exclude filters on group name (#91)
- `mtdata list` has `-id/--id` flag to print only dataset IDs (#91) 
- add WMT21 tests (#90)
- add ccaligned datasets wmt21 (#89)
- add ParIce datasets (#88)
- add wmt21 en-ha (#87)
- add wmt21 wikititles v3 (#86)
- Add train and test sets from StanfordNLP NMT page (large: en-cs, medium: en-de, small: en-vi) (#84) 
  - Add support for two URLs for a single dataset (i.e. without zip/tar files)
- Fix: buggy matching of languages `y1==y1`
- Fix: `get` command: ensure train/dev/test datasets are indeed compatible with languages specified in `--langs` args 
 
## v0.3.2 - 20211205

- Fix: recipes.yml is missing in the pip installed package
- Add Project Anuvaad: 196 datasets belonging to Indian languages
- add CLI `mtdata get` has `--fail / --no-fail` arguments to tell whether to crash or no-crash upon errors


## v0.3.1 - 20211028

- Add support for recipes; list-recipe get-recipe subcommands added
- add support for viewing stats of dataset; words, chars, segs
- FIX url for UN dev and test sets (source was updated so we updated too)
- Multilingual experiment support; ISO 639-3 code `mul` implies multilingual; e.g. mul-eng or eng-mul
- `--dev` accepts multiple datasets, and merges it (useful for multilingual experiments) 
- tar files are extracted before read (performance improvements)
- setup.py: version and descriptions accessed via regex 

---

## v0.3.0 - 20211021

> Big Changes: BCP-47, data compression 

- BCP47: (Language, Script, Region)
  - Our implementation is strictly not BCP-47. We differ on the following
    - We use ISO 639-3 codes (i.e three letters) for all languages, where as BCP47 uses two letters for some (e.g. `en`) and three letters for many.
    - We use `_` (underscore)  to join language, script, region whereas BCP-47 uses `-` (hyphen)
- Dataset IDs (aka `did` in short) are standardized `<group>-<name>-<version>-<lang1>-<lang2>`
  - `<group>` can have mixed case, `<name>` has to be lowercase
- CLI interface now accept `did`s. 

- `mtdata get --dev <did>` now accepts a single dataset ID; creates `dev.{xxx,yyy}` links at the root of out dir
- `mtdata get --test <did1> ... <did3>` creates `test{1..4}.{xxx,yyy}` links at the root of out dir  
- `--compress` option to store compressed datasets under output dir
- `zip` and `tar` files are no longer extracted. we read directly from compressed files without extracting them
- `._lock` files are removed after download job is done
- Add JESC, jpn paracrawl, news commentary 15 and 16
- Force unicode encoding; make it work on windows (Issue #71)
- JW300 -> JW300_v1 (tokenized); Added JW300_v1c (raw)  (Issue #70)
- Add all Wikititle datasets from lingual tool (Issue #63) 
- progressbar : `englighten` is used
- `wget` is replaced with `requests`. _User-Agent_ header along with mtdata version is sent in HTTP request headers
- Paracrawl v9 added

---
## v0.2.10 - 20210503 

- OPUS index updated (crawled on 20210522) 
  - new: 
    - CCAlignedV1
    - EiTBParCC_v1
    - EuroPat_v2
    - MultiCCAligned_v1.1
    - NewsCommentary_v14
    - WikiMatrix_v1
    - tico19_v20201028 
  - updates (replaces old with new):
    - GlobalVoices_v2017q3 -> GlobalVoices_v2018q4  
    - MultiParaCrawl_v5 -> MultiParaCrawl_v7.1 
    - ParaCrawl_v5 -> ParaCrawl_v7
    - TED2013_v1.1 -> TED2020_v1 
    - Tatoeba_v20190709 -> Tatoeba_v20210310  -- [#37][i37]
    - wikimedia_v20190628 -> wikimedia_v20210402 -- [#35][i35]
- Multilingual TMX parsing, add ECDC and EAC -- [#39][p39] -- by [@kpu](https://github.com/kpu)
- Removed Global Voices -- now available via OPUS -- [#41][i41]
- Move all BibTeX to a separate file -- [#42][p42]
- Add ELRC-Share datasets [#43][p43] --  by [@kpu](https://github.com/kpu)
- Fix line count mismatch in some XML formats [#45][p45] 
- Parse BCP47 codes by removing everything after first hyphen [#48][p48] -- by [@kpu](https://github.com/kpu) 
- Add Khresmoi datasets [#53][p53] -- by [@kpu](https://github.com/kpu)
- Optimize index loading by using cache; 
  - Added `-re | --reindex` CLI flag to force update index cache [#54][i54]  
  - Removed `--cache` CLI argument. Use `export MTDATA=/path/to/cache-dir` instead (which was already supported)
- Add : `DCEP` corpus, 253 language pairs [#58](p58) -- by [@kpu](https://github.com/kpu)
- Add : WMT 21 dev sets: eng-hau eng-isl isl-eng hau-eng [#36](i36)

[i37]: https://github.com/thammegowda/mtdata/issues/37
[i35]: https://github.com/thammegowda/mtdata/issues/35
[i36]: https://github.com/thammegowda/mtdata/issues/36
[i41]: https://github.com/thammegowda/mtdata/issues/41
[p39]: https://github.com/thammegowda/mtdata/pull/39  
[p42]:  https://github.com/thammegowda/mtdata/pull/42
[p45]: https://github.com/thammegowda/mtdata/pull/45
[p48]: https://github.com/thammegowda/mtdata/pull/48
[p53]: https://github.com/thammegowda/mtdata/pull/53 
[p43]: https://github.com/thammegowda/mtdata/pull/43 
[i54]: https://github.com/thammegowda/mtdata/issues/54
[p58]: https://github.com/thammegowda/mtdata/pull/58

----
## v0.2.9 - 20210517
- New datasets 
  - WMT20 Tests
  - Paracrawl_v5_1 for Pashto and Khmer -English
  - NunavutHansard_v3 for Inuktitut -English
  - paracrawl_v8 and paracrawl_bonus datasets ([#29][i29])
  - ELRC-Share contributed by [@kpu](https://github.com/kpu) ([#32][p32])
  - AI4Bharath Samanathar v0.2
- New features
  - 'mtdata -b' for short outputs and crash on error input
- Fixes and improvements:
  - ISO 639-1 -> ISO 639-3 mapping bug fix e.g. `nb` ([#24][i24])
  - Consistent docs for the default behavior of --merge ([#26][i26])
  - broken pipe error when `mtdata list | head` is now handled

[i29]: https://github.com/thammegowda/mtdata/issues/29
[i24]: https://github.com/thammegowda/mtdata/issues/24
[i26]: https://github.com/thammegowda/mtdata/issues/26 
[p32]: https://github.com/thammegowda/mtdata/pull/32

----
## v0.2.8 - 20210126
- Paracrawl v7 and v7.1  -- 29 new datasets
- Fix swapping issue with TMX format (TILDE corpus); add a testcase for TMX entry 
- Add mtdata-iso shell command
- Add "mtdata report" sub command to summarize datasets by language and names

----
## v0.2.7 - 20200912
- Add OPUS 100 corpus

----
## v0.2.6 - 20200827
- Add all pairs of neulab_tedtalksv1 - train,test,dev  -- 4,455 of them
- Add support for cleaning noise. Entry.is_noise(seg1, seg2)
- some basic noise is removed by default from training 
- add `__slots__` to Entry class (takes less memory and faster attrib lookup)

----
## v0.2.5 - 20200610
- Add all pairs of Wikimatrix  -- 1,617 of them
- Add support for specifying `cols` of `.tsv` file
- Add all Europarlv7 sets
- Remove hin-eng `dict` from JoshuaIndianParallelCorpus
- Remove Wikimatrix1 from statmt -- they are moved to separate file 

----
## v0.2.4 - 20200605
- File locking using portalocker to deal with race conditions 
 when multiple `mtdata get` are invoked in parallel
- Remove language name from local file name 
  -- as a same tar file can be used by many languages, and they dont need copy
- CLI to print version name
- Added KFTT Japanese-English set

----
## 0.2.3 - (Not released to PyPi)
- IITB hin-eng datasets
- Fix issue with dataset counting

----
## 0.2.2 - 

- Pypi release bug fix: select all nested packages
- add UnitedNations test set

----
## 0.2.1 -  
-  Add JW300 Corpus 

----
## 0.2.0 - 
- All Languages are internally mapped to 3 letter codes of ISO codes
- 53,000 entries from OPUS are indexed



