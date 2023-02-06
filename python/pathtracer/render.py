"""Render."""

import functools
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

    hit, record = world.hit(ray, 0.0001, math.inf)
    if hit:
        target = record.point + record.normal + random_in_unit_sphere()
        return 0.5 * ray_color(Ray(record.point, target - record.point), world, depth-1)

    unit_direction = ray.direction.unit_vector()
    parameter = 0.5 * (unit_direction.y + 1.0)  # remap from -1<x<1 to 0<x<1
    # blended_value = (1 - t) * start_value + t * end_value
    return (1 - parameter)*_WHITE + parameter*_LIGHT_BLUE  # lerp


def _scanline(scanline, kwargs):
    test = kwargs.get("test", False)
    resx = kwargs.get("resx", 0)
    resy = kwargs.get("resy", 0)
    samples = kwargs.get("samples", 1)
    camera = kwargs.get("camera")
    world = kwargs.get("world")
    max_depth = kwargs.get("max_depth")

    pixels = []

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


def render_progress(tasks_registry, task_num, total, _):
    """Print progress bar.

    This is used as the callback function for pool.apply_async which gets passed
    the process result, thus the use of `_` in the function definition.

    Args:
        tasks_registry (dict): Registry passed by reference to keep track of
            how many tasks of the pool are done.
        task_num (int): The task number that just completed - this not necessarily
            equivalent to the num of tasks done (thus the registry parameter).
        total (int): Total number of tasks expected, so we can calculate the
            percentage of tasks done.

    """
    block_char = "\u2588"
    tasks_registry[str(task_num)] = task_num
    percent = 100 * len(tasks_registry) // total
    progress = block_char * percent + '-' * (100 - percent)
    print(f"Progress: |{progress}| {percent}% complete", end="\r", flush=True)


def _image(test=False, **kwargs):
    resy = kwargs.get("resy")
    kwargs.update({"test": test})

    results = []
    tasks_registry = {}  # used by passing by reference to print the progress bar

    with multiprocessing.Pool(_PROCESSES) as pool:
        pool_results = [
            pool.apply_async(
                _scanline,
                args=(j, kwargs),
                callback=functools.partial(render_progress, tasks_registry, resy-j, resy)
            )
            for j in range(resy-1, -1, -1)
        ]
        results = [result.get() for result in pool_results]

    print()  # ensure new line for future prints
    return (pixel_color for pixel_row in results for pixel_color in pixel_row)


def image(path=None):
    """Render image."""
    if not path:
        path = "image.ppm"

    # Image
    aspect_ratio = 16.0 / 9.0
    resx = 400
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


def hello_world(path=None):
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
        test=True,
        resx=resx,
        resy=resy,
    )

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(header)
        for pixel in pixels:
            f.write(f"{pixel}\n")


def main():
    """Main entry point."""
    image()
