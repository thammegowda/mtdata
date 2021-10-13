#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 9/12/20
from mtdata.index import Index, Entry, DatasetId
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
    cite = index.ref_db.get_bibtex('zhang-etal-2020-improving')
    cite += '\n\n' + index.ref_db.get_bibtex('tiedemann2012parallel')
    filename = 'opus-100-corpus-v1.0.tar.gz'
    code_map = dict(nb='nob', sh='hbs')  # these arent obvious to iso lookup function, so helping
    group, name = 'OPUS', 'opus100'
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
            ent = Entry(did=DatasetId(group=group, name=f'{name}_{split}', version='1', langs=(l1, l2)),
                    url=URL, filename=filename, in_paths=[f1, f2], in_ext='txt', cite=cite)
            index.add_entry(ent)
    for pair in zeroshot_v1:
        l1, l2 = pair.split("-")
        f1 = f'opus-100-corpus/v1.0/zero-shot/{l1}-{l2}/opus.{l1}-{l2}-test.{l1}'
        f2 = f'opus-100-corpus/v1.0/zero-shot/{l1}-{l2}/opus.{l1}-{l2}-test.{l2}'
        ent = Entry(did=DatasetId(group=group, name=f'{name}_test', version='1', langs=(l1, l2)),
                    url=URL, filename=filename, in_paths=[f1, f2], in_ext='txt', cite=cite)
        index.add_entry(ent)
