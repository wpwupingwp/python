#!/usr/bin/python3
from pathlib import Path
import shutil


pwd = Path().cwd().absolute()
result = pwd / (pwd.name+'-result')
if result.exists():
    result = pwd / (pwd.name+'-result2')
result.mkdir()
files1 = pwd.glob('Result.*')
files2 = pwd.glob('*masked*')
for i in files1:
    new_i = result / i.name
    shutil.move(i, new_i)
for i in files2:
    new_i = result / i.name
    shutil.move(i, new_i)
