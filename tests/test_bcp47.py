#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 10/4/21
from mtdata.iso.bcp47 import bcp47, BCP47Tag
from pytest import fail


def test_bcp47():
    assert bcp47("en-GB") == ('eng', None, 'GB', 'eng-GB')
    assert bcp47("en") == ('eng', None, None, 'eng')
    assert bcp47("en-IN") == ('eng', None, 'IN', 'eng-IN')
    assert bcp47("en-US") == ('eng', None, 'US', 'eng-US')
    # Latn script is default, so None
    assert bcp47("en-Latn") == ('eng', None, None, 'eng')
    # hypothetical;
    assert bcp47("en-Knda") == ('eng', 'Knda', None, 'eng-Knda')
    assert bcp47("en-Latn-GB") == ('eng', None, 'GB', 'eng-GB')

    try:
        bcp47("en-Latn-UK")
        fail("UK is not ISO country code")
    except ValueError:
        pass  # expected

    assert bcp47("kn") == ('kan', None, None, 'kan')
    assert bcp47("kn-Knda") == ('kan', None, None, 'kan')    # default script
    assert bcp47("kn-Knda-IN") == ('kan', None, 'IN', 'kan-IN')
    assert bcp47("kn_Knda_IN") == ('kan', None, 'IN', 'kan-IN')
    assert bcp47("kn_Knda_in") == ('kan', None, 'IN', 'kan-IN')
    assert bcp47("kn_Latn_IN") == ('kan', 'Latn', 'IN', 'kan-Latn-IN')
    assert bcp47("kn_Deva_IN") == ('kan', 'Deva', 'IN', 'kan-Deva-IN')
    assert bcp47("hi_Deva_IN") == ('hin', None, 'IN', 'hin-IN')    # default script

    assert bcp47("pt_PT") == ('por', None, 'PT', 'por-PT')
    assert bcp47("pt_pt") == ('por', None, 'PT', 'por-PT')
    assert bcp47("pt_BR") == ('por', None, 'BR', 'por-BR')
    assert bcp47("pt_br") == ('por', None, 'BR', 'por-BR')
    assert bcp47("pt_Latn_br") == ('por', None, 'BR', 'por-BR')  # default script
    assert bcp47("pt_Cyrl_br") == ('por', 'Cyrl', 'BR', 'por-Cyrl-BR')  # non default script
    assert bcp47("fr") == ('fra', None, None, 'fra')
    assert bcp47("fr-CA") == ('fra', None, 'CA', 'fra-CA')


def test_py_obj_model():
    """Test cases for python object model"""
    assert bcp47("en-GB") is not bcp47("en-GB")  # object comparison: two objects are two different references
    assert bcp47("en-GB") == bcp47("en-GB")      # but they have same value and hence equal
    assert bcp47("en-GB") == bcp47("en-Latn-GB")  # ignore the default script
    assert bcp47("en-Latn-US") == bcp47("en-US")  # ignore default script again
    assert bcp47("en-Latn") == bcp47("en")  # ignore default script again
    assert bcp47("en-Latn") == bcp47("english")  # ignore default script again
    assert bcp47("en-Latn") == bcp47("English")  # ignore default script again
    assert bcp47("en-Latn") == bcp47("ENG")  # ignore default script again
    assert bcp47("en-US") != bcp47("en")      # dont ignore region
