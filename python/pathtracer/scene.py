"""Our scene objects."""

import random

from .hittable import HittableList, Sphere
from . import material
from .vec3 import Color, Point3


def construct_scene(greyshaded=False, randomize=False):
    """Construct 3d scene for rendering."""
    if randomize:
        return _random_scene()
    return _manual_scene(greyshaded=greyshaded)


def _manual_scene(greyshaded=False):
    """Manually construct a scene."""
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


def _random_scene():
    """Construct a random scene."""
    world = HittableList()

    mat_ground = material.Lambertian(Color(0.5, 0.5, 0.5))
    world.append(Sphere(Point3(0, -1000, 0), 1000, mat_ground))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.random()
            center = Point3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())

            if (center - Point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo = Color.random() * Color.random()
                    mat_sphere = material.Lambertian(albedo)
                elif choose_mat < 0.95:
                    # metal
                    albedo = Color.random(0.5, 1)
                    fuzz = random.uniform(0, 0.5)
                    mat_sphere = material.Metal(albedo, fuzz)
                else:
                    # glass
                    mat_sphere = material.Dielectric(1.5)

                world.append(Sphere(center, 0.2, mat_sphere))

    mat_1 = material.Dielectric(1.5)
    world.append(Sphere(Point3(0, 1, 0), 1.0, mat_1))

    mat_2 = material.Lambertian(Color(0.4, 0.2, 0.1))
    world.append(Sphere(Point3(-4, 1, 0), 1.0, mat_2))

    mat_3 = material.Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.append(Sphere(Point3(4, 1, 0), 1.0, mat_3))

    return world
