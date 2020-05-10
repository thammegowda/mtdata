#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/8/20



def iso3_code(lang: str, fail_error=False, default=None) -> str:
    """
    Lookup 693_3 code of a language
    :param code: language name or a code, maybe of 2 or 3 letters
    :param default: return this value when no iso code is found
    :param fail_error: raise error when no ISO code is found
    :return: ISO 639_3 code
    """
    from mtdata.iso.iso639_3 import CODES as iso3_codes, name_to_code
    from mtdata.iso.iso639_2 import CODE2_TO_3, code2_to_code3_name

    if lang.lower() in iso3_codes:
        return lang.lower()
    if lang.lower() in CODE2_TO_3:
        _, name = code2_to_code3_name(lang.lower())
        iso3_code = name_to_code(name)
        if iso3_code:
            return iso3_code
    if name_to_code(lang, None):
        return name_to_code(lang)
    if fail_error:
        raise Exception(f"Unable to find ISO 639-3 code for '{lang}'. "
                        f"Please run\npython -m mtdata.iso | grep -i <name>\n"
                        f"to know the 3 letter ISO code for the language.")
    return default