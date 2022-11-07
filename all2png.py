from PIL import Image
from PIL import UnidentifiedImageError
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor


def convert(old):
    if old.suffix == '.png':
        return old
    try:
        x = Image.open(old)
    except UnidentifiedImageError:
        print('Skip', old)
        return old
    new = old.with_suffix('.png')
    x.save(new, 'PNG')
    print(old, '->', new)
    return new


def main():
    print('start')
    files = Path('.').glob('*.*')
    files_list = list(files)
    with ProcessPoolExecutor() as pool:
        results = [pool.submit(convert, i) for i in files_list]
    pool.shutdown(wait=True)
    print('done')


if __name__ == '__main__':
    main()
