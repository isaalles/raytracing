"""Camera."""

from .ray import Ray
from .vec3 import Vec3


class Camera:
    """Camera object."""

    def __init__(
        self,
        origin=Vec3(0.0, 0.0, 0.0),
        lower_left_corner=Vec3(-2.0, -1.0, -1.0),
        horizontal=Vec3(4.0, 0.0, 0.0),
        vertical=Vec3(0.0, 2.0, 0.0),
    ):
        self.origin = origin
        self.lower_left_corner = lower_left_corner
        self.horizontal = horizontal
        self.vertical = vertical

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
