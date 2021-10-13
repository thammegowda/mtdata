#!/usr/bin/env python
# This module along with accompanying bcp47.json, tries to parse BCP47 like language IDs
# This is not 100% compatible with BCP47
# We diverge on :
#   using three letter code for all languages
#      => language: 3 letter (lowercase), script: 4 letter (title case), and country: 2 letter (uppercase)
#   no support for too many variations: limited to (lll, Ssss, CC) i.e (lang, script, country)
#
# Author: Thamme Gowda [tg (at) isi.edu]
# Created: 10/3/21

from pathlib import Path
import json
from mtdata.iso import iso3_code
from dataclasses import dataclass
from typing import Optional
from collections import namedtuple


def load_json(path: Path):
    assert path.exists()
    with open(path, encoding='utf-8') as fp:
        return json.load(fp)


class BCP47Tag(namedtuple('BCP47Tag', ('lang', 'script', 'region', 'tag'))):
    __slots__ = ()

    def __new__(cls, lang, script: Optional[str]=None, region: Optional[str]=None):
        tag = ''.join([lang, f'-{script}' if script else '', f'-{region}' if region else ''])
        obj = super(BCP47Tag, cls).__new__(cls, lang, script, region, tag)
        #obj.tag = tag
        return obj

    def __str__(self):
        return self.tag


class BCP47Parser:

    def __init__(self, data):
        self.data = data
        assert all(key in data for key in ['languages', 'scripts', 'countries']), 'malformed bcp4j data'
        self.scripts = {code: name for code, name in data['scripts']}
        self.countries = {code: name for code, name in data['countries']}
        self.languages = {code3: (code2, name) for code3, code2, name in data['languages']}
        for key in self.languages:  # validation
            assert key == iso3_code(key, fail_error=True)
        self.default_scripts = {}  # these needs suppression; eng-Latn is just eng, as Latn is default
        for lang_code, script_code, lang_name in data['default_scripts']:
            code3 = iso3_code(lang_code, fail_error=True)
            assert script_code in self.scripts
            self.default_scripts[code3] = script_code

    def parse(self, tag) -> BCP47Tag:
        """
        Parameters
        ----------
        tag : tag to be parsed

        Returns
        -------
            BCP47Tag
        """
        code_orig = tag
        tag = tag.replace('_', '-').strip()
        assert tag
        parts = tag.split('-')
        assert 1 <= len(parts) <= 3, f'BCP47 code longer than 3 parts not supported yet; given {code_orig}'
        lang, script, region = None, None, None
        # part 1: it has to be language
        lang = iso3_code(parts[0], default=None)
        assert lang, f'Unable to recognize {code_orig}; Unknown language'
        assert lang in self.languages, f'{lang} is invalid'

        parts = parts[1:]
        if parts:  # part 2 can be either script or region code
            if parts[0].title() in self.scripts:
                script = parts[0].title()
            elif parts[0].upper() in self.countries:
                region = parts[0].upper()
            else:
                raise ValueError(f'Unable to parse {code_orig}')
            parts = parts[1:]
        if parts:  # part 3, if it exists, must be a region
            assert script
            assert not region
            if parts[0].upper() in self.countries:
                region = parts[0].upper()
            else:
                raise ValueError(f"Cant find {code_orig}; Unknown region")
            parts = parts[1:]
        assert not parts  # all parts are consumed
        if script and self.default_scripts[lang] == script:
            script = None  # suppress script
        tag = BCP47Tag(lang=lang, script=script, region=region)
        return tag

    def __call__(self, tag) -> BCP47Tag:
        """
        Parameters
        ----------
        tag : tag to be parsed
        Returns
        -------
           BCP47Tag
        """
        return self.parse(tag)


data_file = Path(__file__).parent / "bcp47.json"
bcp47_data = load_json(data_file)
bcp47 = BCP47Parser(data=bcp47_data)

if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser(prog='python -m mtdata.iso.bcp47', description="BCP47 lookup tool")
    p.add_argument("langs", nargs='+', help="Language code or name that needs to be looked up. "
                                            "When no language code is given, all languages are listed.")
    args = vars(p.parse_args())
    if args.get('langs'):
        print("INPUT\tSTD\tLANG\tSCRIPT\tREGION")
        for inp in args['langs']:
            tag = bcp47(inp)
            print(f'{inp}\t{tag}\t{tag.lang}\t{tag.script}\t{tag.region}')
