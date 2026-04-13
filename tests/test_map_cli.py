import sys
import subprocess
from pathlib import Path
import pytest

pytestmark = pytest.mark.skipif(sys.platform == 'win32', reason='map uses shell subprocesses not available on Windows')


def run_map_cmd(cmd_args, cwd):
    cmd = [sys.executable, '-m', 'mtdata.map', '-c', 'cat', '-i', str(cmd_args['list_file'])]
    if cmd_args.get('make_parents'):
        cmd.append('-p')
    if cmd_args.get('skip'):
        cmd.extend(['-s', str(cmd_args['skip'])])
    if cmd_args.get('limit'):
        cmd.extend(['-l', str(cmd_args['limit'])])
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def test_map_cli_basic(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    # create a simple input file
    inp = tmp_path / 'in1.txt'
    inp.write_text('line1\nline2\n')

    outp = tmp_path / 'out' / 'o1.txt'
    listing = tmp_path / 'list.txt'
    listing.write_text(f"{inp}\t{outp}\n")

    res = run_map_cmd({'list_file': listing, 'make_parents': True}, cwd=repo_root)
    assert res.returncode == 0, f"STDERR:\n{res.stderr}"

    assert outp.exists()
    assert outp.read_text().splitlines() == ['line1', 'line2']


def test_map_cli_skip_limit(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    inp = tmp_path / 'in2.txt'
    inp.write_text('L1\nL2\nL3\n')

    outp = tmp_path / 'out2.txt'
    listing = tmp_path / 'list2.txt'
    listing.write_text(f"{inp}\t{outp}\n")

    # skip=1 should skip the first data line; limit=3 yields ctrl + two data lines
    res = subprocess.run([sys.executable, '-m', 'mtdata.map', '-c', 'cat', '-i', str(listing), '-p', '-s', '1', '-l', '3'],
                         capture_output=True, text=True, cwd=repo_root)
    assert res.returncode == 0, f"STDERR:\n{res.stderr}"

    assert outp.exists()
    assert outp.read_text().splitlines() == ['L2', 'L3']


def test_map_cli_multi_columns(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]

    # first group of three input files
    in1a = tmp_path / 'g1_a.txt'
    in1b = tmp_path / 'g1_b.txt'
    in1c = tmp_path / 'g1_c.txt'
    in1a.write_text('a1\na2\n')
    in1b.write_text('b1\nb2\n')
    in1c.write_text('c1\nc2\n')

    out1 = tmp_path / 'out_g1.txt'

    # second group of three input files
    in2a = tmp_path / 'g2_a.txt'
    in2b = tmp_path / 'g2_b.txt'
    in2c = tmp_path / 'g2_c.txt'
    in2a.write_text('x1\nx2\n')
    in2b.write_text('y1\ny2\n')
    in2c.write_text('z1\nz2\n')

    out2 = tmp_path / 'out_g2.txt'

    listing = tmp_path / 'list_multi.txt'
    listing.write_text(
        f"{in1a}\t{in1b}\t{in1c}\t{out1}\n"
        f"{in2a}\t{in2b}\t{in2c}\t{out2}\n"
    )

    res = subprocess.run([sys.executable, '-m', 'mtdata.map', '-c', 'cat', '-i', str(listing), '-p'],
                         capture_output=True, text=True, cwd=repo_root)
    assert res.returncode == 0, f"STDERR:\n{res.stderr}"

    assert out1.exists()
    assert out1.read_text().splitlines() == ['a1\tb1\tc1', 'a2\tb2\tc2']

    assert out2.exists()
    assert out2.read_text().splitlines() == ['x1\ty1\tz1', 'x2\ty2\tz2']
