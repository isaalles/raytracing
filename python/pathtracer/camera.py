"""Camera."""

import math

from .ray import Ray
from .vec3 import Point3, Vec3


class Camera:
    """Camera object."""

    def __init__(
        self,
        lookfrom: Point3,
        lookat: Point3,
        vup: Vec3,
        vfov: float,  # vertical field-of-view in degrees
        aspect_ratio: float,
    ):
        theta = math.radians(vfov)
        h = math.tan(theta / 2)
        self.aspect_ratio = aspect_ratio
        self.viewport_height = 2.0 * h
        self.viewport_width = aspect_ratio * self.viewport_height

        w = (lookfrom - lookat).unit_vector()
        u = vup.cross(w).unit_vector()
        v = w.cross(u)

        self.origin = lookfrom
        self.horizontal = self.viewport_width * u
        self.vertical = self.viewport_height * v
        self.lower_left_corner = (
            self.origin - self.horizontal / 2 - self.vertical / 2 - w
        )

    def get_ray(self, u: float, v: float) -> Ray:
        """Camera ray."""
        return Ray(
            self.origin,
            (
                self.lower_left_corner
                + u * self.horizontal
                + v * self.vertical
                - self.origin
            ),
        )
