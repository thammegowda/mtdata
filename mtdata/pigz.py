import subprocess
import shutil


class SubprocessCompressor:
    """Generic subprocess-based compressor/decompressor. Drop-in replacement for gzip.open/lzma.open/bz2.open."""

    _WBUF_LIMIT = 1 << 20  # 1 MiB write buffer

    def __init__(self, path, mode='r', *, decompress_cmd, compress_cmd=None):
        self.path = path
        self.mode = mode
        self._file = None
        self._wbuf = []
        self._wbuf_size = 0
        self._stdout_file = None  # keep reference to close on write mode
        assert 'b' not in mode, "Binary mode not supported"
        if 'r' in mode:
            self._file = subprocess.Popen(
                decompress_cmd + [str(path)],
                stdin=None, stdout=subprocess.PIPE, bufsize=-1, text=True)
        elif 'w' in mode:
            assert compress_cmd, "compress_cmd required for write mode"
            self._stdout_file = open(path, 'wb')
            self._file = subprocess.Popen(
                compress_cmd,
                stdin=subprocess.PIPE, stdout=self._stdout_file,
                bufsize=-1, text=True)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    def close(self):
        if not self._file:
            return
        if self._wbuf:
            self._file.stdin.write(''.join(self._wbuf))
            self._wbuf.clear()
            self._wbuf_size = 0
        for stream in [self._file.stdin, self._file.stdout, self._file.stderr]:
            if stream:
                stream.close()
        self._file.wait()
        self._file = None
        if self._stdout_file:
            self._stdout_file.close()
            self._stdout_file = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        line = self._file.stdout.readline()
        if not line:
            raise StopIteration
        return line

    def write(self, data):
        if 'w' not in self.mode:
            raise ValueError("File not open for writing")
        self._wbuf.append(data)
        self._wbuf_size += len(data)
        if self._wbuf_size >= self._WBUF_LIMIT:
            self._file.stdin.write(''.join(self._wbuf))
            self._wbuf.clear()
            self._wbuf_size = 0


class pigz(SubprocessCompressor):
    """pigz based file opener. Drop-in replacement for gzip.open"""
    DEF_LEVEL = 6
    PGZ_BIN = shutil.which('pigz')

    @classmethod
    def is_available(cls):
        return cls.PGZ_BIN is not None

    def __init__(self, path, mode='r', level=DEF_LEVEL):
        super().__init__(
            path, mode,
            decompress_cmd=[self.PGZ_BIN, '-dc'],
            compress_cmd=[self.PGZ_BIN, '-c', f'-{level}', '-'],
        )

    @classmethod
    def open(cls, path, mode='rb', level=DEF_LEVEL, **kwargs):
        return cls(path, mode, level)


class xz_subprocess:
    """xz subprocess wrapper. Drop-in replacement for lzma.open (read-only)."""
    XZ_BIN = shutil.which('xz')

    @classmethod
    def is_available(cls):
        return cls.XZ_BIN is not None

    @classmethod
    def open(cls, path, mode='rb', **kwargs):
        assert 'r' in mode, "xz_subprocess only supports read mode"
        # xz -T0 uses all cores for decompression (xz >= 5.4)
        return SubprocessCompressor(
            path, mode.replace('b', ''),
            decompress_cmd=[cls.XZ_BIN, '-dc', '-T0'],
        )


class bzip2_subprocess:
    """bzip2 subprocess wrapper. Uses pbzip2/lbzip2 if available, falls back to bzip2."""
    BZ2_BIN = shutil.which('pbzip2') or shutil.which('lbzip2') or shutil.which('bzip2')

    @classmethod
    def is_available(cls):
        return cls.BZ2_BIN is not None

    @classmethod
    def open(cls, path, mode='rb', **kwargs):
        assert 'r' in mode, "bzip2_subprocess only supports read mode"
        return SubprocessCompressor(
            path, mode.replace('b', ''),
            decompress_cmd=[cls.BZ2_BIN, '-dc'],
        )

