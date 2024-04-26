# this script ensures the data files are sorted
from pathlib import Path
import mtdata
from mtdata import resource_dir
import logging as log


log.basicConfig(level=log.INFO)


def test_sorted_data():
    """Ensure the data files are sorted
    """
    # if this test case fails, see https://twitter.com/thammegowda/status/1783292996773134695
    # probably locale issue while sorting rows
    assert resource_dir.exists()
    tsv_files = list(resource_dir.glob('*.tsv'))
    assert len(tsv_files) > 0
    for file in tsv_files:
        if file.stem == "anuvaad":
            continue  # no sorting enforced
        lines = file.read_text().splitlines(keepends=False)
        log.info(f"Sorting {file}; lines={len(lines)}")

        if file.stem == 'elrc_share':
            # sort by third column i.e., elrc ID
            sorted_lines = list(sorted(lines, key=lambda x: int(x.split('\t')[2])))
        else:
            sorted_lines = list(sorted(lines))
        log.info(f"Sorted {file}; checking if the order is different")
        # assert lines == sorted_lines, f'{file} is not sorted' # this will make pytest hang on "-v"
        for i in range(len(lines)):
            assert lines[i] == sorted_lines[i], f"{file} :: line {i} is different"
        log.info(f"Pass: {file}")
