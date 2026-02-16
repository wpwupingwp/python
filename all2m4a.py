from pathlib import Path
from subprocess import run, DEVNULL
from concurrent.futures import ProcessPoolExecutor

m4a = set([".m4a", ".M4A"])
bitrate = "320k"


def convert(old):
    if old.suffix in m4a:
        return old
    new = old.with_suffix(".m4a")
    if new.exists():
        print(f"{new} exists. Skip.")
        return old
    r = run(
        f"ffmpeg -i {old} -b:a {bitrate} {new}",
        shell=True,
        stdout=DEVNULL,
        stderr=DEVNULL,
    )
    if r.returncode != 0:
        print("Convert fail:", old)
        return old
    print(old, "->", new)
    return new


def main():
    print("start")
    files = Path(".").glob("*.*")
    files_list = list(files)
    with ProcessPoolExecutor() as pool:
        results = [pool.submit(convert, i) for i in files_list]
    pool.shutdown(wait=True)
    print("done")


if __name__ == "__main__":
    main()
