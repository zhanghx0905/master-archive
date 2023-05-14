
def build_next(P: str):
    next, q = [-1], -1
    for i in range(1, len(P)):
        while q >= 0 and P[q + 1] != P[i]:
            q = next[q]
        if P[q + 1] == P[i]:
            q += 1
        next.append(q)
    return next


def kmp_search(T: str, P: str):
    next, M = build_next(P), len(P)
    q = -1
    for i, c in enumerate(T):
        while q >= 0 and P[q + 1] != c:
            q = next[q]
        if P[q + 1] == c:
            q += 1
        if q + 1 == M:
            return i - M + 1
    return -1


# print(build_next("bbc"))
# print(kmp_search("abbabbbaabbcab", "bbc"))


def suffix_array_bf(s: str, length: int):
    rk = sorted((s[i : i + length], i) for i in range(len(s)))
    rk_deu = {}
    cnt = 0
    for subs, _ in rk:
        if subs not in rk_deu:
            rk_deu[subs] = cnt
            cnt += 1

    sa = [0] * len(rk)
    for subs, idx in rk:
        sa[idx] = rk_deu[subs]

    return rk_deu, sa


# s = 'alotofklokkokko'
# i = 1
# while True:
#     rk, sa = suffix_array_bf(s, i)
#     print(i)
#     pprint(rk)
#     pprint(sa)
#     if i >= len(s):
#         break
#     i *= 2


def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[0] * (n + 1) for _ in range(m + 1)]

    """Following steps build L[m + 1][n + 1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]


def max_increasing_subseq(A: list):
    A_sorted = sorted(A)
    A_sorted = list(dict.fromkeys(A_sorted))
    return lcs(A, A_sorted)


# print(max_increasing_subseq([1, 3, 2, 5, 4]))


