#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20


__version__ = '0.4.3-dev'
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
resource_dir:Path = Path(__file__).parent / 'resource'
pbar_man = enlighten.get_manager()

class MTDataException(Exception):
    pass


class MTDataUserError(MTDataException):
    """
    This exception is for the cases where printing the whole stack trace is bad UI
    and we want to show a user-friendly message. https://github.com/thammegowda/mtdata/issues/162
    """
    def __init__(self, msg, exitcode=1, *args):
        super().__init__(*args)
        self.msg = msg
        self.exitcode = exitcode


class Defaults:
    FILE_LOCK_TIMEOUT = 2 * 60 * 60  # 2 hours
    PBAR_REFRESH_INTERVAL = 1    # seconds