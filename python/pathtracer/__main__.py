"""CLI entry point.

To be called with `python -m pathtracer` from inside the dir `python/`.
"""

import argparse
import sys

from . import render


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(prog="pathtracer")
    parser.add_argument("mode", choices=("hello-world", "image"))
    args = parser.parse_args()
    if args.mode == "hello-world":
        render.hello_world()
    else:
        render.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
