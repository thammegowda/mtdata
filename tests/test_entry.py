#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 10/13/21

from mtdata.entry import Entry, DatasetId


def test_dataset_id():

    obj1 = DatasetId(group='uscisi', name='dataset1', version='1', langs=('en', 'kn'))
    obj2 = DatasetId(group='uscisi', name='dataset1', version='1', langs=('en', 'kn'))
    obj3 = DatasetId(group='uscisi', name='dataset1', version='2', langs=('en', 'kn'))
    obj4 = DatasetId(group='uscisi', name='dataset1', version='1', langs=('en', 'fr'))
    obj5 = DatasetId(group='opus', name='dataset1', version='1', langs=('en', 'kn'))

    assert obj2 == obj1
    assert obj3 != obj1
    assert obj4 != obj1
    assert obj5 != obj1

    mem = set()
    assert obj1 not in mem   # obj1 should be hashable to work
    mem.add(obj1)
    assert obj1 in mem      # obj1 should be hashable to work
    assert obj2 in mem      # this should work! obj2 is a dupe of obj1
    assert obj3 not in mem

    mem = dict()
    mem[obj1] = 10
    assert obj1 in mem
    assert obj2 in mem
    assert mem[obj2] == 10
    assert obj3 not in mem
