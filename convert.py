#!/usr/bin/env python3

import urllib.parse, ipaddress, re, sys

ipv4_pattern = re.compile('\\.'.join(['(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])'] * 4))
class TranslateClass(dict[int, str]):
    special_chars = set(''':/?#[]@!$&'()*+,;=''')

    def __getitem__(self, ordinal: int) -> str:
        char = chr(ordinal)
        if char in self.special_chars:
            return char
        hexchar = char.encode().hex()
        hexout = ''
        for i in range(0, len(hexchar), 2):
            hexout += '%' + hexchar[i:i+2]
        return hexout

tr_obj = TranslateClass()

def obfuscate_ipv4(adr: str) -> list[str]:
    addr = ipaddress.IPv4Address(adr)
    packed = addr.packed
    octal = '0' + '.0'.join(oct(x)[2:] for x in packed)
    hex1 = hex(int.from_bytes(packed, 'big'))
    hex2 = '.'.join(hex(x) for x in packed)
    dword = str(int.from_bytes(packed, 'big'))

    return [octal, hex1, hex2, dword]

def obfuscate_url(url: str) -> list[str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc == '':
        parsed = urllib.parse.urlparse('//' + url)

    assert parsed.hostname is not None
    possible_hostnames = [parsed.hostname.translate(tr_obj)]
    if ipv4_pattern.fullmatch(parsed.hostname):
        possible_hostnames += obfuscate_ipv4(parsed.hostname)

    obf_url = [
        parsed.scheme if parsed.scheme else '',
        '', # hostname goes here
        parsed.path.translate(tr_obj),
        '', # params (literally never seen them)
        parsed.query.translate(tr_obj) if parsed.query else '',
        parsed.fragment.translate(tr_obj) if parsed.fragment else ''
    ]

    out_urls = []
    for hostname in possible_hostnames:
        url_l = obf_url.copy()
        url_l[1] = f'{hostname}:{parsed.port}' if parsed.port else hostname
        newurl = urllib.parse.urlunparse(url_l)
        if not parsed.scheme:
            newurl = newurl[2:] # cut off // prefix
        out_urls.append(newurl)

    return out_urls

def main() -> None:
    if len(sys.argv) != 2:
        print('Invalid amount of arguments passed')
        exit(1)

    obf_urls = obfuscate_url(sys.argv[1])
    print('\n'.join(obf_urls))

if __name__ == '__main__':
    main()
