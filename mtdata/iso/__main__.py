#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/8/20
import logging as log

log.basicConfig(level=log.INFO)


def main(langs=None):
    from mtdata.iso import iso3_code
    from mtdata.iso.iso639_3 import code_to_name, data as ISO639_3
    langs = langs or parse_args().get('langs', [])
    if not langs:
        print(ISO639_3)
    else:
        print(f"Input\tISO639_3\tName")
        for lang in langs:
            iso_code = iso3_code(lang)
            iso_name = code_to_name(iso_code) if iso_code else '-none-'
            iso_code = iso_code or '-none-'
            print(f"{lang}\t{iso_code}\t{iso_name}")


def parse_args():
    import argparse
    p = argparse.ArgumentParser(prog='python -m mtdata.iso', description="ISO 639-3 lookup tool")
    p.add_argument("langs", nargs='*', help="Language code or name that needs to be looked up. "
                                            "When no language code is given, all languages are listed.")
    return vars(p.parse_args())


if __name__ == '__main__':
    main()
