#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/16/21

data = '''
ns,nso
sz,szl
tz,zgh
zz,zza
cb,ckb
cx,bsb
sh,hbs
in,ind
iw,heb
jp,jpn
jap,jpn
daf,dnj
'''
# these are manual mappings from https://wp-info.org/tools/languagecodes.php

CUSTOM_TO_3 = {}
for line in data.splitlines():
    line = line.strip()
    if not line:
        continue
    xx, iso = line.split(',')
    CUSTOM_TO_3[xx] = iso
