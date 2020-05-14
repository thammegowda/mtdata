#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/5/20
from typing import Union
from pathlib import Path
from xml.etree import ElementTree as ET
import argparse
from mtdata import log
from mtdata.utils import IO
from typing import Iterator
import re
from html import unescape

def read_sgm_xml(data: Path) -> Iterator[str]:
    """Extract sgm using XML parse
    This one breaks if there is any error in XML e.g. an & is not escaped ;
      see newstest2019-frde-ref.de.sgm for example!
    """
    with IO.reader(data) as data:
        context = ET.iterparse(data, events=['end'])
        segs = (el for event, el in context if el.tag == 'seg')
        count = 0
        for seg in segs:
            yield seg.text
            seg.clear()
            count += 1
        log.info(f"read {count} segments from {data}")

def read_sgm_regex(data: Path) -> Iterator[str]:
    """
    Extract sgm using regex.
    assumes each sgm is in its own line of form <seg id="xx"> yy</sgm>
    and line breaks are used between
    :param data:
    :return:
    """
    patt = re.compile(r'<seg id="(.*)">(.*)</seg>')
    count = 0
    with IO.reader(data) as data:
        for line in data:
            line = line.strip()
            match = patt.search(line)
            if match:
                yield unescape(match.group(2))
                count += 1
    log.info(f"read {count} segments from {data}")

# alias
read_sgm = read_sgm_regex

def main(inp, out):
    segs = read_sgm(inp)
    with IO.writer(out) as out:
        count = 0
        for seg in segs:
            seg = seg.replace('\t', ' ')
            out.write(seg + '\n')
            count += 1
        log.warning(f"Wrote {count} lines to {out}")


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='A tool to convert TMX to TSV',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('-i', '--inp', type=Path, required=True, help='Input file path')
    p.add_argument('-o', '--out', type=Path, default=Path('/dev/stdout'),
                   help='Output file path')
    args = vars(p.parse_args())
    main(**args)
