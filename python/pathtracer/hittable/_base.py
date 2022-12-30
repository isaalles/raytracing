"""Hittable object base implementation."""

from collections import namedtuple


HitRecord = namedtuple("HitRecord", ["t", "p", "normal"])


class Hittable:
    """Hittable base class."""
    def hit(self, ray, t_min: float, t_max: float):
        """Whether the ray hit the object."""
        raise NotImplementedError
