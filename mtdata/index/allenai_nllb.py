# AllenAi version of NLLB dataset
# Originally published on HF dataset hub https://huggingface.co/datasets/allenai/nllb

from mtdata.index import Index, Entry, DatasetId

import json
from pathlib import Path

_ALLENAI_URL = "https://storage.googleapis.com/allennlp-data-bucket/nllb/"
_LICENSE = "https://opendatacommons.org/licenses/by/1-0/"
_CITATION="""Schwenk et al, CCMatrix: Mining Billions of High-Quality Parallel Sentences on the Web. ACL https://aclanthology.org/2021.acl-long.507/ Hefferman et al, Bitext Mining Using Distilled Sentence Representations for Low-Resource Languages. Arxiv https://arxiv.org/abs/2205.12654, 2022.
NLLB Team et al, No Language Left Behind: Scaling Human-Centered Machine Translation, Arxiv https://arxiv.org/abs/2207.04672, 2022."""

NLLB_PAIRS = json.load(open(Path(__file__).parent / "allenai_nllb.json"))

def load_all(index: Index):
    for src_lang, tgt_lang in NLLB_PAIRS:
        download_url = f"{_ALLENAI_URL}{src_lang}-{tgt_lang}.gz"
        ent = Entry(did=DatasetId(group='AllenAi', name="nllb", version='1', langs=(src_lang, tgt_lang)),
                in_paths=[f"{src_lang}-{tgt_lang}"], in_ext="tsv", cite=_CITATION, ext="gz",
                url=download_url, filename=f"{src_lang}-{tgt_lang}.gz")
        index.add_entry(ent)

