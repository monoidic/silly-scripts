#!/usr/bin/env python3

import sys, urllib.parse

if len(sys.argv) != 2:
  print('Invalid amount of arguments passed')
  exit(1)

class TranslateClass(object):
  def __getitem__(self, ordinal):
    special_chars = (
      ':', '/', '?', '#', '[', ']', '@', '!', '$',
      '&', "'", '(', ')', '*', '+', ',', ';', '='
    ) #	rfc3986
    if chr(ordinal) in special_chars:
      return ordinal
    hexchar = bytes(chr(ordinal), 'UTF-8').hex()
    hexout = ''
    for i in range(0, len(hexchar), 2):
      hexout += '%' + hexchar[i:i+2]
    return hexout


tr_obj = TranslateClass()

parsed = urllib.parse.urlparse(sys.argv[1])
if parsed.netloc == '':
  parsed = urllib.parse.urlparse('//' + sys.argv[1])

newurl = (
  parsed.scheme if parsed.scheme else '',
  parsed.hostname.translate(tr_obj) +
    (':' + str(parsed.port) if parsed.port else ''),
  parsed.path.translate(tr_obj),
  '',
  parsed.query.translate(tr_obj) if parsed.query else '',
  parsed.fragment.translate(tr_obj) if parsed.fragment else ''
)

print(urllib.parse.urlunparse(newurl))
