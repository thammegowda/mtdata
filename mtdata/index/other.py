#!/usr/bin/env python
# All other single corpus
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/23/20

from mtdata.index import Index, Entry, DatasetId


def load_all(index: Index):
    # === IITB hin eng http://www.cfilt.iitb.ac.in/iitb_parallel/
    cite = ('Kunchukuttan-etal-iitb',)
    l1, l2 = 'hi', 'en'
    for version, prefix in [
        # ('1.0', 'http://www.cfilt.iitb.ac.in/iitb_parallel/iitb_corpus_download'),
        ('1.5', 'http://www.cfilt.iitb.ac.in/~moses/iitb_en_hi_parallel/iitb_corpus_download')]:
        # they also have v2, but the link is broken http://www.cfilt.iitb.ac.in/iitb_parallel/
        # version is not explicit, but guessed from file modification time and description
        url = prefix + "/parallel.tgz"
        index += Entry(did=DatasetId(group='IITB', name=f'hien_train', version=version, langs=(l1, l2)),
                    url=url, filename=f'IITB{version}-hin_eng-parallel.tar.gz',
                    in_ext='txt', cite=cite,
                    in_paths=[f'parallel/IITB.en-hi.{l1}',
                              f'parallel/IITB.en-hi.{l2}'])

        url = prefix + "/dev_test.tgz"
        for split in ['dev', 'test']:
            f1 = f'dev_test/{split}.{l1}'
            f2 = f'dev_test/{split}.{l2}'
            index += Entry(did=DatasetId(group='IITB', name=f'hien_{split}', version=version, langs=(l1, l2)),
                        url=url, filename=f'IITB{version}-hin_eng-dev_test.tar.gz',
                        in_ext='txt', in_paths=[f1, f2], cite=cite)

    # == Japanese ==
    cite = ('neubig11kftt',)
    url = "http://www.phontron.com/kftt/download/kftt-data-1.0.tar.gz"
    l1, l2 = 'en', 'ja'
    for split in ['train', 'test', 'dev', 'tune']:
        f1 = f'kftt-data-1.0/data/orig/kyoto-{split}.{l1}'
        f2 = f'kftt-data-1.0/data/orig/kyoto-{split}.{l2}'
        index += Entry(did=DatasetId(group='Phontron', name=f'kftt_{split}', version='1', langs=(l1, l2)),
                    url=url, filename="kftt-data-1.0.tar.gz", in_ext='txt', in_paths=[f1, f2], cite=cite)

    url = "http://lotus.kuee.kyoto-u.ac.jp/WAT/my-en-data/wat2020.my-en.zip"
    cite = ('ding2020a',)
    for split in ['dev', 'test', 'train']:
        index += Entry(did=DatasetId(group='WAT', name=f'alt_{split}', version='2020', langs=('my', 'en')),
                    url=url, in_ext='txt', cite=cite, filename='wat2020.my-en.zip',
                    in_paths=[f'wat2020.my-en/alt/{split}.alt.my', f'wat2020.my-en/alt/{split}.alt.en'])

    l1, l2 = 'iu', 'en'
    url = "https://nrc-digital-repository.canada.ca/eng/view/dataset/?id=c7e34fa7-7629-43c2-bd6d-19b32bf64f60"
    cite = ('joanis-etal-2020-nunavut',)
    for split in ['dev', 'devtest', 'test', 'train']:
        path_pref = f'Nunavut-Hansard-Inuktitut-English-Parallel-Corpus-3.0/split/{split}'
        if split != 'train':
            path_pref += '-dedup'
        index += Entry(did=DatasetId(group='NRC_CA', name=f'nunavut_hansard_{split}', version='3', langs=(l1, l2)),
                    url=url, in_ext='txt', cite=cite, filename='NunavutHansard_iuen_v3.tgz',
                    in_paths=[f'{path_pref}.{l1}', f'{path_pref}.{l2}'])

    # https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-2122
    url = "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2122/khresmoi-summary-test-set-2.0.zip"
    cite = ('Khresmoi',)
    langs = ["cs", "de", "en", "es", "fr", "hu", "pl", "sv"]
    for i, l1 in enumerate(langs):
        for l2 in langs[i + 1:]:
            index += Entry(did=DatasetId(group='Lindat', name=f'khresmoi_summary_test', version='2', langs=(l1, l2)),
                        url=url, filename='khresmoi-summary-test-set-2.0.zip', cite=cite, in_ext='txt',
                        in_paths=[f"khresmoi-summary-test-set-2.0/khresmoi-summary-test.{l1}",
                                  f"khresmoi-summary-test-set-2.0/khresmoi-summary-test.{l2}"])
            index += Entry(did=DatasetId(group='Lindat', name=f'khresmoi_summary_dev', version='2', langs=(l1, l2)),
                        url=url, filename='khresmoi-summary-test-set-2.0.zip', cite=cite, in_ext='txt',
                        in_paths=[f"khresmoi-summary-test-set-2.0/khresmoi-summary-dev.{l1}",
                                  f"khresmoi-summary-test-set-2.0/khresmoi-summary-dev.{l2}"])

    jesc_cite = ('pryzant_jesc_2018',)
    for split in ['train', 'dev', 'test']:
        index += Entry(url='https://nlp.stanford.edu/projects/jesc/data/split.tar.gz',
                    did=DatasetId(group='StanfordNLP', name=f'jesc_{split}', version='1', langs=('en', 'ja')),
                    filename='jesc-split.tar.gz', in_ext='tsv', in_paths=[f"split/{split}"], cite=jesc_cite)

    prefix = 'https://nlp.stanford.edu/projects/nmt/data'
    for name, subdir, src, tgt, cite_key in [
        ("wmt15_train", "wmt15.en-cs", "train.en", "train.cs", "luong2016acl_hybrid"),
        ("newstest2013", "wmt15.en-cs", "newstest2013.en", "newstest2013.cs", "luong2016acl_hybrid"),
        ("newstest2014", "wmt15.en-cs", "newstest2014.en", "newstest2014.cs", "luong2016acl_hybrid"),
        ("newstest2015", "wmt15.en-cs", "newstest2015.en", "newstest2015.cs", "luong2016acl_hybrid"),
        ("wmt14_train", "wmt14.en-de", "train.en", "train.de", "luong-pham-manning:2015:EMNLP"),
        ("newstest2012", "wmt14.en-de", "newstest2012.en", "newstest2012.de", "luong-pham-manning:2015:EMNLP"),
        ("newstest2013", "wmt14.en-de", "newstest2013.en", "newstest2013.de", "luong-pham-manning:2015:EMNLP"),
        ("newstest2014", "wmt14.en-de", "newstest2014.en", "newstest2014.de", "luong-pham-manning:2015:EMNLP"),
        ("newstest2015", "wmt14.en-de", "newstest2015.en", "newstest2015.de", "luong-pham-manning:2015:EMNLP"),
        ("iwslt15_train", "iwslt15.en-vi", "train.en", "train.vi", "Luong-Manning:iwslt15"),
        ("test2012", "iwslt15.en-vi", "tst2012.en", "tst2012.vi", "Luong-Manning:iwslt15"),
        ("test2013", "iwslt15.en-vi", "tst2013.en", "tst2013.vi", "Luong-Manning:iwslt15")]:
        l1, l2 = src.split(".")[-1], tgt.split(".")[-1]
        url1 = f"{prefix}/{subdir}/{src}"
        url2 = f"{prefix}/{subdir}/{tgt}"
        index += Entry(did=DatasetId(group='StanfordNLP', name=name, version='1', langs=(l1, l2)),
                    ext='txt', url=(url1, url2), cite=(cite_key,))

    _url = 'https://repository.clarin.is/repository/xmlui/bitstream/handle/20.500.12537/24/Parice_dev_test.20.05.zip'
    cite = ('Barkarson-et-al-2020',)
    for sub in ['eea train dev test', 'ema train dev test', 'opensubtitles dev test']:
        l1, l2 = 'en', 'is'
        sub, *splits = sub.split()
        for split in splits:
            in_paths = [f'Parice_dev_test.20.05/csv/{sub}/{sub}_{split}_{l1}.csv',
                        f'Parice_dev_test.20.05/csv/{sub}/{sub}_{split}_{l2}.csv']
            if split == 'train' and sub == 'eea':
                in_paths = [in_paths[1], in_paths[0]] # aha! they have swapped it
            index += Entry(did=DatasetId(group='ParIce', name=f'{sub}_{split}', version='20.05', langs=(l1, l2)),
                        url=_url, ext='zip', in_ext='txt', in_paths=in_paths, cite=cite,
                        filename='Parice_dev_test.20.05.zip')

    # https://github.com/bonaventuredossou/ffr-v1/tree/master/FFR-Dataset/FFR%20Dataset%20v2
    _url = 'https://raw.githubusercontent.com/bonaventuredossou/ffr-v1/master/FFR-Dataset/FFR%20Dataset%20v2/ffr_dataset_v2.txt'
    cite = ("emezue-dossou-2020-ffr",)
    index += Entry(did=DatasetId(group='Masakhane', name=f'ffr', version='2', langs=('fon', 'fra')),
                url=_url, ext='tsv', cite=cite)

    # https://zenodo.org/record/4432712
    _url = 'https://zenodo.org/record/4432712/files/Fon_French_Parallel_Data_25377.csv?download=1'
    cite = ("dossou2021crowdsourced",)
    index += Entry(did=DatasetId(group='Masakhane', name=f'daily_dialogues', version='1', langs=('fon', 'fra')),
                url=_url, ext='csvwithheader', cite=cite)

    _url = "https://github.com/MicrosoftTranslator/NTREX/archive/52b9c57c.tar.gz"
    ntrex128_langs = ("afr amh arb aze_Latn bak bel bem ben bod bos bul cat ces ckb_Arab cym dan deu div dzo ell"
             " eng_GB eng_IN eng_US est eus ewe fao fas fij fil fin fra fra_CA fuc gle glg guj hau heb hin"
             " hmn hrv hun hye ibo ind isl ita jpn kan kat kaz khm kin kir kmr kor lao lav lit ltz mal mar"
             " mey mkd mlg mlt mon mri msa mya nde nep nld nno nob nso nya orm pan pol por por_BR prs pus"
             " ron rus shi sin slk slv smo sna_Latn snd_Arab som spa spa_MX sqi srp_Cyrl srp_Latn ssw swa"
             " swe tah tam tat tel tgk_Cyrl tha tir ton tsn tuk tur uig ukr urd uzb ven vie wol xho yor"
             " yue zho_CN zho_TW zul").split()  # NOTE: fij tgk_Cyrl urd vie wol zul had extra lines
    for l2 in ntrex128_langs:
        index += Entry(did=f"Microsoft-ntrex-128-eng-{l2}", url=_url, filename="NTREX-52b9c57c.tar.gz",
                       in_ext='txt', in_paths=["*/NTREX-128/newstest2019-src.eng.txt", f"*/NTREX-128/newstest2019-ref.{l2}.txt"])

    for i, l1 in enumerate(ntrex128_langs):
        for l2 in ntrex128_langs[i+1:]:
             index += Entry(did=f"Microsoft-ntrex-128-{l1}-{l2}", url=_url, filename="NTREX-52b9c57c.tar.gz",
                       in_ext='txt', in_paths=[f"*/NTREX-128/newstest2019-ref.{l1}.txt", f"*/NTREX-128/newstest2019-ref.{l2}.txt"])
