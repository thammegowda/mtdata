#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/8/20
import pytest

from mtdata.iso import iso3_code

def test_iso3_code():
    assert iso3_code("kn") == 'kan'
    assert iso3_code("KN") == 'kan'
    assert iso3_code("Kannada") == 'kan'
    assert iso3_code("kannada") == 'kan'
    assert iso3_code("kan") == 'kan'
    assert iso3_code("KANNADA") == 'kan'
    assert iso3_code("KaNnAdA") == 'kan'
    assert iso3_code("KAN") == 'kan'

    assert iso3_code("ne") == 'nep'
    assert iso3_code("nep") == 'nep'
    assert iso3_code("Nepali") == 'nep'
    assert iso3_code("Nepali (individual)") == 'npi'

    assert iso3_code("xyz") == None
    assert iso3_code("xyz", default="Error") == "Error"
    try:
        iso3_code("xyz", fail_error=True)
        assert False, 'Expected an exception'
    except:
        assert True

