#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20

def main():
    from mtdata import main
    try:
        main.main()
    except BrokenPipeError as e:
        # this happens when piped to '| head' which aborts pipe after limit. And that is okay.
        pass


if __name__ == '__main__':
    main()
