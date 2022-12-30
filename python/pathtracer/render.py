"""Render."""

from .vec3 import Vec3


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
    for j in range(resy-1, 0, -1):
        for i in range(resx):
            col = Vec3(i / resx, j / resy, 0.2)
            lines.append(str((255.99 * col).to_int()))

    with open(path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(lines))
        f.write("\n")


def main():
    """Main entry point."""
    hello_world()
