#!/usr/bin/env python
#
# Author: Kenneth Heafield [mtdata (at) kheafield (dot) com] 
# Created: 5/16/21
from mtdata.index import Index, Entry

from typing import Tuple, List, Optional

def make_entry(index : Index, langs : Tuple[str, str], name : str, elrchash : str, in_paths : List[str], cite : Optional[str] = None):
    url = 'https://elrc-share.eu/repository/download/' + elrchash + '/'
    filename = 'ELRC_' + elrchash + ".zip"
    name = 'ELRC_' + name
    index.add_entry(Entry(langs=langs, name=name, url=url, filename=filename,  in_ext='tmx', in_paths=in_paths))

def load_all(index: Index):
    # EMEA from ELRC-SHARE
    # Both OPUS and ELRC scraped EMEA.  OPUS seems better because it's
    # multiple directions instead of just with English.  Also OPUS was larger.
    # However, ELRC collected Croatian, Icelandic, and Norwegian Bokmål with
    # English whereas OPUS did not.
    # ELRC-SHARE main page: https://elrc-share.eu/repository/browse/multilingual-corpus-made-out-of-pdf-documents-from-the-european-medicines-agency-emea-httpswwwemaeuropaeu-february-2020/3cf9da8e858511ea913100155d0267062d01c2d847c349628584d10293948de3/
    # But that's just a zip file of zip files, might as well download the
    # individual zip files.
    # I've commented out the ones that duplicate OPUS, albeit with different
    # processing and presumably a different crawl.
    languages = {
        #bg": "22a07fe8862611ea913100155d02670625795dadf4ef4bd0aabf904b19e1a5f1",
        #cs": "7ec1f8b0862611ea913100155d02670659d281b85ea74c14944ea93afd45ea34",
        #da": "82c81ac4862711ea913100155d0267069e964ab24f0f4825a6ef0bd26be8925d",
        #de": "d6ce198a862611ea913100155d0267064011b731322946a6b897cf495fb6f023",
        #el": "bdf58192862511ea913100155d02670607a8e118f9e04cbf95790f835bea2ba8",
        #es": "4b1884a4862911ea913100155d026706e72bcbc1be4044f48cd94f4cc6e5bca2",
        #et": "9e1a7a18862911ea913100155d02670620c5530a0457429c9e233d911472cdbf",
        #fi": "e4cc7aa6862411ea913100155d0267065defb6a660e64db4b1a82353211efdf2",
        #fr": "a00e5afc862811ea913100155d026706e1fe6375ffb241c6ad44f85e3914c82f",
        "hr": "4c654ea0862411ea913100155d026706f6cb3a7f036d4fd9bb13fe3e2202f929",
        #"hu": "2ab94826862711ea913100155d02670692bc653db12349cb9e1934cc3e0d5874",
        "is": "29110788862811ea913100155d0267069f685ed8fd1e4ae088600d9c99af303c",
        #"it": "66b0180c862511ea913100155d026706d300a6e2e463400b89ff99feb8ae8450",
        #"lt": "d4154316862711ea913100155d02670656ed90a4ca3a49a0a30c83879864e130",
        #"lv": "93477aee862b11ea913100155d026706c18c9d57cfde4181b6d19763db2413a8",
        #"mt": "388ebb0e862511ea913100155d02670638ea7d4577004c97a1862ed7066fbf5f",
        #"nl": "93284c8e862411ea913100155d026706d3313f47bec143cd98cc4ba1aa62b4b5",
        "no": "63da4d16862811ea913100155d026706a43b5e13c3c34c9ba0a650a352092630", # This is labeled as no in file names and nb in XML, backing off to no
        #"pl": "923a4330862a11ea913100155d02670658fe0af7fc3144ee8caef5d547625fc7",
        #"pt": "f07e3600862911ea913100155d026706be569144d13d41409a05001118509762",
        #"ro": "3e38f500862b11ea913100155d026706378f2850bc3a47cd908640d762ef1de7",
        #"sk": "f55601c2862811ea913100155d026706c1a7bdf78d434198b84aeef3d01a5d5b",
        #"sl": "ea686816862a11ea913100155d02670668b9fab37b3b4cc6ad154056c1b4b092",
        #"sv": "4324fb28862a11ea913100155d0267061e379582560d4dae9d8d332273d53518",
    }
    cite = "This dataset has been generated out of public content available through European Medicines Agency: https://www.ema.europa.eu/, in February 2020"
    # This data set is different from the OPUS EMEA corpus but overlaps, so put elrc_share into the name.
    for l2, elrchash in languages.items():
        make_entry(index, langs=('en', l2), name='EMEA', elrchash=elrchash, in_paths=[f'en-{l2}.tmx'], cite=cite)

    # Antibiotic crawl by ELRC https://elrc-share.eu/repository/browse/covid-19-antibiotic-dataset-multilingual-cef-languages/e118d7f2903c11ea913100155d02670679a442295c174a899232193999b7abb6/
    languages = {
        "bg": "a3e20efe904511ea913100155d026706ca5a9aeed3db486e9ecf53ee6d164989",
        "cs": "a5870d68904511ea913100155d026706516408bab9d340d39e93f7b65cfa7551",
        "da": "aa23e968904511ea913100155d026706cf8b2000777e4501b57e0001591ed6d4",
        "de": "a731b5b4904511ea913100155d026706f88517ceed694d7f9101638b0419d3d5",
        "el": "a2205dfa904511ea913100155d0267069e4ac43bdcfb469693463838bc2035dd",
        "es": "b316ab14904511ea913100155d026706aaec036b93ef4cba9195d8dab3d132b7",
        "et": "b4a5caaa904511ea913100155d02670615e78d5aa7f849d8836e0ab3a5e9ae7b",
        "fi": "9db9bb4e904511ea913100155d0267069a84b259970147739e76c76202a81170",
        "fr": "b003ef36904511ea913100155d02670609bf770a58694260ae3662c493de26b7",
        "ga": "9b472a90904511ea913100155d0267062373e4bbd69c4b5a8258cca360473c04",
        "hr": "99a73ebe904511ea913100155d026706c489fb7ccad64854aaf787d5afe45a9e",
        "hu": "a8c7fadc904511ea913100155d02670600bc522b260c47d7ae9950668cdb700f",
        "is": "ad3b21a2904511ea913100155d026706bc31807f7e214f13a88b2cc78b7d9397",
        "it": "a084a4ce904511ea913100155d026706e145c18737a34ed797215df0847d7dc3",
        "lt": "abace546904511ea913100155d0267068f6e75f9e87f426d8eb879f79a828a08",
        "lv": "bea98b86904511ea913100155d026706428844c55c5640a1b7c35a48d28e7550",
        "mt": "9f36a7ac904511ea913100155d02670686436625c8234202a72304687d800def",
        "nb": "aeb981d6904511ea913100155d026706c4801a62c6eb40ebb8b2bbe32764ee85",
        "nl": "9c5009c0904511ea913100155d026706169da04f5eb448178c8954eb8f874db1",
        "pl": "b90fb4c0904511ea913100155d026706e4fc12f46b0d469699838229a836b175",
        "pt": "b6085d72904511ea913100155d026706f279f7b5f89f4f4885d37e6ce040442c",
        "ro": "bcff62b0904511ea913100155d026706b1e737c8afd047cc8ee763e50e49189d",
        "sk": "b1932218904511ea913100155d0267066d0513f912c34ae5b36ea6cfd8d94e7c",
        "sl": "bb25c1e6904511ea913100155d026706c870bffdc76147c98638bd50ab3e1a1e",
        "sv": "b77c2e4a904511ea913100155d026706f75f1d0a3fa343edb0a9cd384120729f",
    }
    cite = "This dataset has been generated out of public content available through the portal (https://antibiotic.ecdc.europa.eu/) of the European Centre for Disease Prevention and Control ( https://www.ecdc.europa.eu/en) in April 2020"
    for l2, elrchash in languages.items():
        make_entry(index, langs=('en', l2), name='antibiotic', elrchash=elrchash, in_paths=[f'en-{l2}.tmx'], cite=cite)

    # Icelandic data that isn't part of a larger collection
    data = """en is harpa b56c64c2e4d411e7b7d400155d0267060908d10ea65d42b58b429dd9301a7582 harpa.is_tilde_en-is.tmx
    en is fme f2a5b200e4c311e7b7d400155d02670665375c54796744de9689b6b49deb74ed fme.is.en-is.tmx
    en is pfs d6cc14a8e4c711e7b7d400155d02670668f4c1b127ee42ab9108ee2d0f2eb4b7 clean.pfs.is.en-is.tmx
    en is nordisketax c0970ab4eadd11e7b7d400155d026706fd923049f0ab48678edf9c4ae3fcdf71 clean.nordisketax.net.en-is.tmx
    en is statice b415363367f411e8b7d400155d0267060a94736a7fad4d7f9a73b191d1e5b09e statice.UNIQUE.en-is.tmx
    en is lyfjastofnun 4a6ddf7ae56011e7b7d400155d026706bfb8c1760a814dea8b0ce4300da6b504 lyfjastofnun.is.en-is.tmx
    en is listasafn 0958d46ee4d311e7b7d400155d0267061663be21d26647d1accefea64fc4db3b listasafn.is_tilde_en-is.tmx
    en is utl 2467fa26e56111e7b7d400155d026706bfd15d2901e94fdf979f4f1fff86c318 utl.is.en-is.tmx
    en is bokmenntaborgin b5a7f5fee4d511e7b7d400155d026706cfd7be18e5bd497fb00355ba4d23741d bokmenntaborgin.is_tilde_en-is.tmx"""
    for line in data.splitlines():
        src, tgt, name, elrchash, path = line.strip().split(' ')
        make_entry(index, langs=(src, tgt), name=name, elrchash=elrchash, in_paths=[path])

    #TODO a whole lot more!
