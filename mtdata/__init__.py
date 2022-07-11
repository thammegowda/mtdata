#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20


__version__ = '0.3.7'
__description__ = 'mtdata is a tool to download datasets for machine translation'
__author__ = 'Thamme Gowda'

import logging as log
from pathlib import Path
import os
import enlighten
from ruamel.yaml import YAML

yaml = YAML()
debug_mode = False
_log_format = '%(asctime)s %(module)s.%(funcName)s:%(lineno)s %(levelname)s:: %(message)s'
log.basicConfig(level=log.INFO, datefmt='%Y-%m-%d %H:%M:%S', format=_log_format)
cache_dir = Path(os.environ.get('MTDATA', '~/.mtdata')).expanduser()
recipes_dir = Path(os.getenv('MTDATA_RECIPES', '.')).resolve()
cached_index_file = cache_dir / f'mtdata.index.{__version__}.pkl'

FILE_LOCK_TIMEOUT = 2 * 60 * 60  # 2 hours
pbar_man = enlighten.get_manager()


class MTDataException(Exception):
    pass
