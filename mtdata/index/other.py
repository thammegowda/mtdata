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