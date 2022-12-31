"""Render."""

import random
import sys

from .camera import Camera
from .hittable import (HittableList, Sphere)
from .ray import Ray
from .vec3 import (unit_vector, Vec3)


_WHITE = Vec3(1.0, 1.0, 1.0)
_LIGHT_BLUE = Vec3(0.5, 0.7, 1.0)


def color(ray: Ray, world: HittableList) -> Vec3:
    """Calculate pixel color."""
    hit, record = world.hit(ray, 0.0, sys.float_info.max)
    if hit:
        return 0.5*Vec3(record.normal.x + 1, record.normal.y + 1, record.normal.z + 1)

    unit_direction = unit_vector(ray.direction)
    parameter = 0.5 * (unit_direction.y + 1.0)  # remap from -1<x<1 to 0<x<1
    return (1 - parameter)*_WHITE + parameter*_LIGHT_BLUE  # lerp


def image(path=None):
    """Render image."""
    if not path:
        path = "image.ppm"

    resx = 200
    resy = 100
    samples = 100
    lines = [
        "P3",
        f"{resx} {resy}",
        "255",
    ]

    camera = Camera()
    world = HittableList([
        Sphere(Vec3(0, 0, -1), 0.5),
        Sphere(Vec3(0, -100.5, -1), 100),
    ])

    for j in range(resy-1, -1, -1):
        for i in range(resx):
            col = Vec3(0, 0, 0)
            for _ in range(samples):
                u = (i + random.random()) / (resx - 1)
                v = (j + random.random()) / (resy - 1)
                ray = camera.get_ray(u, v)
                # point = ray.point_at_parameter(2.0)
                col += color(ray, world)

            col /= samples
            lines.append(str((255.99 * col).to_int()))

    with open(path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(lines))
        f.write("\n")


def hello_world(path=None):
    """Hello World render of ppm image file."""
    if not path:
        path = "hello_world.ppm"

    resx = 200
    resy = 100
    lines = [
        "P3",
        f"{resx} {resy}",
        "255",
    ]
    for j in range(resy-1, -1, -1):
        for i in range(resx):
            col = Vec3(i / resx, j / resy, 0.2)
            lines.append(str((255.99 * col).to_int()))

    with open(path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(lines))
        f.write("\n")


def main():
    """Main entry point."""
    image()
