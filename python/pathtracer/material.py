"""Material."""

from collections import namedtuple
import math

from .ray import Ray
from .vec3 import (
    Color,
    random_in_unit_sphere,
    random_unit_vector,
    reflect,
    refract,
)


_RayAttenuation = namedtuple("RayAttenuation", ["scatter", "attenuation", "scattered"])
"""tuple: for use as the :func:`scatter` return value.

- scatter (bool): whether the light should scatter,
- atteniation (Color): what colour should it scatter with,
- scattered (Ray): the ray scattered.

"""


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


class Dielectric(_Material):
    """Dielectric."""

    def __init__(self, index_of_refraction):
        super().__init__()
        self.index_of_refraction = index_of_refraction

    def scatter(self, ray_in, record):
        if record.front_face:
            refraction_ratio = 1.0 / self.index_of_refraction
        else:
            refraction_ratio = self.index_of_refraction

        unit_direction = ray_in.direction.unit_vector()
        cos_theta = min(-unit_direction.dot(record.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0
        if cannot_refract:
            # cannot refract, so we reflect
            direction = reflect(unit_direction, record.normal)
        else:
            direction = refract(unit_direction, record.normal, refraction_ratio)

        scattered = Ray(record.point, direction)
        return _RayAttenuation(
            scatter=True,
            attenuation=Color(1.0, 1.0, 1.0),  # glass surface absorbs nothing
            scattered=scattered,
        )
