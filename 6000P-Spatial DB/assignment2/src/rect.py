"""20932780 Zhang Hexiao"""

from dataclasses import dataclass
from functools import cached_property, reduce
from random import uniform
from typing import Iterable, Optional

from shapely import Polygon


@dataclass
class Rect:
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    def __str__(self) -> str:
        return f"{self.xmin} {self.ymin} {self.xmax} {self.ymax}"

    @classmethod
    def build_fromstr(cls, s: str):
        return cls(*map(float, s.split()))

    def union(self, rect: "Rect"):
        return Rect(
            xmin=min(self.xmin, rect.xmin),
            ymin=min(self.ymin, rect.ymin),
            xmax=max(self.xmax, rect.xmax),
            ymax=max(self.ymax, rect.ymax),
        )

    def intersects(self, rect: "Rect") -> bool:
        a, b = self, rect
        x1 = max(min(a.xmin, a.xmax), min(b.xmin, b.xmax))
        y1 = max(min(a.ymin, a.ymax), min(b.ymin, b.ymax))
        x2 = min(max(a.xmin, a.xmax), max(b.xmin, b.xmax))
        y2 = min(max(a.ymin, a.ymax), max(b.ymin, b.ymax))
        return x1 < x2 and y1 < y2

    @cached_property
    def area(self):
        return (self.xmax - self.xmin) * (self.ymax - self.ymin)


def union_all(rects: list[Rect]) -> Optional[Rect]:
    if not rects:
        return None
    return reduce(Rect.union, rects[1:], rects[0])


def random_rectangle(mbr: Rect):
    width = uniform(0, mbr.xmax - mbr.xmin) / 16
    height = uniform(0, mbr.ymax - mbr.ymin) / 16
    x = uniform(mbr.xmin, mbr.xmax - width)
    y = uniform(mbr.ymin, mbr.ymax - height)
    polygon = Polygon(
        [(x, y), (x + width, y), (x + width, y + height), (x, y + height), (x, y)]
    )
    rect = Rect(*polygon.bounds)
    return rect, polygon
