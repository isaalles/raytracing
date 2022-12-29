"""Render."""


def hello_world(path=None):
    """Hello World render of ppm image file."""
    if not path:
        path = "hello_world.ppm"

    nx = 200
    ny = 100
    lines = [
        "P3",
        f"{nx} {ny}",
        "255",
    ]
    for j in range(ny-1, 0, -1):
        for i in range(nx):
            r = i / nx
            g = j / ny
            b = 0.2
            ir = int(255.99 * r)
            ig = int(255.99 * g)
            ib = int(255.99 * b)

            lines.append(f"{ir} {ig} {ib}")

    with open(path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(lines))
        f.write("\n")


def main():
    """Main entry point."""
    hello_world()


if __name__ == "__main__":
    main()
