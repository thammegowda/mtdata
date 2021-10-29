#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 10/27/21

from pathlib import Path
from tempfile import TemporaryDirectory
from mtdata.main import get_recipe


def test_recipe_multilingual():
    recipe_id = 'tg01_2to1_test'
    with TemporaryDirectory() as out_dir:
        out_dir = Path(out_dir)
        get_recipe(recipe_id=recipe_id, out_dir=out_dir, drop_dupes=True, drop_tests=True)
        assert (out_dir / 'mtdata.signature.txt').stat().st_size > 0
        assert (out_dir / 'train.eng').stat().st_size > 0
        assert (out_dir / 'train.mul').stat().st_size > 0
        assert (out_dir / 'dev.eng').stat().st_size > 0
        assert (out_dir / 'dev.mul').stat().st_size > 0

