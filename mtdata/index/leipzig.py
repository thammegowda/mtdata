
from mtdata import log, resource_dir
from mtdata.index import Index, Entry, bcp47, DatasetId

GROUP_ID = 'Leipzig'
dataset_ids = resource_dir / 'leipzig_de.txt'

"""
curl https://wortschatz.uni-leipzig.de/en/download |
grep -o 'href="[^"]*/download/[^"]*"' | cut -f2 -d\" |
while read i; do 
    curl -L $i | grep -o 'data-corpora-file="[^"]*"' | cut -f2 -d\" | sed 's/.tar.gz//';
done | sort | uniq > leipzig_de.txt
"""

def load_all(index: Index):
    assert dataset_ids.exists()
    URL = 'https://downloads.wortschatz-leipzig.de/corpora/%s.tar.gz'
    cites = ('goldhahn-etal-2012-building',)
    errors = []
    for data_id in dataset_ids.read_text().splitlines():
        data_id = data_id.strip()
        if not data_id:
            continue
        parts = data_id.split('_')
        name = ''
        try:
            lang = bcp47(parts[0])  #expected format: lang-country_*
        except:
            # part after "-: was not a country code? Then take it as name prefix
            subparts = parts[0].split('-')  
            try:
                lang = bcp47(subparts[0])
                name += '_'.join(subparts[1:])
            except:    
                errors.append(data_id)
                continue
        name += parts[1].lower().replace('-', '_')
        version = '_'.join(parts[2:]).lower().replace('-','_')
        index += Entry(did=DatasetId(GROUP_ID, name, version, langs=(lang,)),
                       url=URL % data_id, in_ext='tsv', in_paths=['*/*-sentences.txt'], cols=[1], cite=cites)
    if errors:
        log.info(f'Could not load these Leipzig corpora: {errors}')
