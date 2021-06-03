#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/5/20
from pathlib import Path
from xml.etree import ElementTree as ET
import argparse
from mtdata import log
from mtdata.utils import IO
from typing import Iterator
import re
from html import unescape


def clean(text):
    """
    unescape
    remove unnecessary white spaces
    replace \\n and \\t with regular space
    :param text:
    :return:
    """
    return ' '.join(unescape(text).split())


def read_sgm_xml(data: Path) -> Iterator[str]:
    """Extract sgm using XML parse
    This reader crashes if there is any error in XML e.g. an & is not escaped ;
      see newstest2019-frde-ref.de.sgm for example!
    """
    with IO.reader(data) as data:
        context = ET.iterparse(data, events=['end'])
        segs = (el for event, el in context if el.tag == 'seg')
        count = 0
        for seg in segs:
            yield clean(seg.text)
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
                yield clean(match.group(2))
                count += 1
    log.info(f"read {count} segments from {data}")

# alias
read_sgm = read_sgm_regex
#read_sgm = read_sgm_xml


def read_wmt21_xml(data):
    """
    This is a new XML format (instead of SGM) introduced in WMT2021
    :param data:
    :return:
    """
    tree = ET.parse(data)
    # 1. Assumes exactly one translation
    # 2. buffering in memory.  this can be improved with stream parsing
    def xpath_all(tree, xpath):
        return (clean(seg.text) for seg in tree.findall(xpath))

    srcs = list(xpath_all(tree.getroot(), xpath=".//src//seg"))
    tgts = list(xpath_all(tree.getroot(), xpath=".//ref//seg"))
    assert len(srcs) == len(tgts), f'{data} has unequal number of segs: {len(srcs)} == {len(tgts)}?'
    yield from zip(srcs, tgts)
    log.info(f"Read {len(srcs)} segs from {data}")

def main(inp, out, wmt21xml=False):
    parser = read_wmt21_xml if wmt21xml else read_sgm
    stream = parser(inp)
    with IO.writer(out) as out:
        count = 0
        for rec in stream:
            if isinstance(rec, str):
                rec = (rec,)
            line = '\t'.join(rec) + '\n'
            out.write(line)
            count += 1
        log.info(f"Wrote {count} lines to {out}")


if __name__ == '__main__':
    import sys
    p = argparse.ArgumentParser(description='A tool to convert TMX to TSV',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('-i', '--inp', type=Path, required=True, help='Input file path')
    p.add_argument('-o', '--out', type=Path, default=sys.stdout, help='Output file path')
    p.add_argument('--wmt21xml', action='store_true', help='Input is wmt21 XML format')
    args = vars(p.parse_args())
    main(**args)
