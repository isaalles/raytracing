"""Camera."""

import math

from .ray import Ray
from .vec3 import Point3, Vec3


class Camera:
    """Camera object."""

    def __init__(
        self,
        vfov: float,  # vertical field-of-view in degrees
        aspect_ratio: float,
    ):
        theta = math.radians(vfov)
        h = math.tan(theta / 2)
        self.aspect_ratio = aspect_ratio
        self.viewport_height = 2.0 * h
        self.viewport_width = aspect_ratio * self.viewport_height

        self.focal_length = 1.0

        self.origin = Point3(0.0, 0.0, 0.0)
        self.horizontal = Vec3(self.viewport_width, self.origin.y, self.origin.z)
        self.vertical = Vec3(self.origin.x, self.viewport_height, self.origin.z)

    @property
    def lower_left_corner(self):
        """Viewport's lower left corner coordinate."""
        return (
            self.origin
            - self.horizontal / 2
            - self.vertical / 2
            - Vec3(0, 0, self.focal_length)
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
