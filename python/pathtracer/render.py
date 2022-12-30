"""Render."""

from .ray import Ray
from .vec3 import (unit_vector, Vec3)


_WHITE = Vec3(1.0, 1.0, 1.0)
_LIGHT_BLUE = Vec3(0.5, 0.7, 1.0)


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


def color_blend(
        ray: Ray, start_color: Vec3 = _WHITE, end_color: Vec3 = _LIGHT_BLUE
) -> Vec3:
    """Blend colors vertically."""
    unit_direction = unit_vector(ray.direction)
    parameter = 0.5 * (unit_direction.y + 1.0)
    return (1 - parameter)*start_color + parameter*end_color  # lerp


def image(path=None):
    """Render image."""
    if not path:
        path = "image.ppm"

    resx = 200
    resy = 100
    lines = [
        "P3",
        f"{resx} {resy}",
        "255",
    ]

    lower_left_corner = Vec3(-2.0, -1.0, -1.0)
    horizontal = Vec3(4.0, 0.0, 0.0)
    vertical = Vec3(0.0, 2.0, 0.0)
    origin = Vec3(0.0, 0.0, 0.0)

    for j in range(resy-1, -1, -1):
        for i in range(resx):
            u = i / resx
            v = j / resy
            ray = Ray(origin, lower_left_corner + u*horizontal + v*vertical)
            col = color_blend(ray)
            lines.append(str((255.99 * col).to_int()))

    with open(path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(lines))
        f.write("\n")


def main():
    """Main entry point."""
    image()
