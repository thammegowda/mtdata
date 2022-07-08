#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20

from mtdata.index import Entry, Index, DatasetId


def load(index: Index):
    URL_PREFIX = 'https://s3.amazonaws.com/web-language-models/paracrawl'
    cite = index.ref_db.get_bibtex('espla-etal-2019-paracrawl')
    cite += '\n' + index.ref_db.get_bibtex('banon-etal-2020-paracrawl')
    group_id = 'ParaCrawl'
    # === Para crawl corpus
    PARACRAWL_v3 = f'{URL_PREFIX}/release3/%s-%s.bicleaner07.tmx.gz'
    for pair in ['en cs', 'en de', 'en fi', 'en lt']:
        l1, l2 = pair.split()
        index.add_entry(Entry(did=DatasetId(group=group_id, name=f'paracrawl', version='3', langs=(l1, l2)),
                              url=PARACRAWL_v3 % (l1, l2), cite=cite))

    # === Paracrawl V6
    PARACRAWL_v6 = f'{URL_PREFIX}/release6/%s-%s.txt.gz'
    for l2 in ['is', 'bg', 'hr', 'cs', 'da', 'nl', 'et', 'fi', 'fr', 'de', 'el', 'hu', 'ga', 'it', 'lv',
               'lt', 'mt', 'pl', 'pt', 'ro', 'sk', 'sl', 'es', 'sv']:
        l1 = 'en'
        index.add_entry(Entry(did=DatasetId(group=group_id, name=f'paracrawl', version='6', langs=(l1, l2)),
                              url=PARACRAWL_v6 % (l1, l2), cite=cite, ext='tsv.gz'))
    # these are bonus
    PARACRAWL_v6_B = f'{URL_PREFIX}/release6/%s-%s.bicleaner07.txt.gz'
    for l1, l2 in [('nl', 'fr'), ('pl', 'de')]:
        index.add_entry(Entry(did=DatasetId(group=group_id, name=f'paracrawl', version='6B', langs=(l1, l2)),
                              url=PARACRAWL_v6_B % (l1, l2), cite=cite, ext='tsv.gz'))

    l1 = 'en'
    PARACRAWL_v7_1 = f'{URL_PREFIX}/release7.1/%s-%s.txt.gz'
    for l2 in 'bg cs da de el es et fi fr ga hr hu is it lt lv mt nl pl pt ro sk sl sv'.split():
        index.add_entry(Entry(did=DatasetId(group=group_id, name=f'paracrawl', version='7.1', langs=(l1, l2)),
                              url=PARACRAWL_v7_1 % (l1, l2), cite=cite, ext='tsv.gz'))
    PARACRAWL_v7_1 = f'{URL_PREFIX}/release7/%s-%s.txt.gz'
    for pair in 'en-nb en-nn es-ca es-eu es-gl'.split():
        l1, l2 = pair.split('-')
        index.add_entry(Entry(did=DatasetId(group=group_id, name=f'paracrawl', version='7.1', langs=(l1, l2)),
                              url=PARACRAWL_v7_1 % (l1, l2), cite=cite, ext='tsv.gz'))

    PARACRAWL_V8 = 'https://archive.org/download/ParaCrawl-{version}/{pair}.txt.gz'
    for version, pairs in [
        ('v8.0', 'en-bg en-cs en-da en-de en-el'),
        ('v8.0-0001',
         'en-et en-fi en-fr en-ga en-hr en-hu en-is en-it en-lt en-lv en-mt en-nl en-no en-pl en-pt en-ro en-sk en-sl'),
        ('v8.0-0002', 'en-sv es-eu'),
        ('v8.1-0000', 'es-ca es-gl')]:
        for pair in pairs.split():
            l1, l2 = pair.split('-')
            url = PARACRAWL_V8.format(version=version, pair=pair)
            ent = Entry(did=DatasetId(group=group_id, name=f'paracrawl', version='8', langs=(l1, l2)),
                        url=url, cite=cite, ext='tsv.gz')
            index.add_entry(ent)

    PARACRAWL_BONUS = URL_PREFIX + '/bonus/{pair}.txt.gz'
    for pair in 'en-km en-my en-ne en-ps en-si en-so en-sw en-tl en-ru en-ko'.split():
        l1, l2 = pair.split('-')
        url = PARACRAWL_BONUS.format(pair=pair)
        ent = Entry(did=DatasetId(group=group_id, name=f'paracrawl', version='1_bonus', langs=(l1, l2)),
                    url=url, cite=cite, ext='tsv.gz')
        index.add_entry(ent)

    PARACRAWL_V9 = URL_PREFIX + '/release9/{l1}-{l2}/{l1}-{l2}.txt.gz'
    for pair in ('en-bg en-cs en-da en-de en-el en-es en-et en-fi en-fr en-ga en-hr en-hu en-is en-it en-lt en-lv'
                 ' en-mt en-nb en-nl en-nn en-pl en-pt en-ro en-sk en-sl en-sv es-ca es-eu es-gl').split():
        l1, l2 = pair.split('-')
        url = PARACRAWL_V9.format(l1=l1, l2=l2)
        ent = Entry(did=DatasetId(group=group_id, name=f'paracrawl', version='9', langs=(l1, l2)),
                    url=url, cite=cite, ext='tsv.gz')
        index.add_entry(ent)
    # this is a new addition in Sept 2021
    index.add_entry(Entry(
        did=DatasetId(group=group_id, name=f'paracrawl', version='1_bonus', langs=('en', 'zh')),
        url=f'{URL_PREFIX}/bonus/en-zh-v1.txt.gz',
        cite=cite, ext='tsv.gz'))

    index.add_entry(Entry(
        did=DatasetId(group=group_id, name=f'paracrawl', version='1_bonus', langs=('en', 'uk')),
        url=f'{URL_PREFIX}/bonus/en-uk-v1.txt.gz',
        cite=cite, ext='tsv.gz'))

    # Japanese-English paracrawl (5.1) used by WMT20 and WMT21
    for version, cols in [('2', (2, 3)), ('3', (3, 4))]:
        ent = Entry(did=DatasetId(group='KECL', name=f'paracrawl', version=version, langs=('eng', 'jpn')),
                    in_paths=['en-ja/en-ja.bicleaner05.txt'], in_ext='tsv', cols=cols, cite='',
                    url=f'http://www.kecl.ntt.co.jp/icl/lirg/jparacrawl/release/{version}.0/bitext/en-ja.tar.gz')
        index.add_entry(ent)
