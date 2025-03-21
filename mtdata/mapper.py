import argparse
from pathlib import Path
from typing import List, Tuple, Union, Iterator
from itertools import zip_longest
import subprocess as sp
import multiprocessing as mp
import threading as mt
import queue
import sys

from mtdata import log
from mtdata.utils import IO


DELIM = '\t'
SENTINEL = None

def producer(paths: Iterator[List[Path]]) -> Iterator[Union[dict,list]]:
    """
    Reads streams of data from the given paths

    :paths: stream of list of paths. each item should have atleast two paths where first is input and last is output. If more than 2 paths are given, the first n-1 paths are "pasted" to form TSV records
    """
    n_data = 0
    n_ctrls = 0
    counter = -1
    for ps in paths:
        assert len(ps) >= 2, f"Expected two or more paths"
        ps = [Path(p) for p in ps]
        inps = ps[:-1]
        outp = ps[-1]
        yield dict(inputs=inps, output=outp, last_count=counter)  # control record
        n_ctrls += 1
        counter = 0
        assert len(inps) == 1, f'Currently only single input is suppprted. TODO: support pasting'
        stream = IO.get_lines(inps[0])
        for rec in stream:
            yield rec.strip()  # data record
            counter += 1
        n_data += counter
        log.info(f"Producer: end of {inps}; count: {counter}")
    log.info(f"Producer: finishing... n_ctrls: {n_ctrls};  n_data: {n_data:,}")


def mapper(stream: Iterator, cmdline: str):

    def writer(proc: sp.Popen, stream: Iterator, ctrl_queue: mp.Queue):
        log.info("STDIN Writer: starting...")
        n_ctrls = 0
        n_data = 0
        for rec in stream:
            #log.info(f"Writer rec: {rec}")
            if isinstance(rec, dict): # control record
                ctrl_queue.put(rec)
                n_ctrls += 1
            else: # data record
                assert isinstance(rec, str), f"string expected, got {type(rec)}"
                proc.stdin.write(rec + '\n')
                n_data += 1
        log.info(f"STDIN Writer: finishing... n_ctrls: {n_ctrls:,}; n_data: {n_data:,}")
        proc.stdin.close()
        ctrl_queue.put(SENTINEL)

    def reader(proc: sp.Popen, data_queue: mp.Queue):
        log.info("STDOUT reader: starting...")
        i = 0
        for line in proc.stdout:
            data_queue.put(line.strip('\n'))
            i += 1
        log.info(f"STDOUT reader: finishing... n_data: {i:,}")
        data_queue.put(SENTINEL)

    def merge(ctrl_queue, data_queue):
        log.info("Data and ctrl merger:  strarting...")
        # interleave controls and data; preserve input order; 
        yield ctrl_queue.get() # the first ctrl msg; last_count=0
        ctrl_msg = None
        timeout = 0.5
        i = 0
        n_ctrls = 1
        n_data = 0
        while True:
            #log.info(f"ctrl_msg: {ctrl_msg}")
            if ctrl_msg is None and not ctrl_queue.empty():
                ctrl_msg = ctrl_queue.get(timeout=timeout)
            if ctrl_msg is not None and i == ctrl_msg['last_count']:
                yield ctrl_msg
                # get the next ctrl msg by going back to beginning of loop
                n_ctrls += 1
                i = 0
                ctrl_msg = None
                continue
            rec = data_queue.get()
            if rec is SENTINEL:  # end of queue
                break
            yield rec
            i += 1
            n_data += 1
        log.info(f"Data and ctrl merger: finishing... n_ctrls: {n_ctrls:,}; n_data: {n_data:,}")
        # expect empty queues at the end
        assert ctrl_queue.empty(), 'ctrl_queue is not empty'
        assert data_queue.empty(), 'data_queue is not empty'

    try:
        proc = sp.Popen(cmdline, stdin=sp.PIPE, stdout=sp.PIPE, text=True, shell=True)
        ctrl_queue = mp.Queue()
        data_queue = mp.Queue()
        writer_t = mt.Thread(target=writer, args=(proc, stream, ctrl_queue))
        writer_t.start()
        reader_t = mt.Thread(target=reader, args=(proc, data_queue,))
        reader_t.start()
        yield from merge(ctrl_queue, data_queue)
    finally:
        proc.terminate()


def read_input_paths(input, delim=DELIM):
    for line in input:
        parts = line.rstrip("\n").split(delim)
        parts = [Path(p) for p in parts]
        yield parts

def main():
    args = parse_args()
    args = vars(args)
    paths = read_input_paths(args['input'], delim=args['delim'])

    stream = producer(paths)
    out_stream = mapper(stream, cmdline=args['cmdline'])
    for rec in out_stream:
        print(rec)


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--cmd', dest='cmdline', type=str, required=True,
        help="mapper command that maps line-by-line and maintains 1:1 mapping and input order")
    parser.add_argument('-i', '--input', type=argparse.FileType('r'), default=sys.stdin,
        help="Listing file containing file paths. Atleast two paths per line is expected first one is input and last one is output")
    parser.add_argument('-d', '--delim', type=str, default=DELIM, help="delimiter for paths in input")
    return parser.parse_args()

if __name__ == '__main__':
    main()