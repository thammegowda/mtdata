#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 10/4/21
from mtdata.iso.bcp47 import bcp47
from pytest import fail


def test_bcp47():
    assert bcp47("en-GB") == ('eng', None, 'GB')
    assert bcp47("en") == ('eng', None, None)
    assert bcp47("en-IN") == ('eng', None, 'IN')
    assert bcp47("en-US") == ('eng', None, 'US')
    # Latn script is default, so None
    assert bcp47("en-Latn") == ('eng', None, None)
    # hypothetical;
    assert bcp47("en-Knda") == ('eng', 'Knda', None)
    assert bcp47("en-Latn-GB") == ('eng', None, 'GB')

    try:
        bcp47("en-Latn-UK")
        fail("UK is not ISO country code")
    except ValueError:
        pass  # expected

    assert bcp47("kn") == ('kan', None, None)
    assert bcp47("kn-Knda") == ('kan', None, None)    # default script
    assert bcp47("kn-Knda-IN") == ('kan', None, 'IN')
    assert bcp47("kn_Knda_IN") == ('kan', None, 'IN')
    assert bcp47("kn_Knda_in") == ('kan', None, 'IN')
    assert bcp47("kn_Latn_IN") == ('kan', 'Latn', 'IN')
    assert bcp47("kn_Deva_IN") == ('kan', 'Deva', 'IN')
    assert bcp47("hi_Deva_IN") == ('hin', None, 'IN')    # default script

    assert bcp47("pt_PT") == ('por', None, 'PT')
    assert bcp47("pt_pt") == ('por', None, 'PT')
    assert bcp47("pt_BR") == ('por', None, 'BR')
    assert bcp47("pt_br") == ('por', None, 'BR')
    assert bcp47("fr") == ('fra', None, None)
    assert bcp47("fr-CA") == ('fra', None, 'CA')
