"""Render."""

import math
import multiprocessing
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

_PROCESSES = multiprocessing.cpu_count()


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


def _scanline(scanline, kwargs):
    test = kwargs.get("test", False)
    verbose = kwargs.get("verbose", False)
    resx = kwargs.get("resx", 0)
    resy = kwargs.get("resy", 0)
    samples = kwargs.get("samples", 1)
    camera = kwargs.get("camera")
    world = kwargs.get("world")
    max_depth = kwargs.get("max_depth")

    pixels = []

    if verbose:
        print(f"Scanlines remaining: {scanline}", flush=True)

    if test:
        for i in range(resx):
            pixel_color = Color(i / (resx-1), scanline / (resy-1), 0.2)
            pixels.append(pixel_color.as_string())

    else:
        for i in range(resx):
            pixel_color = Color(0, 0, 0)
            for _ in range(samples):
                u = (i + random.random()) / (resx - 1)
                v = (scanline + random.random()) / (resy - 1)
                ray = camera.get_ray(u, v)
                # point = ray.point_at_parameter(2.0)
                pixel_color += ray_color(ray, world, max_depth)
            pixels.append(pixel_color.as_string(samples))

    return pixels


def _image(verbose=False, test=False, **kwargs):
    resy = kwargs.get("resy")
    kwargs.update({"test": test, "verbose": verbose})

    with multiprocessing.Pool(_PROCESSES) as pool:
        results = pool.starmap(_scanline, ((j, kwargs) for j in range(resy-1, -1, -1)))

    return (pixel_color for pixel_row in results for pixel_color in pixel_row)


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
    header = [
        "P3\n",
        f"{resx} {resy}\n",
        "255\n",
    ]

    pixels = _image(
        verbose=verbose,
        test=False,
        resx=resx,
        resy=resy,
        camera=camera,
        world=world,
        samples=samples,
        max_depth=max_depth,
    )

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(header)
        # `pixels` is a generator so let's extract one value at a time
        for pixel in pixels:
            f.write(f"{pixel}\n")

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
    header = [
        "P3\n",
        f"{resx} {resy}\n",
        "255\n",
    ]

    pixels = _image(
        verbose=verbose,
        test=True,
        resx=resx,
        resy=resy,
    )

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(header)
        for pixel in pixels:
            f.write(f"{pixel}\n")

    if verbose:
        print("Done")


def main():
    """Main entry point."""
    image()
