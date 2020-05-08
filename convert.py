#!/usr/bin/env python3

import urllib.parse, ipaddress, re

class TranslateClass(object):
  def __init__(self):
    self.special_chars = (
      ':', '/', '?', '#', '[', ']', '@', '!', '$',
      '&', "'", '(', ')', '*', '+', ',', ';', '='
    ) #	rfc3986

  def __getitem__(self, ordinal):
    if chr(ordinal) in self.special_chars:
      return ordinal
    hexchar = bytes(chr(ordinal), 'UTF-8').hex()
    hexout = ''
    for i in range(0, len(hexchar), 2):
      hexout += '%' + hexchar[i:i+2]
    return hexout

tr_obj = TranslateClass()

def ipv4_obfuscate(addr):
  addr = ipaddress.IPv4Address(addr)
  packed = addr.packed
  octal = f'0{oct(packed[0])[2:]}.0{oct(packed[1])[2:]}.0{oct(packed[2])[2:]}.0{oct(packed[3])[2:]}'
  hex1 = hex(int.from_bytes(packed, 'big'))
  hex2 = f'{hex(packed[0])}.{hex(packed[1])}.{hex(packed[2])}.{hex(packed[3])}'
  dword = str(int.from_bytes(packed, 'big'))

  return [octal, hex1, hex2, dword]

def match_ipv4(hostname):
  pattern = r'[12]?[0-9]{1,2}\.[12]?[0-9]{1,2}\.[12]?[0-9]{1,2}\.[12]?[0-9]{1,2}'
  return re.fullmatch(pattern, hostname) != None

def obfuscate_url(url):
  parsed = urllib.parse.urlparse(url)
  if parsed.netloc == '':
    parsed = urllib.parse.urlparse('//' + url)

  possible_hostnames = [parsed.hostname.translate(tr_obj)]
  if match_ipv4(parsed.hostname):
    possible_hostnames += ipv4_obfuscate(parsed.hostname)

  obf_url = [
    parsed.scheme if parsed.scheme else '',
    'hostname goes here',
    parsed.path.translate(tr_obj),
    '', #params (literally never seen them)
    parsed.query.translate(tr_obj) if parsed.query else '',
    parsed.fragment.translate(tr_obj) if parsed.fragment else ''
  ]
  out_urls = []
  for hostname in possible_hostnames:
    newurl = obf_url.copy()
    newurl[1] = hostname + ':' + str(parsed.port) if parsed.port else hostname
    newurl = urllib.parse.urlunparse(newurl)
    if not parsed.scheme:
      newurl = newurl[2:] # cut off // prefix
    out_urls.append(newurl)
  return out_urls

if __name__ == '__main__':
  import sys
  if len(sys.argv) != 2:
    print('Invalid amount of arguments passed')
    exit(1)

  obf_urls = obfuscate_url(sys.argv[1])
  for url in obf_urls:
    print(url)
