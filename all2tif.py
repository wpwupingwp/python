from PIL import Image
from pathlib import Path

files = Path().glob('*.*')
for f in files:
    if f.suffix == '.tif':
        continue
    with Image.open(f) as x:
        new = f.with_suffix('.tif')
        x.save(new, 'TIFF')
        print(f, '->', new)
