"""Hittable object base implementation."""


class HitRecord:
    """To record ray hits."""
    def __init__(self, t, point, normal, front_face=True, material=None):
        self.t = t
        self.point = point
        self.normal = normal
        self.front_face = front_face
        self.material = material

    def set_face_normal(self, ray, outward_normal):
        """Front face vs back face."""
        self.front_face = ray.direction.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else - outward_normal


class Hittable:
    """Hittable base class."""
    def hit(self, ray, t_min: float, t_max: float):
        """Whether the ray hit the object."""
        raise NotImplementedError
