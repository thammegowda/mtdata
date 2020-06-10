#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20

__version__ = '0.2.5'
__description__ = 'mtdata is a tool to download datasets for machine translation'
__author__ = 'Thamme Gowda'

import logging as log
from pathlib import Path
import os

debug_mode = False
log.basicConfig(level=log.INFO)
cache_dir = Path(os.environ.get('MTDATA', '~/.mtdata')).expanduser()