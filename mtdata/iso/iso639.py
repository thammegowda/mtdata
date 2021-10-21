#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 10/12/21
from mtdata.iso.iso639_3 import CODES as iso3_codes, name_to_code
from mtdata.iso.iso639_2 import CODE2_TO_3, code2_to_code3_name
from mtdata.iso.iso639_1 import ISO693_1_to_3 as code1_to_3
from mtdata.iso.custom import CUSTOM_TO_3 as custom_to_3


def iso3_code(lang: str, fail_error=False, default=None) -> str:
    """
    Lookup 693_3 code of a language
    :param lang: language name or a code, maybe of 2 or 3 letters
    :param default: return this value when no iso code is found
    :param fail_error: raise error when no ISO code is found
    :return: ISO 639_3 code
    """
    lang = lang.lower()
    part1 = lang.split('-')[0]     # BCP47
    lookups = (lang, part1) if lang != part1 else (lang,)
    for lang in lookups:
        if lang in iso3_codes:
            return lang
        if lang in CODE2_TO_3:
            _, name = code2_to_code3_name(lang)
            iso3_code = name_to_code(name)
            if iso3_code:
                return iso3_code
        if lang in code1_to_3:
            return code1_to_3[lang]
        if name_to_code(lang, None):
            return name_to_code(lang)
        if lang in custom_to_3:  # at last
            return custom_to_3[lang]

    if fail_error:
        raise Exception(f"Unable to find ISO 639-3 code for '{lang}'. "
                        f"Please run\npython -m mtdata.iso | grep -i <name>\n"
                        f"to know the 3 letter ISO code for the language.")
    return default
