from pathlib import Path
from time import sleep

import requests
from faker import Faker

f = Faker(locale='zh')


def get_face(number=5):
    folder = Path('train')
    if not folder.exists():
        folder.mkdir()
    url = 'https://thispersondoesnotexist.com/'
    number = 5
    for _ in range(number):
        r = requests.get(url)
        filename = f.name() + '.webp'
        out = open(filename, 'wb')
        out.write(r.content)
        print('Got', filename)
        sleep(2)
    return folder


import cv2
import numpy as np
from pathlib import Path
names = list()
encodings = list()
train = Path('train')
train_images = train.glob('*.webp')
for i in train_images:
    name = i.stem
    names.append(name)
    encodings.append(encoding)

test = Path('test') / 'trump-sessions-resign.webp'