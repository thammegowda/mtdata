# Change Log

v0.2.10-dev - WIP 

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
    - GlobalVoices_v2017q3 ->GlobalVoices_v2018q4  
    - MultiParaCrawl_v5 -> MultiParaCrawl_v7.1 
    - ParaCrawl_v5 -> ParaCrawl_v7
    - TED2013_v1.1 -> TED2020_v1 
    - Tatoeba_v20190709 -> Tatoeba_v20210310  -- [#37][i37]
    - wikimedia_v20190628 -> wikimedia_v20210402 -- [#35][i35]
- Removed Global Voices -- now available via OPUS -- [#41][i41]
- Multilingual TMX parsing, add ECDC and EAC -- [#39][p39] -- contributed by [@kpu](https://github.com/kpu) 
- Move all BibTeX to a separate file -- [#42][p42]
- Fix line count mismatch in some XML formats [#45][p45]


[i37]: https://github.com/thammegowda/mtdata/issues/37
[i35]: https://github.com/thammegowda/mtdata/issues/35
[i41]: https://github.com/thammegowda/mtdata/issues/41
[p39]: https://github.com/thammegowda/mtdata/pull/39  
[p42]:  https://github.com/thammegowda/mtdata/pull/42
[p45]: https://github.com/thammegowda/mtdata/pull/45

----
# v0.2.9 - 20210517
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
# v0.2.8 - 20210126
- Paracrawl v7 and v7.1  -- 29 new datasets
- Fix swapping issue with TMX format (TILDE corpus); add a testcase for TMX entry 
- Add mtdata-iso shell command
- Add "mtdata report" sub command to summarize datasets by language and names

----
# v0.2.7 - 20200912
- Add OPUS 100 corpus

----
# v0.2.6 - 20200827
- Add all pairs of neulab_tedtalksv1 - train,test,dev  -- 4,455 of them
- Add support for cleaning noise. Entry.is_noise(seg1, seg2)
- some basic noise is removed by default from training 
- add `__slots__` to Entry class (takes less memory and faster attrib lookup)

----
# v0.2.5 - 20200610
- Add all pairs of Wikimatrix  -- 1,617 of them
- Add support for specifying `cols` of `.tsv` file
- Add all Europarlv7 sets
- Remove hin-eng `dict` from JoshuaIndianParallelCorpus
- Remove Wikimatrix1 from statmt -- they are moved to separate file 

----
# v0.2.4 - 20200605
- File locking using portalocker to deal with race conditions 
 when multiple `mtdata get` are invoked in parallel
- Remove language name from local file name 
  -- as a same tar file can be used by many languages, and they dont need copy
- CLI to print version name
- Added KFTT Japanese-English set

----
# 0.2.3 - (Not released to PyPi)
- IITB hin-eng datasets
- Fix issue with dataset counting

----
# 0.2.2 - 

- Pypi release bug fix: select all nested packages
- add UnitedNations test set

----
# 0.2.1 -  
-  Add JW300 Corpus 

----
# 0.2.0 - 
- All Languages are internally mapped to 3 letter codes of ISO codes
- 53,000 entries from OPUS are indexed



