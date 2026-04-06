"""Progress bar manager using rich, with support for multi-process workers."""

import logging
import os
import threading
from contextlib import contextmanager

from rich.progress import (Progress, TextColumn, BarColumn, TaskProgressColumn,
    TimeElapsedColumn, TimeRemainingColumn, SpinnerColumn)
from rich.console import Console
from rich.logging import RichHandler

console = Console(stderr=True)


class _ProgressAwareRichHandler(RichHandler):
    def emit(self, record):
        with pbar_man.render_lock():
            super().emit(record)


def get_log_handler():
    """Return a RichHandler that coordinates with the progress bars."""
    return _ProgressAwareRichHandler(console=console, show_path=False, show_time=True,
                                     omit_repeated_times=False)


class _PbarManager:
    """A shared rich Progress that supports multiple concurrent tasks.

    Supports remote mode for worker processes: set _queue to a multiprocessing.Queue
    and progress updates will be forwarded to the main process.
    """
    def __init__(self):
        self.enabled = True
        self._lock = threading.RLock()
        self._progress = None
        self._active = 0
        self._queue = None  # set in worker processes for remote mode
        self._columns = [
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=30),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TextColumn("eta"),
            TimeRemainingColumn(),
        ]

    def _start(self):
        with self._lock:
            if self._progress is None:
                self._progress = Progress(*self._columns, console=console, auto_refresh=False)
                self._progress.start()
            self._active += 1

    def _stop(self, task_id):
        with self._lock:
            self._progress.update(task_id, visible=False, refresh=True)
            self._active -= 1
            if self._active <= 0:
                self._progress.stop()
                self._progress = None
                self._active = 0

    def _add_task(self, desc, total=None):
        with self._lock:
            return self._progress.add_task(desc, total=total)

    def _advance(self, task_id, incr=1):
        with self._lock:
            self._progress.update(task_id, advance=incr, refresh=True)

    @contextmanager
    def render_lock(self):
        with self._lock:
            yield

    @contextmanager
    def counter(self, desc='', total=None, unit='it', **kwargs):
        if not self.enabled:
            yield _NoopPbar()
            return
        if self._queue is not None:
            pbar = _RemotePbar(self._queue)
            self._queue.put(('start', pbar._id, desc, total))
            try:
                yield pbar
            finally:
                pbar.flush()
                self._queue.put(('stop', pbar._id))
            return
        self._start()
        task_id = self._add_task(desc, total=total)
        try:
            yield _RichPbar(self, task_id)
        finally:
            self._stop(task_id)

    @contextmanager
    def consume_remote(self, queue):
        """Consume progress events from worker processes and render them in the shared Progress."""
        sentinel = ('shutdown', None)
        remote_tasks = {}

        def _consume():
            while True:
                msg = queue.get()
                kind = msg[0]
                if msg == sentinel:
                    break
                if kind == 'start':
                    _, tid, desc, total = msg
                    ptid = self._add_task(desc, total=total)
                    remote_tasks[tid] = ptid
                elif kind == 'update':
                    _, tid, incr = msg
                    if tid in remote_tasks:
                        self._advance(remote_tasks[tid], incr=incr)
                elif kind == 'stop':
                    _, tid = msg
                    if tid in remote_tasks:
                        with self._lock:
                            self._progress.stop_task(remote_tasks[tid])
                            self._progress.update(remote_tasks[tid], visible=False, refresh=True)
                        del remote_tasks[tid]

        t = threading.Thread(target=_consume, daemon=True)
        t.start()
        try:
            yield
        finally:
            queue.put(sentinel)
            t.join(timeout=5)


class _RichPbar:
    def __init__(self, manager, task_id):
        self._manager = manager
        self._task_id = task_id

    def update(self, incr=1, **kwargs):
        self._manager._advance(self._task_id, incr=incr)


class _RemotePbar:
    """Batches progress updates and sends them via queue at most once per FLUSH_INTERVAL."""
    _counter = 0
    _lock = threading.Lock()
    FLUSH_INTERVAL = 0.5  # seconds

    def __init__(self, queue):
        import time
        with _RemotePbar._lock:
            _RemotePbar._counter += 1
            self._id = (os.getpid(), _RemotePbar._counter)
        self._queue = queue
        self._pending = 0
        self._last_flush = time.monotonic()
        self._time = time

    def update(self, incr=1, **kwargs):
        self._pending += incr
        now = self._time.monotonic()
        if now - self._last_flush >= self.FLUSH_INTERVAL:
            self.flush()

    def flush(self):
        if self._pending > 0:
            self._queue.put(('update', self._id, self._pending))
            self._pending = 0
            self._last_flush = self._time.monotonic()


class _NoopPbar:
    def update(self, incr=1, **kwargs):
        pass


pbar_man = _PbarManager()
