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
    list_p = sub_ps.add_parser('list', formatter_class=MyFormatter)
    list_p.add_argument('-l', '--langs', metavar='L1-L2', type=LangPair, help='Language pairs; e.g.: de-en')
    list_p.add_argument('-n', '--names', metavar='NAME', nargs='*', help='Name of dataset set; eg europarl_v9.')
    list_p.add_argument('-nn', '--not-names', metavar='NAME', nargs='*', help='Exclude these names')
    list_p.add_argument('-f', '--full', action='store_true', help='Show Full Citation')
    list_p.add_argument('-o', '--out', type=Path, help='This arg is ignored. '
                                                         'Only used in "get" subcommand.')

    get_p = sub_ps.add_parser('get', formatter_class=MyFormatter)
    get_p.add_argument('-l', '--langs', metavar='L1-L2', type=LangPair, help='Language pairs; e.g.: de-en',
                          required=True)
    get_p.add_argument('-tr', '--train', metavar='NAME', dest='train_names', nargs='*',
                       help='''R|Names of datasets separated by space, to be used for *training*.
  e.g. -tr news_commentary_v14 europarl_v9 .
  All these datasets gets concatenated into one big file. 
  ''')
    get_p.add_argument('-ts', '--test', metavar='NAME', dest='test_names', nargs='*',
                       help='''R|Names of datasets separated by space, to be used for *testing*. 
  e.g. "-tt newstest2018_deen newstest2019_deen".
You may also use shell expansion if your shell supports it.
  e.g. "-tt newstest201{8,9}_deen." ''')

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
        assert args.train_names or args.test_names, 'Required --train or --test or both'
        dataset = Dataset.prepare(args.langs, train_names=args.train_names,
                                  test_names=args.test_names, out_dir=args.out, cache_dir=args.cache)
        cli_sig = f'-l {"-".join(args.langs)}'
        cli_sig += f' -tr {" ".join(args.train_names)}' if args.train_names else ''
        cli_sig += f' -ts {" ".join(args.test_names)}' if args.test_names else ''
        log.info(f'Dataset is ready at {dataset.dir}')
        log.info(f'mtdata args for reproducing this dataset:\nmtdat get {cli_sig} -o <out-dir>\n'
                 f'mtdata version: {mtdata.__version__}')

if __name__ == '__main__':
    main()
