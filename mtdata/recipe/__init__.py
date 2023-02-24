#!/usr/bin/env python
#
#
# Author: Thamme Gowda
# Created: 10/27/21
import copy
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, ClassVar, Tuple

from mtdata import yaml, cache_dir, recipes_dir, log, resource_dir
from mtdata.entry import Langs, LangPair, DatasetId, BCP47Tag, bcp47
from mtdata.data import DATA_FIELDS


_def_recipes: Path = resource_dir / 'recipes.yml'
_home_recipes: Path = cache_dir / 'mtdata.recipes.yml'
_cwd_recipes: List[Path] = list(recipes_dir.glob('mtdata.recipes*.yml'))


@dataclass
class Recipe:

    id: str
    langs: LangPair
    train: List[DatasetId] = None
    test: Optional[List[DatasetId]] = None
    dev: Optional[List[DatasetId]] = None
    mono_train: Optional[List[DatasetId]] = None
    mono_dev: Optional[List[DatasetId]] = None
    mono_test: Optional[List[DatasetId]] = None
    desc: Optional[str] = ''
    url: str = ''
    # class variables below
    _id_field_names: ClassVar[Tuple] = DATA_FIELDS

    @classmethod
    def parse(cls, id:str, langs, **kwargs):
        langs = Langs(langs)
        data_fields = {}
        for name in cls._id_field_names:
            if name in kwargs:
                data_ids = kwargs.pop(name)
                if not data_ids:
                    continue
                if isinstance(data_ids, str):
                    data_ids = [data_ids]
                res = []
                assert isinstance(data_ids, list)
                for data_id in data_ids:
                    if isinstance(data_id, str):
                        res += data_id.split(',')
                    else:     # nested list
                        assert isinstance(data_id, list)
                        res += data_id
                res = [i.strip() for i in res if i.strip()]  # drop emtpy
                assert len(res) == len(set(res)), f'Duplicate ids found in {id}.{name}; expected unique ids'
                data_fields[name] = [DatasetId.parse(i.strip()) for i in res]
        return cls(id=id, langs=langs, **data_fields, **kwargs)

    @property
    def data_fields(self) -> Dict:
        return {name: getattr(self, name) for name in self._id_field_names}

    def format(self, compact=True):
        rec = copy.copy(vars(self))
        rec['langs'] = '-'.join(map(str, self.langs))
        for name, dids in self.data_fields.items():
            if dids:
                dids = [str(did) for did in dids]
                if compact:
                    dids = ','.join(dids)
                rec[name] = dids
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
                    log.error(f"Error while parsing recipe: {path}\n{r.get('id') or r}")
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

RECIPES = Recipe.load_all()
