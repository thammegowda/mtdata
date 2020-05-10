#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/8/20
import logging as log


log.basicConfig(level=log.INFO)

def main(langs=None):
    from mtdata.iso import iso3_code
    from mtdata.iso.iso639_3 import code_to_name
    langs = langs or parse_args()
    print(f"Input\tISO639_3\tName")
    for lang in langs:
        iso_code = iso3_code(lang)
        iso_name = code_to_name(iso_code) if iso_code else '-none-'
        iso_code = iso_code or '-none-'
        print(f"{lang}\t{iso_code}\t{iso_name}")

def parse_args():
    import argparse
    p = argparse.ArgumentParser(description="ISO 639-3 lookup tool")
    p.add_argument("lang", nargs='+', help="Language code or name")
    return vars(p.parse_args())['lang']

if __name__ == '__main__':
    main()
