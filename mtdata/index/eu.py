#!/usr/bin/env python
# Corpora from the EU https://ec.europa.eu/jrc/en/language-technologies
# Author: Kenneth Heafield [mtdata (at) kheafield (dot) com] 
# Created: 5/23/21

from mtdata.index import Index, Entry, DatasetId


def load_all(index: Index):
    group = 'europa'
    # === ECDC ===
    # https://ec.europa.eu/jrc/en/language-technologies/ecdc-translation-memory
    cite = index.ref_db.get_bibtex('Steinberger2014')
    langs = 'en bg cs da de el es et fi fr ga hu is it lt lv mt nl no pl pt ro sk sl sv'.split()
    for i, l1 in enumerate(langs):
        for l2 in langs[i+1:]:
            ent = Entry(did=DatasetId(group='EU', name=f'ecdc', version='1', langs=(l1, l2)),
                        url="http://optima.jrc.it/Resources/ECDC-TM/ECDC-TM.zip",
                        in_ext='tmx', cite=cite, in_paths=["ECDC-TM/ECDC.tmx"])
            index.add_entry(ent)

    # === EAC ===
    # https://ec.europa.eu/jrc/en/language-technologies/eac-translation-memory
    # This corpus has two 
    langs = 'bg cs da de el en es et fi fr hu is it lt lv mt nb nl pl pt ro sk sl sv tr'.split()
    for i, l1 in enumerate(langs):
        for l2 in langs[i+1:]:
            ent = Entry(did=DatasetId(group='EU', name=f'eac_forms', version='1', langs=(l1, l2)),
                        url="https://wt-public.emm4u.eu/Resources/EAC-TM/EAC-TM-all.zip",
                        in_ext='tmx', cite=cite, in_paths=["EAC_FORMS.tmx"])
            index.add_entry(ent)
    langs = 'bg cs da de el en es et fi fr hr hu is it lt lv mt nl no pl pt ro sk sl sv tr'.split()
    for i, l1 in enumerate(langs):
        for l2 in langs[i+1:]:
            ent = Entry(did=DatasetId(group='EU', name=f'eac_reference', version='1', langs=(l1, l2)),
                        url="https://wt-public.emm4u.eu/Resources/EAC-TM/EAC-TM-all.zip",
                        in_ext='tmx', cite=cite, in_paths=["EAC_REFRENCE_DATA.tmx"])
            index.add_entry(ent)

    # === DCEP ===
    # https://ec.europa.eu/jrc/en/language-technologies/dcep
    # This was annoying to process so I ended up rehosting it.
    # Don't bother with TR; it doesn't have sentences anyway.
    cite = index.ref_db.get_bibtex('dcep')
    langs = 'BG CS DA DE EL EN ES ET FI FR GA HU IT LT LV MT NL PL PT RO SK SL SV'.split()
    for i, l1 in enumerate(langs):
        for l2 in langs[i+1:]:
            ent = Entry(did=DatasetId(group='EU', name=f'dcep', version='1', langs=(l1, l2)),
                url=f"http://data.statmt.org/DCEP/{l1}-{l2}.tsv.xz", in_ext='tsv', cite=cite)
            index.add_entry(ent)

    # Note: DGT-TM is already in via OPUS.
