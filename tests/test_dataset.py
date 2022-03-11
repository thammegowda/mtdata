#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 12/6/21

from pathlib import Path
from tempfile import TemporaryDirectory
from mtdata.main import get_data, DatasetId, lang_pair


def check_parallel(path1:Path, path2: Path):
    assert path1.stat().st_size > 0
    assert path2.stat().st_size > 0
    l1 = len(path1.read_text().splitlines())
    l2 = len(path2.read_text().splitlines())
    assert l1 == l2, f'Expected same number of lines: {l1} == {l2} ?\n{path1} == {path2}'


def test_2url_dataset():
    with TemporaryDirectory() as out_dir:
        out_dir = Path(out_dir)
        train_dids = [DatasetId.parse('StanfordNLP-iwslt15_train-1-eng-vie')]
        dev_dids = [DatasetId.parse('StanfordNLP-test2012-1-eng-vie')]
        test_dids = [DatasetId.parse('StanfordNLP-test2013-1-eng-vie')]
        langs = lang_pair("eng-vie")
        get_data(langs=langs, out_dir=out_dir, drop_dupes=True, drop_tests=True,
                 train_dids=train_dids, dev_dids=dev_dids, test_dids=test_dids, merge_train=True)
        assert (out_dir / 'mtdata.signature.txt').stat().st_size > 0
        check_parallel(out_dir / 'train.eng', out_dir / 'train.vie')
        check_parallel(out_dir / 'dev.eng', out_dir / 'dev.vie')
        check_parallel(out_dir / 'test1.eng', out_dir / 'test1.vie')


def test_simple_dataset():
    with TemporaryDirectory() as out_dir:
        out_dir = Path(out_dir)
        # some random test sets
        train_dids = [DatasetId.parse('Anuvaad-drivespark-20210303-eng-kan'),
                      DatasetId.parse('Anuvaad-nativeplanet-20210315-eng-kan'),
                      DatasetId.parse('OPUS-ccaligned-v1-eng-kan')]
        dev_dids = [DatasetId.parse('Anuvaad-oneindia-20210320-eng-kan')]
        test_dids = [DatasetId.parse('Anuvaad-mk-20210320-eng-kan')]
        langs = lang_pair("eng-kan")
        get_data(langs=langs, out_dir=out_dir, drop_dupes=True, drop_tests=True,
                 train_dids=train_dids, dev_dids=dev_dids, test_dids=test_dids, merge_train=True)
        assert (out_dir / 'mtdata.signature.txt').stat().st_size > 0
        check_parallel(out_dir / 'train.eng', out_dir / 'train.kan')
        check_parallel(out_dir / 'dev.eng', out_dir / 'dev.kan')
        check_parallel(out_dir / 'test1.eng', out_dir / 'test1.kan')
