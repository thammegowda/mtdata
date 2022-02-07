#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20
import zipfile
import tarfile
import fnmatch
from dataclasses import dataclass
from pathlib import Path
from mtdata.index import Entry
from mtdata import log, __version__, pbar_man, MTDataException, FILE_LOCK_TIMEOUT
from mtdata.utils import ZipPath, TarPath
from mtdata.parser import Parser
from typing import List, Union

import portalocker
from hashlib import md5
from urllib.parse import urlparse
from .parser import detect_extension
import requests
import math


headers = {'User-Agent': f'mtdata downloader {__version__}; cURL and wget like.'}


@dataclass
class Cache:
    root: Path

    def __post_init__(self):
        if isinstance(self.root, str):
            self.root = Path(self.root)
        log.info(f"Local cache is at {self.root}")

    def get_entry(self, entry: Entry, fix_missing=True) -> Union[Path, List[Path]]:
        if entry.in_ext == 'opus_xces':
            return self.opus_xces_format(entry=entry, fix_missing=fix_missing)

        if isinstance(entry.url, (list, tuple)):
            assert isinstance(entry.url[0], str)
            local = [self.get_local_path(url, fix_missing=fix_missing) for url in entry.url]
        else:
            assert isinstance(entry.url, str)
            local = self.get_local_path(entry.url, filename=entry.filename, fix_missing=fix_missing)
            if zipfile.is_zipfile(local) or tarfile.is_tarfile(local):
                # look inside the archives and get the desired files
                local = self.get_local_in_paths(path=local, entry=entry)
        return local

    def get_stats(self, entry: Entry):
        path = self.get_entry(entry)
        parser = Parser(path, ext=entry.in_ext or None, ent=entry)
        count, skips, noise = 0, 0, 0
        toks = [0, 0]
        chars = [0, 0]
        for rec in parser.read_segs():
            if len(rec) < 2 or not rec[0] or not rec[1]:
                skips += 1
                continue
            if entry.is_noisy(seg1=rec[0], seg2=rec[1]):
                noise += 1
                skips += 1
                continue
            count += 1
            s1, s2 = rec[:2]  # get the first two recs
            chars[0] += len(s1)
            chars[1] += len(s2)
            s1_tok, s2_tok = s1.split(), s2.split()
            toks[0] += len(s1_tok)
            toks[1] += len(s2_tok)

        l1, l2 = entry.did.langs
        l1, l2 = l1.lang, l2.lang
        assert count > 0, f'No valid records are found for {entry.did}'
        if l2 < l1:
            l1, l2 = l2, l1
            toks = toks[1], toks[0]
            chars = chars[1], chars[0]
        return {
            'id': str(entry.did),
            'segs': count,
            'segs_err': skips,
            'segs_noise': noise,
            f'{l1}_toks': toks[0],
            f'{l2}_toks': toks[1],
            f'{l1}_chars': chars[0],
            f'{l2}_chars': chars[0]
        }

    def get_flag_file(self, file: Path):
        return file.with_name(file.name + '._valid')

    def get_local_path(self, url, filename=None, fix_missing=True):
        hostname = urlparse(url).hostname or 'nohost'
        filename = filename or url.split('/')[-1]
        assert hostname and filename
        mdf5_sum = md5(url.encode('utf-8')).hexdigest()
        local = self.root / hostname / mdf5_sum[:4] / mdf5_sum[4:] / filename
        if fix_missing:
            self.download(url, local)
        return local

    @classmethod
    def match_globs(cls, names, globs, meta=''):
        result = []
        for pat in globs:
            matches = fnmatch.filter(names, pat)
            if len(matches) != 1:
                raise MTDataException(f'{meta} {pat} matched {matches}; expected one file')
            result.append(matches[0])
        return result

    def opus_xces_format(self, entry, fix_missing=True) -> List[Path]:
        assert entry.in_ext == 'opus_xces'
        l1_url, l2_url = entry.in_paths
        align_file = self.get_local_path(entry.url, fix_missing=fix_missing)
        l1_path = self.get_local_path(l1_url, fix_missing=fix_missing)
        l2_path = self.get_local_path(l2_url, fix_missing=fix_missing)
        return [align_file, l1_path, l2_path]

    def get_local_in_paths(self, path: Path, entry: Entry,):
        in_paths = entry.in_paths
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as root:
                in_paths = self.match_globs(names=root.namelist(), globs=in_paths)
            return [ZipPath(path, p) for p in in_paths]   # stdlib is buggy, so I made a workaround
        elif tarfile.is_tarfile(path):
            return [TarPath(path, p).child for p in in_paths]
        else:
            raise MTDataException(f'Unable to read {entry.did}; the file is neither zip nor tar')

    def download(self, url: str, save_at: Path, timeout=(5, 10)):
        valid_flag = self.get_flag_file(save_at)
        lock_file = valid_flag.with_suffix("._lock")
        if valid_flag.exists() and save_at.exists():
            return save_at
        save_at.parent.mkdir(parents=True, exist_ok=True)

        log.info(f"Acquiring lock on {lock_file}")
        with portalocker.Lock(lock_file, 'w', timeout=FILE_LOCK_TIMEOUT) as fh:
            # check if downloaded by  other parallel process
            if valid_flag.exists() and save_at.exists():
                return save_at
            log.info(f"GET {url} → {save_at}")
            resp = requests.get(url=url, allow_redirects=True, headers=headers, stream=True, timeout=timeout)
            assert resp.status_code == 200, resp.status_code
            buf_size = 2 ** 14
            tot_bytes = int(resp.headers.get('Content-Length', '0'))
            n_buffers = math.ceil(tot_bytes / buf_size) or None
            desc = url
            if len(desc) > 60:
                desc = desc[:30] + '...' + desc[-28:]
            with pbar_man.counter(color='green', total=tot_bytes//2**10, unit='KiB', leave=False, position=2,
                                  desc=f"{desc}") as pbar, open(save_at, 'wb', buffering=2**24) as out:
                for chunk in resp.iter_content(chunk_size=buf_size):
                    out.write(chunk)
                    pbar.update(incr=buf_size//2**10)
            valid_flag.touch()
            lock_file.unlink()
            return save_at


def right_replace(string, old, new):
    """
    replaces last occurrence of old with new in a string
    :param string:
    :param old:
    :param new:
    :return:
    """
    return new.join(string.rsplit(old))
