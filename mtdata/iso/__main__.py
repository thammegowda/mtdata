#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/8/20
import logging as log

log.basicConfig(level=log.INFO)


def main(langs=None):
    from mtdata.iso import iso3_code
    from mtdata.iso.iso639_3 import code_to_name, data as ISO639_3
    args = parse_args()
    langs = langs or args.get('langs', [])
    brief = args.get('brief')
    if not langs:
        print(ISO639_3)
    else:
        if not brief:
            print(f"Input\tISO639_3\tName")
        for lang in langs:
            iso_code = iso3_code(lang, fail_error=brief)
            iso_name = code_to_name(iso_code) if iso_code else '-none-'
            if brief:
                assert iso_code, f'Unable to resolve {lang} to valid language code.'
                print(f"{iso_code}\t{iso_name}")
            else:
                iso_code = iso_code or '-none-'
                print(f"{lang}\t{iso_code}\t{iso_name}")


def parse_args():
    import argparse
    p = argparse.ArgumentParser(prog='python -m mtdata.iso', description="ISO 639-3 lookup tool")
    p.add_argument("langs", nargs='*', help="Language code or name that needs to be looked up. "
                                            "When no language code is given, all languages are listed.")
    p.add_argument('-b', '--brief', action='store_true', help="be brief; do crash on error inputs")

    return vars(p.parse_args())


if __name__ == '__main__':
    main()
