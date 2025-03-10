
from . import MTDATA_CMD

import subprocess as sp


def test_hf_echo():
    """Test the hf echo command."""
    data_id = "Google-wmt24pp-1-eng-zho_TW"  # an example dataset from HF
    expected_lines = 998
    cmd = f"{MTDATA_CMD} echo {data_id}"
    result = sp.run(cmd, shell=True, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed with error: {result.stderr}"
    out_lines = result.stdout.strip().splitlines()
    assert len(out_lines) == expected_lines, f"Expected {expected_lines} lines, but got {len(out_lines)} lines."