"""Entry program for the make.fun bounty news-image-20261122.

Draws "The World in One Day" for Sunday 22 November 2026 — a newspaper
front page summing up 48 verified stories from that day — and writes it to
/output/entry.png. The drawing lives in generate_image.py; this file only
chooses the destination and runs it. No network, no clock, no randomness:
two runs write byte-identical output.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_image import render

DEFAULT_OUT = "/output/entry.png"


def main(argv):
    dest = argv[1] if len(argv) > 1 else DEFAULT_OUT
    render(dest)
    print("wrote", dest)


if __name__ == "__main__":
    main(sys.argv)
