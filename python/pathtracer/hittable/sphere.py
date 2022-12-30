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

        if discriminant > 0:
            temp = (-b - math.sqrt(discriminant)) / a
            if t_min < temp < t_max:
                point = ray.point_at_parameter(temp)
                return (True, HitRecord(temp, point, (point - self.center) / self.radius))

            temp = (-b + math.sqrt(discriminant)) / a
            if t_min < temp < t_max:
                point = ray.point_at_parameter(temp)
                return (True, HitRecord(temp, point, (point - self.center) / self.radius))

        return (False, None)
