"""Material."""

from collections import namedtuple

from .ray import Ray
from .vec3 import (
    random_in_unit_sphere,
    random_unit_vector,
    reflect,
)


_RayAttenuation = namedtuple("RayAttenuation", ["scatter", "attenuation", "scattered"])


class _Material:
    """Base material class implementation."""

    def scatter(self, ray_in, record):
        """Whether we should scatter the light and how."""
        raise NotImplementedError


class Lambertian(_Material):
    """Lambertian (diffuse) material."""

    def __init__(self, albedo):
        super().__init__()
        self.albedo = albedo

    def scatter(self, ray_in, record):
        scatter_direction = record.normal + random_unit_vector()

        # Catch degenerate scatter direction to avoid inf and NaNs.
        if scatter_direction.near_zero():
            scatter_direction = record.normal

        scattered = Ray(record.point, scatter_direction)
        attenuation = self.albedo

        return _RayAttenuation(
            scatter=True,
            attenuation=attenuation,
            scattered=scattered,
        )


class Metal(_Material):
    """Metal."""

    def __init__(self, albedo, fuzz=0.0):
        super().__init__()
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1.0

    def scatter(self, ray_in, record):
        reflected = reflect(ray_in.direction.unit_vector(), record.normal)
        scattered = Ray(record.point, reflected + self.fuzz * random_in_unit_sphere())
        attenuation = self.albedo

        return _RayAttenuation(
            scatter=scattered.direction.dot(record.normal) > 0,
            scattered=scattered,
            attenuation=attenuation,
        )
