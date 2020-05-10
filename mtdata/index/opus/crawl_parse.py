#!/usr/bin/env python
#
# parses the min jsonline file from OPUS
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/9/20
import json
import logging as log

log.basicConfig(level=log.INFO)


def main(args=None):
    args = args or parse_args()
    args.out.write('data="""')
    for line in args.inp:
        data = json.loads(line)
        url = data['url'].split("?f=")[-1]
        name = data['name']
        langs = " ".join(f"{l1}-{l2}" for l1, l2 in data['langs'])
        args.out.write(f"{name}\t{url}\t{langs}\n")
    args.out.write('"""')

def parse_args():
    import argparse
    import sys
    import io
    stdin = io.TextIOWrapper(sys.stdin, encoding='utf-8', errors='ignore')
    stdout = io.TextIOWrapper(sys.stdout, encoding='utf-8', errors='ignore')
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    p.add_argument('-i', '--inp', type=argparse.FileType('r', encoding='utf-8'), default=stdin,
                   help='Input file path')
    p.add_argument('-o', '--out', type=argparse.FileType('w', encoding='utf-8'), default=stdout,
                   help='Output file path')
    return p.parse_args()


if __name__ == '__main__':
    main()
