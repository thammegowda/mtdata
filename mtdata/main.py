#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20
import argparse
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Mapping, Tuple, Optional
import json
import fnmatch

import mtdata
from mtdata import log, __version__, cache_dir as CACHE_DIR, cached_index_file
from mtdata import pbar_man
from mtdata.entry import DatasetId, Langs
from mtdata.utils import IO, format_byte_size

DEF_N_JOBS = 1


def list_data(langs, names, not_names=None, full=False, groups=None, not_groups=None, id_only=False):
    from mtdata.index import get_entries
    entries = get_entries(langs, names, not_names, groups=groups, not_groups=not_groups, fuzzy_match=True)
    for i, ent in enumerate(entries):
        if id_only:
            print(ent.did)
        else:
            print(ent.format(delim='\t'))
        if full:
            print(ent.cite or "CITATION_NOT_LISTED", end='\n\n')
    log.info(f"Total {len(entries)} entries")


def get_data(langs, out_dir, merge_train=False, compress=False,
             drop_dupes=False, drop_tests=False, fail_on_error=False, n_jobs=DEF_N_JOBS, **kwargs):
    from mtdata.data import Dataset, DATA_FIELDS
    dataset_ids: Dict[str, List] = {}
    for name in DATA_FIELDS:
        old_name = f'{name}_dids'  # previously, "train_dids" was used. now "train"
        if kwargs.get(old_name):
            dataset_ids[name] = kwargs.pop(old_name)
    if kwargs:
        log.info(f"Args are ignored: {kwargs}")
    assert any(bool(ids) for ids in dataset_ids.values()),\
        f'Required at least one of --train --test --dev --mono-train --mono-test --mono-dev \n given={dataset_ids.keys()}'
    dataset = Dataset.prepare(
        langs, dataset_ids=dataset_ids, out_dir=out_dir, cache_dir=CACHE_DIR,
        merge_train=merge_train, compress=compress,
        drop_dupes=drop_dupes, drop_tests=drop_tests, fail_on_error=fail_on_error, n_jobs=n_jobs)
    cli_sig = f'-l {"-".join(str(l) for l in langs)}'

    for name, dids in dataset_ids.items():
        if dids:
            flag = '--' + name.replace('_', '-')
            cli_sig += f' {flag} {" ".join(map(str, dids))}'
    for flag, val in [('--merge', merge_train), ('--compress', compress), ('-dd', drop_dupes), ('-dt', drop_tests)]:
        if val:
            cli_sig += ' ' + flag
    sig = f'mtdata get {cli_sig} -o <out-dir>\nmtdata version {mtdata.__version__}\n'
    log.info(f'Dataset is ready at {dataset.dir}')
    log.info(f'mtdata args for reproducing this dataset:\n {sig}')
    with IO.writer(out_dir / 'mtdata.signature.txt', append=True) as w:
        w.write(sig)


def echo_data(did:DatasetId, delim='\t'):
    from mtdata.data import INDEX, Cache, Parser
    assert did in INDEX
    entry = INDEX[did]
    cache = Cache(CACHE_DIR)
    path = cache.get_entry(entry)
    parser = Parser(path, ext=entry.in_ext or None, ent=entry)
    count = 0
    all_segs = parser.read_segs()
    for rec in all_segs:
        if isinstance(rec, (list, tuple)):
            rec = (col.replace(delim, ' ').replace('\n', ' ') for col in rec)
            rec = delim.join(rec)
        print(rec)
        count += 1
    log.info(f'Total rows={count:,}')


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
    for key, val in sorted(group_stats.items(), key=lambda x:x[1], reverse=True):
        print(f'{key}\t{val:,}')
    print(f'[Total]\t{sum(group_stats.values()):,}')


def list_recipes(id_only=False, delim='\t', format='plain'):
    from mtdata.recipe import RECIPES
    log.info(f"Found {len(RECIPES)} recipes")
    for i, recipe in enumerate(RECIPES.values()):
        if id_only:
            print(recipe.id)
        else:
            if format == 'plain':
                kvs = recipe.format(compact=True).items()
                if i == 0:
                    print(delim.join([kv[0] or '' for kv in kvs]))
                print(delim.join([kv[1] or '' for kv in kvs]))
            elif format == 'json':
                kvs = recipe.format(compact=False).items()
                print(json.dumps({k:v for k, v in kvs if v}))
            else:
                raise f'{format} not supported'


def get_recipe(recipe_id, out_dir: Path, compress=False, drop_dupes=False, drop_tests=False, fail_on_error=False,
               n_jobs=DEF_N_JOBS, merge_train=True, **kwargs):
    if kwargs:
        log.warning(f"Args are ignored: {kwargs}")
    from mtdata.recipe import RECIPES
    recipe = RECIPES.get(recipe_id)
    if not recipe:
        raise ValueError(f'recipe {recipe_id} not found. See "mtdata list-recipe"')

    data_fields = {f'{k}_dids': v for k, v in recipe.data_fields.items()}
    get_data(langs=recipe.langs, merge_train=merge_train, out_dir=out_dir, compress=compress, drop_dupes=drop_dupes,
             drop_tests=drop_tests, fail_on_error=fail_on_error, n_jobs=n_jobs, **data_fields)


def show_stats(*dids: DatasetId, quick=False):
    from mtdata.index import INDEX as index
    from mtdata.cache import Cache
    cache = Cache(CACHE_DIR)
    for did in dids:
        entry = index[did]
        if quick:
            stats = cache.get_content_length(entry)
        else:
            stats = cache.get_stats(entry)
        print(json.dumps(stats))

def cache_datasets(recipes:List[str]=None, dids:List[DatasetId]=None, n_jobs=DEF_N_JOBS):
    from mtdata.cache import Cache
    from mtdata.data import Dataset
    from mtdata.recipe import RECIPES

    cache = Cache(CACHE_DIR)
    all_dids = set()
    if dids:
        all_dids.update(dids)
    if recipes:
        GLOB_CHARS = '*?[]!'
        for recipe_id in recipes:
            if any(c in recipe_id for c in GLOB_CHARS):  # glob pattern
                matched_rids = fnmatch.filter(RECIPES.keys(), recipe_id)
                if not matched_rids: # at least one match expected
                    log.warning(f'No recipe matched for {recipe_id}')
                for rid in matched_rids:
                    all_dids.update(RECIPES.get(rid).all_dids())
            else:  # exact match
                recipe = RECIPES.get(recipe_id)
                if not recipe:
                    raise ValueError(f'recipe {recipe_id} not found. See "mtdata list-recipe"')
                all_dids.update(recipe.all_dids())
    assert all_dids, 'No datasets found to cache'
    entries = Dataset.resolve_entries(all_dids)
    assert entries, f'No entries found'
    log.info(f"Going to cache {len(entries)} entries at {cache.root}; n_jobs={n_jobs}")
    Dataset.parallel_download(entries, cache=cache, n_jobs=n_jobs)

class MyFormatter(argparse.ArgumentDefaultsHelpFormatter):

    def _split_lines(self, text, width: int):
        if text.startswith("R|"):
            return text[2:].splitlines()
        return super()._split_lines(text, width)


def add_boolean_arg(parser: argparse.ArgumentParser, name, dest=None, default=False, help=''):
    group = parser.add_mutually_exclusive_group()
    dest = dest or name
    group.add_argument(f'--{name}', action='store_true', dest=dest, default=default, help=help)
    group.add_argument(f'--no-{name}', action='store_false', dest=dest, default=not default,
                       help='Do not ' + help)


def parse_args():
    my_path = str(Path(__file__).parent)
    p = argparse.ArgumentParser(formatter_class=MyFormatter, epilog=f'Loaded from {my_path} (v{__version__})')
    p.add_argument('-vv', '--verbose', action='store_true', help='verbose mode')
    p.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__} \n{my_path}')
    log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    p.add_argument('-ll', '--log-level', default='INFO', metavar='LEVEL',
                   choices=log_levels, help=f'Set log level. Choices={log_levels}')
    p.add_argument('-ri', '--reindex', action='store_true',
                   help=f"Invalidate index of entries and recreate it. This deletes"
                        f" {cached_index_file} only and not the downloaded files. "
                        f"Use this if you've modifying mtdata source code and want to force reload.")
    grp = p.add_mutually_exclusive_group()
    grp.add_argument('-pb', '--pbar', action='store_true', dest='progressbar',
                     help=f"Show progressbar", default=True)
    grp.add_argument('-no-pb', '--no-pbar', action='store_false', dest='progressbar',
                    help=f"Do not show progressbar", default=False)

    sub_ps = p.add_subparsers(required=True, dest='task', metavar='<task>',
                              help='''R|
"list" - List the available entries
"get" - Downloads the entry files and prepares them for experiment
"echo" - Print contents of a dataset into STDOUT.
"list-recipe" - List the (well) known papers and dataset recipes used in their experiments
"get-recipe" - Get the datasets used in the specified experiment from "list-recipe"
"stats" - Get stats of dataset"
"cache" - download datasets into cache
''')

    list_p = sub_ps.add_parser('list', formatter_class=MyFormatter)
    list_p.add_argument('-l', '--langs', metavar='L1/L1-L2', type=Langs,
                        help='Language ID e.g. eng (monolingual) or a pair, e.g.: deu-eng (bitext)')
    list_p.add_argument('-id', '--id', action='store_true', help="Show dataset ID only", default=False)
    list_p.add_argument('-n', '--names', metavar='NAME', nargs='*',
                        help='Name of dataset set; eg europarl_v9.')
    list_p.add_argument('-nn', '--not-names', metavar='NAME', nargs='*', help='Exclude these names')
    list_p.add_argument('-g', '--groups', metavar='GROUP', nargs='*', help='Only select datasets from these groups')
    list_p.add_argument('-ng', '--not-groups', metavar='GROUP', nargs='*', help='Exclude these groups')
    list_p.add_argument('-f', '--full', action='store_true', help='Show Full Citation')
    list_p.add_argument('-o', '--out', type=Path, help='This arg is ignored. Only used in "get" subcommand,'
                                                       ' but added here for convenience of switching b/w get and list')

    get_p = sub_ps.add_parser('get', formatter_class=MyFormatter)
    get_p.add_argument('-l', '--langs', metavar='L1-L2', type=Langs,
                       help='Language pairs; e.g.: deu-eng', required=True)
    get_p.add_argument('-tr', '--train', metavar='ID', dest='train_dids', nargs='*', type=DatasetId.parse,
                       help='''R|Names of datasets separated by space, to be used for *training*.
    e.g. -tr Statmt-news_commentary-16-deu-eng.
     To concatenate all these into a single train file, set --merge flag.''')
    get_p.add_argument('-ts', '--test', metavar='ID', dest='test_dids', nargs='*', type=DatasetId.parse,
                       help='''R|Names of datasets separated by space, to be used for *testing*. 
    e.g. "-ts Statmt-newstest_deen-2019-deu-eng Statmt-newstest_deen-2020-deu-eng ".
    You may also use shell expansion if your shell supports it.
    e.g. "-ts Statmt-newstest_deen-20{19,20}-deu-eng" ''')
    get_p.add_argument('-dv', '--dev', metavar='ID', dest='dev_dids', type=DatasetId.parse, nargs='*',
                       help='''R|Dataset to be used for development (aka validation).
    e.g. "-dev Statmt-newstest_deen-2017-deu-eng"''')
    add_boolean_arg(get_p, 'merge', dest='merge_train', default=False, help='Merge train into a single file')
    add_boolean_arg(get_p, 'fail', dest='fail_on_error', default=True,
                    help='Fail if an error occurs on any one of dataset pars')
    get_p.add_argument('-j', '--n-jobs', type=int, help="Number of worker jobs", default=DEF_N_JOBS)

    echo_p = sub_ps.add_parser('echo', formatter_class=MyFormatter)
    echo_p.add_argument('dataset_id', type=DatasetId.parse, help='Dataset ID')

    def add_getter_args(parser):
        parser.add_argument(f'--compress', action='store_true', default=False, help="Keep the files compressed")
        parser.add_argument('-dd', f'--dedupe', '--drop-dupes', dest='drop_dupes', action='store_true', default=False,
                            help="Remove duplicate (src, tgt) pairs in training (if any); valid when --merge. "
                                 "Not recommended for large datasets. ")
        parser.add_argument('-dt', f'--drop-tests', dest='drop_tests', action='store_true', default=False,
                            help="Remove dev/test sentences from training sets (if any); valid when --merge")
        parser.add_argument('-o', '--out', dest='out_dir', type=Path, required=True, help='Output directory name')

    add_getter_args(get_p)

    report_p = sub_ps.add_parser('report', formatter_class=MyFormatter)
    report_p.add_argument('-l', '--langs', metavar='L1-L2', type=Langs, help='Language pairs; e.g.: deu-eng')
    report_p.add_argument('-n', '--names', metavar='NAME', nargs='*', help='Name of dataset set; eg europarl_v9.')
    report_p.add_argument('-nn', '--not-names', metavar='NAME', nargs='*', help='Exclude these names')

    listr_p = sub_ps.add_parser('list-recipe', formatter_class=MyFormatter)
    listr_p.add_argument('-id', '--id', action='store_true', help="List recipe IDs only", default=False)
    listr_p.add_argument('-f', '--format',  help="Format", default='plain', choices=['plain', 'json'])
    getr_p = sub_ps.add_parser('get-recipe', formatter_class=MyFormatter)
    getr_p.add_argument('-ri', '-i', '--recipe-id', type=str, help='Recipe ID', required=True)
    getr_p.add_argument('-f', '--fail-on-error', action='store_true', help='Fail on error')
    getr_p.add_argument('-j', '--n-jobs', type=int, help="Number of worker jobs (processes)", default=DEF_N_JOBS)
    add_boolean_arg(getr_p, 'merge', dest='merge_train', default=True, help='Merge train into a single file')
    add_getter_args(getr_p)

    stats_p = sub_ps.add_parser('stats', formatter_class=MyFormatter)
    stats_p.add_argument('did', nargs='+', type=DatasetId.parse, help="Show stats of dataset IDs")
    stats_p.add_argument('-q', '--quick', action='store_true',
                         help=("Show quick stats without downloading or parsing dataset."
                               "This flag sends HEAD request and shows Content-Length"))

    cache_p = sub_ps.add_parser('cache', formatter_class=MyFormatter)
    cache_p.add_argument('-ri', '--recipe-id', type=str, nargs='*', help='Recipe ID. Glob patterns are supported. Example: "wmt24-*"')
    cache_p.add_argument('-di', '--dataset-id', type=DatasetId.parse, nargs='*', help='Dataset ID')
    cache_p.add_argument('-j', '--n-jobs', type=int, help="Number of worker jobs (processes)", default=DEF_N_JOBS)

    args = p.parse_args()
    if args.log_level:
        log_level = log._nameToLevel[args.log_level]
        log.getLogger().setLevel(level=log_level)
        log.debug(f'log level set to {args.log_level}')

    pbar_man.enabled = bool(args.progressbar)

    if args.verbose:
        mtdata.debug_mode = True
    return args


def main():

    args = parse_args()
    if args.reindex and cached_index_file.exists():
        bak_file = cached_index_file.with_suffix(".bak")
        log.info(f"Invalidate index: {cached_index_file} -> {bak_file}")
        cached_index_file.rename(bak_file)
    if args.task == 'list':
        list_data(args.langs, args.names, not_names=args.not_names, full=args.full,
                  groups=args.groups, not_groups=args.not_groups, id_only=args.id)
    elif args.task == 'get':
        get_data(**vars(args))
    elif args.task == 'echo':
        # disable progress bar for echo; it sometimes insert new lines in the output
        pbar_man.enabled = False
        echo_data(did=args.dataset_id)
    elif args.task == 'list-recipe':
        list_recipes(id_only=args.id, format=args.format)
    elif args.task == 'get-recipe':
        get_recipe(**vars(args))
    elif args.task == 'stats':
        show_stats(*args.did, quick=args.quick)
    elif args.task == 'report':
        generate_report(args.langs, names=args.names, not_names=args.not_names)
    elif args.task == 'cache':
        assert args.recipe_id or args.dataset_id, "Need at least one of --recipe-id or --dataset-id"
        cache_datasets(recipes=args.recipe_id, dids=args.dataset_id, n_jobs=args.n_jobs)
    else:
        raise Exception(f'task={args.task} not implemented')


if __name__ == '__main__':
    main()
