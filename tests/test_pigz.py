from tempfile import TemporaryDirectory
from pathlib import Path

from mtdata import log
from mtdata.utils import pigz, IO


def test_pigz():
    if not pigz.is_available():
        log.warning(f'pigz is unavailable')
        return

    lines = ['Hello', 'World', 'This is a test', 'of pigz']

    with TemporaryDirectory() as tmp_dir:
        tmp_file = Path(tmp_dir) / 'tmp.gz'
        with pigz.open(tmp_file, 'w') as f:
            for line in lines:
                f.write(line + '\n')
        with pigz.open(tmp_file, 'r') as f:
            for got, expected in zip(f, lines):
                assert got.strip() == expected

def test_IO():
    if not pigz.is_available():
        log.warning(f'pigz is unavailable')
        return

    lines = ['Hello', 'World', 'This is a test', 'of pigz']

    with TemporaryDirectory() as tmp_dir:
        tmp_file = Path(tmp_dir) / 'tmp.gz'
        with IO.writer(tmp_file) as out:
            for line in lines:
                out.write(line + '\n')
        with IO.reader(tmp_file) as inp:
            for got, expected in zip(inp, lines):
                assert got.strip() == expected