"""20932780 Zhang Hexiao"""

import os
import pickle
from time import perf_counter
from typing import Callable, Iterable

import numpy as np
import pandas as pd
from shapely import Polygon, from_wkt
from tqdm import tqdm

from rect import Rect, random_rectangle
from rtree import RTree

INPUT = "Buildings.xlsx"
os.makedirs("model", exist_ok=True)


def load_data():
    df = pd.read_excel(INPUT)
    polys: list[Polygon] = [from_wkt(polygon) for polygon in df["geometry"]]
    return [(poly, Rect(*poly.bounds)) for poly in polys]


def model_name(fanout: int, max_entries: int):
    return f"./model/model-{fanout}-{max_entries}.pkl"


def load_model(fname: str):
    """Load model if it exists"""
    with open(fname, "rb") as f:
        model: RTree = pickle.load(f)
    return model


def save_model(fname, model):
    """ save the model after the program exits """
    with open(fname, "wb") as f:
        pickle.dump(model, f)


def task1():
    def split_list(lst):
        middle = len(lst) // 2
        return lst[:middle], lst[middle:]

    dataset = load_data()
    first, second = split_list(dataset)

    def trainer(tree: RTree):
        for poly, mbr in tqdm(first):
            tree.insert(poly, mbr)

        print(
            f"Half nodes inserted,\n"
            f"Tree height = {tree.tree_height()}\n"
            f"Leaf and non-leaf nodes = {tree.count_nodes()}"
        )

        for poly, mbr in tqdm(second):
            tree.insert(poly, mbr)
        print(
            f"All nodes inserted,\n"
            f"Tree height = {tree.tree_height()}\n"
            f"Leaf and non-leaf nodes = {tree.count_nodes()}"
        )

    for fanout in (8, 32):
        for max_entries in (64, 256):
            print(f"{fanout=}, {max_entries=}")
            model = RTree(fanout, max_entries)
            trainer(model)
            fname = model_name(fanout, max_entries)
            save_model(fname, model)


def timeit(fn: Callable, times=10):
    elapsed = []
    for _ in range(times):
        start = perf_counter()
        fn()
        elapsed.append(perf_counter() - start)
    tmin, tmax, tavg = np.min(elapsed), np.max(elapsed), np.average(elapsed)
    print(f"min/max/avg time: {tmin:.6f}s {tmax:.6f}s {tavg:.6f}s")
    return tmin, tmax, tavg


def bf_search(dataset: Iterable[Polygon], query: Polygon):
    cnt = 0
    for data in dataset:
        if query.contains(data):
            cnt += 1
    return cnt


def task2():
    tree = load_model(model_name(8, 256))
    dataset = load_data()
    dataset = [data[0] for data in dataset]
    total_mbr = tree.root.get_bounding_rect()
    for i in range(30):
        query_mbr, query_poly = random_rectangle(total_mbr)

        bf_fn = lambda: bf_search(dataset, query_poly)
        bf_ret = bf_fn()
        print(
            f"====== Testcase {i} ======\n"
            f"Got {bf_ret} objects\n"
            f"brute-force algo traversed {len(dataset)} objects"
        )
        timeit(bf_fn)

        tree_fn = lambda: tree.window_query(query_mbr, query_poly)
        tree_ret, tree_tot = tree_fn()
        assert tree_ret == bf_ret, (
            f"The result of Z-value based search "
            f"not equal to brute force search {tree_ret:} != {bf_ret:}"
        )
        print(f"Rtree traversed {tree_tot} objects")
        timeit(tree_fn, 20)


if __name__ == "__main__":
    task1()
    task2()
