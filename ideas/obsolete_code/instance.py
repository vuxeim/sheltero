import os
import sys
import tempfile

if sys.platform != "win32":
    import fcntl

# https://github.com/pycontribs/tendo

class SingleInstanceException(BaseException):
    pass

class SingleInstance(object):
    def __init__(self, path):
        self.initialized = False
        basename = path[1:-1].replace("/", "-").replace("\\", "-").replace(":", "") + '.lock'
        self.lockfile = os.path.normpath(tempfile.gettempdir() + '/' + basename)
        if sys.platform == 'win32':
            try:
                if os.path.exists(self.lockfile):
                    os.unlink(self.lockfile)
                self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            except OSError:
                _, e, _ = sys.exc_info()
                if e.errno == 13:
                    raise SingleInstanceException()
                print(e.errno)
                raise
        else:
            self.fp = open(self.lockfile, 'w')
            self.fp.flush()
            try:
                fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                raise SingleInstanceException()
        self.initialized = True
