"""Sphere hittable object."""

import math

from ._base import Hittable, HitRecord


class Sphere(Hittable):
    """Sphere."""

    def __init__(self, center, radius: float, material=None):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, ray, t_min, t_max):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - a * c

        # Find the nearest root that lies in the acceptable range.
        if discriminant >= 0:
            root = (-b - math.sqrt(discriminant)) / a
            if t_min <= root <= t_max:
                point = ray.point_at_parameter(root)
                normal = (point - self.center) / self.radius
                record = HitRecord(root, point, normal, material=self.material)
                record.set_face_normal(ray, normal)
                return (True, record)

            root = (-b + math.sqrt(discriminant)) / a
            if t_min <= root <= t_max:
                point = ray.point_at_parameter(root)
                normal = (point - self.center) / self.radius
                record = HitRecord(root, point, normal, material=self.material)
                record.set_face_normal(ray, normal)
                return (True, record)

        return (False, None)
