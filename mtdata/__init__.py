#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20

__version__ = '0.2.10'
__description__ = 'mtdata is a tool to download datasets for machine translation'
__author__ = 'Thamme Gowda'

import logging as log
from pathlib import Path
import os

debug_mode = False
_log_format = '%(asctime)s %(module)s.%(funcName)s:%(lineno)s %(levelname)s:: %(message)s'
log.basicConfig(level=log.INFO, datefmt='%Y-%m-%d %H:%M:%S', format=_log_format)
cache_dir = Path(os.environ.get('MTDATA', '~/.mtdata')).expanduser()
cached_index_file = cache_dir / f'mtdata.index.{__version__}.pkl'
