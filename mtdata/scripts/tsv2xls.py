
import argparse
import logging
from pathlib import Path
import logging
import pandas as pd
pd.options.display.float_format = '{:.2f}'.format


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def tsv_to_xls(xls_path:Path, *tsv_paths:Path):
    assert len(tsv_paths) > 0
    if xls_path.suffix != 'xls':
        xls_path = xls_path.parent / (xls_path.name + '.xls')

    log.info(f'Creating Excel book {xls_path}')
    with pd.ExcelWriter(xls_path) as writer:
        for tsv_path in tsv_paths:
            log.info(f'processing {tsv_path}')
            df = pd.read_table(tsv_path, sep='\t')
            df.to_excel(writer, sheet_name=tsv_path.name)
    log.info('All done')

def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a bunch of TSV files into single Excel workbook",
         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('xls', metavar='XLS', help='Output XLS file path', type=Path)
    parser.add_argument('tsv', metavar='TSV', help='Input TSV path(s)',
                        nargs='+', type=Path)
    args = parser.parse_args()
    return vars(args)

def main(**args):
    args = args or parse_args()
    tsv_to_xls(args['xls'], *args['tsv'])


if '__main__' == __name__:
 main()
