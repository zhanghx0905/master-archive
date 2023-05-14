from typing import Counter


def print_as_mdtable(headers: list, c1, c2):
    print("|  | " + "| ".join(map(str, headers)) + "|")
    print("| ---- |" + "---- |" * len(headers))

    # for c in content:
    print("| true freq | " + "| ".join(map(str, c2)) + "|")
    print("| estimated freq | " + "| ".join(map(str, c1)) + "|")


def MG_count_feq(nums: list[int], k: int):
    table = {}
    for num in nums:
        if num in table:
            table[num] += 1
        elif len(table.keys()) < k - 1:
            table[num] = 1
        else:
            for key in table:
                table[key] -= 1
            remove = {key for key in table if table[key] == 0}
            for key in remove:
                table.pop(key)
    return table


def countmin_sketch(nums: list[int]):
    ''' range [0, 9] '''
    h0 = lambda x: (2 * x + 3) % 5
    h1 = lambda x: (3 * x + 1) % 5
    C = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    for num in nums:
        C[0][h0(num)] += 1
        C[1][h1(num)] += 1
    freq = [0] * 10
    for i in range(10):
        freq[i] = min(C[0][h0(i)], C[1][h1(i)])
    return C, freq


nums = [6, 5, 4, 6, 3, 7, 2, 5, 4, 8, 1, 3, 4, 3, 6, 1, 8, 2, 5, 4, 6, 7, 8, 1, 4, 6, 3, 7, 5, 4]
print(Counter(nums), len(nums), sorted(nums)[14])