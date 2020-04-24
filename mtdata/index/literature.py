#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/23/20

from mtdata.entry import Experiment, Paper, Entry
from mtdata.index import Index


def load(index: Index):
    vaswani_etal_2017 = Paper(
        name="vaswani-etal-2017",
        title="Attention is all you need",
        url="https://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf",
        cite="""@inproceedings{vaswani2017attention,
                  title={Attention is all you need},
                  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and Kaiser, {\L}ukasz and Polosukhin, Illia},
                  booktitle={Advances in neural information processing systems},
                  pages={5998--6008},
                  year={2017}
                }""",
        experiments=[Experiment(
            name='en-de',
            train=[index.get_entry('wmt13_europarl_v7', ('en', 'de')),
                   index.get_entry('wmt13_commoncrawl', ('en', 'de')),
                   index.get_entry('wmt18_news_commentary_v13', ('en', 'de')),
                   ],
            tests=[index.get_entry('newstest2013', ('en', 'de')),
                   index.get_entry('newstest2014_deen', ('en', 'de'))]
        )])
    index.add_paper(vaswani_etal_2017)

