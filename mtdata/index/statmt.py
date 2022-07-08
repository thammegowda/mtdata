#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20
from mtdata.index import Entry, Index, DatasetId, bcp47
import itertools


def load(index: Index):
    group_id = 'Statmt'
    WMT13_CCRAWL = "http://www.statmt.org/wmt13/training-parallel-commoncrawl.tgz"
    WMT14_CITE = index.ref_db.get_bibtex('ws-2014-statistical')
    for l1 in ['de', 'cs', 'fr', 'ru', 'es']:
        l2 = 'en'
        f1 = f'commoncrawl.{l1}-en.{l1}'
        f2 = f'commoncrawl.{l1}-en.en'
        data_id = DatasetId(group=group_id, name='commoncrawl_wmt13', version='1', langs=(l1, l2))
        index.add_entry(Entry(did=data_id, url=WMT13_CCRAWL,
                              filename='wmt13_parallel_commoncrawl.tgz',
                              in_paths=[f1, f2], in_ext='txt', cite=WMT14_CITE))

    # === WMT 13 release of europarl_v7 ===
    for l1 in ['cs', 'de', 'fr', 'es']:
        l2 = 'en'
        f1 = f'training/europarl-v7.{l1}-{l2}.{l1}'
        f2 = f'training/europarl-v7.{l1}-{l2}.{l2}'
        data_id = DatasetId(group=group_id, name='europarl_wmt13', version='7', langs=(l1, l2))
        index.add_entry(Entry(did=data_id, url="http://www.statmt.org/wmt13/training-parallel-europarl-v7.tgz",
                              filename="wmt13_europarl_v7.tgz",
                              in_paths=[f1, f2], in_ext='txt', cite=WMT14_CITE))

    # ==== WMT 18  news commentary v13 ===
    for l1 in ['cs', 'de', 'ru', 'zh']:
        l2 = 'en'
        f1 = f'training-parallel-nc-v13/news-commentary-v13.{l1}-{l2}.{l1}'
        f2 = f'training-parallel-nc-v13/news-commentary-v13.{l1}-{l2}.{l2}'
        data_id = DatasetId(group=group_id, name='news_commentary_wmt18', version='13', langs=(l1, l2))
        index.add_entry(Entry(did=data_id,
                              url="http://data.statmt.org/wmt18/translation-task/training-parallel-nc-v13.tgz",
                              filename="wmt18_news_commentary_v13.tgz",
                              in_paths=[f1, f2], in_ext='txt', cite=WMT14_CITE))

    # === Europarl V9 corpus
    EUROPARL_v9 = 'http://www.statmt.org/europarl/v9/training/europarl-v9.%s-%s.tsv.gz'
    cite = index.ref_db.get_bibtex('koehn2005europarl')
    for pair in ['de en', 'cs en', 'cs pl', 'es pt', 'fi en', 'lt en']:
        l1, l2 = pair.split()
        index.add_entry(Entry(did=DatasetId(group=group_id, name='europarl', version='9', langs=(l1, l2)),
                              url=EUROPARL_v9 % (l1, l2), cite=cite))

    # === Europarl V7 corpus
    EUROPARL_v7 = 'http://www.statmt.org/europarl/v7/%s-%s.tgz'
    cite = index.ref_db.get_bibtex('bojar-etal-2017-findings')
    for l1 in 'bg cs da de el es et fi fr hu it lt lv nl pl pt ro sk sl sv'.split():
        l2 = 'en'
        src = f'europarl-v7.{l1}-{l2}.{l1}'
        ref = f'europarl-v7.{l1}-{l2}.{l2}'
        index.add_entry(Entry(
            did=DatasetId(group=group_id, name='europarl', version='7', langs=(l1, l2)), in_paths=[src, ref],
                              url=EUROPARL_v7 % (l1, l2), in_ext='txt', cite=cite))

    # === Digital Corpus of European Parliament
    index.add_entry(Entry(did=DatasetId(group=group_id, name='dcep_wmt17', version='1', langs=(l1, l2)),
                          in_paths=['*/*.lv', f'*/*.en'], cite=cite, in_ext='txt',
                          url='http://data.statmt.org/wmt17/translation-task/dcep.lv-en.v1.tgz'))
    index.add_entry(Entry(did=DatasetId(group=group_id, name='books_wmt17', version='1', langs=(l1, l2)),
                          in_paths=['*/*.lv', f'*/*.en'], cite=cite, in_ext='txt',
                          url='http://data.statmt.org/wmt17/translation-task/books.lv-en.v1.tgz'))

    # === News Commentary v14
    NEWSCOM_v14 = "http://data.statmt.org/news-commentary/v14/training/news-commentary-v14.%s-%s.tsv.gz"
    cite = index.ref_db.get_bibtex('bojar-etal-2018-findings')
    for pair in ['ar cs', 'ar de', 'ar en', 'ar es', 'ar fr', 'ar hi', 'ar id', 'ar it',
                 'ar ja', 'ar kk', 'ar nl', 'ar pt', 'ar ru', 'ar zh', 'cs de', 'cs en', 'cs es',
                 'cs fr', 'cs hi', 'cs id', 'cs it', 'cs ja', 'cs kk', 'cs nl', 'cs pt', 'cs ru',
                 'cs zh', 'de en', 'de es', 'de fr', 'de hi', 'de id', 'de it', 'de ja', 'de kk',
                 'de nl', 'de pt', 'de ru', 'de zh', 'en es', 'en fr', 'en hi', 'en id', 'en it',
                 'en ja', 'en kk', 'en nl', 'en pt', 'en ru', 'en zh', 'es fr', 'es hi', 'es id',
                 'es it', 'es ja', 'es kk', 'es nl', 'es pt', 'es ru', 'es zh', 'fr hi', 'fr id',
                 'fr it', 'fr ja', 'fr kk', 'fr nl', 'fr pt', 'fr ru', 'fr zh', 'hi id', 'hi it',
                 'hi nl', 'hi pt', 'hi ru', 'hi zh', 'id it', 'id kk', 'id nl', 'id pt', 'id ru',
                 'id zh', 'it kk', 'it nl', 'it pt', 'it ru', 'it zh', 'ja ru', 'ja zh', 'kk nl',
                 'kk pt', 'kk ru', 'kk zh', 'nl pt', 'nl ru', 'nl zh', 'pt ru', 'pt zh', 'ru zh']:
        l1, l2 = pair.split()
        index.add_entry(Entry(
            did=DatasetId(group=group_id, name='news_commentary', version='14', langs=(l1, l2)),
            url=NEWSCOM_v14 % (l1, l2), cite=cite))

    for v in [15, 16]:
        cite = index.ref_db.get_bibtex('barrault-etal-2020-findings')
        url = f"http://data.statmt.org/news-commentary/v{v}/training/news-commentary-v{v}.%s-%s.tsv.gz"
        for pair in ['ar cs', 'ar de', 'ar en', 'ar es', 'ar fr', 'ar hi', 'ar id', 'ar it', 'ar ja', 'ar kk', 'ar nl',
                     'ar pt', 'ar ru', 'ar zh', 'cs de', 'cs en', 'cs es', 'cs fr', 'cs hi', 'cs id', 'cs it', 'cs ja',
                     'cs kk', 'cs nl', 'cs pt', 'cs ru', 'cs zh', 'de en', 'de es', 'de fr', 'de hi', 'de id', 'de it',
                     'de ja', 'de kk', 'de nl', 'de pt', 'de ru', 'de zh', 'en es', 'en fr', 'en hi', 'en id', 'en it',
                     'en ja', 'en kk', 'en nl', 'en pt', 'en ru', 'en zh', 'es fr', 'es hi', 'es id', 'es it', 'es ja',
                     'es kk', 'es nl', 'es pt', 'es ru', 'es zh', 'fr hi', 'fr id', 'fr it', 'fr ja', 'fr kk', 'fr nl',
                     'fr pt', 'fr ru', 'fr zh', 'hi id', 'hi it', 'hi nl', 'hi pt', 'hi ru', 'hi zh', 'id it', 'id ja',
                     'id kk', 'id nl', 'id pt', 'id ru', 'id zh', 'it kk', 'it nl', 'it pt', 'it ru', 'it zh', 'ja pt',
                     'ja ru', 'ja zh', 'kk nl', 'kk pt', 'kk ru', 'kk zh', 'nl pt', 'nl ru', 'nl zh', 'pt ru', 'pt zh',
                     'ru zh']:
            l1, l2 = pair.split()
            index.add_entry(Entry(did=DatasetId(group=group_id, name='news_commentary', version=f'{v}', langs=(l1, l2)),
                url=url % (l1, l2), cite=cite))


    # ===== Wiki Titles V1
    WIKI_TITLES_v1 = 'http://data.statmt.org/wikititles/v1/wikititles-v1.%s-%s.tsv.gz'
    cite = index.ref_db.get_bibtex('barrault-etal-2019-findings')
    for pair in ['cs en', 'cs pl', 'de en', 'es pt', 'fi en', 'gu en', 'hi ne', 'kk en', 'lt en',
                 'ru en', 'zh en']:
        l1, l2 = pair.split()
        index.add_entry(Entry(did=DatasetId(group=group_id, name='wiki_titles', version='1', langs=(l1, l2)),
                              url=WIKI_TITLES_v1 % (l1, l2), cite=cite))

    # ===== Wiki Titles V2
    WIKI_TITLES_v2 = 'http://data.statmt.org/wikititles/v2/wikititles-v2.%s-%s.tsv.gz'
    for pair in ['ca es', 'cs en', 'de en', 'de fr', 'es pt', 'iu en', 'ja en', 'pl en', 'ps en',
                 'ru en', 'ta en', 'zh en']:
        l1, l2 = pair.split()
        index.add_entry(Entry(did=DatasetId(group=group_id, name='wiki_titles', version='2', langs=(l1, l2)),
                              url=WIKI_TITLES_v2 % (l1, l2), cite=cite))

    WIKI_TITLES_v3 = 'http://data.statmt.org/wikititles/v3/wikititles-v3.{pair}.tsv'
    langs = 'bn-hi ca-es ca-pt ca-ro cs-en de-en de-fr es-pt es-ro ha-en ig-en is-en ja-en ps-en pt-ro ru-en xh-zu zh-en'
    for pair in langs.split():
        l1, l2 = pair.split('-')
        url = WIKI_TITLES_v3.format(pair=pair)
        ent = Entry(did=DatasetId(group=group_id, name=f'wikititles', version='3', langs=(l1, l2)), url=url, cite=cite)
        index.add_entry(ent)

    # ==== WMT  Dev and Tests
    wmt_sets = {
        'newstest2014': [('de', 'en'), ('cs', 'en'), ('fr', 'en'), ('ru', 'en'), ('hi', 'en')],
        'newsdev2015': [('fi', 'en'), ('en', 'fi')],
        'newstest2015': [('fi', 'en'), ('en', 'cs'), ('cs', 'en'), ('en', 'ru'), ('en', 'de'),
                         ('de', 'en'), ('ru', 'en'), ('en', 'fi')],
        'newsdev2016': [('en', 'ro'), ('ro', 'en'), ('tr', 'en'), ('en', 'tr')],
        'newstest2016': [('de', 'en'), ('en', 'de'), ('en', 'ro'), ('en', 'fi'), ('ro', 'en'),
                         ('ru', 'en'), ('fi', 'en'), ('en', 'ru'), ('tr', 'en'), ('cs', 'en'),
                         ('en', 'tr'), ('en', 'cs')],
        'newsdev2017': [('zh', 'en'), ('lv', 'en'), ('en', 'zh'), ('en', 'lv')],
        'newstest2017': [('zh', 'en'), ('ru', 'en'), ('en', 'fi'), ('lv', 'en'), ('en', 'de'),
                         ('de', 'en'), ('cs', 'en'), ('en', 'cs'), ('en', 'tr'), ('en', 'ru'),
                         ('tr', 'en'), ('fi', 'en'), ('en', 'zh'), ('en', 'lv')],
        'newsdev2018': [('et', 'en'), ('en', 'et')],
        'newstest2018': [('ru', 'en'), ('zh', 'en'), ('et', 'en'), ('en', 'fi'), ('en', 'de'),
                         ('de', 'en'), ('en', 'cs'), ('en', 'tr'), ('cs', 'en'), ('tr', 'en'),
                         ('en', 'ru'), ('en', 'et'), ('fi', 'en'), ('en', 'zh')],
        'newsdev2019': [('gu', 'en'), ('kk', 'en'), ('en', 'lt'), ('en', 'kk'), ('lt', 'en'),
                        ('en', 'gu')],
        'newstest2019': [('de', 'en'), ('de', 'fr'), ('kk', 'en'), ('en', 'de'), ('en', 'fi'),
                         ('ru', 'en'), ('zh', 'en'), ('gu', 'en'), ('en', 'kk'), ('en', 'zh'),
                         ('cs', 'de'), ('fi', 'en'), ('en', 'gu'), ('lt', 'en'), ('de', 'cs'),
                         ('en', 'lt'), ('en', 'ru'), ('en', 'cs'), ('fr', 'de')],
        'newsdev2020': [('iu', 'en'), ('en', 'ta'), ('ta', 'en'), ('pl', 'en'), ('en', 'iu'),
                        ('en', 'ja'), ('ja', 'en'), ('en', 'pl')]
    }
    for set_name, pairs in wmt_sets.items():
        sub_name, year = set_name[:-4], set_name[-4:]
        for l1, l2 in pairs:
            src = f'dev/{set_name}-{l1}{l2}-src.{l1}.sgm'
            ref = f'dev/{set_name}-{l1}{l2}-ref.{l2}.sgm'
            name = f'{sub_name}_{l1}{l2}'
            index.add_entry(Entry(did=DatasetId(group=group_id, name=name, version=year, langs=(l1, l2)),
                                  filename='wmt20dev.tgz', in_paths=[src, ref], in_ext='sgm',
                                  url='http://data.statmt.org/wmt20/translation-task/dev.tgz',
                                  cite=cite))

    # Multi parallel
    wmt_sets = {
        '2009': ['en', 'cs', 'de', 'es', 'fr'],
        '2010': ['en', 'cs', 'de', 'es', 'fr'],
        '2011': ['en', 'cs', 'de', 'es', 'fr'],
        '2012': ['en', 'cs', 'de', 'es', 'fr', 'ru'],
        '2013': ['en', 'cs', 'de', 'es', 'fr', 'ru'],
    }
    for year, langs in wmt_sets.items():
        name = 'newstest'
        for l1, l2 in itertools.combinations(langs, 2):
            f1 = f'dev/{name}{year}.{l1}'
            f2 = f'dev/{name}{year}.{l2}'
            index.add_entry(Entry(did=DatasetId(group=group_id, name=name, version=year, langs=(l1, l2)),
                                    filename='wmt20dev.tgz', in_paths=[f1, f2], in_ext='txt', cite=cite,
                                  url='http://data.statmt.org/wmt20/translation-task/dev.tgz'))

    for l1, l2 in [('ps', 'en'), ('km', 'en')]:
        for set_name in ['wikipedia.dev', 'wikipedia.devtest']:
            src = f'dev/{set_name}.{l1}-{l2}.{l1}'
            ref = f'dev/{set_name}.{l1}-{l2}.{l2}'
            name = f'{set_name.replace(".", "_")}_{l1}{l2}'
            index.add_entry(Entry(did=DatasetId(group=group_id, name=name, version='1', langs=(l1, l2)),
                                 filename='wmt20dev.tgz', in_paths=[src, ref], in_ext='txt', cite=cite,
                                  url='http://data.statmt.org/wmt20/translation-task/dev.tgz'))

    #### WMT 20 Tests
    url = "http://data.statmt.org/wmt20/translation-task/test.tgz"
    wmt20_cite = index.ref_db.get_bibtex('barrault-etal-2020-findings')
    for _pref, pairs in {
        "": ["csen", "deen", "defr", "encs", "ende", "eniu", "enja", "enkm", "enpl", "enps",
             "enru", "enta", "enzh", "frde", "iuen", "jaen", "kmen", "plen", "psen", "ruen",
             "taen", "zhen"],
        "B": ["deen", "ende", "enzh", "ruen", "zhen"]}.items():
        year = "2020"
        name = f'newstest{_pref}'
        for pair in pairs:
            l1, l2 = pair[:2], pair[2:]
            f1 = f'sgm/{name}{year}-{pair}-src.{l1}.sgm'
            f2 = f'sgm/{name}{year}-{pair}-ref.{l2}.sgm'
            index.add_entry(Entry(did=DatasetId(group=group_id, name=f'{name}_{pair}'.lower(), version=year, langs=(l1, l2)),
                filename='wmt20tests.tgz', in_paths=[f1, f2], in_ext='sgm', cite=wmt20_cite, url=url))

    # WMT 21 Dev
    url = "http://data.statmt.org/wmt21/translation-task/dev.tgz"
    pairs = "en-ha en-is is-en ha-en".split()
    for pair in pairs:
        l1, l2 = pair.split('-')
        in_path = f'dev/xml/newsdev2021.{l1}-{l2}.xml'
        ent = Entry(did=DatasetId(group=group_id, name=f'newsdev_{l1}{l2}', version='2021', langs=(l1, l2)),
                    filename='wmt21dev.tgz', in_paths=[in_path], in_ext='wmt21xml', cite=wmt20_cite, url=url)
        index.add_entry(ent)

    url = "http://data.statmt.org/wmt21/translation-task/test.tgz"
    pairs = 'bn-hi hi-bn xh-zu zu-xh cs-en de-en de-fr en-cs en-de en-ha en-is en-ja en-ru en-zh fr-de ha-en is-en ja-en ru-en zh-en'.split()
    for pair in pairs:
        l1, l2 = pair.split('-')
        name = 'newstest'
        if pair in 'bn-hi hi-bn xh-zu zu-xh':
            name = 'florestest'
        in_path = f'test/{name}2021.{l1}-{l2}.xml'
        ent = Entry(did=DatasetId(group=group_id, name=f'{name}_{l1}{l2}', version='2021', langs=(l1, l2)),
                    filename='wmt21tests.tgz', in_paths=[in_path], in_ext='wmt21xml', cite=wmt20_cite, url=url)
        index.add_entry(ent)

    # ==== TED Talks 2.0 ar-en
    index.add_entry(Entry(did=DatasetId(group=group_id, name='tedtalks', version='2_clean', langs=('en', 'ar')),
                         ext='tsv.xz', url='http://data.statmt.org/ted-talks/en-ar.v2.aligned.clean.xz'))

    # ==== Europarl v10
    EP_v10 = "http://www.statmt.org/europarl/v10/training/europarl-v10.%s-%s.tsv.gz"
    for pair in ['cs en', 'cs pl', 'de en', 'de fr', 'es pt', 'fi en', 'fr en', 'lt en', 'pl en']:
        l1, l2 = pair.split()
        index.add_entry(Entry(did=DatasetId(group=group_id, name=f'europarl', version='10', langs=(l1, l2)),
                url=EP_v10 % (l1, l2), cite=wmt20_cite))

    # ==== PMIndia V1
    PMINDIA_v1 = "http://data.statmt.org/pmindia/v1/parallel/pmindia.v1.%s-%s.tsv"
    cite = index.ref_db.get_bibtex('Haddow-etal-2020-PMIndia')
    for pair in ["as en", "bn en", "gu en", "hi en", "kn en", "ml en", "mni en", "mr en", "or en",
                 "pa en", "ta en", "te en", "ur en"]:
        l1, l2 = pair.split()
        # Note: listed as xx-en in URL but actually en-xx in the tsv; and its not compressed!
        index.add_entry(Entry(did=DatasetId(group=group_id, name=f'pmindia', version='1', langs=(l2, l1)),
                              url=PMINDIA_v1 % (l1, l2), cite=cite))

    # Pashto - English  pseudo parallel dataset for alignment
    index.add_entry(Entry(did=DatasetId(group=group_id, name=f'wmt20_enps_aligntask', version='1', langs=('en', 'ps')),
                          url='http://data.statmt.org/wmt20/translation-task/ps-km/wmt20-sent.en-ps.xz',
                          cite=wmt20_cite, ext='tsv.xz'))

    # Pashto - English  mostly parallel dataset
    for name in ["GNOME.en-ps", "KDE4.en-ps", "Tatoeba.en-ps", "Ubuntu.en-ps", "bible.en-ps.clean",
                 "ted-wmt20.en-ps", "wikimedia.en-ps"]:
        ps = f'ps-parallel/{name}.ps'
        en = f'ps-parallel/{name}.en'
        url = 'http://data.statmt.org/wmt20/translation-task/ps-km/ps-parallel.tgz'
        name = name.replace('.en-ps', '').replace('.', '_').replace('-', '_').lower()
        entry = Entry(did=DatasetId(group=group_id, name=name, version='1', langs=('ps', 'en')), url=url,
                      cite=wmt20_cite, in_paths=[ps, en], filename='wmt20-psen-parallel.tgz', in_ext='txt')
        index.add_entry(entry)

    for l2 in ['ps', 'km']:
        url = f"http://data.statmt.org/wmt20/translation-task/ps-km/wmt20-sent.en-{l2}.xz"
        entry = Entry(did=DatasetId(group=group_id, name='paracrawl', version='5.1', langs=('en', l2)),
                    url=url, cite=wmt20_cite, ext='tsv.xz', cols=(0, 1))
        index.add_entry(entry)

    # for ja-en only TED was available
    index.add_entry(Entry(url="http://data.statmt.org/wmt20/translation-task/ja-en/ted.en-ja.tgz",
                    did=DatasetId(group=group_id, name='ted', version='wmt20', langs=('en', 'ja')),
                    cite=wmt20_cite, ext='tgz', in_ext='txt',
                    in_paths=['en-ja/train.tags.en-ja.en', 'en-ja/train.tags.en-ja.ja']))

    ccalign_cite = index.ref_db.get_bibtex('chaudhary-EtAl:2019:WMT')
    CC_ALIGNED = 'http://www.statmt.org/cc-aligned/sentence-aligned/{src}-{tgt}.tsv.xz'
    tgts='es_XX et_EE fa_IR ff_NG fi_FI fr_XX gu_IN ha_NG he_IL hi_IN hr_HR ht_HT hu_HU hy_AM id_ID ig_NG is_IS it_IT ja_XX jv_ID ka_GE kg_AO kk_KZ km_KH kn_IN ko_KR ku_TR ky_KG lg_UG ln_CD lo_LA lt_LT lv_LV mg_MG mi_NZ mk_MK ml_IN mn_MN mr_IN ms_MY mt_MT my_MM ne_NP nl_XX no_XX ns_ZA ny_MW om_KE or_IN pa_IN pl_PL ps_AF pt_XX qa_MM qd_MM ro_RO ru_RU si_LK sk_SK sl_SI sn_ZW so_SO sq_AL sr_RS ss_SZ st_ZA su_ID sv_SE sw_KE sz_PL ta_IN te_IN tg_TJ th_TH ti_ET tl_XX tn_BW tr_TR ts_ZA tz_MA uk_UA ur_PK ve_ZA vi_VN wo_SN xh_ZA yo_NG zh_CN zh_TW zu_ZA zz_TR'.split()
    srcs = 'af_ZA ak_GH am_ET ar_AR as_IN ay_BO az_AZ az_IR be_BY bg_BG bm_ML bn_IN br_FR bs_BA ca_ES cb_IQ cs_CZ cx_PH cy_GB da_DK de_DE el_GR'.split()
    pairs = [('en_XX', tgt) for tgt in tgts] + [(src, 'en_XX') for src in srcs]
    dont_know = {'qa', 'qd'}   # looks like some Myanmar languages, but not sure which one.
    # Cant find them in ISO 639-1:  https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    #                and lingo http://www.lingoes.net/en/translator/langcode.htm
    #               and web-info https://wp-info.org/tools/languagecodes.php
    #unsupported = {'zh_TW', 'az_IR'}
    # country locales are not supported; they create conflicts. keeping large ones instead
    for src, tgt in pairs:
        # l1, l2 = src.split('_')[0], tgt.split('_')[0]
        if src[:2] in dont_know or tgt[:2] in dont_know:   # I dont know what language these are
            continue
        url = CC_ALIGNED.format(src=src, tgt=tgt)
        entry = Entry(did=DatasetId(group=group_id, name='ccaligned', version='1', langs=(src, tgt)), url=url,
                      cite=ccalign_cite, ext='tsv.xz', cols=(0, 1))
        index.add_entry(entry)

    wmt21_cite = 'WMT21'  # unavailable at the time of adding
    index.add_entry(Entry(
        did=DatasetId(group=group_id, name=f'khamenei', version='wmt21', langs=('ha','en')), cite=wmt21_cite,
        url='http://data.statmt.org/wmt21/translation-task/ha-en/khamenei.v1.ha-en.tsv', ext='tsv', cols=(2, 3)))
    index.add_entry(Entry(
        did=DatasetId(group=group_id, name=f'opus', version='wmt21', langs=('ha', 'en')), cite=wmt21_cite,
        url='http://data.statmt.org/wmt21/translation-task/ha-en/opus.ha-en.tsv', ext='tsv', cols=(1, 0)))
    index.add_entry(Entry(
        did=DatasetId(group=group_id, name=f'paracrawl', version='8.wmt21', langs=('en', 'ha')), cite=wmt21_cite,
        url='http://data.statmt.org/wmt21/translation-task/paracrawl8/paracrawl-release8.en-ha.bifixed.dedup.laser.filter-0.9.xz',
        ext='tsv.xz', cols=[1, 2]))
    index.add_entry(Entry(
        did=DatasetId(group=group_id, name=f'paracrawl', version='8.wmt21', langs=('en', 'ru')), cite=wmt21_cite,
        url='http://data.statmt.org/wmt21/translation-task/paracrawl8/paracrawl-release8.en-ru.bifixed.dedup.filter-1.1.xz',
        ext='tsv.xz', cols=[0, 1]))

    for pair in ['bn-hi', 'xh-zu']:
        l1, l2 = pair.split('-')
        url = f'http://data.statmt.org/wmt21/translation-task/cc-aligned/{pair}.tsv.xz'
        index.add_entry(Entry(
            did=DatasetId(group=group_id, name=f'ccaligned', version='wmt21', langs=(l1, l2)), cite=wmt21_cite,
            url='http://data.statmt.org/wmt21/translation-task/ha-en/opus.ha-en.tsv', ext='tsv', cols=(1, 0)))

    # https://data.statmt.org/wmt19/translation-task/fr-de/bitexts/de-fr.bicleaner07.de.gz
    for cln_name, name in [('commoncrawl', ''), ('paracrawl', 'de-fr.bicleaner07'), ('europarl_v7', '')]:
        l1, l2 = 'fr', 'de'
        prefix = 'https://data.statmt.org/wmt19/translation-task/fr-de/bitexts'
        index.add_entry(Entry(did=DatasetId(group=group_id, name=cln_name or name, version='wmt19', langs=(l1, l2)),
                              ext='txt.gz', url=(f'{prefix}/{name}.{l1}.gz', f'{prefix}/{name}.{l2}.gz')))

    # Back Translation
    prefix = 'https://data.statmt.org/wmt20/translation-task/back-translation/zh-en'
    index.add_entry(Entry(
        did=DatasetId(group=group_id, name='backtrans_enzh', version='wmt20', langs=('en', 'zh')),
        ext='txt.gz', url=(f'{prefix}/news.en.gz', f'{prefix}/news.translatedto.zh.gz')))

    prefix = 'https://data.statmt.org/wmt20/translation-task/back-translation/ru-en'
    index.add_entry(Entry(
        did=DatasetId(group=group_id, name='backtrans_enru', version='wmt20', langs=('en', 'ru')),
                      ext='txt.gz', url=(f'{prefix}/news.en.gz', f'{prefix}/news.en.translatedto.ru.gz')))
    index.add_entry(Entry(
        did=DatasetId(group=group_id, name='backtrans_ruen', version='wmt20', langs=('ru', 'en')),
        ext='txt.gz', url=(f'{prefix}/news.ru.gz', f'{prefix}/news.ru.translatedto.en.gz')))


    index.add_entry(Entry(
        did=DatasetId(group=group_id, name='yandex', version='wmt22', langs=('en', 'ru')),
        ext='zip', in_ext='tsv', cols=(0,1), in_paths=[f'WMT2022-data-main/en-ru/en-ru.1m_{i}.tsv' for i in range(1, 11)], 
        url='https://github.com/mashashma/WMT2022-data/archive/refs/heads/main.zip'))

    index.add_entry(Entry(
        did=DatasetId(group=group_id, name='yakut', version='wmt22', langs=('sah', 'rus')),
        ext='zip', in_ext='tsv', cols=(0,1), in_paths=['yakut/sah-ru.parallel.uniq.tsv'], 
        url='http://data.statmt.org/wmt22/translation-task/yakut.zip'))