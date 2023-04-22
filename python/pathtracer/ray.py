"""Ray."""

from .vec3 import Vec3


class Ray:
    """Ray."""

    def __init__(self, origin: Vec3 = Vec3(), direction: Vec3 = Vec3()):
        self._origin = origin
        self._direction = direction

    @property
    def origin(self) -> Vec3:
        """Ray origin point."""
        return self._origin

    @origin.setter
    def origin(self, origin):
        self._origin = origin

    @property
    def direction(self) -> Vec3:
        """Ray direction vector."""
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    def point_at_parameter(self, parameter: float):
        """Ray point at parameter."""
        return self._origin + parameter * self._direction

    def __str__(self):
        return f"{self._origin} {self._direction}"
