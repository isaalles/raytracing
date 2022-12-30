"""Vector 3 implementation."""

import math


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
        if isinstance(other, float):
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
        if isinstance(other, float):
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            assert isinstance(other, Vec3)
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        return self

    def __div__(self, other):
        if isinstance(other, float):
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

    def __idiv__(self, other):
        if isinstance(other, float):
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
