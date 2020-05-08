#!/usr/bin/env python3

import ctypes as _ctypes
import ctypes.util

# <linux/random.h>
GRND_RANDOM = 0x2
GRND_NONBLOCK = 0x1

_libc = _ctypes.CDLL(_ctypes.util.find_library('c'))

_getrandom = _libc.getrandom
_getrandom.argtypes = (_ctypes.c_void_p, _ctypes.c_ssize_t, _ctypes.c_uint)
_getrandom.restype = _ctypes.c_ssize_t

def getrandom(buflen, flags=0):
  assert flags & ~(GRND_RANDOM | GRND_NONBLOCK) == 0 # the only valid flags
  buf = _ctypes.create_string_buffer(buflen)
  written = _getrandom(buf, buflen, flags)
  ret = buf.raw
  del buf
  if written != buflen: # didn't write enough or returned -1
    if written == -1:
      written = 0
    return ret[:written]
  return ret

def main():
  print('0x' + getrandom(256).hex())

if __name__ == '__main__':
  main()
