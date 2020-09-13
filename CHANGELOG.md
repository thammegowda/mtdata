# Change Log

# v0.2.7 20200912
- Add OPUS 100 corpus

# v0.2.6 - 20200827
- Add all pairs of neulab_tedtalksv1 - train,test,dev  -- 4,455 of them
- Add support for cleaning noise. Entry.is_noise(seg1, seg2)
- some basic noise is removed by default from training 
- add `__slots__` to Entry class (takes less memory and faster attrib lookup)


# v0.2.5 - 20200610
- Add all pairs of Wikimatrix  -- 1,617 of them
- Add support for specifying `cols` of `.tsv` file
- Add all Europarlv7 sets
- Remove hin-eng `dict` from JoshuaIndianParallelCorpus
- Remove Wikimatrix1 from statmt -- they are moved to separate file 

# v0.2.4 - 20200605
- File locking using portalocker to deal with race conditions 
 when multiple `mtdata get` are invoked in parallel
- Remove language name from local file name 
  -- as a same tar file can be used by many languages, and they dont need copy
- CLI to print version name
- Added KFTT Japanese-English set

# 0.2.3 - (Not released to PyPi)
- IITB hin-eng datasets
- Fix issue with dataset counting

# 0.2.2 - 

- Pypi release bug fix: select all nested packages
- add UnitedNations test set

# 0.2.1 -  
-  Add JW300 Corpus 

# 0.2.0 - 
- All Languages are internally mapped to 3 letter codes of ISO codes
- 53,000 entries from OPUS are indexed



