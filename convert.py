#!/usr/bin/env python3

import sys, urllib.parse

if len(sys.argv) != 2:
  print("Invalid amount of arguments passed")
  exit(1)

parsed = urllib.parse.urlparse(sys.argv[1])
if parsed.scheme == "":
  parsed = urllib.parse.urlparse("//" + sys.argv[1])

class TranslateClass(object):
  def __getitem__(self, ordinal):
    hexchar = bytes(chr(ordinal), "UTF-8").hex()
    special_chars = (
      ":", "/", "?", "#", "[", "]", "@", "!", "$",
      "&", "'", "(", ")", "*", "+", ",", ";", "="
    ) #	rfc3986
    if chr(ordinal) in special_chars:
      return chr(ordinal)
    hexout = ""
    for i in range(len(hexchar)):
      if i % 2 == 0:
        hexout += "%"
      hexout += hexchar[i]
    return hexout

tr_obj = TranslateClass()

schemestuff = parsed.scheme + "://" if parsed.scheme else ""
portstuff = ":" + str(parsed.port) if parsed.port else ""
querystuff = "?" + parsed.query.translate(tr_obj) if parsed.query else ""
fragmentstuff = "#" + parsed.fragment.translate(tr_obj) if parsed.fragment  else ""


translated = schemestuff + parsed.hostname.translate(tr_obj) + portstuff
translated = translated + parsed.path.translate(tr_obj) + querystuff + fragmentstuff
print(translated)
