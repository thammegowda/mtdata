
from mtdata.main import show_stats, CACHE_DIR, DatasetId
from mtdata import log
from mtdata.index import INDEX as index
from mtdata.cache import Cache
import random


cache = Cache(CACHE_DIR)

# some datasets
dids = ['OPUS-ted2020-v1-slk-tgl', 'Facebook-wikimatrix-1-slk-sqi', 'EU-eac_reference-1-deu-lit']
dids = [DatasetId.parse(d) for d in dids]


def test_content_length():
    for did in dids:
        entry = index[did]
        stats = cache.get_content_length(entry)
        assert stats['total_bytes'] > 0

def test_stats():
    did = random.choice(dids)
    log.info(f"Random dataset chosen: {did}")
    entry = index[did]
    stats = cache.get_stats(entry)
    assert stats['segs'] > 0

