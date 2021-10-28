#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 10/27/21
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union, Dict, Optional


from mtdata import yaml, cache_dir, log
from mtdata.entry import lang_pair, LangPair, DatasetId


_def_recipes: Path = Path(__file__).parent / 'recipes.yml'
_cwd_recipes: Path = Path('.').expanduser() / 'mtdata.recipes.yml'
_home_recipes: Path = cache_dir / 'mtdata.recipes.yml'


@dataclass
class Recipe:

    id: str
    langs: Union[LangPair, List[LangPair]]
    train: List[DatasetId]
    test: List[DatasetId]
    dev: Optional[DatasetId] = ''
    desc: Optional[str] = ''
    url: str = ''

    @classmethod
    def parse(cls, langs, train, test, dev='', **kwargs):
        if isinstance(langs, str):
            langs = langs.split(',')
        if isinstance(train, str):
            train = train.split(',')
        if isinstance(test, str):
            test = test.split(',')
        assert isinstance(langs, list)
        assert isinstance(train, list)
        assert isinstance(test, list)
        langs = [lang_pair(lang) for lang in langs]
        train = [DatasetId.parse(i) for i in train]
        test = [DatasetId.parse(i) for i in test]
        dev = dev and DatasetId.parse(dev)
        return cls(langs=langs, train=train, test=test, dev=dev, **kwargs)

    def format(self):
        rec = vars(self)
        rec['langs'] = ','.join(f'{pair[0]}-{pair[1]}' for pair in self.langs)
        rec['train'] = ','.join(str(did) for did in self.train)
        rec['test'] = ','.join(str(did) for did in self.test)
        rec['dev'] = str(self.dev)
        return rec

    @classmethod
    def load(cls, *paths) -> Dict[str, 'Recipe']:
        assert len(paths) > 0
        recipes = {}
        for path in paths:
            log.info(f"Loading recipes from {path}")
            with open(path) as inp:
                recipes_raw = yaml.load(inp)
            for r in recipes_raw:
                assert isinstance(r, dict), f'{r} expected to be a dict'
                r = cls.parse(**r)
                assert r.id not in recipes, f'{r} is a duplicate'
                recipes[r.id] = r
        return recipes

    @classmethod
    def load_all(cls):
        assert _def_recipes.exists(), f'{_def_recipes} file expected but not found'
        paths = [_def_recipes]
        if _home_recipes.exists():
            paths.append(_home_recipes)
        if _cwd_recipes.exists():
            paths.append(_cwd_recipes)
        return cls.load(*paths)


def print_all(recipes: List[Recipe], delim='\t', out=sys.stdout):
    for i, val in enumerate(recipes):
        kvs = val.format().items()
        if i == 0:
            out.write(delim.join([kv[0] for kv in kvs]) + '\n')
        out.write(delim.join([kv[1] for kv in kvs]) + '\n')


RECIPES = Recipe.load_all()


if __name__ == '__main__':
    print_all(list(RECIPES.values()))
