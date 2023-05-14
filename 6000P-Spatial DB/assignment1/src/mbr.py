''' 20932780 Zhang Hexiao '''

from dataclasses import dataclass
from functools import cached_property, reduce

from pyproj import Geod
from shapely import LineString

GEOD = Geod(ellps="WGS84")


@dataclass
class MBR:
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    def __str__(self) -> str:
        return f"{self.xmin} {self.ymin} {self.xmax} {self.ymax}"

    @classmethod
    def build_fromstr(cls, s: str):
        return cls(*map(float, s.split()))

    def proj(self, total_MBR: "MBR"):
        return MBR(
            self.xmin - total_MBR.xmin,
            self.ymin - total_MBR.ymin,
            self.xmax - total_MBR.xmin,
            self.ymax - total_MBR.ymin,
        )

    def union(self, other: "MBR"):
        xmin = min(self.xmin, other.xmin)
        ymin = min(self.ymin, other.ymin)
        xmax = max(self.xmax, other.xmax)
        ymax = max(self.ymax, other.ymax)
        return MBR(xmin, ymin, xmax, ymax)

    @cached_property
    def tlength(self):
        """True length of MBR"""
        return (
            GEOD.geometry_length(
                LineString([(self.xmin, self.ymin), (self.xmax, self.ymin)])
            )
            * 100
        )

    @cached_property
    def twidth(self):
        return (
            GEOD.geometry_length(
                LineString([(self.xmax, self.ymax), (self.xmax, self.ymin)])
            )
            * 100
        )


def get_total_mbr(mbrs: list[MBR]):
    return reduce(lambda x, y: x.union(y), mbrs[1:], mbrs[0])
