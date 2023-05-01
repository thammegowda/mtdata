#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 10/4/21
from mtdata.iso.bcp47 import bcp47, BCP47Tag, bcp47e
from pytest import fail


def test_bcp47():
    assert bcp47("en-GB")[:3] == ('eng', None, 'GB')
    assert bcp47("en-GB") == ('eng', None, 'GB', 'eng_GB')
    assert bcp47("en") == ('eng', None, None, 'eng')
    assert bcp47("en-IN") == ('eng', None, 'IN', 'eng_IN')
    assert bcp47("en-US") == ('eng', None, 'US', 'eng_US')
    # Latn script is default, so None
    assert bcp47("en-Latn") == ('eng', None, None, 'eng')
    # hypothetical;
    assert bcp47("en-Knda") == ('eng', 'Knda', None, 'eng_Knda')
    assert bcp47("en-Latn-GB") == ('eng', None, 'GB', 'eng_GB')

    try:
        bcp47("en-Latn-UK")
        fail("UK is not ISO country code")
    except ValueError:
        pass  # expected

    assert bcp47("kn") == ('kan', None, None, 'kan')
    assert bcp47("kn-Knda") == ('kan', None, None, 'kan')    # default script
    assert bcp47("kn-Knda-IN") == ('kan', None, 'IN', 'kan_IN')
    assert bcp47("kn_Knda_IN") == ('kan', None, 'IN', 'kan_IN')
    assert bcp47("kn_Knda_in") == ('kan', None, 'IN', 'kan_IN')
    assert bcp47("kn_Latn_IN") == ('kan', 'Latn', 'IN', 'kan_Latn_IN')
    assert bcp47("kn_Deva_IN") == ('kan', 'Deva', 'IN', 'kan_Deva_IN')
    assert bcp47("hi_Deva_IN") == ('hin', None, 'IN', 'hin_IN')    # default script

    assert bcp47("pt_PT") == ('por', None, 'PT', 'por_PT')
    assert bcp47("pt_pt") == ('por', None, 'PT', 'por_PT')
    assert bcp47("pt_BR") == ('por', None, 'BR', 'por_BR')
    assert bcp47("pt_br") == ('por', None, 'BR', 'por_BR')
    assert bcp47("pt_Latn_br") == ('por', None, 'BR', 'por_BR')  # default script
    assert bcp47("pt_Cyrl_br") == ('por', 'Cyrl', 'BR', 'por_Cyrl_BR')  # non default script
    assert bcp47("fr") == ('fra', None, None, 'fra')
    assert bcp47("fr-CA") == ('fra', None, 'CA', 'fra_CA')


def test_py_obj_model():
    """Test cases for python object model"""
    assert bcp47("en-GB") is not bcp47("en_GB")  # object comparison: two objects are two different references
    assert bcp47("en-GB") == bcp47("en_GB")      # but they have same value and hence equal
    assert bcp47("en-GB") == bcp47("en_Latn_GB")  # ignore the default script
    assert bcp47("en-Latn-US") == bcp47("en_US")  # ignore default script again
    assert bcp47("en-Latn") == bcp47("en")  # ignore default script again
    assert bcp47("en-Latn") == bcp47("english")  # ignore default script again
    assert bcp47("en-Latn") == bcp47("English")  # ignore default script again
    assert bcp47("en-Latn") == bcp47("ENG")  # ignore default script again
    assert bcp47("en-US") != bcp47("en")      # dont ignore region

    # Custom class, e.g. BCP47Tag, instead of plain old str obj could create bugs due to improper hashing;
    # so test it out
    mem = set()
    assert bcp47('en') not in mem
    mem.add(bcp47('en'))
    assert bcp47('en') in mem
    mem.add(bcp47('en'))
    assert len(mem) == 1  # dupes are removed
    mem.add(bcp47('en-Latn'))
    mem.add(bcp47('english'))
    mem.add(bcp47('English'))
    mem.add(bcp47('eng'))
    assert len(mem) == 1       # dupes are removed

    mem = dict()
    mem[bcp47('en')] = 10
    assert mem[bcp47('en')] == 10
    assert mem[bcp47('en')] != 11
    assert mem[bcp47('eng')] == 10
    assert mem[bcp47('english')] == 10
    assert mem[bcp47('English-Latn')] == 10

def test_bcp47_express():

    # express script
    assert bcp47e("en-GB")[:3] == ('eng', 'Latn', 'GB')
    assert bcp47e("en-GB") == ('eng', 'Latn', 'GB', 'eng_Latn_GB')
    assert bcp47e("en") == ('eng', 'Latn', None, 'eng_Latn')
    assert bcp47e("en-IN") == ('eng', 'Latn', 'IN', 'eng_Latn_IN')
    assert bcp47e("en-US") == ('eng', 'Latn', 'US', 'eng_Latn_US')
    assert bcp47e("en-Latn") == ('eng', 'Latn', None, 'eng_Latn')
    
    # hypothetical;
    assert bcp47e("en-Knda") == ('eng', 'Knda', None, 'eng_Knda')
    assert bcp47e("en-Latn-GB") == ('eng', 'Latn', 'GB', 'eng_Latn_GB')

    try:
        bcp47e("en-Latn-UK")
        fail("UK is not ISO country code")
    except ValueError:
        pass  # expected

    assert bcp47e("kn") == ('kan', 'Knda', None, 'kan_Knda')              # missing, express
    assert bcp47e("kn-Knda") == ('kan', 'Knda', None, 'kan_Knda')         # default script, keep
    assert bcp47e("kn_Deva_IN") == ('kan', 'Deva', 'IN', 'kan_Deva_IN')  # Non default, keep
    
