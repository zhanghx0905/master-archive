''' 20932780 Zhang Hexiao '''

import math
from bisect import bisect_left, bisect_right
from random import uniform

from shapely.geometry import Polygon

from mbr import MBR


class ZIndex:
    def __init__(self, polygons: list[Polygon], zvalues: list[str]):
        self.data = [(str(z), p) for p, z in zip(polygons, zvalues)]
        self.data.sort(key=lambda x: x[0])

    def search(self, query: Polygon, query_zlow: str, query_zhigh: str):
        start = bisect_left(self.data, query_zlow, key=lambda x: x[0])
        end = bisect_right(self.data, query_zhigh, key=lambda x: x[0])
        cnt = 0
        for ind in range(start, end):
            poly = self.data[ind][1]
            if query.contains(poly):
                cnt += 1
        return cnt, end - start + 1


def get_cell_size(length: float, width: float, n: int):
    np = 2**n
    return length / np, width / np


class ZValueGetter:
    def __init__(self, total_mbr: MBR) -> None:
        self.length = total_mbr.xmax - total_mbr.xmin
        self.width = total_mbr.ymax - total_mbr.ymin

    def _cal_cell(self, x, y, n: int):
        seg = get_cell_size(self.length, self.width, n)
        return math.floor(x / seg[0]), math.floor(y / seg[1])

    def _get_zlen(self, target: MBR):
        zlen = 0
        while True:
            zlen += 1
            xhigh, yhigh = self._cal_cell(target.xmax, target.ymax, zlen)
            xlow, ylow = self._cal_cell(target.xmin, target.ymin, zlen)
            if xlow != xhigh or ylow != yhigh:
                zlen -= 1
                break
        return zlen

    def _get_zvals_from_point(self, x, y, resolution: int):
        zval = []
        x, y = self._cal_cell(x, y, resolution)
        for _ in range(resolution):
            zval.append(str((x & 1) * 2 + (y & 1) + 1))
            x >>= 1
            y >>= 1
        zval.reverse()
        return "".join(zval)

    def get_zvals_from_mbr(self, target: MBR, resolutions):
        zlen = self._get_zlen(target)
        zvalue = self._get_zvals_from_point(target.xmin, target.ymin, zlen)
        ret = ["1" + zvalue[: n + 1] + "0" * (n - zlen) for n in resolutions]
        return ret, zlen

    def get_zvals_for_winquery(self, query: MBR, resolutions):
        ret = []
        for n in resolutions:
            # FIXME: is it correct?
            zlen = self._get_zlen(query)
            zlow = self._get_zvals_from_point(query.xmin, query.ymin, zlen)
            zhigh = self._get_zvals_from_point(query.xmax, query.ymax, n)
            ret.append(("1" +zlow, "1" +zhigh))
        return ret


def random_rectangle(mbr: MBR) -> Polygon:
    width = uniform(0, mbr.xmax - mbr.xmin) / 16
    height = uniform(0, mbr.ymax - mbr.ymin) / 16
    x = uniform(mbr.xmin, mbr.xmax - width)
    y = uniform(mbr.ymin, mbr.ymax - height)
    return Polygon(
        [(x, y), (x + width, y), (x + width, y + height), (x, y + height), (x, y)]
    )


def bf_search(dataset: list[Polygon], query: Polygon):
    cnt = 0
    for data in dataset:
        if query.contains(data):
            cnt += 1
    return cnt
