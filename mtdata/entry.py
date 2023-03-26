#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20

from typing import Tuple, List, Optional, Union, Any
from dataclasses import dataclass
import json

from mtdata import log
from mtdata.iso.bcp47 import BCP47Tag, bcp47


DID_DELIM = '-'  # I  wanted to use ":", but Windows, they dont like ":" in path! :(

LangPair = Tuple[BCP47Tag, BCP47Tag]


def Langs(string) -> Union[BCP47Tag, LangPair]:
    parts = string.strip().split('-')
    assert 1 <= len(parts) <= 2, f'Expected at most two language IDs where one for monolingual and two for bitexts, but given {string}'
    std_codes = tuple([bcp47(part) for part in parts])
    std_form = '-'.join(str(lang) for lang in std_codes)
    if std_form != string:
        log.info(f"Suggestion: consider using '{std_form}' instead of '{string}'.")
    return std_codes


@dataclass(frozen=True)
class DatasetId:
    group: str
    name: str
    version: str
    langs: Union[Tuple[str], Tuple[BCP47Tag], Tuple[str, str], LangPair]  # one=monolingual, two=bitext; many=multi

    def __post_init__(self):
        assert self.group
        assert self.name
        assert self.version
        assert self.name.islower(), f'name {self.name} has to be lower cased for consistency'
        for name in [self.group, self.version, self.name]:
            for ch in '-/*|[](){}<>?&:;,!^$"\' ':
                assert ch not in name, f"Character '{ch}' is not permitted in name {name}"
        # ensure lang ID is BCP47 tag
        
        assert isinstance(self.langs, tuple),\
            f'Expected tuple (l1, l2) for parallel or tuple(str,) for mono; given={self.langs}'
        langs = tuple(lang if isinstance(lang, BCP47Tag) else bcp47(lang) for lang in self.langs)
        if langs != self.langs:
            object.__setattr__(self, 'langs', langs)  # bypass frozen=True

    @property
    def type(self):
        if len(self.langs) == 1:
            return 'mono'
        elif len(self.langs) == 2:
            return 'bitext'
        else:
            raise Exception(f'Not supported. langs={self.langs}')

    @property
    def lang_str(self):
        return DID_DELIM.join(str(lang) for lang in self.langs)

    def format(self, delim=DID_DELIM):
        return delim.join([self.group, self.name, self.version, self.lang_str])

    def __str__(self):
        return self.format()

    @classmethod
    def parse(cls, string, delim=DID_DELIM) -> 'DatasetId':
        expected_format = f"<group>{delim}<name>{delim}<version>{delim}<l1>[{delim}<l2>]"
        parts = string.strip().split(delim)
        if len(parts) < 4 or len(parts) > 5:
            raise Exception(f'Dataset ID expected in format: {expected_format}; but given {string} ({len(parts)}).'
                            f' If you are unsure, run "mtdata list -id | grep -i <name>" and copy its id.')
        group, name, version, *langs = parts
        return cls(group=group, name=name, version=version, langs=tuple(langs))


class Entry:
    __slots__ = ('did', 'url', 'filename', 'ext', 'in_paths', 'in_ext', 'cite', 'cols', 'is_archive')

    def __init__(self, did: Union[str, DatasetId],
                 url: Union[str, Tuple[str, str]],
                 filename: Optional[str] = None,
                 ext: Optional[str] = None,
                 in_paths: Optional[List[str]] = None,
                 in_ext: Optional[str] = None,
                 cite: Optional[Tuple[str]] = None,
                 cols: Optional[Tuple[int, int]] = None):
        if not isinstance(did, DatasetId):
            did = DatasetId.parse(did)
        self.did = did
        self.url = url
        self.filename = filename
        self.ext = ext
        if not self.ext:
            from mtdata.parser import detect_extension
            assert isinstance(self.url, str), '"ext" attribute must be explicitely set for multi-URL entries'
            orig_name = self.url.split('/')[-1]
            self.ext = detect_extension(filename or orig_name)
        self.filename = self.filename or f'{self.did.name}.{self.ext}'

        self.in_paths = in_paths
        self.in_ext = in_ext
        self.cite = cite
        self.cols = cols   # column index starts from zero

        assert not self.ext.startswith("."), f'{did} :: ext {self.ext} should not start with a dot (.)'
        self.is_archive = self.ext in ('zip', 'tar', 'tar.gz', 'tgz')
        if self.is_archive:
            assert self.in_paths and len(self.in_paths) > 0, 'Archive entries must have in_paths'
            if not self.in_ext:
                raise Exception('in_ext is required for archive files')
        else:
            if self.in_ext != 'opus_xces':
                assert not self.in_paths, f"in_paths is not applicable for non archive format {self.ext}"

    def is_swap(self, langs):
        if self.in_ext == 'tmx':
            return False
        return tuple(reversed(langs)) == tuple(self.lang_str)
    
    def is_compatible(self, langs: Union[LangPair, Tuple[BCP47Tag]]):
        """
        Checks if the entry is compatible with given languages
        :param: langs 
        """
        if len(self.did.langs) == 2 and len(langs) == 2: # bitext bitext
            compat, _swap = BCP47Tag.check_compat_swap(pair1=langs, pair2=self.did.langs)
            return compat
        elif len(self.did.langs) == 1 and len(langs) == 1: # mono mono
            return self.did.langs[0].is_compatible(langs[0])
        else: 
            assert len(self.did.langs) + len(langs) == 3 
            if len(self.did.langs) == 2 and len(langs) == 1: # bitext mono
                pair = self.did.langs
                mono = langs[0]
            elif len(self.did.langs) == 1 and len(langs) == 2: # mono bitext
                mono = self.did.langs[0]
                pair = langs
            else:
                raise Exception(f'Compat check for {self.did.langs} x {langs} is not implemented')
            return mono.is_compatible(pair[0]) or mono.is_compatible(pair[1])  # either side
        
    def __str__(self):
        return self.format(delim=' ')

    @property
    def lang_str(self):
        return self.did.lang_str

    def format(self, delim: str = ' '):
        msg = f'{self.did}{delim}{self.url}{delim}{",".join(self.in_paths or [])}'
        return msg

    def is_noisy(self, seg1, seg2) -> bool:
        # None or Empty
        noisy = seg1 is None or seg2 is None or not seg1.strip() or not seg2.strip()
        return noisy

    class JSONEncoder(json.JSONEncoder):
        def default(self, obj: Any) -> Any:
            if isinstance(obj, Entry):
                state = {}
                for field in obj.__slots__:
                    val = getattr(obj, field)
                    if not val:
                        continue
                    if field == 'did':
                        val = str(val)
                    state[field] = val
                return state
            else:
                return super().default(obj)

class JW300Entry(Entry):
    url: Tuple[str, str, str]  # (align.xml, src.xml, tgt.xml)

