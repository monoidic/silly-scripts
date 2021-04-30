#!/usr/bin/env python3

import re

class ipv4(object):
    _pattern = re.compile(r'\.'.join([r'(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])']*4) + r'/(3[0-2]|[12]?[0-9])')

    def __init__(self, addr: str) -> None:
        if not self._pattern.fullmatch(addr):
            raise ValueError('Invalid IPv4 address given')

        address, subnet = addr.split('/')

        self.address = self._addr_to_bits(address)
        self.subnet_mask = self._subnet_to_mask(int(subnet))
        self.network = self.address & self.subnet_mask

    def __contains__(self, other: 'ipv4') -> bool:
        return other.address & self.subnet_mask == self.network

    def _subnet_to_mask(self, subnet: int) -> int:
        if not isinstance(subnet, int) or subnet < 0 or subnet > 32:
            raise ValueError('Invalid subnet mask')

        return (0xff_ff_ff_ff_00_00_00_00 >> subnet) & 0xff_ff_ff_ff

    def _addr_to_bits(self, address: str) -> int:
        octets = address.split('.')
        if not len(octets) == 4:
            raise ValueError('Invalid octet count in IPv4 address')

        return int.from_bytes(bytes(map(int, octets)), 'big')


def main() -> None:
    host = ipv4('10.20.10.10/32')
    net = ipv4('10.20.0.0/16')

    print(host in net)

if __name__ == '__main__':
    main()
