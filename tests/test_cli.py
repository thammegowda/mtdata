import subprocess
from typing import List, Union
from mtdata.index import INDEX as index
from pathlib import Path
from tempfile import TemporaryDirectory


def shrun(cmd: Union[str, List[str]], capture_output=False):
    p = subprocess.run(cmd, shell=isinstance(cmd, str),
            capture_output=True)
    if capture_output:
        return p.returncode, p.stdout
    return p.returncode

def test_cli_help():
    assert shrun('python -m mtdata --help') == 0

def test_cli_list():
    code, out = shrun('python -m mtdata list --id', capture_output=True)
    assert code == 0
    assert len(out.splitlines()) >= len(index.entries)

def test_cli_get():
    with TemporaryDirectory() as out_dir:
        did = 'OPUS-gnome-v1-eng-kan'
        assert shrun(f'python -m mtdata get -l eng-kan -tr {did} -o {out_dir}') == 0
        assert (Path(out_dir) / 'mtdata.signature.txt').exists()
