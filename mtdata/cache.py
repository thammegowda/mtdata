#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20
from dataclasses import dataclass
from pathlib import Path
from mtdata.index import Entry
from mtdata import log
import wget

from hashlib import md5
from urllib.parse import urlparse
from .parser import detect_extension


@dataclass
class Cache:
    root: Path

    def __post_init__(self):
        if isinstance(self.root, str):
            self.root = Path(self.root)
        log.info(f"Local cache is at {self.root}")

    def get_entry(self, entry: Entry, fix_missing=True) -> Path:
        if entry.is_archive or entry.in_ext == 'opus_xces':
            local = self.get_local_in_paths(entry, fix_missing=fix_missing)
        else:
            local = self.get_local_path(entry.url, filename=entry.filename, fix_missing=fix_missing)
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
            if not local.exists() or not self.get_flag_file(local).exists():
                self.download(url, local)
                self.get_flag_file(local).touch()
        return local

    def get_local_in_paths(self, entry: Entry, fix_missing=True):
        if entry.in_ext == 'opus_xces': # this is special case
            l1_url, l2_url = entry.in_paths
            align_file = self.get_local_path(entry.url, fix_missing=fix_missing)
            l1_path = self.get_local_path(l1_url, fix_missing=True)
            l2_path = self.get_local_path(l2_url, fix_missing=True)
            #l1_dir = self._get_extracted_path(l1_url, ext='', fix_missing=fix_missing)
            #l2_dir = self._get_extracted_path(l2_url, ext='', fix_missing=fix_missing)
            #return [align_file, l1_dir, l2_dir]
            return [align_file, l1_path, l2_path]

        x_dir = self.get_extracted_path(entry, fix_missing=fix_missing)
        local_x_path = []
        for p in entry.in_paths:
            if '*' in p: # glob
                paths = list(x_dir.glob(p))
                if not paths:
                    raise Exception(f"{entry} with in path {p} did not find a match")
                local_x_path.extend(paths)
            else:
                local_x_path.append(x_dir / p)
        return local_x_path

    def get_extracted_path(self, entry: Entry, fix_missing=True):
        assert entry.is_archive
        return self._get_extracted_path(url=entry.url, ext=entry.ext, filename=entry.filename,
                                        fix_missing=fix_missing)

    def _get_extracted_path(self, url: str, ext=None, filename=None, fix_missing=True):
        ext = ext or detect_extension(url)
        # path of archive file, local
        local = self.get_local_path(url, filename=filename, fix_missing=fix_missing)
        # path of extract dir:  remove extension from dir name
        local_xdir = local.with_name(right_replace(local.name, f'.{ext}', ''))
        if fix_missing:
            if not local_xdir.exists() or not self.get_flag_file(local_xdir).exists():
                self.extract(local, ext, local_xdir)
                self.get_flag_file(local_xdir).touch()
        return local_xdir

    def download(self, url: str, save_at: Path):
        save_at.parent.mkdir(parents=True, exist_ok=True)
        log.info(f"GET: {url} --> {save_at}")
        out_file = wget.download(url, out=str(save_at))
        log.info(" Done.")
        assert Path(out_file).resolve() == save_at.resolve()  # saved where we asked it to save
        return save_at

    def extract(self, archive_file: Path, ext: str, x_dir: Path):
        assert archive_file.exists(), f'{archive_file} not found'
        x_dir.mkdir(parents=True, exist_ok=True)
        if ext in {'tar', 'tgz', 'tar.gz', 'tar.bz2', 'tbz2', 'tar.xz', 'txz'}:
            log.info(f"Going to extract tar {archive_file} --> {x_dir}")
            import tarfile
            with tarfile.open(archive_file) as tar:
                tar.extractall(path=x_dir)
        elif ext == 'zip':
            log.info(f"Going to extract zip {archive_file} --> {x_dir}")
            from zipfile import ZipFile
            with ZipFile(archive_file) as zip:
                zip.extractall(path=x_dir)
        else:
            raise Exception(f'"{ext}" type extraction not supported')


def right_replace(string, old, new):
    """
    replaces last occurrence of old with new in a string
    :param string:
    :param old:
    :param new:
    :return:
    """
    return new.join(string.rsplit(old))