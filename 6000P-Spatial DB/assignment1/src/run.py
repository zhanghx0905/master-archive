''' 20932780 Zhang Hexiao '''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import percentileofscore
from shapely import from_wkt
from shapely.geometry import Polygon
from tqdm import tqdm

from mbr import *
from zindex import *

INPUT = "Buildings.xlsx"
TASK1_OUT = "Task1.xlsx"
TASK2_OUT = "Task2.xlsx"
RESOLUTIONS = (12, 16, 20)


def print_func_name(func):
    def wrapper(*args, **kwargs):
        print(f"++++++++ {func.__name__} ++++++++")
        return func(*args, **kwargs)

    return wrapper


@print_func_name
def task1():
    df = pd.read_excel(INPUT)
    mbrs: list[MBR] = []
    for polygon in tqdm(df["geometry"]):
        poly: Polygon = from_wkt(polygon)
        mbrs.append(MBR(*poly.bounds))
    total_mbr = get_total_mbr(mbrs)
    print(f"{total_mbr=}")

    df["MBR"] = mbrs
    df.to_excel(TASK1_OUT)

    widths = np.array([mbr.twidth for mbr in mbrs])
    lengths = np.array([mbr.tlength for mbr in mbrs])
    for resolution in RESOLUTIONS:
        length, width = get_cell_size(total_mbr.tlength, total_mbr.twidth, resolution)
        print(
            f"{resolution=}, {length=:.2f} cm, {width=:.2f} cm\n"
            f"width is larger than {percentileofscore(widths, width):.2f}% MBRs, ",
            f"length is larger than {percentileofscore(lengths, length):.2f}% MBRs.",
        )


@print_func_name
def task2():
    df = pd.read_excel(TASK1_OUT)
    mbrs = [MBR.build_fromstr(s) for s in df["MBR"]]
    total_mbr = get_total_mbr(mbrs)
    zvalues = []
    zlens = []
    zgetter = ZValueGetter(total_mbr)
    for mbr in tqdm(mbrs):
        target = mbr.proj(total_mbr)
        zvals, zlen = zgetter.get_zvals_from_mbr(target, RESOLUTIONS)
        zvalues.append(zvals)
        zlens.append(zlen)
    for i, r in enumerate(RESOLUTIONS):
        df[f"z-values {r}"] = [zvals[i] for zvals in zvalues]
    df.to_excel(TASK2_OUT)

    plt.hist(zlens)
    plt.savefig("zlens.png")


@print_func_name
def task3():
    df = pd.read_excel(TASK2_OUT)
    total_mbr = get_total_mbr([MBR.build_fromstr(s) for s in df["MBR"]])
    polygons: list[Polygon] = [from_wkt(v) for v in df["geometry"]]
    indexs: list[ZIndex] = []
    zgetter = ZValueGetter(total_mbr)
    for r in RESOLUTIONS:
        indexs.append(ZIndex(polygons, df[f"z-values {r}"].to_list()))
    for i in range(20):
        query = random_rectangle(total_mbr)
        ret_bf = bf_search(polygons, query)
        print(
            f"====== Testcase {i} ======\n"
            f"Got {ret_bf} objects\n"
            f"brute-force algo traversed {len(polygons)} objects"
        )
        target = MBR(*query.bounds).proj(total_mbr)
        zvals = zgetter.get_zvals_for_winquery(target, RESOLUTIONS)
        for r, index, zvalue in zip(RESOLUTIONS, indexs, zvals):
            zlow, zhigh = zvalue
            ret, tot = index.search(query, zlow, zhigh)
            assert ret == ret_bf, (
                f"The result of Z-value based search "
                f"not equal to brute force search {ret} != {ret_bf}"
            )
            print(f"Z-value algo ({r}) traversed {tot} objects")
        

if __name__ == "__main__":
    task1()
    task2()
    task3()
