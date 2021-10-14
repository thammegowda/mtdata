#!/usr/bin/env python
# All other single corpus
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/23/20

from mtdata.index import Index, Entry, DatasetId


def load_all(index: Index):

    # === IITB hin eng http://www.cfilt.iitb.ac.in/iitb_parallel/
    cite = index.ref_db.get_bibtex('Kunchukuttan-etal-iitb')
    l1, l2 = 'hi', 'en'
    for version, prefix in [
        #('1.0', 'http://www.cfilt.iitb.ac.in/iitb_parallel/iitb_corpus_download'),
        ('1.5', 'http://www.cfilt.iitb.ac.in/~moses/iitb_en_hi_parallel/iitb_corpus_download')]:
        # they also have v2, but the link is broken http://www.cfilt.iitb.ac.in/iitb_parallel/
        # version is not explicit, but guessed from file modification time and description
        url = prefix + "/parallel.tgz"
        ent = Entry(did=DatasetId(group='IITB', name=f'hien_train', version=version, langs=(l1, l2)),
                    url=url, filename=f'IITB{version}-hin_eng-parallel.tar.gz',
                    in_ext='txt', cite=cite,
                    in_paths=[f'parallel/IITB.en-hi.{l1}',
                              f'parallel/IITB.en-hi.{l2}'])
        index.add_entry(ent)

        url = prefix + "/dev_test.tgz"
        for split in ['dev', 'test']:
            f1 = f'dev_test/{split}.{l1}'
            f2 = f'dev_test/{split}.{l2}'
            ent = Entry(did=DatasetId(group='IITB', name=f'hien_{split}', version=version, langs=(l1, l2)),
                        url=url, filename=f'IITB{version}-hin_eng-dev_test.tar.gz',
                        in_ext='txt', in_paths=[f1, f2], cite=cite)
            index.add_entry(ent)


    # == Japanese ==
    cite = index.ref_db.get_bibtex('neubig11kftt')
    url = "http://www.phontron.com/kftt/download/kftt-data-1.0.tar.gz"
    l1, l2 = 'en', 'ja'
    for split in ['train', 'test', 'dev', 'tune']:
        f1 = f'kftt-data-1.0/data/orig/kyoto-{split}.{l1}'
        f2 = f'kftt-data-1.0/data/orig/kyoto-{split}.{l2}'
        ent = Entry(did=DatasetId(group='Phontron', name=f'kftt_{split}', version='1', langs=(l1, l2)),
                    url=url, filename="kftt-data-1.0.tar.gz", in_ext='txt', in_paths=[f1, f2], cite=cite)
        index.add_entry(ent)

    url = "http://lotus.kuee.kyoto-u.ac.jp/WAT/my-en-data/wat2020.my-en.zip"
    cite = index.ref_db.get_bibtex('ding2020a')
    for split in ['dev', 'test', 'train']:
        ent = Entry(did=DatasetId(group='WAT', name=f'alt_{split}', version='2020', langs=('my', 'en')),
                    url=url, in_ext='txt', cite=cite, filename='wat2020.my-en.zip',
                    in_paths=[f'wat2020.my-en/alt/{split}.alt.my', f'wat2020.my-en/alt/{split}.alt.en'])
        index.add_entry(ent)

    l1, l2 = 'iu', 'en'
    url = "https://nrc-digital-repository.canada.ca/eng/view/dataset/?id=c7e34fa7-7629-43c2-bd6d-19b32bf64f60"
    cite = index.ref_db.get_bibtex('joanis-etal-2020-nunavut')
    for split in ['dev', 'devtest', 'test', 'train']:
        path_pref = f'Nunavut-Hansard-Inuktitut-English-Parallel-Corpus-3.0/split/{split}'
        if split != 'train':
            path_pref += '-dedup'
        ent = Entry(did=DatasetId(group='NRC_CA', name=f'nunavut_hansard_{split}', version='3', langs=(l1, l2)),
                    url=url, in_ext='txt', cite=cite, filename='NunavutHansard_iuen_v3.tgz',
                    in_paths=[f'{path_pref}.{l1}', f'{path_pref}.{l2}'])
        index.add_entry(ent)

    # https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-2122
    url = "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2122/khresmoi-summary-test-set-2.0.zip"
    cite = index.ref_db.get_bibtex('Khresmoi')
    langs = ["cs", "de", "en", "es", "fr", "hu", "pl", "sv"]
    for i, l1 in enumerate(langs):
        for l2 in langs[i+1:]:
            ent = Entry(did=DatasetId(group='Lindat', name=f'khresmoi_summary_test', version='2', langs=(l1, l2)),
                        url=url, filename='khresmoi-summary-test-set-2.0.zip', cite=cite, in_ext='txt',
                        in_paths=[f"khresmoi-summary-test-set-2.0/khresmoi-summary-test.{l1}",
                                  f"khresmoi-summary-test-set-2.0/khresmoi-summary-test.{l2}"])
            index.add_entry(ent)
            ent = Entry(did=DatasetId(group='Lindat', name=f'khresmoi_summary_dev', version='2', langs=(l1, l2)),
                        url=url, filename='khresmoi-summary-test-set-2.0.zip', cite=cite, in_ext='txt',
                        in_paths=[f"khresmoi-summary-test-set-2.0/khresmoi-summary-dev.{l1}",
                                  f"khresmoi-summary-test-set-2.0/khresmoi-summary-dev.{l2}"])
            index.add_entry(ent)

    jesc_url = 'https://nlp.stanford.edu/projects/jesc/data/split.tar.gz'
    jesc_cite = index.ref_db.get_bibtex('pryzant_jesc_2018')
    for split in ['train', 'dev', 'test']:
        ent = Entry(did=DatasetId(group='StanfordNLP', name=f'jesc_{split}', version='1', langs=(l1, l2)),
                    url=jesc_url, filename='jesc-split.tar.gz', in_ext='tsv',
                    in_paths=[f"split/{split}"], cite=jesc_cite)
        index.add_entry(ent)
