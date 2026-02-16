#!/usr/bin/python3
from pathlib import Path
from sys import argv
from subprocess import run

PROBE_CMD = "ffprobe -show_entries stream=bit_rate -select_streams v -v quiet -of compact=p=0:nk=1"


def get_bitrate(input: Path) -> int:
    cmd = f"{PROBE_CMD} -i {input}"
    result = run(cmd, shell=True, capture_output=True, encoding="utf-8")
    v_bitrate = int(result.stdout.strip())
    return v_bitrate


input_file = Path(argv[1])
output_file = input_file.with_suffix(".small.mp4")
accel = "cuda"
# h.265
v_codec = "hevc_nvenc"
v_bitrate = get_bitrate(input_file)
encode_cmd = f"ffmpeg -hwaccel {accel} -i {input_file} -c:v {v_codec} -c:a copy -b:v {v_bitrate} {output_file}"
r = run(encode_cmd, shell=True)
