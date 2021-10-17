#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 1/26/21

from mtdata.main import get_data, lang_pair, DatasetId
from pathlib import Path
from tempfile import TemporaryDirectory


dataset_id = DatasetId.parse


def test_rapid1019():
    # out_dir = Path('tmp-test-tmx1')
    with TemporaryDirectory() as out_dir:
        out_dir = Path(out_dir)
        langs = lang_pair('eng-ces')
        did = dataset_id('Tilde-rapid-2019-ces-eng')
        args = dict(langs=langs, out_dir=out_dir, train_dids=[did])
        get_data(**args)
        parts_dir = out_dir / 'train-parts'
        eng = parts_dir / f'{did}.eng'
        ces = parts_dir / f'{did}.ces'
        eng = eng.read_text().splitlines()
        ces = ces.read_text().splitlines()
        assert len(eng) == len(ces) == 263_287
        assert eng[0].strip() == '(^) Products that are put to sale before 20 May 2016 can still be sold in the EU until 2017.'
        assert ces[0].strip() =='(^) Výrobky, které byly určeny k prodeji před 20. květnem 2016, mohou být v EU stále prodávány do roku 2017.'


def test_eac_ref():
    with TemporaryDirectory() as out_dir:
        out_dir = Path(out_dir)
        langs = lang_pair('nor-slk')
        did = dataset_id('EU-eac_reference-1-nor-slk')

        args = dict(langs=langs, out_dir=out_dir, train_dids=[did])
        get_data(**args)
        parts_dir = out_dir / 'train-parts'
        nor = parts_dir / f'{did}.nor'
        slk = parts_dir / f'{did}.slk'
        nor = nor.read_text().splitlines()
        slk = slk.read_text().splitlines()
        print('nor, slk == ', len(nor), len(slk))
        assert len(nor) == len(slk)
