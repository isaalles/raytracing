"""Render."""

import random
import sys

from .camera import Camera
from .hittable import (HittableList, Sphere)
from .ray import Ray
from .vec3 import (Color, Point3, Vec3)


_WHITE = Color(1.0, 1.0, 1.0)
_LIGHT_BLUE = Color(0.5, 0.7, 1.0)


def ray_color(ray: Ray, world: HittableList) -> Vec3:
    """Calculate pixel color."""
    hit, record = world.hit(ray, 0.0, sys.float_info.max)
    if hit:
        return 0.5*Vec3(record.normal.x + 1, record.normal.y + 1, record.normal.z + 1)

    unit_direction = ray.direction.unit_vector()
    parameter = 0.5 * (unit_direction.y + 1.0)  # remap from -1<x<1 to 0<x<1
    return (1 - parameter)*_WHITE + parameter*_LIGHT_BLUE  # lerp


def image(path=None):
    """Render image."""
    if not path:
        path = "image.ppm"

    # Image
    aspect_ratio = 2.0 / 1.0
    resx = 200
    resy = int(resx // aspect_ratio)
    samples = 100

    # Camera
    # For square pixels, we want the viewport's aspect ratio to match our image's.
    viewport_height = 2.0
    viewport_width = aspect_ratio * viewport_height
    focal_length = 1.0
    origin = Point3(0, 0, 0)
    horizontal = Vec3(viewport_width, 0.0, 0.0)
    vertical = Vec3(0.0, viewport_height, 0.0)
    lower_left_corner = origin - horizontal/2 - vertical/2 - Vec3(0, 0, focal_length)
    camera = Camera(lower_left_corner, horizontal, vertical, origin)

    # Render
    lines = [
        "P3",
        f"{resx} {resy}",
        "255",
    ]

    world = HittableList([
        Sphere(Vec3(0, 0, -1), 0.5),
        Sphere(Vec3(0, -100.5, -1), 100),
    ])

    for j in range(resy-1, -1, -1):
        print(f"Scanlines remaining: {j}")
        for i in range(resx):
            col = Vec3(0, 0, 0)
            for _ in range(samples):
                u = (i + random.random()) / (resx - 1)
                v = (j + random.random()) / (resy - 1)
                ray = camera.get_ray(u, v)
                # point = ray.point_at_parameter(2.0)
                col += ray_color(ray, world)

            col /= samples
            lines.append(str((255.99 * col).to_int()))

    with open(path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(lines))
        f.write("\n")

    print("Done")


def hello_world(path=None):
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
    for j in range(resy-1, -1, -1):
        print(f"Scanlines remaining: {j}")
        for i in range(resx):
            col = Color(i / (resx-1), j / (resy-1), 0.2)
            lines.append(col.color_string())

    with open(path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(lines))
        f.write("\n")

    print("Done")


def main():
    """Main entry point."""
    image()
