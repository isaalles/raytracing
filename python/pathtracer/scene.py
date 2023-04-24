"""Our scene objects."""
from .hittable import HittableList, Sphere
from . import material
from .vec3 import Color, Point3


def construct_scene(greyshaded=False):
    """Construct 3d scene for rendering."""
    # Materials
    if greyshaded:
        mat_ground = None
        mat_center = None
        mat_left = None
        mat_right = None
    else:
        mat_ground = material.Lambertian(Color(0.8, 0.8, 0.0))
        mat_center = material.Lambertian(Color(0.1, 0.2, 0.5))
        mat_left = material.Dielectric(1.5)
        mat_right = material.Metal(Color(0.8, 0.6, 0.2), 0.0)

    # World scene with materials assigned
    scene = HittableList(
        [
            Sphere(Point3(0.0, -100.5, -1.0), 100.0, material=mat_ground),
            Sphere(Point3(0.0, 0.0, -1.0), 0.5, material=mat_center),
            Sphere(Point3(-1.0, 0.0, -1.0), 0.5, material=mat_left),
            Sphere(Point3(-1.0, 0.0, -1.0), 0.4, material=mat_left),
            Sphere(Point3(1.0, 0.0, -1.0), 0.5, material=mat_right),
        ]
    )

    return scene
