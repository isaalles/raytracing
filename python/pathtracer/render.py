"""Render."""

import math
import random

from .camera import Camera
from .hittable import (HittableList, Sphere)
from .ray import Ray
from .vec3 import (
    Color,
    Point3,
    Vec3,
    random_in_unit_sphere,
)


_BLACK = Color(0.0, 0.0, 0.0)
_WHITE = Color(1.0, 1.0, 1.0)
_LIGHT_BLUE = Color(0.5, 0.7, 1.0)


def ray_color(ray: Ray, world: HittableList, depth: int) -> Vec3:
    """Calculate pixel color."""
    # Protect against recursion limit:
    # If we have exceeded the ray bounce limit, no more light is gathered.
    if depth <= 0:
        return _BLACK

    hit, record = world.hit(ray, 0.0, math.inf)
    if hit:
        target = record.point + record.normal + random_in_unit_sphere()
        return 0.5 * ray_color(Ray(record.point, target - record.point), world, depth-1)

    unit_direction = ray.direction.unit_vector()
    parameter = 0.5 * (unit_direction.y + 1.0)  # remap from -1<x<1 to 0<x<1
    # blended_value = (1 - t) * start_value + t * end_value
    return (1 - parameter)*_WHITE + parameter*_LIGHT_BLUE  # lerp


def _scanline(scanline, test=False, **kwargs):
    resx = kwargs.get("resx")
    resy = kwargs.get("resy")
    samples = kwargs.get("samples")
    camera = kwargs.get("camera")
    world = kwargs.get("world")
    max_depth = kwargs.get("max_depth")

    lines = []

    if test:
        for i in range(resx):
            col = Color(i / (resx-1), scanline / (resy-1), 0.2)
            lines.append(col.as_string())

    else:
        for i in range(resx):
            pixel_color = Color(0, 0, 0)
            for _ in range(samples):
                u = (i + random.random()) / (resx - 1)
                v = (scanline + random.random()) / (resy - 1)
                ray = camera.get_ray(u, v)
                # point = ray.point_at_parameter(2.0)
                pixel_color += ray_color(ray, world, max_depth)

            lines.append(pixel_color.as_string(samples))

    return lines


def _image(verbose=False, test=False, **kwargs):
    resy = kwargs.get("resy")

    lines = []

    for j in range(resy-1, -1, -1):
        if verbose:
            print(f"Scanlines remaining: {j}")
        lines.extend(_scanline(j, test=test, **kwargs))

    return lines


def image(path=None, verbose=False):
    """Render image."""
    if not path:
        path = "image.ppm"

    # Image
    aspect_ratio = 2.0 / 1.0
    resx = 200
    resy = int(resx // aspect_ratio)

    samples = 10
    max_depth = 50

    # World
    world = HittableList([
        Sphere(Point3(0, 0, -1), 0.5),
        Sphere(Point3(0, -100.5, -1), 100),
    ])

    # Camera
    # For square pixels, we want the viewport's aspect ratio to match our image's.
    viewport_height = 2.0
    # viewport_width is calculated with the height and the aspect ratio
    focal_length = 1.0

    origin = Point3(0, 0, 0)
    # The horizontal and vertical vectors are origin + the width/height in the
    # corresponding axis; these are calculated directly by the camera object.

    camera = Camera(
        aspect_ratio=aspect_ratio,
        viewport_height=viewport_height,
        focal_length=focal_length,
        origin=origin,
    )

    # Render
    lines = [
        "P3",
        f"{resx} {resy}",
        "255",
    ]

    lines.extend(
        _image(
            verbose=verbose,
            test=False,
            resx=resx,
            resy=resy,
            camera=camera,
            world=world,
            samples=samples,
            max_depth=max_depth,
        )
    )

    with open(path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(lines))
        f.write("\n")

    if verbose:
        print("Done")


def hello_world(path=None, verbose=False):
    """Hello World render of ppm image file."""
    if not path:
        path = "hello_world.ppm"

    # Image
    resx = 200
    resy = 100

    # Render
    lines = [
        "P3",
        f"{resx} {resy}",
        "255",
    ]

    lines.extend(
        _image(
            verbose=verbose,
            test=True,
            resx=resx,
            resy=resy,
        )
    )

    with open(path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(lines))
        f.write("\n")

    if verbose:
        print("Done")


def main():
    """Main entry point."""
    image()
