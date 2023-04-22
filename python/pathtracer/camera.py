"""Camera."""

from .ray import Ray
from .vec3 import Point3, Vec3


class Camera:
    """Camera object."""

    def __init__(
        self,
        aspect_ratio=None,
        viewport_width=None,
        viewport_height=None,
        focal_length=1.0,
        origin=Point3(0.0, 0.0, 0.0),
        horizontal=None,
        vertical=None,
    ):
        self._aspect_ratio = aspect_ratio
        self._viewport_width = viewport_width
        self._viewport_height = viewport_height
        self.focal_length = focal_length

        self.origin = origin
        self._horizontal = horizontal or Vec3(self.viewport_width, origin.y, origin.z)
        self._vertical = vertical or Vec3(origin.x, viewport_height, origin.z)

    @property
    def viewport_width(self):
        """Return or calculate viewport width if not set."""
        if self._viewport_width is None:
            self._viewport_width = self._aspect_ratio * self._viewport_height
        return self._viewport_width

    @property
    def viewport_height(self):
        """Return or calculate viewport heigth if not set."""
        if self._viewport_height is None:
            self._viewport_height = self._viewport_width / self._aspect_ratio
        return self._viewport_height

    @property
    def aspect_ratio(self):
        """Return or calculate viewport aspect ratio if not set."""
        if self._aspect_ratio is None:
            self._aspect_ratio = self._viewport_width / self._viewport_height
        return self._aspect_ratio

    @property
    def horizontal(self):
        """Return or calculate horizontal space."""
        if self._horizontal is None:
            self._horizontal = Vec3(self.viewport_width, self.origin.y, self.origin.z)
        return self._horizontal

    @property
    def vertical(self):
        """Return or calculate vertical space."""
        if self._vertical is None:
            self._vertical = Vec3(self.origin.x, self.viewport_height, self.origin.z)
        return self._vertical

    @property
    def lower_left_corner(self):
        """Viewport's lower left corner coordinate."""
        return (
            self.origin
            - self.horizontal / 2
            - self.vertical / 2
            - Vec3(0, 0, self.focal_length)
        )

    def get_ray(self, u: float, v: float) -> Ray:
        """Camera ray."""
        return Ray(
            self.origin,
            (
                self.lower_left_corner
                + u * self.horizontal
                + v * self.vertical
                - self.origin
            ),
        )
