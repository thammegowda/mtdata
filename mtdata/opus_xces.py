#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/13/20
from pathlib import Path
from mtdata.utils import IO, log
from xml.etree import ElementTree as ET
import collections as coll
import re


class OpusXcesParser:

    @classmethod
    def read_alignments(cls, align_file: Path):
        assert align_file.is_file(), f'{align_file} not found'
        with IO.reader(align_file) as reader:
            context = ET.iterparse(reader, events=['end'])
            docs = (el for event, el in context if el.tag == 'linkGrp')
            count = 0
            skip_count = 0
            for doc in docs:
                algn = []
                doc_parse = {'src_doc': doc.attrib['fromDoc'], 'tgt_doc': doc.attrib['toDoc'],
                             'align': algn}
                for seg in doc.findall('.//link'):
                    parts = seg.attrib.get('xtargets', ';').strip().split(';')
                    if len(parts) != 2:
                        skip_count += 1
                        continue
                    src_ids, tgt_ids = parts
                    src_ids, tgt_ids = src_ids.split(), tgt_ids.split()
                    confidence = float(seg.attrib.get('certainty', '-inf'))
                    algn.append((confidence, src_ids, tgt_ids))
                yield doc_parse
                doc.clear()
                count += 1
            log.info(f"read {count} docs from {align_file}")

    @classmethod
    def read_doc(cls, data):
        mem = {}
        context = ET.iterparse(data, events=['end'])
        segs = (el for event, el in context if el.tag == 's')
        for seg in segs:
            seg_id = seg.attrib['id']
            mem[seg_id] = ' '.join(w.text for w in seg.findall('.//w'))
        return mem

    @classmethod
    def read(cls, align_file: Path, l1_dir: Path, l2_dir: Path, name='JW300', min_confidence=0.01):
        doc_aligns = cls.read_alignments(align_file)
        assert l1_dir.is_file() and l1_dir.suffix == '.zip', f'{l1_dir}'
        assert l2_dir.is_file() and l2_dir.suffix == '.zip', f'{l2_dir}'
        from zipfile import ZipFile
        stats = coll.defaultdict(int)

        with ZipFile(l1_dir) as l1_zip, ZipFile(l2_dir) as l2_zip:
            l1_doc_names = set(l1_zip.namelist())
            l2_doc_names = set(l2_zip.namelist())
            for d in doc_aligns:
                src_doc_path = f'{name}/xml/' + re.sub(r'\.gz$', '', d['src_doc'])
                tgt_doc_path = f'{name}/xml/' + re.sub(r'\.gz$', '', d['tgt_doc'])
                if src_doc_path not in l1_doc_names or tgt_doc_path not in l2_doc_names:
                    stats['doc_not_found'] += 1
                    continue
                with l1_zip.open(src_doc_path) as f1:
                    src_doc = cls.read_doc(f1)
                with l2_zip.open(tgt_doc_path) as f2:
                    tgt_doc = cls.read_doc(f2)

                for confidence, src_ids, tgt_ids in d['align']:
                    if not src_ids or not tgt_ids:
                        stats['missing_seg_skips'] += 1
                        continue
                    if confidence < min_confidence:
                        stats['low_conf_skips'] += 1
                        continue

                    src_segs = [src_doc.get(id, None) for id in src_ids]
                    tgt_segs = [tgt_doc.get(id, None) for id in tgt_ids]
                    if not all(src_segs) or not all(tgt_segs):
                        stats['error_seg_skips'] += 1
                        continue
                    src_seg = ' '.join(src_segs)
                    tgt_seg = ' '.join(tgt_segs)
                    yield src_seg, tgt_seg
                    stats['success'] += 1
        stats = dict(stats)
        log.info(f"Read aligned segments from {l1_dir}, {l2_dir} {stats}")
