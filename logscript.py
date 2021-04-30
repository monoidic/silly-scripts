#!/usr/bin/env python3

import sys
import time
import re
import signal
import atexit
import ctypes
import ctypes.util
from functools import partial
from typing import Generator

BUF_SIZE = 16 # smallest I could get it to
IN_MODIFY = 2 # from <linux/inotify.h>

linematch = re.compile(r'^\[ *([0-9]+)/([0-9]+)\]'.encode())
_libc = ctypes.CDLL(ctypes.util.find_library('libc.so.6'))

_c_inotify_init = _libc.inotify_init
_c_inotify_add_watch = _libc.inotify_add_watch
_c_inotify_rm_watch = _libc.inotify_rm_watch
_c_read = _libc.read
_c_close = _libc.close

_c_inotify_add_watch.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32)
_c_inotify_rm_watch.argtypes = (ctypes.c_int, ctypes.c_int)
_c_read.argtypes = (ctypes.c_int, ctypes.c_void_p, ctypes.c_size_t)
_c_close.argtypes = (ctypes.c_int,)


def mysleep(path: str) -> Generator[None, None, None]:
    inotify_fd = _c_inotify_init()
    watch = _c_inotify_add_watch(inotify_fd,
            path.encode(), IN_MODIFY)
    buf = ctypes.create_string_buffer(BUF_SIZE)

    atexit.register(partial(_c_close, inotify_fd))
    atexit.register(partial(_c_inotify_rm_watch, inotify_fd, watch))

    while True:
        _c_read(inotify_fd, buf, BUF_SIZE)
        yield None


# TODO \r support

def main() -> None:
    print('\x1b[?25l', end='')
    atexit.register(print, '\x1b[?25h', end='')

    signal.signal(signal.SIGINT, lambda *args: exit())

    logfile = sys.argv[1]

    logfd = open(logfile, 'rb')
    atexit.register(logfd.close)


    logfd.seek(0, 2) # seek to end
    progress = ''
    sleeper = mysleep(logfile)

    while True:
        line = logfd.readline()
        if not line:
            if progress:
                print(progress, end='', flush=True)
            progress = ''
            next(sleeper)
            continue
        match = linematch.search(line)
        if not match:
            continue
        num1, num2 = (int(match.group(i)) for i in (1,2))
        progress = f'\r{match.group().decode()} {num1 / num2 * 100:.2f}%{" " * 5}'
        if num1 == num2:
            progress += 'done!\n'

if __name__ == '__main__':
    main()
