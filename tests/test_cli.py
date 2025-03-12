import json
import subprocess
from typing import List, Union
from mtdata.index import INDEX as index
from pathlib import Path
from tempfile import TemporaryDirectory

from mtdata.utils import IO
from . import MTDATA_CMD

def shrun(cmd: Union[str, List[str]], capture_output=False):
    p = subprocess.run(cmd, shell=isinstance(cmd, str),
            capture_output=True)
    if capture_output:
        return p.returncode, p.stdout
    return p.returncode

def test_cli_help():
    assert shrun(f'{MTDATA_CMD} --help') == 0

def test_cli_list():
    code, out = shrun(f'{MTDATA_CMD} list --id', capture_output=True)
    assert code == 0
    assert len(out.splitlines()) >= len(index.entries)

def test_cli_get():
    with TemporaryDirectory() as out_dir:
        did = 'OPUS-gnome-v1-eng-kan'
        assert shrun(f'{MTDATA_CMD} get -l eng-kan -tr {did} -o {out_dir}') == 0
        assert (Path(out_dir) / 'mtdata.signature.txt').exists()

def test_cache():
    code = shrun(f'{MTDATA_CMD} cache -ri tg01_2to1_test -j3', capture_output=False)
    assert code == 0


def test_get_recipe():
    with TemporaryDirectory() as out_dir:
        code = shrun(f'{MTDATA_CMD} get-recipe -ri tg01_2to1_test -o {out_dir}', capture_output=False)
        assert code == 0

def test_metadata():
    with TemporaryDirectory() as out_dir:
        out_dir = Path(out_dir)
        did = "Statmt-europarl-10-slv-eng"
        code = shrun(f'{MTDATA_CMD} get -l slv-eng -tr {did} -o {out_dir}', capture_output=False)
        assert code == 0
        assert (out_dir / 'mtdata.signature.txt').exists()
        meta_file = out_dir / "train-parts" / f"{did}.meta.jsonl.gz"

        with IO.reader(meta_file) as inp:
            count = 0
            for line in inp:
                meta = json.loads(line)
                assert meta.get('doc_id') is not None
                count += 1
        seg_file = out_dir / "train-parts" / f"{did}.eng"
        seg_count = sum(1 for _ in IO.get_lines(seg_file))
        assert seg_count == count, f"Seg count {seg_count} != meta count {count}"
