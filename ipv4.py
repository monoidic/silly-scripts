#!/usr/bin/env python3

import re

def subnet_to_mask(subnet):
  if not isinstance(subnet, int) or subnet < 0 or subnet > 32:
    raise ValueError('Invalid subnet mask')

  return (0xff_ff_ff_ff_00_00_00_00 >> subnet) & 0xff_ff_ff_ff

def addr_to_bits(address):
  address = address.split('.')
  if not len(address) == 4:
    raise ValueError('Invalid octet count in IPv4 address')

  return int.from_bytes(bytes(map(int, address)), 'big')


class ipv4(object):
  def __init__(self, addr):
    pattern = re.compile('\.'.join(['(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])']*4) + '/(3[0-2]|[12]?[0-9])')
    if not pattern.fullmatch(addr):
      raise ValueError('Invalid IPv4 address given')

    address, subnet = addr.split('/')

    self.address = addr_to_bits(address)
    self.subnet_mask = subnet_to_mask(int(subnet))
    self.network = self.address & self.subnet_mask

  def __contains__(self, other):
    return other.address & self.subnet_mask == self.network


host = ipv4('10.20.10.10/32')
net = ipv4('10.20.0.0/16')

print(host in net)
