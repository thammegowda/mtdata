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
        cite=index.ref_db.get_bibtex('vaswani2017attention'),
        experiments=[
            Experiment.make(index=index,
                langs=('eng', 'deu'),
                train=['wmt13_europarl_v7', 'wmt13_commoncrawl', 'wmt18_news_commentary_v13'],
                tests=['newstest2013', 'newstest2014_deen'])
        ]
    )
    index.add_paper(vaswani_etal_2017)
