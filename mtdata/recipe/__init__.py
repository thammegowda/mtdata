#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 10/27/21
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional

from mtdata import yaml, cache_dir, recipes_dir, log
from mtdata.entry import lang_pair, LangPair, DatasetId, BCP47Tag, bcp47


_def_recipes: Path = Path(__file__).parent / 'recipes.yml'
_home_recipes: Path = cache_dir / 'mtdata.recipes.yml'
_cwd_recipes: List[Path] = list(recipes_dir.glob('mtdata.recipes*.yml'))


@dataclass
class Recipe:

    id: str
    langs: LangPair
    train: List[DatasetId]
    test: Optional[List[DatasetId]] = None
    dev: Optional[List[DatasetId]] = None
    desc: Optional[str] = ''
    url: str = ''

    @classmethod
    def parse(cls, langs, train, test=None, dev=None, **kwargs):
        train, dev, test = [None if not x else
                            isinstance(x, list) and x or x.split(',') for x in (train, dev, test)]
        langs = lang_pair(langs)
        train = train and [DatasetId.parse(i) for i in train]
        test = test and [DatasetId.parse(i) for i in test]
        dev = dev and [DatasetId.parse(i) for i in dev]
        return cls(langs=langs, train=train, test=test, dev=dev, **kwargs)

    def format(self):
        rec = vars(self)
        rec['langs'] = '-'.join(map(str, self.langs))
        rec['train'] = self.train and ','.join(str(did) for did in self.train)
        rec['test'] = self.test and ','.join(str(did) for did in self.test)
        rec['dev'] = self.dev and ','.join(str(did) for did in self.dev)
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
                try:
                    r = cls.parse(**r)
                except:
                    log.error(f"Error while parsing recipe:\n{r}")
                    raise
                assert r.id not in recipes, f'{r} is a duplicate'
                recipes[r.id] = r
        return recipes

    @classmethod
    def load_all(cls):
        assert _def_recipes.exists(), f'{_def_recipes} file expected but not found'
        paths = [_def_recipes]
        if _home_recipes.exists():
            paths.append(_home_recipes)
        if _cwd_recipes:
            paths.extend(_cwd_recipes)
        return cls.load(*paths)


def print_all(recipes: List[Recipe], delim='\t', out=sys.stdout):
    for i, val in enumerate(recipes):
        kvs = val.format().items()
        if i == 0:
            out.write(delim.join([kv[0] or '' for kv in kvs]) + '\n')
        out.write(delim.join([kv[1] or '' for kv in kvs]) + '\n')


RECIPES = Recipe.load_all()


if __name__ == '__main__':
    print_all(list(RECIPES.values()))
