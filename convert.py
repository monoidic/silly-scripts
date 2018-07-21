#!/usr/bin/env python3

import sys, re

if len(sys.argv) != 2:
  print("Invalid amount of arguments passed")
  exit(1)
text = sys.argv[1]

class TranslateClass(object):
  def __getitem__(self, ordinal):
    hexout = ""
    hexchar = bytes(chr(ordinal), "UTF-8").hex()
    special_chars = (
      "!","*","'","(",")",";",":","@","&",
      "=","+","$",",","/","?","#","[","]"
    ) # "."	rfc3986
    if chr(ordinal) in special_chars:
      return(chr(ordinal))
    elif len(hexchar) > 0:
      for i in range(len(hexchar)):
        if i % 2 == 0:
          hexout += "%"
        hexout += hexchar[i]
    return(hexout)

translateobject = TranslateClass()
prefixmatch = re.match(".*://", text)

if prefixmatch == None:
  prefix = ""
else:
  prefix = prefixmatch.group()

translated = prefix + text[len(prefix):].translate(translateobject)
print(translated)
