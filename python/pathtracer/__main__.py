"""CLI entry point.

To be called with `python -m pathtracer` from inside the dir `python/`.
"""

import argparse
import sys

from . import render


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(prog="pathtracer")
    parser.add_argument("mode", nargs="?", choices=("hello-world", "image"), default="image")
    parser.add_argument("-p", "--path")
    args = parser.parse_args()
    if args.mode == "hello-world":
        render.hello_world(args.path)
    elif args.mode == "image":
        render.image(args.path)
    else:
        render.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
