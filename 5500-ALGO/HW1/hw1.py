from copy import copy
from itertools import tee
from pprint import pprint
from typing import Tuple

# Q2


def gen_permutations(arr: list[int], k: int):
    assert 1 <= k <= len(arr)

    def do_ruc(k: int):
        ret: list[Tuple[list[int], list[int]]] = []

        if k == 1:
            for e in arr:
                arr_ne = copy(arr)
                arr_ne.remove(e)
                ret.append(([e], arr_ne))
            return ret

        perm = do_ruc(k - 1)
        for ele in perm:
            e, arr_ne = ele
            for iter in arr_ne:
                arr_ne_niter = copy(arr_ne)
                arr_ne_niter.remove(iter)
                ret.append((e + [iter], arr_ne_niter))
        return ret

    ret = [i[0] for i in do_ruc(k)]
    pprint(ret)


# gen_permutations([3, 0, 1, 4], 2)


# Q3


def partition(l, r, nums: list[int]):
    # Last element will be the pivot and the first element the pointer
    pivot, ptr = nums[r], l
    for i in range(l, r):
        if nums[i] <= pivot:
            # Swapping values smaller than the pivot to the front
            nums[i], nums[ptr] = nums[ptr], nums[i]
            ptr += 1
    # Finally swapping the last element with the pointer indexed number
    nums[ptr], nums[r] = nums[r], nums[ptr]
    return ptr


def quickselect(l: int, r: int, nums, k):
    """
    select from [l, r]
    """
    if l < r:
        pi = partition(l, r, nums)
        if pi == k - 1:
            return
        elif pi > k - 1:
            quickselect(l, pi - 1, nums, k)  # Recursively sorting the right values
        else:
            quickselect(pi + 1, r, nums, k - pi)  # Recursively sorting the left values


def get_segments(nums: list[int], k: int, i: int):
    n = len(nums)
    assert (n % k == 0) and (1 <= i <= k)
    quickselect(0, n - 1, nums, (i - 1) * n // k)
    quickselect((i - 1) * n // k, n - 1, nums, n / k)
    return nums[(i - 1) * n // k : i * n // k]


def get_kquantile(A, K: int):
    n = len(A)
    assert n % K == 0
    sublen = n // K

    def binary_cal(l: int, r: int, seg: int):
        if seg == 0:
            return
        pi = seg // 2 * sublen
        quickselect(l, r - 1, A, pi)

        binary_cal(l, pi, seg // 2)
        binary_cal(pi, r, seg // 2)

    binary_cal(0, n, K)
    return [A[i * sublen] for i in range(K)]


# example = [2, 5, 6, 1, 3, 4, 7, 8]
# print(get_segments(example, 2, 1))
# print(get_kquantile(example, 4))


def get_skyline_dc(rects: list[list[int]]):
    def merge(left: list[list[int]], right: list[list[int]]):
        i, j = 0, 0
        lh, rh = 0, 0
        ret = []
        x = 0
        while i < len(left) and j < len(right):
            x = min(left[i][0], right[j][0])
            if left[i][0] < right[j][0]:
                lh = left[i][1]
                i += 1
            elif left[i][0] > right[j][0]:
                rh = right[j][1]
                j += 1
            else:
                rh = right[j][1]
                lh = left[i][1]
                i += 1
                j += 1
            h = max(lh, rh)
            if not ret or ret[-1][1] != h:
                ret.append((x, h))
        if i < len(left):
            ret.extend(left[i:])
        if j < len(right):
            ret.extend(right[j:])
        return ret

    if not rects:
        return []
    if len(rects) == 1:
        rect = rects[0]
        return [(rect[0], rect[2]), (rect[1], 0)]

    mid = len(rects) // 2
    left = get_skyline_dc(rects[:mid])
    right = get_skyline_dc(rects[mid:])

    return merge(left, right)


def get_skyline(rects: list[list[int]]):
    ret = get_skyline_dc(rects)
    processed = []
    for i in range(len(ret) - 1):
        cur, next = ret[i], ret[i + 1]
        processed.extend([cur, (next[0], cur[1])])
    processed.append(ret[-1])
    return [ele for ele in processed if ele[1] != 0]


if __name__ == "__main__":
    testcase = [[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]
    skyline = get_skyline(testcase)
    pprint(skyline)
