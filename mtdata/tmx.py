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
import time
from html import unescape
import datetime

DEF_PROGRESS = 10  # seconds

def parse_tmx(data, n_langs=2, log_every=DEF_PROGRESS):
    context = ET.iterparse(data, events=['end'])
    tus = (el for event, el in context if el.tag == 'tu')
    count, skips = 0, 0
    st = t = time.time()
    for tu in tus:
        langs, segs = [], []
        for tuv in tu.findall('tuv'):
            lang = [v for k, v in tuv.attrib.items() if k.endswith('lang')]
            if lang:
                langs.append(lang[0])
            seg = tuv.findtext('seg')
            if seg:
                segs.append(unescape(seg.strip()))
        if n_langs and len(segs) == len(langs) == n_langs:
            count += 1
            yield list(zip(langs, segs))
        else:
            skips += 1
            log.warning(f"Skipped: langs {langs} segs {len(segs)} ; Parsed count {count}")
        if log_every and (time.time() - t) > log_every:
            elapsed = datetime.timedelta(seconds=round(time.time() - st))
            log.info(f"{elapsed} :: Parsed: {count:,} Skipped:{skips:,}")
            t = time.time()
        tu.clear()
    log.info(f"Skipped ={skips}; parsed: {count}")

def read_tmx(path: Union[Path], langs=None):
    """
    reads a TMX file as records
    :param path: path to .tmx file
    :param langs: (lang1, lang2) codes eg (de, en); when it is None the code tries to auto detect
    :return: stream of (text1, text2)
    """
    with IO.reader(path) as data:
        recs = parse_tmx(data)
        for rec in recs:
            if langs is None:
                langs = [name for name, val in rec]
            (l1, t1), (l2, t2) = rec
            if l1 == langs[0] and l2 == langs[1]:
                yield t1, t2
            else:
                yield t2, t1

def main(inp, out):
    recs = read_tmx(inp)
    with IO.writer(out) as out:
        count = 0
        for rec in recs:
            rec = [l.replace('\t', ' ') for l in rec]
            out.write('\t'.join(rec) + '\n')
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
