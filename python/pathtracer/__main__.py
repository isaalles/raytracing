"""CLI entry point.

To be called with `python -m pathtracer` from inside the dir `python/`.
"""

import argparse
from datetime import timedelta
import enum
import sys
import time

from . import render


class EnumAction(argparse.Action):
    """Argparse action for handling Enums."""

    def __init__(self, **kwargs):
        # Pop off the type value
        enum_type = kwargs.pop("type", None)

        # Ensure an Enum subclass is provided
        if enum_type is None:
            raise ValueError("type must be assigned an Enum when using EnumAction")
        if not issubclass(enum_type, enum.Enum):
            raise TypeError("type must be an Enum when using EnumAction")
        # Generate choices from the Enum
        kwargs.setdefault(
            "choices",
            tuple(  # flat tuple with all the possibilities
                sum(
                    [  # name upper and lower case, int and str value
                        [e.name, e.name.lower(), e.value, str(e.value)]
                        for e in enum_type
                    ],
                    [],
                )
            ),
        )

        super(EnumAction, self).__init__(**kwargs)
        self._enum = enum_type

    def __call__(self, parser, namespace, values, option_string=None):
        # Convert value back into an Enum
        if isinstance(values, str):
            if values.isdigit():
                values = int(values)
            else:
                value = self._enum[values.upper()]
        if isinstance(values, int):
            value = self._enum(values)

        setattr(namespace, self.dest, value)


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(prog="pathtracer")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=("hello-world", "image"),
        default="image",
        help="Render mode. Defaults to `image` i.e. render a scene."
    )
    parser.add_argument(
        "-p", "--path", help="Path to save image to. Defaults to `./image.ppm`"
    )
    parser.add_argument(
        "-d",
        "--diffuse",
        type=render.DIFFUSE_MODE,
        action=EnumAction,
        default=render.DIFFUSE_MODE.SIMPLE,
        dest="diffuse_mode",
        help="Which diffuse mode/implementation to use. Defaults to `simple`.",
    )
    parser.add_argument(
        "-g",
        "--grey",
        action="store_true",
        default=False,
        help=(
            "Whether to render greyshaded (good for testing) "
            "-- only works on the manual scene."
        ),
    )
    parser.add_argument(
        "-m",
        "--manual-scene",
        action="store_true",
        default=False,
        help=(
            "Whether to render the manually built scene. "
            "By default (if not passed) renders the random one."
        ),
    )
    args = parser.parse_args()

    start_time = time.time()
    if args.mode == "hello-world":
        render.hello_world(path=args.path)
    elif args.mode == "image":
        render.image(
            path=args.path,
            diffuse_mode=args.diffuse_mode,
            greyshaded=args.grey,
            randomize=not args.manual_scene,
        )
    else:
        render.main()
    total_time = time.time() - start_time

    print(f"Render took {total_time:0.2f}s -- {timedelta(seconds=total_time)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
