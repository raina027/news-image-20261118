#!/usr/bin/env python3
"""THE WORLD TODAY — front page for Wednesday 18 November 2026.

make.fun competition: news-image-20261118 (program/v1).
Writes one image to /output/entry.png.

The image is baked into this repository as entry.png (rendered by
render.py from 33 stories verified against live reporting on 18 Nov
2026). This program only copies those exact bytes to /output/entry.png,
so it needs no network, no clock and no randomness: two runs write
byte-identical output.

Run:  python3 main.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.png")


def main() -> int:
    if not os.path.isfile(SRC):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
