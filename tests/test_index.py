#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 10/12/21

from mtdata.index import is_compatible, bcp47


def test_is_compatible():
    assert is_compatible(bcp47('en'), bcp47('en'))
    assert is_compatible(bcp47('en'), bcp47('en_US'))
    assert is_compatible(bcp47('en_US'), bcp47('en'))
    assert not is_compatible(bcp47('en_US'), bcp47('en_GB'))
    assert not is_compatible(bcp47('en_US'), bcp47('en_IN'))
    assert is_compatible(bcp47('en_US'), bcp47('en_Latn'))
    assert is_compatible(bcp47('en_US'), bcp47('en_Latn_US'))

    assert is_compatible(bcp47('por_BR'), bcp47('por'))
    assert is_compatible(bcp47('por_PT'), bcp47('por'))
    assert not is_compatible(bcp47('por_PT'), bcp47('por_BR'))

    assert is_compatible(bcp47('kan'), bcp47('kan_IN'))
    assert is_compatible(bcp47('kan'), bcp47('kan_Knda'))
    assert is_compatible(bcp47('kan'), bcp47('kan_Knda_IN'))
    assert not is_compatible(bcp47('kan'), bcp47('kan_Deva_IN'))
    assert not is_compatible(bcp47('hin_Deva_In'), bcp47('kan_Deva_IN'))
    assert not is_compatible(bcp47('hin_In'), bcp47('kan_Deva_IN'))
    assert not is_compatible(bcp47('hin'), bcp47('kan_Deva_IN'))
