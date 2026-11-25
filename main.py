#!/usr/bin/env python3
"""Entry point: copy the pre-rendered infographic to /output/entry.png.

Deterministic: the same bytes are written on every run. No network, no
randomness, no time dependence. The image itself was drawn offline by
compose.py during the build session from the verified 24 Nov 2026 stories
recorded in stories.md.
"""
import os
import shutil

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "image.png")
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(src, os.path.join(OUT_DIR, "entry.png"))


if __name__ == "__main__":
    main()
