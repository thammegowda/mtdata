#!/usr/bin/env python
# Corpora from the EU https://ec.europa.eu/jrc/en/language-technologies
# Author: Kenneth Heafield [mtdata (at) kheafield (dot) com] 
# Created: 5/23/21

from mtdata.index import Index, Entry

def load_all(index: Index):
    # === ECDC ===
    # https://ec.europa.eu/jrc/en/language-technologies/ecdc-translation-memory
    cite="""@article{Steinberger2014,
    title={An overview of the European Union's highly multilingual parallel corpora},
    journal={Language Resources and Evaluation},
    author={Steinberger, Ralf and Ebrahim, Mohamed and Poulis, Alexandros and Carrasco-Benitez, Manuel and Schlüter, Patrick and Przybyszewski, Marek and Gilbro, Signe},
    year={2014},
    doi={10.1007/s10579-014-9277-0},
    url={https://ec.europa.eu/jrc/sites/jrcsh/files/2014_08_LRE-Journal_JRC-Linguistic-Resources_Manuscript.pdf},
    pages={679--707},
}"""
    langs = ["en", "bg", "cs", "da", "de", "el", "es", "et", "fi", "fr", "ga", "hu", "is", "it", "lt", "lv", "mt", "nl", "no", "pl", "pt", "ro", "sk", "sl", "sv"]
    for i, l1 in enumerate(langs):
        for l2 in langs[i+1:]:
            ent = Entry(langs=(l1, l2), url="http://optima.jrc.it/Resources/ECDC-TM/ECDC-TM.zip", name="ECDC", in_ext='tmx', cite=cite, in_paths=["ECDC-TM/ECDC.tmx"])
            index.add_entry(ent)

    # === EAC ===
    # https://ec.europa.eu/jrc/en/language-technologies/eac-translation-memory
    # This corpus has two 
    langs = ["bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr", "hu", "is", "it", "lt", "lv", "mt", "nb", "nl", "pl", "pt", "ro", "sk", "sl", "sv", "tr"]
    for i, l1 in enumerate(langs):
        for l2 in langs[i+1:]:
            ent = Entry(langs=(l1, l2), url="https://wt-public.emm4u.eu/Resources/EAC-TM/EAC-TM-all.zip", name="EAC_Forms", in_ext='tmx', cite=cite, in_paths=["EAC_FORMS.tmx"])
            index.add_entry(ent)
    langs = ["bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr", "hr", "hu", "is", "it", "lt", "lv", "mt", "nl", "no", "pl", "pt", "ro", "sk", "sl", "sv", "tr"]
    for i, l1 in enumerate(langs):
        for l2 in langs[i+1:]:
            ent = Entry(langs=(l1, l2), url="https://wt-public.emm4u.eu/Resources/EAC-TM/EAC-TM-all.zip", name="EAC_Reference", in_ext='tmx', cite=cite, in_paths=["EAC_REFRENCE_DATA.tmx"])
            index.add_entry(ent)

    # Note: DGT-TM is already in via OPUS.
