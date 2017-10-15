#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import requests
import re
if __name__ == "__main__":
    name = socket.gethostname()
    ip = socket.gethostbyname(name)
    url = r'http://2017.ip138.com/ic.asp'
    r = requests.get(url)
    txt = r.text

    # ip = txt[txt.find("[") + 1: txt.find("]")]
    ip = re.search(r'\d+\.\d+\.\d+\.\d+', txt).group(0)

    print ip
    print r.status_code
    print r.encoding
    print r.cookies
    print r.raw
    print r.raw.read(1)