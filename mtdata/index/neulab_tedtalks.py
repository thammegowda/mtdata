#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 8/27/20


from mtdata.index import Index, Entry, DatasetId


class NoisyEntry(Entry):

    def is_NULL(self, seg):
        return '__NULL__' in seg or '_ _ NULL _ _' in seg

    def is_noisy(self, seg1, seg2) -> bool:
        noise = super().is_noisy(seg1, seg2) or self.is_NULL(seg1) or self.is_NULL(seg2)
        return noise


def load_all(index: Index):
    url = "http://phontron.com/data/ted_talks.tar.gz"
    cite = index.ref_db.get_bibtex('Ye2018WordEmbeddings')
    header = (
        "-,en,es,pt-br,fr,ru,he,ar,ko,zh-cn,it,ja,zh-tw,nl,ro,tr,de,vi,pl,pt,bg,el,fa,sr,hu,hr,"
        "uk,cs,id,th,sv,sk,sq,lt,da,calv-,my,sl,mk,fr-ca,fi,hy,hi,nor,ka,mn,et,ku,gl,mr,zh,ur,"
        "eo,ms,az,ta,bn,kk,be,eu,bs").split(',')
    col_idx = {lang: idx for idx, lang in enumerate(header)}

    # langs that I care; exclude <lang>-<country> bcoz the iso3 code doesnt have a way to map it
    langs = [x for x in header if '-' not in x]
    for split in ['train', 'test', 'dev']:
        for idx1, lang1 in enumerate(langs):
            col1 = col_idx[lang1]
            for lang2 in langs[idx1 + 1:]:
                col2 = col_idx[lang2]
                ent = NoisyEntry(did=DatasetId(group='Neulab', name=f'tedtalks_{split}', version='1', langs=(lang1, lang2)),
                                 filename='neulab_ted_talksv1.tar.gz', url=url, in_paths=[f"all_talks_{split}.tsv"],
                                 in_ext='tsv', cols=(col1, col2), cite=cite,)
                index.add_entry(ent)
