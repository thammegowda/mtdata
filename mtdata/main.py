#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20
import argparse
from pathlib import Path
import mtdata
from mtdata import log
from mtdata.data import Dataset, get_entries


def listing(langs, names, not_names=None, full=False, cache_dir=None):
    entries = get_entries(langs, names, not_names)
    log.info(f"Found {len(entries)}")
    for i, ent in enumerate(entries):
        print(ent.format(delim='\t'))
        if full:
            print(ent.cite or "CITATION_NOT_LISTED", end='\n\n')
    print(f"Total {len(entries)} entries")


class MyFormatter(argparse.ArgumentDefaultsHelpFormatter):

    def _split_lines(self, text, width: int):
        if text.startswith("R|"):
            return text[2:].splitlines()
        return super()._split_lines(text, width)

def LangPair(string):
    parts = string.split('-')
    if len(parts) != 2:
        msg = f'expected value of form "xx-yy" eg "de-en"; given {string}'
        raise argparse.ArgumentTypeError(msg)
    return tuple(parts)

def parse_args():
    p = argparse.ArgumentParser(formatter_class=MyFormatter)
    p.add_argument('-c', '--cache', type=Path, help='Cache dir', default=mtdata.cache_dir)
    p.add_argument('-vv', '--verbose', action='store_true', help='verbose mode')

    sub_ps = p.add_subparsers(required=True, dest='task',
                              help='''R|"list" - list the available entries 
"get" - downloads the files and prepares them''')
    list_p = sub_ps.add_parser('list')
    list_p.add_argument('-l', '--langs', type=LangPair, help='Language pairs; e.g.: de-en')
    list_p.add_argument('-n', '--names', nargs='*', help='Name of dataset set; eg europarl_v9.')
    list_p.add_argument('-nn', '--not-names', nargs='*', help='Exclude these names')
    list_p.add_argument('-f', '--full', action='store_true', help='Show Full Citation')

    get_p = sub_ps.add_parser('get')
    get_p.add_argument('-l', '--langs', type=LangPair, help='Language pairs; e.g.: de-en',
                          required=True)
    get_p.add_argument('-n', '--names', nargs='*', help='Name of dataset set; eg europarl_v9.')
    get_p.add_argument('-nn', '--not-names', nargs='*', help='Exclude these names.')
    get_p.add_argument('-o', '--out', type=Path, required=True, help='Output directory name')

    args = p.parse_args()
    if args.verbose:
        log.getLogger().setLevel(level=log.DEBUG)
        mtdata.debug_mode = True
    return args


def main():
    args = parse_args()
    if args.task == 'list':
        listing(args.langs, args.names, not_names=args.not_names, full=args.full,
                cache_dir=args.cache)
    elif args.task == 'get':
        dataset = Dataset.prepare(args.langs, args.names, not_names=args.not_names, out_dir=args.out,
                                  cache_dir=args.cache)
        log.info(f'Dataset is ready at {dataset.dir}')

if __name__ == '__main__':
    main()
