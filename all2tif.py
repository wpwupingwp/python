from PIL import Image
from PIL import UnidentifiedImageError
from pathlib import Path

files = Path('.').glob('*.*')
for f in files:
    if f.suffix == '.tif':
        continue
    try:
        x = Image.open(f)
    except UnidentifiedImageError:
        print('Skil', f)
        continue
    new = f.with_suffix('.tif')
    x.save(new, 'TIFF')
    print(f, '->', new)
