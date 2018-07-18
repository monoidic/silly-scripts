#!/usr/bin/env python3

import sys, re

try:
  text = sys.argv[1]
except IndexError:
  print("No argument provided")
  exit(1)
class TranslateClass(object):
  def __getitem__(self, ordinal):
    hexout = ""
    hexchar = bytes(chr(ordinal), "UTF-8").hex()
    if chr(ordinal) in [".","/","?","#", ":"]:
      return(chr(ordinal))
    elif len(hexchar) > 0:
      for i in range(len(hexchar)):
        if i % 2 == 0:
          hexout += "%"
        hexout += hexchar[i]
    return(hexout)
translateobject = TranslateClass()
prefixmatch = re.match(".*://", text)
try:
  prefix = prefixmatch.group()
except AttributeError:
  prefix = ""
translated = prefix + text[len(prefix):].translate(translateobject)
print(translated)
