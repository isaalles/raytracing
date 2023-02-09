"""Vector 3 implementation."""

import math
import random


class Vec3:
    """Vector 3 implementation."""
    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self._values = [x, y, z]

    def to_int(self):
        """Cast the 3 vector values to int."""
        self._values = [int(value) for value in self._values]
        return self

    def squared_length(self) -> float:
        """Calculate the vector squared length."""
        return self.x*self.x + self.y*self.y + self.z*self.z

    def length(self) -> float:
        """Calculate vector length."""
        return math.sqrt(self.squared_length())

    def make_unit_vector(self):
        """Transform into a unit vector."""
        k = 1 / self.length()
        self.x *= k
        self.y *= k
        self.z *= k

    def unit_vector(self):
        """Get unit vector."""
        return self / self.length()

    def near_zero(self):
        """Whether the vector is close to zero in all dimensions."""
        zero = 1e-8
        return (
            abs(self.x) < zero
            and abs(self.y) < zero
            and abs(self.z) < zero
        )

    def dot(self, other) -> float:
        """Calculate the dot product with another vector."""
        assert isinstance(other, Vec3)
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """Calculate the cross product with another vector."""
        assert isinstance(other, Vec3)
        return Vec3(
            self.y * other.z - other.y * self.z,
            - (self.x * other.z - other.x * self.z),
            self.x * other.y - other.x * self.y,
        )

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"

    def __len__(self):
        return len(self._values)

    def __getitem__(self, index):
        return self._values[index]

    def __setitem__(self, index, value):
        self._values[index] = value

    def __pos__(self):
        return self

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        assert isinstance(other, Vec3)
        return Vec3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        assert isinstance(other, Vec3)
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other):
        assert isinstance(other, Vec3)
        return Vec3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __isub__(self, other):
        assert isinstance(other, Vec3)
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return Vec3(
                self.x * other,
                self.y * other,
                self.z * other,
            )

        assert isinstance(other, Vec3)
        return Vec3(
            self.x * other.x,
            self.y * other.y,
            self.z * other.z,
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        if isinstance(other, (float, int)):
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            assert isinstance(other, Vec3)
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        return self

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return Vec3(
                self.x / other,
                self.y / other,
                self.z / other,
            )

        assert isinstance(other, Vec3)
        return Vec3(
            self.x / other.x,
            self.y / other.y,
            self.z / other.z,
        )

    def __itruediv__(self, other):
        if isinstance(other, (float, int)):
            factor = 1 / other
            self.x *= factor
            self.y *= factor
            self.z *= factor
        else:
            assert isinstance(other, Vec3)
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        return self

    @property
    def x(self) -> float:
        """X value."""
        return self._values[0]

    @x.setter
    def x(self, value: float):
        self._values[0] = value

    @property
    def r(self) -> float:
        """R value."""
        return self._values[0]

    @r.setter
    def r(self, value: float):
        self._values[0] = value

    @property
    def y(self) -> float:
        """Y value."""
        return self._values[1]

    @y.setter
    def y(self, value: float):
        self._values[1] = value

    @property
    def g(self) -> float:
        """G value."""
        return self._values[1]

    @g.setter
    def g(self, value: float):
        self._values[1] = value

    @property
    def z(self) -> float:
        """Z value."""
        return self._values[2]

    @z.setter
    def z(self, value: float):
        self._values[2] = value

    @property
    def b(self) -> float:
        """B value."""
        return self._values[2]

    @b.setter
    def b(self, value: float):
        self._values[2] = value

    @staticmethod
    def random(min_value=None, max_value=None):
        """Generate random vector."""
        if min_value is None or max_value is None:
            return Vec3(random.random(), random.random(), random.random())
        return Vec3(
            random.uniform(min_value, max_value),
            random.uniform(min_value, max_value),
            random.uniform(min_value, max_value)
        )


class Point3(Vec3):
    """Point"""


class Color(Vec3):
    """Color."""
    def as_string(self, samples_per_pixel=1):
        """Translate to a [0, 255] color value as string for each component."""
        r = self.r
        g = self.g
        b = self.b

        # Divide the color by the number of samples and gamma-correct for gamma=2.0.
        # Which means raising the color to the power 1/gamma, which in our case
        # is 1/2 i.e. the square root.
        scale = 1 / samples_per_pixel
        color = Color(
            clamp(math.sqrt(scale * r), 0.0, 0.999),
            clamp(math.sqrt(scale * g), 0.0, 0.999),
            clamp(math.sqrt(scale * b), 0.0, 0.999),
        )
        return str((256 * color).to_int())


def clamp(value, min_value, max_value):
    """Clamp value in between a mix and max."""
    return max(min(value, max_value), min_value)


def random_in_unit_sphere():
    """Rejection method to check if a point in a unit cube is also inside a unit sphere."""
    while True:
        point = Vec3.random(-1, 1)
        if point.squared_length() >= 1:
            continue
        return point


def random_unit_vector():
    """Unit random in sphere vector."""
    return random_in_unit_sphere().unit_vector()


def random_in_hemisphere(normal):
    """Check if point is in the same hemisphere as the normal."""
    in_unit_sphere = random_in_unit_sphere()
    if in_unit_sphere.dot(normal) > 0.0:
        return in_unit_sphere
    return -in_unit_sphere


def reflect(vector_a, vector_b):
    """Reflected ray."""
    return vector_a - 2 * vector_a.dot(vector_b) * vector_b
