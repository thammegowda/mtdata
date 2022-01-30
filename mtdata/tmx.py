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
from mtdata.iso.bcp47 import bcp47, BCP47Tag
from mtdata.main import lang_pair
from html import unescape
import datetime

DEF_PROGRESS = 10  # seconds


def parse_tmx(data, log_every=DEF_PROGRESS):
    context = ET.iterparse(data, events=['end'])
    tus = (el for event, el in context if el.tag == 'tu')
    count = 0
    st = t = time.time()
    for tu in tus:
        lang_seg = {}
        for tuv in tu.findall('tuv'):
            lang = [v for k, v in tuv.attrib.items() if k.endswith('lang')]
            seg = tuv.findtext('seg')
            if lang and seg:
                lang = bcp47(lang[0])
                seg = unescape(seg.strip()).replace('\n', ' ').replace('\t', ' ')
                if lang in lang_seg:
                    log.warning(f"Language {lang} appears twice in same translation unit.")
                lang_seg[lang] = seg
        yield lang_seg
        count += 1
        if log_every and (time.time() - t) > log_every:
            elapsed = datetime.timedelta(seconds=round(time.time() - st))
            log.info(f"{elapsed} :: Parsed: {count:,}")
            t = time.time()
        tu.clear()


def read_tmx(path: Union[Path, str], langs=None):
    """
    reads a TMX file as records
    :param path: path to .tmx file
    :param langs: (lang1, lang2) codes eg (de, en); when it is None the code tries to auto detect
    :return: stream of (text1, text2)
    """
    passes = 0
    fails = 0
    if langs:
        assert len(langs) == 2
        langs = [bcp47(lang) for lang in langs]
        assert not BCP47Tag.are_compatible(*langs), f'{langs} expected to be different (/unambiguous)'
    with IO.reader(path) as data:
        recs = parse_tmx(data)
        for lang_seg in recs:
            if langs is None:
                log.warning("langs not set; this could result in language mismatch")
                if len(lang_seg) == 2:
                    langs = tuple(lang_seg.keys())
                else:
                    raise Exception(f"Language autodetect for TMX only supports 2 languages,"
                                    f" but provided with {lang_seg.keys()} in TMX {path}")
            seg1, seg2 = None, None
            for lang, seg in lang_seg.items():
                if BCP47Tag.are_compatible(langs[0], lang):
                    seg1 = seg
                elif BCP47Tag.are_compatible(langs[1], lang):
                    seg2 = seg
                # else ignore
            if seg1 and seg2:  # both segs are found
                yield seg1, seg2
                passes += 1
            else:
                fails += 1
    if passes == 0:
        if fails == 0:
            raise Exception(f"Empty TMX {path}")
        raise Exception(f"Nothing for {langs[0]}-{langs[1]} in TMX {path}")
    if fails != 0:
        log.warning(f"Skipped {fails} entries due to language mismatch in TMX {path}")
    log.info(f"Extracted {passes} pairs from TMX {path}")


def main(inp, out, langs):
    recs = read_tmx(inp, langs=langs)
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
    p.add_argument('-l', '--langs', type=lang_pair, default=None,
                   help='Languages from TMX. example: eng-fra or en-fr')

    args = vars(p.parse_args())
    main(**args)
