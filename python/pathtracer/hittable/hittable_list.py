"""List of Hittable objects."""

from ._base import Hittable


class HittableList(Hittable):
    """List of hittable items."""
    def __init__(self, hittable_list=None):
        self.hittable_list = hittable_list or []

    def __len__(self):
        return len(self.hittable_list)

    def append(self, other: Hittable):
        """Append item to hittable list."""
        self.hittable_list.append(other)

    def hit(self, ray, t_min, t_max):
        hit_anything = False
        closest_so_far = t_max
        record_so_far = None
        for item in self.hittable_list:
            hit, record = item.hit(ray, t_min, closest_so_far)
            if hit:
                hit_anything = True
                closest_so_far = record.t
                record_so_far = record

        return (hit_anything, record_so_far)
