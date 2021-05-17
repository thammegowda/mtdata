#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20
import errno
from mtdata import main, log

if __name__ == '__main__':
    try:
        main.main()
    except BrokenPipeError as e:
        # this happens when piped to '| head' which aborts pipe after limit. And that is okay.
        pass