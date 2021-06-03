#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 1/26/21

import mtdata
from mtdata.main import get_data
from argparse import Namespace
from pathlib import Path
from tempfile import TemporaryDirectory


def test_rapid1019():
    #out_dir = Path('tmp-test-tmx1')
    with TemporaryDirectory() as out_dir:
        out_dir = Path(out_dir)
        args = Namespace(cache=mtdata.cache_dir, langs=('eng', 'ces'), merge=False,
                         out=out_dir, task='get', test_names=None, train_names=['rapid2019'])
        get_data(args)
        parts_dir = out_dir / 'train-parts'
        eng = parts_dir / 'rapid2019-eng_ces.eng'
        ces = parts_dir / 'rapid2019-eng_ces.ces'
        eng = eng.read_text().splitlines()
        ces = ces.read_text().splitlines()
        assert len(eng) == len(ces) == 263_287
        assert eng[0].strip() == '(^) Products that are put to sale before 20 May 2016 can still be sold in the EU until 2017.'
        assert ces[0].strip() =='(^) Výrobky, které byly určeny k prodeji před 20. květnem 2016, mohou být v EU stále prodávány do roku 2017.'


def test_eac_ref():
    with TemporaryDirectory() as out_dir:
        out_dir = Path(out_dir)
        args = Namespace(cache=mtdata.cache_dir, langs=('nor', 'slk'), merge=False,
                         out=out_dir, task='get', test_names=None, train_names=['EAC_Reference'])
        get_data(args)
        parts_dir = out_dir / 'train-parts'
        nor = parts_dir / 'EAC_Reference-nor_slk.nor'
        slk = parts_dir / 'EAC_Reference-nor_slk.slk'
        nor = nor.read_text().splitlines()
        slk = slk.read_text().splitlines()
        print('nor, slk == ', len(nor), len(slk))
        assert len(nor) == len(slk)
