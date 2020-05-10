#!/usr/bin/env python
#
# This file should contain popular papers and their experiment setup
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/23/20

from mtdata.entry import Experiment, Paper
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
        experiments=[
            Experiment.make(
                langs=('eng', 'deu'),
                train=['wmt13_europarl_v7', 'wmt13_commoncrawl', 'wmt18_news_commentary_v13'],
                tests=['newstest2013', 'newstest2014_deen'])
        ]
    )
    index.add_paper(vaswani_etal_2017)
