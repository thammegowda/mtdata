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
    }
@inproceedings{banon-etal-2020-paracrawl,
    title = "{P}ara{C}rawl: Web-Scale Acquisition of Parallel Corpora",
    author = "Ba{\~n}{\'o}n, Marta  and
      Chen, Pinzhen  and
      Haddow, Barry  and
      Heafield, Kenneth  and
      Hoang, Hieu  and
      Espl{\`a}-Gomis, Miquel  and
      Forcada, Mikel L.  and
      Kamran, Amir  and
      Kirefu, Faheem  and
      Koehn, Philipp  and
      Ortiz Rojas, Sergio  and
      Pla Sempere, Leopoldo  and
      Ram{\'\i}rez-S{\'a}nchez, Gema  and
      Sarr{\'\i}as, Elsa  and
      Strelec, Marek  and
      Thompson, Brian  and
      Waites, William  and
      Wiggins, Dion  and
      Zaragoza, Jaume",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.417",
    doi = "10.18653/v1/2020.acl-main.417",
    pages = "4555--4567",
}    
    """
    for pair in ['en cs', 'en de', 'en fi', 'en lt']:
        l1, l2 = pair.split()
        index.add_entry(
            Entry(langs=(l1, l2), name='paracrawl_v3', url=PARACRAWL_v3 % (l1, l2), cite=cite))

    # === Paracrawl V6
    PARACRAWL_v6 = 'https://s3.amazonaws.com/web-language-models/paracrawl/release6/%s-%s.txt.gz'
    for l2 in ['is', 'bg', 'hr', 'cs', 'da', 'nl', 'et', 'fi', 'fr', 'de', 'el', 'hu', 'ga', 'it',
               'lv',
               'lt', 'mt', 'pl', 'pt', 'ro', 'sk', 'sl', 'es', 'sv']:
        l1 = 'en'
        index.add_entry(Entry(langs=(l1, l2), name='paracrawl_v6', url=PARACRAWL_v6 % (l1, l2),
                              cite=cite, ext='tsv.gz'))
    # these are bonus
    PARACRAWL_v6_B = 'https://s3.amazonaws.com/web-language-models/paracrawl/release6/%s-%s.bicleaner07.txt.gz'
    for l1, l2 in [('nl', 'fr'), ('pl', 'de')]:
        index.add_entry(Entry(langs=(l1, l2), name='paracrawl_v6', url=PARACRAWL_v6_B % (l1, l2),
                              cite=cite, ext='tsv.gz'))

    l1 = 'en'
    PARACRAWL_v7_1 = 'https://s3.amazonaws.com/web-language-models/paracrawl/release7.1/%s-%s.txt.gz'
    for l2 in 'bg cs da de el es et fi fr ga hr hu is it lt lv mt nl pl pt ro sk sl sv'.split():
        index.add_entry(Entry(langs=(l1, l2), name='paracrawl_v7_1', url=PARACRAWL_v7_1 % (l1, l2),
                              cite=cite, ext='tsv.gz'))
    PARACRAWL_v7_1 = 'https://s3.amazonaws.com/web-language-models/paracrawl/release7/%s-%s.txt.gz'
    for pair in 'en-nb en-nn es-ca es-eu es-gl'.split():
        l1, l2 = pair.split('-')
        index.add_entry(Entry(langs=(l1, l2), name='paracrawl_v7', url=PARACRAWL_v7_1 % (l1, l2),
                              cite=cite, ext='tsv.gz'))

    PARACRAWL_V8 = 'https://archive.org/download/ParaCrawl-{version}/{pair}.txt.gz'
    for version, pairs in [
        ('v8.0', 'en-bg en-cs en-da en-de en-el'),
        ('v8.0-0001','en-et en-fi en-fr en-ga en-hr en-hu en-is en-it en-lt en-lv en-mt en-nl en-no en-pl en-pt en-ro en-sk en-sl'),
        ('v8.0-0002', 'en-sv es-eu'),
        ('v8.1-0000', 'es-ca es-gl')]:
        for pair in pairs.split():
            l1, l2 = pair.split('-')
            url = PARACRAWL_V8.format(version=version, pair=pair)
            ent = Entry(langs=(l1, l2), name='paracrawl_v8', url=url, cite=cite, ext='tsv.gz')
            index.add_entry(ent)

    PARACRAWL_BONUS = 'https://s3.amazonaws.com/web-language-models/paracrawl/bonus/{pair}.txt.gz'
    for pair in 'en-km en-my en-ne en-ps en-si en-so en-sw en-tl en-ru en-ko'.split():
        l1, l2 = pair.split('-')
        url = PARACRAWL_BONUS.format(pair=pair)
        ent = Entry(langs=(l1, l2), name='paracrawl_bonus', url=url, cite=cite, ext='tsv.gz')
        index.add_entry(ent)
