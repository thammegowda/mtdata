#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20

from mtdata.index import Entry, Index

def load(index: Index):
    # === Para crawl corpus
    PARACRAWL_v3 = 'https://s3.amazonaws.com/web-language-models/paracrawl/release3/%s-%s.bicleaner07.tmx.gz'
    cite = r"""@inproceedings{espla-etal-2019-paracrawl,
        title = "{P}ara{C}rawl: Web-scale parallel corpora for the languages of the {EU}",
        author = "Espl{\`a}, Miquel  and
          Forcada, Mikel  and
          Ram{\'\i}rez-S{\'a}nchez, Gema  and
          Hoang, Hieu",
        booktitle = "Proceedings of Machine Translation Summit XVII Volume 2: Translator, Project and User Tracks",
        month = aug,
        year = "2019",
        address = "Dublin, Ireland",
        publisher = "European Association for Machine Translation",
        url = "https://www.aclweb.org/anthology/W19-6721",
        pages = "118--119",
    }"""
    for pair in ['en cs', 'en de', 'en fi', 'en lt']:
        l1, l2 = pair.split()
        index.add_entry(
            Entry(langs=(l1, l2), name='paracrawl_v3', url=PARACRAWL_v3 % (l1, l2), cite=cite))

    # === Paracrawl V6
    PARACRAWL_v6 = 'https://s3.amazonaws.com/web-language-models/paracrawl/release6/%s-%s.txt.gz'
    for l2 in ['is', 'bg', 'hr', 'cs', 'da', 'nl', 'et', 'fi', 'fr', 'de', 'el', 'hu', 'ga', 'it', 'lv',
               'lt', 'mt', 'pl', 'pt', 'ro', 'sk', 'sl', 'es', 'sv']:
        l1 = 'en'
        index.add_entry(Entry(langs=(l1, l2), name='paracrawl_v6', url=PARACRAWL_v6 % (l1, l2),
                             cite=cite, ext='tsv.gz'))
    # these are bonus
    PARACRAWL_v6_B = 'https://s3.amazonaws.com/web-language-models/paracrawl/release6/%s-%s.bicleaner07.txt.gz'
    for l1, l2 in [('nl', 'fr'), ('pl', 'de')]:
        index.add_entry(Entry(langs=(l1, l2), name='paracrawl_v6', url=PARACRAWL_v6_B % (l1, l2),
                             cite=cite, ext='tsv.gz'))
