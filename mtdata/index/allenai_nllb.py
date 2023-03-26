# AllenAi version of NLLB dataset
# Originally published on HF dataset hub https://huggingface.co/datasets/allenai/nllb

from mtdata import resource_dir
from mtdata.index import Index, Entry, DatasetId

import json
from pathlib import Path

_ALLENAI_URL = "https://storage.googleapis.com/allennlp-data-bucket/nllb/"
_LICENSE = "https://opendatacommons.org/licenses/by/1-0/"

def load_all(index: Index):
    nllb_pairs = json.load(open(resource_dir / "allenai_nllb.json"))
    # these bib keys are as per listed on https://huggingface.co/datasets/allenai/nllb 
    bibkeys = ('schwenk-etal-2021-ccmatrix', 'heffernan2022bitext', 'nllb-2022')

    for pair in nllb_pairs:
        src_lang, tgt_lang = pair.split('-')
        download_url = f"{_ALLENAI_URL}{src_lang}-{tgt_lang}.gz"
        ent = Entry(did=DatasetId(group='AllenAi', name="nllb", version='1', langs=(src_lang, tgt_lang)),
            cite=bibkeys, ext="tsv.gz", url=download_url)
        index.add_entry(ent)

