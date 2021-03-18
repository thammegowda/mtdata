#!/usr/bin/env python
# All other single corpus
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/23/20

from mtdata.index import Index, Entry


def load_all(index: Index):

    # === IITB hin eng http://www.cfilt.iitb.ac.in/iitb_parallel/
    cite="""@article{DBLP:journals/corr/abs-1710-02855,
  author    = {Anoop Kunchukuttan and
               Pratik Mehta and
               Pushpak Bhattacharyya},
  title     = {The {IIT} Bombay English-Hindi Parallel Corpus},
  journal   = {CoRR},
  volume    = {abs/1710.02855},
  year      = {2017},
  url       = {http://arxiv.org/abs/1710.02855},
  archivePrefix = {arXiv},
  eprint    = {1710.02855},
  timestamp = {Mon, 13 Aug 2018 16:48:50 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1710-02855.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}"""
    l1, l2 = 'hi', 'en'
    for version, prefix in [
        #('v1_0', 'http://www.cfilt.iitb.ac.in/iitb_parallel/iitb_corpus_download'),
        ('v1_5', 'http://www.cfilt.iitb.ac.in/~moses/iitb_en_hi_parallel/iitb_corpus_download')]:
        # they also have v2, but the link is broken http://www.cfilt.iitb.ac.in/iitb_parallel/
        # version is not explicit, but guessed from file modification time and description
        url = prefix + "/parallel.tgz"
        ent = Entry(langs=(l1, l2), url=url, filename=f'IITB{version}-hin_eng-parallel.tar.gz',
                    name=f'IITB{version}_train', in_ext='txt', cite=cite,
                    in_paths=[f'parallel/IITB.en-hi.{l1}',
                              f'parallel/IITB.en-hi.{l2}'])
        index.add_entry(ent)

        url = prefix + "/dev_test.tgz"
        for split in ['dev', 'test']:
            f1 = f'dev_test/{split}.{l1}'
            f2 = f'dev_test/{split}.{l2}'
            ent = Entry(langs=(l1, l2), url=url, filename=f'IITB{version}-hin_eng-dev_test.tar.gz',
                        name=f'IITB{version}_{split}', in_ext='txt',
                        in_paths=[f1, f2], cite=cite)
            index.add_entry(ent)


    # == Japanese ==
    cite="""@misc{neubig11kftt,
    author = {Graham Neubig},
    title = {The {Kyoto} Free Translation Task},
    howpublished = {http://www.phontron.com/kftt},
    year = {2011}
    }"""
    url = "http://www.phontron.com/kftt/download/kftt-data-1.0.tar.gz"
    l1, l2 = 'en', 'ja'
    for split in ['train', 'test', 'dev', 'tune']:
        f1 = f'kftt-data-1.0/data/orig/kyoto-{split}.{l1}'
        f2 = f'kftt-data-1.0/data/orig/kyoto-{split}.{l2}'
        ent = Entry(langs=(l1, l2), url=url, filename="kftt-data-1.0.tar.gz",
                    name=f'kftt_v1_{split}', in_ext='txt',
                    in_paths=[f1, f2], cite=cite)
        index.add_entry(ent)

    url = "http://lotus.kuee.kyoto-u.ac.jp/WAT/my-en-data/wat2020.my-en.zip"
    cite = """@article{ding2020a,
        title={A {Burmese} ({Myanmar}) Treebank: Guildline and Analysis},
        author={Ding, Chenchen and {Sann Su Su Yee} and {Win Pa Pa} and {Khin Mar Soe} and Utiyama, Masao and Sumita, Eiichiro},
        journal={ACM Transactions on Asian and Low-Resource Language Information Processing (TALLIP)},
        volume={19},
        number={3},
        pages={40},
        year={2020},
        publisher={ACM}
        }
    """
    for split in ['dev', 'test', 'train']:
        ent = Entry(langs=('my', 'en'), url=url, name=f'WAT2020_ALT_{split}', in_ext='txt',
                    cite=cite, filename='wat2020.my-en.zip',
              in_paths=[f'wat2020.my-en/alt/{split}.alt.my', f'wat2020.my-en/alt/{split}.alt.en'])
        index.add_entry(ent)


    l1, l2 = 'iu', 'en'
    url="https://nrc-digital-repository.canada.ca/eng/view/dataset/?id=c7e34fa7-7629-43c2-bd6d-19b32bf64f60"
    cite ="""@inproceedings{joanis-etal-2020-nunavut,
    title = "The {N}unavut Hansard {I}nuktitut{--}{E}nglish Parallel Corpus 3.0 with Preliminary Machine Translation Results",
    author = "Joanis, Eric  and
      Knowles, Rebecca  and
      Kuhn, Roland  and
      Larkin, Samuel  and
      Littell, Patrick  and
      Lo, Chi-kiu  and
      Stewart, Darlene  and
      Micher, Jeffrey",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.312",
    pages = "2562--2572",
    language = "English",
    ISBN = "979-10-95546-34-4",
}"""
    for split in ['dev', 'devtest', 'test', 'train']:
        path_pref = f'Nunavut-Hansard-Inuktitut-English-Parallel-Corpus-3.0/split/{split}'
        if split != 'train':
            path_pref += '-dedup'
        ent = Entry(langs=(l1, l2), url=url, name=f'NunavutHansard_v3_{split}', in_ext='txt',
                    cite=cite, filename='NunavutHansard_iuen_v3.tgz',
                    in_paths=[f'{path_pref}.{l1}', f'{path_pref}.{l2}'])
        index.add_entry(ent)