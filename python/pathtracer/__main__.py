"""CLI entry point.

To be called with `python -m pathtracer` from inside the dir `python/`.
"""

import argparse
import time
import sys

from . import render


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(prog="pathtracer")
    parser.add_argument("mode", nargs="?", choices=("hello-world", "image"), default="image")
    parser.add_argument("-p", "--path")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    start_time = time.time()
    if args.mode == "hello-world":
        render.hello_world(path=args.path, verbose=args.verbose)
    elif args.mode == "image":
        render.image(path=args.path, verbose=args.verbose)
    else:
        render.main()
    print(f"Render took {time.time() - start_time:0.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
