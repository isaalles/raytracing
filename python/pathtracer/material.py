"""Material."""

from collections import namedtuple

from .ray import Ray
from .vec3 import (
    random_unit_vector,
    reflect,
)


_RayAttenuation = namedtuple("RayAttenuation", ["scatter", "attenuation", "scattered"])


class _Material:
    """Base material class implementation."""
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray_in, record):
        """Whether we should scatter the light and how."""
        raise NotImplementedError


class Lambertian(_Material):
    """Lambertian (diffuse) material."""

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

    def scatter(self, ray_in, record):
        reflected = reflect(ray_in.direction.unit_vector(), record.normal)
        scattered = Ray(record.point, reflected)
        attenuation = self.albedo

        return _RayAttenuation(
            scatter=scattered.direction.dot(record.normal) > 0,
            scattered=scattered,
            attenuation=attenuation,
        )
