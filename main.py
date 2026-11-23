#!/usr/bin/env python3
"""Copy the finished front page to the output file.

entry.png sits next to this script, already drawn. All this program does
is copy it to the output location, so it runs anywhere with a plain
Python install: no imaging library, no fonts, no network, no clock, no
randomness. Two runs produce the same bytes.
"""

import os
import shutil
import sys

FALLBACK_DEST = "/output/entry.png"


def run(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = argv[1] if len(argv) > 1 else FALLBACK_DEST
    outdir = os.path.dirname(dst)
    if outdir:
        os.makedirs(outdir, exist_ok=True)
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    run(sys.argv)
