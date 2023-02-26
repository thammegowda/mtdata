#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/13/20
import io
import gzip
import tarfile
import zipfile
from dataclasses import dataclass
import portalocker
import gzip
import bz2
import lzma

from mtdata import log, Defaults
import shutil
from datetime import datetime
from pathlib import Path

COMPRESSORS = {
    '.gz': gzip.open,
    '.bz2': bz2.open,
    '.xz': lzma.open
}


class IO:
    """File opener and automatic closer
    Copied from my other project https://github.com/isi-nlp/rtg/blob/master/rtg/utils.py
    """
    
    def __init__(self, path, mode='r', encoding=None, errors=None, smart_ext=True):
        """

        Parameters
        ----------
        path: path or pathlke object
        mode: reader
        encoding
        errors
        smart_ext : enable compression when extension .xz or .gz are detected
        """
        self.smart_ext = smart_ext
        if hasattr(path, 'write') or hasattr(path, 'read'):
            self.path = None
            self.fd = path
        if hasattr(path, 'open'):  # pathlib.Path and zipfile.Path has open
            self.fd = None
            self.path = path
        else:
            self.fd = None
            self.path = Path(path)
        self.mode = mode
        self.encoding = encoding or 'utf-8' if 't' in mode else None
        self.errors = errors or 'replace'

    def __enter__(self):
        if not self.path and self.fd is not None: # already opened
            return self.fd

        if self.smart_ext and self.path.suffix in COMPRESSORS:
            open_func = COMPRESSORS[self.path.suffix]
            self.fd = open_func(self.path, self.mode, encoding=self.encoding, errors=self.errors)
        else:
            if 'b' in self.mode:  # binary mode doesnt take encoding or errors
                self.fd = self.path.open(self.mode)
            else:
                self.fd = self.path.open(self.mode, encoding=self.encoding, errors=self.errors, newline='\n')
        return self.fd

    def __exit__(self, _type, value, traceback):
        self.fd.close()
        self.fd = None

    @classmethod
    def reader(cls, path, text=True, **kwargs):
        return cls(path, 'rt' if text else 'rb', **kwargs)

    @classmethod
    def writer(cls, path, text=True, append=False, **kwargs):
        return cls(path, ('a' if append else 'w') + ('t' if text else 'b'), **kwargs)

    @classmethod
    def get_lines(cls, path, col=0, delim='\t', line_mapper=None, newline_fix=True):
        with cls.reader(path) as inp:
            if newline_fix and delim != '\r':
                inp = (line.replace(b'\r', b'') for line in inp)
            if col >= 0:
                inp = (line.split(delim)[col].strip() for line in inp)
            if line_mapper:
                inp = (line_mapper(line) for line in inp)
            yield from inp

    @classmethod
    def get_liness(cls, *paths, **kwargs):
        for path in paths:
            yield from cls.get_lines(path, **kwargs)

    @classmethod
    def write_lines(cls, path: Path, text):
        if isinstance(text, str):
            text = [text]
        with cls.writer(path) as out:
            for line in text:
                out.write(line)
                out.write('\n')

    @classmethod
    def copy_file(cls, src: Path, dest: Path, text=False):
        assert src.resolve() != dest.resolve()
        log.info(f"Copy {src} → {dest}")
        with IO.reader(src, text=text) as inp, IO.writer(dest, text=text) as out:
            shutil.copyfileobj(inp, out)

    @classmethod
    def maybe_backup(cls, file: Path):
        if file.exists():
            time = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            dest = file.with_suffix(f'.{time}')
            log.info(f"Backup {file} → {dest}")
            file.rename(dest)


@dataclass
class ArchivedPath:

    root: Path
    name: str
    fd = None
    
    @property
    def suffix(self):
        return self.root.suffix

    def __post_init__(self):
        assert self.root.exists()
        assert self.name

    def open(self, mode='r', **kwargs):
        raise NotImplemented


@dataclass
class ZipPath (ArchivedPath):
    # there is a bug in stdlib's zipfile.Path https://bugs.python.org/issue40564, so this is a workaround

    def __post_init__(self):
        assert zipfile.is_zipfile(self.root)

    def exists(self):
        with zipfile.ZipFile(self.root) as root:
            #  zipfile.Path is available in 3.8+
            return self.name in root.namelist()

    def open(self, mode='r', **kwargs):
        assert mode in ('r', 'rt'), f'only "r" is supported, given: {mode}'
        log.debug(f"Reading zip: {self.root}?{self.name}")
        container = zipfile.ZipFile(self.root, mode='r')
        stream = container.open(self.name, 'r')
        reader = io.TextIOWrapper(stream, **kwargs)
        reader_close = reader.close  # original close

        def close(*args, **kwargs):
            reader_close()
            stream.close()
            container.close()
        reader.close = close   # hijack
        return reader


@dataclass
class TarPath(ArchivedPath):

    def __post_init__(self):
        self.ext_dir = self.extract()
        matches = list(self.ext_dir.glob(self.name))
        if len(matches) != 1:
            raise Exception(f'expected to find exactly one path inside tarball, but found {matches}')
        self.child = matches[0]
        self.open = self.child.open

    def exists(self):
        return self.child.exists()

    def open_old(self, mode='r', **kwargs):
        assert mode in ('r', 'rt'), f'only "r" is supported, given: {mode}'
        log.info(f"Reading tar: {self.root}?{self.name}")
        container = tarfile.open(self.root, mode='r', encoding='utf-8')
        stream = container.extractfile(self.name)
        reader = io.TextIOWrapper(stream, **kwargs)
        reader_close = reader.close   # original close

        def close(*args, **kwargs):
            reader_close()
            stream.close()
            container and container.close()
        reader.close = close   # hijack
        return reader

    def extract(self):
        dir_name = self.extracted_name()
        out_path = self.root.parent / dir_name
        valid_path = self.root.parent / (dir_name + '.valid')
        lock_path = self.root.parent / (dir_name + '.lock')
        if not valid_path.exists():
            with portalocker.Lock(lock_path, 'w', timeout=Defaults.FILE_LOCK_TIMEOUT) as _:
                if valid_path.exists():
                    return   # extracted by parallel process
                log.info(f"extracting {self.root}")
                with tarfile.open(self.root) as tar:
                    
                    import os
                    
                    def is_within_directory(directory, target):
                        
                        abs_directory = os.path.abspath(directory)
                        abs_target = os.path.abspath(target)
                    
                        prefix = os.path.commonprefix([abs_directory, abs_target])
                        
                        return prefix == abs_directory
                    
                    def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                    
                        for member in tar.getmembers():
                            member_path = os.path.join(path, member.name)
                            if not is_within_directory(path, member_path):
                                raise Exception("Attempted Path Traversal in Tar File")
                    
                        tar.extractall(path, members, numeric_owner=numeric_owner) 
                        
                    
                    safe_extract(tar, out_path)
                valid_path.touch()
        return out_path

    def extracted_name(self):
        exts = ['.tar', '.tar.gz', '.tar.bz2', '.tar.xz']
        name = self.root.name
        dir_name = name + '-extracted'
        for ext in exts:
            if self.root.name.endswith(ext):
                dir_name = name[:-len(ext)]
                break
        return dir_name


def format_byte_size(n: int) -> str:
    """formats byte count into human readable size such as kB, MB, GB..."""
    for power, unit in [(12, 'TB'), (9, 'GB'), (6, 'MB'), (3, 'kB')]:
        if n >= (10 ** power):
            m = n / 10 ** power
            return f'{m:.2f}'.rstrip('0') + f' {unit}'
    return f'{n}B'
