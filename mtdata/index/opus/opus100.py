#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 9/12/20
from mtdata.index import Index, Entry
supervised_v1 = (
    "af-en,am-en,an-en,ar-en,as-en,az-en,be-en,bg-en,bn-en,br-en,bs-en,ca-en,cs-en,cy-en,da-en,"
    "de-en,dz-en,el-en,en-eo,en-es,en-et,en-eu,en-fa,en-fi,en-fr,en-fy,en-ga,en-gd,en-gl,en-gu,"
    "en-ha,en-he,en-hi,en-hr,en-hu,en-hy,en-id,en-ig,en-is,en-it,en-ja,en-ka,en-kk,en-km,en-kn,"
    "en-ko,en-ku,en-ky,en-li,en-lt,en-lv,en-mg,en-mk,en-ml,en-mn,en-mr,en-ms,en-mt,en-my,en-nb,"
    "en-ne,en-nl,en-nn,en-no,en-oc,en-or,en-pa,en-pl,en-ps,en-pt,en-ro,en-ru,en-rw,en-se,en-sh,"
    "en-si,en-sk,en-sl,en-sq,en-sr,en-sv,en-ta,en-te,en-tg,en-th,en-tk,en-tr,en-tt,en-ug,en-uk,"
    "en-ur,en-uz,en-vi,en-wa,en-xh,en-yi,en-yo,en-zh,en-zu").split(",")
zeroshot_v1 = (
    "ar-de,ar-fr,ar-nl,ar-ru,ar-zh,de-fr,de-nl,de-ru,de-zh,fr-nl,fr-ru,fr-zh,nl-ru,nl-zh,ru-zh"
).split(",")


def load_all(index: Index):
    URL = "https://object.pouta.csc.fi/OPUS-100/v1.0/opus-100-corpus-v1.0.tar.gz"
    cite="""
@inproceedings{zhang-etal-2020-improving,
    title = "Improving Massively Multilingual Neural Machine Translation and Zero-Shot Translation",
    author = "Zhang, Biao  and
      Williams, Philip  and
      Titov, Ivan  and
      Sennrich, Rico",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.148",
    doi = "10.18653/v1/2020.acl-main.148",
    pages = "1628--1639",
}
@inproceedings{tiedemann2012parallel,
  title={Parallel Data, Tools and Interfaces in OPUS.},
  author={Tiedemann, J{\"o}rg},
  booktitle={Lrec},
  volume={2012},
  pages={2214--2218},
  year={2012}
}"""
    filename = 'opus-100-corpus-v1.0.tar.gz'
    code_map = dict(nb='nob', sh='hbs')  # these arent obvious to iso lookup function, so helping
    for pair in supervised_v1:
        l1, l2 = pair.split("-")
        l1 = code_map.get(l1, l1)
        l2 = code_map.get(l2, l2)
        splits = ['train', 'dev', 'test']
        if pair in {'an-en', 'en-yo', 'dz-en', 'en-hy', 'en-mn'}:
            splits = ['train']  # somehow they forgot to include test sets for these
        for split in splits:
            f1 = f'opus-100-corpus/v1.0/supervised/{l1}-{l2}/opus.{l1}-{l2}-{split}.{l1}'
            f2 = f'opus-100-corpus/v1.0/supervised/{l1}-{l2}/opus.{l1}-{l2}-{split}.{l2}'
            ent = Entry(langs=(l1, l2), url=URL, name=f'OPUS100v1_{split}',
                        filename=filename, in_paths=[f1, f2], in_ext='txt', cite=cite)
            index.add_entry(ent)
    for pair in zeroshot_v1:
        l1, l2 = pair.split("-")
        f1 = f'opus-100-corpus/v1.0/zero-shot/{l1}-{l2}/opus.{l1}-{l2}-test.{l1}'
        f2 = f'opus-100-corpus/v1.0/zero-shot/{l1}-{l2}/opus.{l1}-{l2}-test.{l2}'
        ent = Entry(langs=(l1, l2), url=URL, name=f'OPUS100v1_test', filename=filename,
                    in_paths=[f1, f2], in_ext='txt', cite=cite)
        index.add_entry(ent)