#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20
from dataclasses import dataclass
from pathlib import Path
from mtdata.index import Entry
from mtdata import log
import wget

@dataclass
class Cache:
    root: Path

    def __post_init__(self):
        if isinstance(self.root, str):
            self.root = Path(self.root)
        log.info(f"Local cache is at {self.root}")

    def get_entry(self, entry: Entry, fix_missing=True) -> Path:

        local = self.get_local_path(entry, fix_missing=fix_missing)
        if entry.is_archive:
            local = self.get_local_in_paths(entry, fix_missing=fix_missing)
        return local

    def get_local_path(self, entry: Entry, fix_missing=True):
        if entry.is_archive:    # exclude name from the path
            local = self.root / entry.filename
        else:
            local =  self.root / entry.name / entry.filename
        if fix_missing:
            if not local.exists() or not local.with_suffix('._valid').exists():
                self.download(entry, local)
                local.with_suffix('._valid').touch()
        return local

    def get_extracted_path(self, entry: Entry, fix_missing=True):
        assert entry.is_archive
        x_path = right_replace(entry.filename, f'.{entry.ext}', '')
        if x_path == entry.filename:
            x_path += '-extracted'
        x_dir =  self.root / x_path
        if fix_missing:
            if not x_dir.exists() or not x_dir.with_suffix('._valid').exists():
                local = self.get_local_path(entry)
                self.extract(local, entry.ext, x_dir)
                x_dir.with_suffix('._valid').touch()
        return x_dir

    def get_local_in_paths(self, entry: Entry, fix_missing=True):
        x_dir = self.get_extracted_path(entry, fix_missing=fix_missing)
        print(x_dir, entry.in_paths)
        return [x_dir / p for p in entry.in_paths]


    def download(self, entry: Entry, save_at: Path):
        save_at.parent.mkdir(parents=True, exist_ok=True)
        log.info(f"GET: {entry.url} --> {save_at}")
        out_file = wget.download(entry.url, out=str(save_at))
        log.info(" Done.")
        assert Path(out_file).resolve() == save_at.resolve()  # saved where we asked it to save
        return save_at

    def extract(self, archive_file: Path, ext: str, x_dir: Path):
        assert archive_file.exists(), f'{archive_file} not found'
        x_dir.mkdir(parents=True, exist_ok=True)
        if ext in {'tar', 'tgz', 'tar.gz', 'tar.bz2', 'tbz2'}:
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