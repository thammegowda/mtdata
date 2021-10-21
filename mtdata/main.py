#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20
import argparse
from pathlib import Path
from collections import defaultdict

import mtdata
from mtdata import log, __version__, cache_dir as CACHE_DIR, cached_index_file
from mtdata.entry import DatasetId, LangPair
from mtdata.utils import IO
from mtdata.iso.bcp47 import bcp47


def list_data(langs, names, not_names=None, full=False):
    from mtdata.index import get_entries
    entries = get_entries(langs, names, not_names, fuzzy_match=True)
    log.info(f"Found {len(entries)}")
    for i, ent in enumerate(entries):
        print(ent.format(delim='\t'))
        if full:
            print(ent.cite or "CITATION_NOT_LISTED", end='\n\n')
    print(f"Total {len(entries)} entries")


def get_data(langs, out_dir, train_dids=None, test_dids=None, dev_did=None, merge_train=False, compress=False,
             drop_dupes=False, drop_tests=False, **kwargs):
    if kwargs:
        log.warning(f"Args are ignored: {kwargs}")
    from mtdata.data import Dataset
    assert train_dids or test_dids, 'Required --train or --test or both'
    dataset = Dataset.prepare(
        langs, train_dids=train_dids, test_dids=test_dids, out_dir=out_dir,
        dev_did=dev_did, cache_dir=CACHE_DIR, merge_train=merge_train, compress=compress,
        drop_dupes=drop_dupes, drop_tests=drop_tests)
    cli_sig = f'-l {"-".join(str(l) for l in langs)}'
    if train_dids:
        cli_sig += f' -tr {" ".join(str(d) for d in train_dids)}'
    if test_dids:
        cli_sig += f' -ts {" ".join(str(d) for d in test_dids)}'
    if dev_did:
        cli_sig += f' -dv {dev_did}'
    for flag, val in [('--merge', merge_train), ('--compress', compress), ('-dd', drop_dupes), ('-dt', drop_tests)]:
        if val:
            cli_sig += ' ' + flag
    sig = f'mtdata get {cli_sig} -o <out-dir>\nmtdata version {mtdata.__version__}\n'
    log.info(f'Dataset is ready at {dataset.dir}')
    log.info(f'mtdata args for reproducing this dataset:\n {sig}')
    with IO.writer(out_dir / 'mtdata.signature.txt', append=True) as w:
        w.write(sig)


def generate_report(langs, names, not_names=None, format='plain'):
    from mtdata.index import get_entries
    entries = get_entries(langs, names, not_names)
    lang_stats = defaultdict(int)
    name_stats = defaultdict(int)
    group_stats = defaultdict(int)
    for ent in entries:
        lang_stats[ent.lang_str] += 1
        name_stats[ent.did.name] += 1
        group_stats[ent.did.group] += 1

    print("Languages:")
    for key, val in lang_stats.items():
        print(f'{key}\t{val:,}')

    print("\nNames:")
    for key, val in name_stats.items():
        print(f'{key}\t{val:,}')

    print("\nGroups:")
    for key, val in group_stats.items():
        print(f'{key}\t{val:,}')


def list_experiments(args):
    raise Exception("Not implemented yet")


class MyFormatter(argparse.ArgumentDefaultsHelpFormatter):

    def _split_lines(self, text, width: int):
        if text.startswith("R|"):
            return text[2:].splitlines()
        return super()._split_lines(text, width)


def lang_pair(string) -> LangPair:
    parts = string.split('-')
    if len(parts) != 2:
        msg = f'expected value of form "xxx-yyz" eg "deu-eng"; given {string}'
        raise argparse.ArgumentTypeError(msg)
    std_codes = (bcp47(parts[0]), bcp47(parts[1]))
    std_form = '-'.join(str(lang) for lang in std_codes)
    if std_form != string:
        log.info(f"Suggestion: Use codes {std_form} instead of {string}."
                 f" Let's make a little space for all languages of our planet 😢.")
    return std_codes


def add_boolean_arg(parser: argparse.ArgumentParser, name, dest=None, default=False, help=''):
    group = parser.add_mutually_exclusive_group()
    dest = dest or name
    group.add_argument(f'--{name}', action='store_true', dest=dest, default=default, help=help)
    group.add_argument(f'--no-{name}', action='store_false', dest=dest, default=not default,
                       help='Do not ' + help)


def parse_args():
    p = argparse.ArgumentParser(formatter_class=MyFormatter, epilog=f'Loaded from {__file__} (v{__version__})')
    p.add_argument('-vv', '--verbose', action='store_true', help='verbose mode')
    p.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    p.add_argument('-ri', '--reindex', action='store_true',
                   help=f"Invalidate index of entries and recreate it. This deletes"
                        f" {cached_index_file} only and not the downloaded files. "
                        f"Use this if you're using in developer mode and modifying mtdata index.")

    sub_ps = p.add_subparsers(required=True, dest='task',
                              help='''R|
"list" - List the available entries 
"get" - Downloads the entry files and prepares them for experiment
"list-exp" - List the (well) known papers and datasets used in their experiments 
"get-exp" - Get the datasets used in the specified experiment from "list-exp" 
''')

    list_p = sub_ps.add_parser('list', formatter_class=MyFormatter)
    list_p.add_argument('-l', '--langs', metavar='L1-L2', type=lang_pair,
                        help='Language pairs; e.g.: deu-eng')
    list_p.add_argument('-n', '--names', metavar='NAME', nargs='*',
                        help='Name of dataset set; eg europarl_v9.')
    list_p.add_argument('-nn', '--not-names', metavar='NAME', nargs='*', help='Exclude these names')
    list_p.add_argument('-f', '--full', action='store_true', help='Show Full Citation')
    list_p.add_argument('-o', '--out', type=Path, help='This arg is ignored. '
                                                       'Only used in "get" subcommand.')

    get_p = sub_ps.add_parser('get', formatter_class=MyFormatter)
    get_p.add_argument('-l', '--langs', metavar='L1-L2', type=lang_pair,
                       help='Language pairs; e.g.: deu-eng', required=True)
    get_p.add_argument('-tr', '--train', metavar='ID', dest='train_dids', nargs='*', type=DatasetId.parse,
                       help='''R|Names of datasets separated by space, to be used for *training*.
    e.g. -tr Statmt-news_commentary-16-deu-eng europarl_v9 .
     To concatenate all these into a single train file, set --merge flag.''')
    get_p.add_argument('-ts', '--test', metavar='ID', dest='test_dids', nargs='*', type=DatasetId.parse,
                       help='''R|Names of datasets separated by space, to be used for *testing*. 
    e.g. "-ts Statmt-newstest_deen-2019-deu-eng Statmt-newstest_deen-2020-deu-eng ".
    You may also use shell expansion if your shell supports it.
    e.g. "-ts Statmt-newstest_deen-20{19,20}-deu-eng" ''')
    get_p.add_argument('-dv', '--dev', metavar='ID', dest='dev_did', type=DatasetId.parse, required=False,
                       help='''R|Dataset to be used for development (aka validation). 
    e.g. "-dev Statmt-newstest_deen-2017-deu-eng"''')
    add_boolean_arg(get_p, 'merge', dest='merge_train', default=False, help='Merge train into a single file')
    get_p.add_argument(f'--compress', action='store_true', default=False, help="Keep the files compressed")
    get_p.add_argument('-dd', f'--dedupe', '--drop-dupes', dest='drop_dupes', action='store_true', default=False,
                       help="Remove duplicate (src, tgt) pairs in training (if any); valid when --merge. "
                            "Not recommended for large datasets. ")
    get_p.add_argument('-dt', f'--drop-tests', dest='drop_tests', action='store_true', default=False,
                       help="Remove dev/test sentences from training sets (if any); valid when --merge")
    get_p.add_argument('-o', '--out', dest='out_dir', type=Path, required=True, help='Output directory name')

    report_p = sub_ps.add_parser('report', formatter_class=MyFormatter)
    report_p.add_argument('-l', '--langs', metavar='L1-L2', type=lang_pair,
                          help='Language pairs; e.g.: deu-eng')
    report_p.add_argument('-n', '--names', metavar='NAME', nargs='*',
                          help='Name of dataset set; eg europarl_v9.')
    report_p.add_argument('-nn', '--not-names', metavar='NAME', nargs='*', help='Exclude these names')

    args = p.parse_args()
    if args.verbose:
        log.getLogger().setLevel(level=log.DEBUG)
        mtdata.debug_mode = True
    return args


def main():
    args = parse_args()
    if args.reindex and cached_index_file.exists():
        bak_file = cached_index_file.with_suffix(".bak")
        log.info(f"Invalidate index: {cached_index_file} -> {bak_file}")
        cached_index_file.rename(bak_file)

    if args.task == 'list':
        list_data(args.langs, args.names, not_names=args.not_names, full=args.full)
    elif args.task == 'get':
        get_data(**vars(args))
    elif args.task == 'list_exp':
        list_experiments(args)
    elif args.task == 'report':
        generate_report(args.langs, names=args.names, not_names=args.not_names)
    else:
        raise Exception(f'{args.task} not implemented')


if __name__ == '__main__':
    main()
