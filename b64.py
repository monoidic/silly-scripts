#!/usr/bin/env python3

import string
import sys

from typing import Union

b64_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'

b64_encode_map = {k: v for k, v in enumerate(b64_chars)}
b64_decode_map = {v: k for k, v in enumerate(b64_chars)}

def my_b64_encode(s: Union[str, bytes]) -> str:
    if isinstance(s, str):
        s = s.encode()

    out = ""

    for i in range(0, len(s), 3):
        block = s[i:i+3]
        data = int.from_bytes(block, 'big')
        pad_n = 3 - len(block)
        data <<= pad_n * 8 # align data
        for shift in range(18, -1, -6)[:len(block)+1]:
            out += b64_encode_map[(data & (63 << shift)) >> shift]
        if pad_n:
            out += pad_n * '='

    return out


def my_b64_decode(s: Union[str, bytes]) -> bytes:
    if isinstance(s, bytes):
        s = s.decode()

    if len(s) % 4:
        raise ValueError("Invalid padding")

    out = b''

    for i in range(0, len(s), 4):
        block = s[i:i+4]
        data = 0
        pad_n = 0
        for c in block:
            if c == '=':
                pad_n += 1
                continue
            data <<= 6
            data += b64_decode_map[c]
        data >>= pad_n * 2
        out += data.to_bytes(3 - pad_n, 'big')

    return out

def main() -> None:
    print(my_b64_encode(b'abcd'))

if __name__ == '__main__':
    main()
