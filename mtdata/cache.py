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
from mtdata import log, __version__, pbar_man, MTDataException
from mtdata.utils import ZipPath, TarPath
from typing import List, Union

import portalocker
from hashlib import md5
from urllib.parse import urlparse
from .parser import detect_extension
import requests
import math

MAX_TIMEOUT = 2 * 60 * 60  # 2 hours

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

        local = self.get_local_path(entry.url, filename=entry.filename, fix_missing=fix_missing)
        if zipfile.is_zipfile(local) or tarfile.is_tarfile(local):
            # look inside the archives and get the desired files
            local = self.get_local_in_paths(path=local, entry=entry)
        return local

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

    def get_local_in_paths(self, path:Path, entry: Entry,):
        in_paths = entry.in_paths
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as root:
                in_paths = self.match_globs(names=root.namelist(), globs=in_paths)
            return [ZipPath(path, p) for p in in_paths]   # stdlib is buggy, so I made a workaround
        elif tarfile.is_tarfile(path):
            with tarfile.open(path, encoding='utf-8') as root:
                in_paths = self.match_globs(names=root.getnames(), globs=in_paths)
            return [TarPath(path, p) for p in in_paths]
        else:
            raise Exception(f'Unable to read {entry.did}; the file is neither zip nor tar')

    def download(self, url: str, save_at: Path):
        valid_flag = self.get_flag_file(save_at)
        lock_file = valid_flag.with_suffix("._lock")
        if valid_flag.exists() and save_at.exists():
            return save_at
        save_at.parent.mkdir(parents=True, exist_ok=True)

        log.info(f"Acquiring lock on {lock_file}")
        with portalocker.Lock(lock_file, 'w', timeout=MAX_TIMEOUT) as fh:
            # check if downloaded by  other parallel process
            if valid_flag.exists() and save_at.exists():
                return save_at
            log.info(f"Downloading {url} --> {save_at}")
            resp = requests.get(url=url, allow_redirects=True, headers=headers, stream=True)
            assert resp.status_code == 200, resp.status_code
            buf_size = 2 ** 10
            n_buffers = math.ceil(int(resp.headers.get('Content-Length', '0')) / buf_size) or None
            desc = url
            if len(desc) > 40:
                desc = desc[:30] + '...' + desc[-10:]
            with pbar_man.counter(color='green', total=n_buffers, unit='KiB', leave=False,
                                  desc=f"{desc}") as pbar, open(save_at, 'wb', buffering=2**24) as out:
                for chunk in resp.iter_content(chunk_size=buf_size):
                    out.write(chunk)
                    pbar.update()
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
