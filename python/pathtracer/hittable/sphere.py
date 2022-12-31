"""Sphere hittable object."""

import math

from ._base import (Hittable, HitRecord)


class Sphere(Hittable):
    """Sphere."""
    def __init__(self, center, radius: float):
        self.center = center
        self.radius = radius

    def hit(self, ray, t_min, t_max):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b*b - a*c

        # Find the nearest root that lies in the acceptable range.
        if discriminant >= 0:
            root = (-b - math.sqrt(discriminant)) / a
            if t_min <= root <= t_max:
                point = ray.point_at_parameter(root)
                return (True, HitRecord(root, point, (point - self.center) / self.radius))

            root = (-b + math.sqrt(discriminant)) / a
            if t_min <= root <= t_max:
                point = ray.point_at_parameter(root)
                return (True, HitRecord(root, point, (point - self.center) / self.radius))

        return (False, None)
