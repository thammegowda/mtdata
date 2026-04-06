#!/usr/bin/env python
#
# Created by TG on March 2025
#
# This is util help map a bunch of small files using a single subproc,
# under a few assumptions
# maps line-by-line STDIN->STDOUT, maintains 1:1 mapping and the input order.
# This util was created to optimize time for scoring many small files using
# a subprocess that takes much time to intialize (e.g. loading a large QE metric model)

import argparse
from pathlib import Path
from typing import List, Tuple, Union, Iterator
from itertools import zip_longest

import subprocess as sp
import multiprocessing as mp
import threading as mt
import sys

from mtdata import log
from mtdata.utils import IO

_MAX_QSIZE = 16384 if sys.platform == 'darwin' else 1024 * 1024


#DELIM = '\t'
DELIM = None


class _Sentinel:
    """Singleton sentinel that preserves identity across pickling."""
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __reduce__(self):
        return (self.__class__, ())

SENTINEL = _Sentinel()


def read_paths(paths: Iterator[List[Path]]) -> Iterator[Union[dict,list]]:
    """
    Reads streams of data from the given paths

    :paths: stream of list of paths. each item should have atleast two paths where first is input and last is output. If more than 2 paths are given, the first n-1 paths are "pasted" to form TSV records
    """
    n_data = 0
    n_ctrls = 0
    counter = -1
    for ps in paths:
        try:
            assert len(ps) >= 2, f"Expected two or more paths"
            ps = [Path(p) for p in ps]
            inps = ps[:-1]
            outp = ps[-1]
            yield dict(inputs=inps, output=outp, last_count=counter)  # control record
            n_ctrls += 1
            counter = 0
            #assert len(inps) == 1, f'Currently only single input is suppprted. TODO: support pasting'
            streams = [IO.get_lines(p, col=-1) for p in inps]
            for rec in zip_longest(*streams):
                if len(inps) > 1 and any(x is None for x in rec):
                    raise ValueError(f"Unequal number of lines detected in {inps} @ count: {counter}")
                rec = '\t'.join(x.strip() for x in rec)
                yield rec
                counter += 1
            n_data += counter
            log.info(f"Producer: End of {','.join(str(x) for x in inps)}; count: {counter}")
        except Exception as e:
            log.exception(f"Producer: error in {inps}: {e}")
    log.info(f"Producer: finishing... n_ctrls: {n_ctrls};  n_data: {n_data:,}")


class SubprocMapper:

    def __init__(self, cmdline: str, max_qsize=_MAX_QSIZE, shell=True):
        self.cmdline = cmdline
        self._subproc_args = dict(shell=shell)
        self.ctrl_queue = None
        self.data_queue = None
        self.proc = None
        self._started = False
        self.max_qsize = max_qsize
        self._stop_event = mt.Event()

    def start(self):
        assert not self._started, f'Already started'
        self.ctrl_queue = mp.Queue(maxsize=self.max_qsize)
        self.data_queue = mp.Queue(maxsize=self.max_qsize)
        log.info(f"RUN: {self.cmdline}")
        self.proc = sp.Popen(self.cmdline, stdin=sp.PIPE, stdout=sp.PIPE, text=True, **self._subproc_args)
        self._stop_event.clear()

    def stdin_writer(self, stream: Iterator):
        log.info("STDIN Writer: starting...")
        n_ctrls = 0
        n_data = 0
        try:
            for rec in stream:
                if self._stop_event.is_set():
                    break
                if isinstance(rec, dict):  # control record
                    self.ctrl_queue.put(rec)
                    n_ctrls += 1
                else:  # data record
                    assert isinstance(rec, str), f"string expected, got {type(rec)}"
                    self.proc.stdin.write(rec + '\n')
                    n_data += 1
        except Exception as e:
            log.error(f"STDIN Writer encountered an error: {e}")
            self._stop_event.set()
        finally:
            log.info(f"STDIN Writer: finishing... n_ctrls: {n_ctrls:,}; n_data: {n_data:,}")
            self.proc.stdin.close()
            self.ctrl_queue.put(SENTINEL)

    def stdout_reader(self):
        log.info("STDOUT reader: starting...")
        i = 0
        try:
            for line in self.proc.stdout:
                if self._stop_event.is_set():
                    break
                self.data_queue.put(line.rstrip('\n'))
                i += 1
        except Exception as e:
            log.error(f"STDOUT Reader encountered an error: {e}")
            self._stop_event.set()
        finally:
            log.info(f"STDOUT reader: finishing... n_data: {i:,}")
            self.data_queue.put(SENTINEL)

    def iterator(self) -> Iterator:
        log.info("Data and ctrl merger: starting...")
        yield self.ctrl_queue.get()  # the first ctrl msg; last_count=0
        n_ctrls = 1
        n_data = 0

        ctrl_msg = None
        line_count = 0
        try:
            while not self._stop_event.is_set():
                if ctrl_msg is None and not self.ctrl_queue.empty():
                    ctrl_msg = self.ctrl_queue.get()
                if isinstance(ctrl_msg, dict):
                    if line_count == ctrl_msg['last_count']:
                        yield ctrl_msg
                        n_ctrls += 1
                        line_count = 0
                        ctrl_msg = None
                        continue
                    else:
                        assert line_count < ctrl_msg['last_count']

                rec = self.data_queue.get()
                if rec is SENTINEL:
                    break
                yield rec
                line_count += 1
                n_data += 1
            # data done; ctrl SENTINEL is guaranteed to have arrived
            # (stdin_writer puts it before subprocess closes stdout)
            if ctrl_msg is not SENTINEL:
                ctrl_msg = self.ctrl_queue.get()
            assert ctrl_msg is SENTINEL, f'Expected ctrl SENTINEL, got {ctrl_msg}'
        except Exception as e:
            log.error(f"Iterator encountered an error: {e}")
            self._stop_event.set()
        finally:
            log.info(f"Data and ctrl merger: finishing... n_ctrls: {n_ctrls:,}; n_data: {n_data:,}")

    def map(self, stream: Iterator) -> Iterator:
        try:
            self.start()
            writer_t = mt.Thread(target=self.stdin_writer, args=(stream,))
            writer_t.start()
            reader_t = mt.Thread(target=self.stdout_reader)
            reader_t.start()
            yield from self.iterator()
            writer_t.join(timeout=10)
            reader_t.join(timeout=10)
            # both SENTINELs consumed by iterator; queues must be empty
            assert self.ctrl_queue.empty(), 'ctrl_queue is not empty'
            assert self.data_queue.empty(), 'data_queue is not empty'
        except Exception as e:
            log.error(f"Mapper encountered an error: {e}")
            self._stop_event.set()
            raise
        finally:
            self.close()

    def __call__(self, stream: Iterator) -> Iterator:
        return self.map(stream)

    def close(self):
        self._stop_event.set()
        if self.proc and self.proc.poll() is None:
            log.info(f"terminating subprocess {self.proc.pid}")
            self.proc.terminate()

    @classmethod
    def read_stream(cls, paths: Iterator[List[Path]]) -> Iterator[Union[dict,list]]:
        return read_paths(paths)


def read_input_paths(input, delim=DELIM):
    for line in input:
        parts = line.rstrip("\n")
        if delim:
            parts = parts.split(delim)
        else:
            parts = parts.split() # white spaces
        parts = [Path(p) for p in parts]
        yield parts


def trim_stream(stream, skip=0, limit=0):
    assert skip > 0 or limit > 0
    i = 0
    for rec in stream:
        if skip > 0:
            if i > 0:  # assumption: i == 0 is a ctrl msg, dont skip it
                skip -= 1
                continue
        yield rec
        i += 1
        if limit > 0 and i == limit:
            break


def main():
    args = vars(parse_args())
    paths = read_input_paths(args['input'], delim=args['delim'])
    stream = read_paths(paths)

    n_skip = args.get('skip', 0)
    n_limit = args.get('limit', 0)
    if n_skip > 0 or n_limit > 0:
        log.warning(f"Trimming the stream: skip: {n_skip}; limit:{n_limit}")
        stream = trim_stream(stream, skip=n_skip, limit=n_limit)

    mapper = SubprocMapper(cmdline=args['cmdline'])
    out = None
    try:
        out_stream = mapper(stream)
        for rec in out_stream:
            if isinstance(rec, dict):
                if out is not None:
                    log.info(f"[[closing]] {out.name}")
                    out.close()
                log.info(f"[[opening]] {rec['output']}")
                out_path = Path(rec['output'])
                if args['make_parents']:
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                out = out_path.open('w', encoding='utf-8', errors='replace')
            else:
                assert out is not None, f"Output file is not opened yet"
                out.write(rec + '\n')
    except Exception as e:
        mapper.close()
        raise
    finally:
        if out is not None:
            log.info(f"((closing)) {out.name}")
            out.close()

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--cmd', dest='cmdline', type=str, required=True,
        help="Mapper command that maps line-by-line, maintains 1:1 mapping and the input order. For example: 'cat'")
    parser.add_argument('-i', '--input', type=argparse.FileType('r'), default=sys.stdin,
        help="Listing file containing file paths. Atleast two paths per line is expected first one is input and last one is output")
    parser.add_argument('-d', '--delim', type=str, default=DELIM, help="delimiter for paths in input. default=None => split by all whitespaces (space, tab etc.)")
    parser.add_argument('-l', '--limit', type=int, default=0,
                        help="Limit data stream to these many lines. Score: for debugging and testing")
    parser.add_argument('-s', '--skip', type=int, default=0,
                        help="Skip the first n records. Scope: for debugging and testing")
    parser.add_argument('-p', '--parents',  action='store_true', dest='make_parents',
                        help="Create parent directories for output files if they do not exist")
    # return the parsed arguments
    return parser.parse_args()

if __name__ == '__main__':
    main()