#!/usr/bin/python3

import re
from sys import argv

chinese = "\u4e00-\u9fa5"
# fuhao = r'[‘’“”…、〈〉《》「」『』【】〔〕﹃﹄﹏！（），：；？～￥]'
# use 0x3001-0x3015 ?
fuhao_hex = [
    0x2018,
    0x2019,
    0x201C,
    0x201D,
    0x2026,
    0x3001,
    0x3002,
    0x3008,
    0x3009,
    0x300A,
    0x300B,
    0x300C,
    0x300D,
    0x300E,
    0x300F,
    0x3010,
    0x3011,
    0x3014,
    0x3015,
    0xFE43,
    0xFE44,
    0xFE4F,
    0xFF01,
    0xFF08,
    0xFF09,
    0xFF0C,
    0xFF1A,
    0xFF1B,
    0xFF1F,
    0xFF5E,
    0xFFE5,
]
fuhao = "".join([chr(i) for i in fuhao_hex])
pattern_str = r"([{}{}]) ([{}{}])".format(chinese, fuhao, chinese, fuhao)
pattern = re.compile(pattern_str)
with open(argv[1], "r", encoding="utf-8") as old:
    raw = old.read()
with open(argv[1] + "-new.txt", "w", encoding="utf-8") as new:
    edit = re.sub(pattern, r"\1\2", raw)
    new.write(edit)
