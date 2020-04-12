#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/10/20

from typing import Mapping, List
from pathlib import Path
from collections import defaultdict
import json
from pprint import pprint

def read_codes(codes:Path) -> Mapping[str, str]:
    with codes.open('r', encoding='utf8', errors='ignore') as f:
        recs = [line.rstrip('\n').split('\t') for line in f]
        recs = recs[1:] # skip header
        return {r[0].strip(): r[6].strip() for r in recs} # Id, Ref_Name

def read_names(names_index:Path) -> Mapping[str, List[str]]:
    names = defaultdict(list)
    with names_index.open('r', encoding='utf8', errors='ignore') as f:
        recs = [line.rstrip('\n').split('\t') for line in f]
        recs = recs[1:] # skip header
        for r in recs:
            names[r[0]].append(r[1])
        return dict(names)

def parse(codes: Path, names_index: Path):
    codes = read_codes(codes)
    names = read_names(names_index)
    assert set(codes.keys()) == set(names.keys())
    res = {}
    for code, ref_name in codes.items():
        more_names = list(set(names[code]) - {ref_name})
        val = [ref_name, more_names]
        res[code] = val
    return res

def myprint(data):
    res = ''
    for code, (ref_name, aliases) in data.items():
        assert not any(',' in a for a in aliases)
        assert not ',' in ref_name
        aliases = ','.join(aliases)
        res += f'{code}\t{ref_name}\t{aliases}\n'
    return res

if __name__ == '__main__':
    codes = Path('iso-639-3.tsv')
    names = Path('iso-639-3-names.tsv')
    res = parse(codes, names)
    res = myprint(res).rstrip('\n')

    out = f"""
# ISO 639-3 codes  retrieved from https://iso639-3.sil.org/code_tables/download_tables
#
# Prepared as python module by Thamme Gowda for mtdata https://github.com/thammegowda/mtdata

data='''{res}'''

codes = dict() 
for line in data.splitlines():
    code, ref_name, aliases = line.split('\\t')
    aliases = set(aliases.split('.')) if aliases else set()
    codes[code] = (ref_name, aliases)
"""
    print(out)

