#!/usr/bin/python3

import re
from sys import argv

chinese = '\u4e00-\u9fa5'
# fuhao = r'[‘’“”…、〈〉《》「」『』【】〔〕﹃﹄﹏！（），：；？～￥]'
# use 0x3001-0x3015 ?
fuhao_hex = [0x2018, 0x2019, 0x201c, 0x201d, 0x2026, 0x3001, 0x3002, 0x3008,
             0x3009, 0x300a, 0x300b, 0x300c, 0x300d, 0x300e, 0x300f, 0x3010,
             0x3011, 0x3014, 0x3015, 0xfe43, 0xfe44, 0xfe4f, 0xff01, 0xff08,
             0xff09, 0xff0c, 0xff1a, 0xff1b, 0xff1f, 0xff5e, 0xffe5]
fuhao = ''.join([chr(i) for i in fuhao_hex])
pattern_str = r'([{}{}]) ([{}{}])'.format(chinese, fuhao, chinese, fuhao)
pattern = re.compile(pattern_str)
with open(argv[1], 'r', encoding='utf-8') as old:
    raw = old.read()
with open(argv[1]+'-new.txt', 'w', encoding='utf-8') as new:
    edit = re.sub(pattern, r'\1\2', raw)
    new.write(edit)
