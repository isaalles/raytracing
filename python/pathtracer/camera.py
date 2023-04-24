"""Camera."""

import math

from .ray import Ray
from .vec3 import (
    random_in_unit_disk,
    Point3,
    Vec3,
)


class Camera:
    """Camera object."""

    def __init__(
        self,
        lookfrom: Point3,
        lookat: Point3,
        vup: Vec3,
        vfov: float,  # vertical field-of-view in degrees
        aspect_ratio: float,
        aperture: float,
        focus_dist: float,
    ):
        theta = math.radians(vfov)
        h = math.tan(theta / 2)
        self.aspect_ratio = aspect_ratio
        self.viewport_height = 2.0 * h
        self.viewport_width = aspect_ratio * self.viewport_height

        self.w = (lookfrom - lookat).unit_vector()
        self.u = vup.cross(self.w).unit_vector()
        self.v = self.w.cross(self.u)

        self.origin = lookfrom
        self.aperture = aperture
        self.focus_dist = focus_dist
        self.horizontal = focus_dist * self.viewport_width * self.u
        self.vertical = focus_dist * self.viewport_height * self.v
        self.lower_left_corner = (
            self.origin - self.horizontal / 2 - self.vertical / 2 - focus_dist * self.w
        )

        self.lens_radius = aperture / 2

    def get_ray(self, s: float, t: float) -> Ray:
        """Camera ray."""
        rd = self.lens_radius * random_in_unit_disk()
        offset = self.u * rd.x + self.v * rd.y

        return Ray(
            self.origin + offset,
            (
                self.lower_left_corner
                + s * self.horizontal
                + t * self.vertical
                - self.origin
                - offset
            ),
        )
