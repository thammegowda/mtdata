#!/usr/bin/env python
#
# parses the min jsonline file from OPUS
# Author: Thamme Gowda [tg (at) isi (dot) edu]
# Created: 5/9/20; updated March 2022


from pathlib import Path
from mtdata import log
from mtdata.index import Index, Entry, DatasetId
from collections import defaultdict
from mtdata.iso.bcp47 import bcp47

data_file = Path(__file__).parent / 'opus_index.tsv'
""" To refresh the data_file from OPUS: 
$ curl "https://opus.nlpl.eu/opusapi/?preprocessing=moses" > opus_all.json 
$ cat opus_all.json |  jq -r  '.corpora[] | [.corpus, .version, .source, .target] | @tsv'  | sort  > opus_all.tsv 
"""


def load_all(index: Index):

    url_pat = 'https://object.pouta.csc.fi/OPUS-{corpus}/{version}/moses/{l1}-{l2}.txt.zip'
    group_id = 'OPUS'
    citation = index.ref_db.get_bibtex('tiedemann2012parallel')
    skip_counts = defaultdict(int)
    dupes = defaultdict(set)
    assert data_file.exists()
    assert data_file.stat().st_size > 0

    with data_file.open() as lines:
        for line in lines:
            line = line.strip()
            if not line:  # empty lines in the top and bottom
                continue
            assert len(line.split('\t')) == 4, line
            corpus, version, l1, l2 = line.split('\t')
            url = url_pat.format(corpus=corpus, version=version, l1=l1, l2=l2)
            iso_l1, iso_l2 = bcp47.try_parse(l1, default=None), bcp47.try_parse(l2, default=None)
            if not iso_l1 or not iso_l2:
                if not iso_l1:
                    skip_counts[str(l1)] += 1
                if not iso_l2:
                    skip_counts[str(l2)] += 1
                continue
            version_cln = version.replace('-', '').lower()
            corpus_cln = corpus.replace('-', '_').lower()

            data_id = DatasetId(group=group_id, name=corpus_cln, version=version_cln, langs=(iso_l1, iso_l2))
            if data_id in index:
                dupes[corpus].add(f'{l1}-{l2}')
                continue
            entry = Entry(did=data_id, url=url, cite=citation, in_paths=[f'*.{l1}', f'*.{l2}'], in_ext='txt')
            index.add_entry(entry)
        if skip_counts:
            skip_counts = list(sorted(dict(skip_counts).items(), key=lambda x: x[1], reverse=True))
            log.info(f"Skipped lang counts: {skip_counts}")
        if dupes:
            log.info(f"Duplicates langs: {dupes}")

