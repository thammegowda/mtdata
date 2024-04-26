import subprocess
import shutil


class pigz:
    """pigz based file opener and writer. This should be a drop in replacement for gzip.open"""
    DEF_LEVEL = 6
    PGZ_BIN = shutil.which('pigz')

    @classmethod
    def is_available(cls):
        return cls.PGZ_BIN is not None

    def __init__(self, path, mode='r', level=DEF_LEVEL):
        self.path = path
        self.mode = mode
        self.level = level
        self._file = None
        assert not 'b' in mode, "Binary mode not supported. Use this for reading and writing lines (text mode)"
        assert self.is_available(), "pigz not found in PATH"
        self._open()

    def _open(self):
        if 'r' in self.mode:  # Open the file using pigz subprocess for reading
            self._file = subprocess.Popen(
                [self.PGZ_BIN, '-dc', self.path],
                stdin=None, stdout=subprocess.PIPE, bufsize=-1, text=True
                )
        elif 'w' in self.mode:
            # Open the file using pigz subprocess for writing
            self._file = subprocess.Popen(
                [self.PGZ_BIN, '-c', f'-{self.level}', '-'],
                stdin=subprocess.PIPE, stdout=open(self.path, 'wb'),
                bufsize=-1,
                text=True)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def close(self):
        if not self._file:
            return  # already closed
        # Close the subprocess
        for stream in [self._file.stdin, self._file.stdout, self._file.stderr]:
            if stream:
                stream.close()
        self._file.wait()
        self._file = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self.close()

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
        self._file.stdin.write(data)

    @classmethod
    def open(cls, path, mode='rb', level=DEF_LEVEL, **kwargs):
        """Open a file using pigz subprocess. This should be a drop in replacement for gzip.open"""
        return cls(path, mode, level)

