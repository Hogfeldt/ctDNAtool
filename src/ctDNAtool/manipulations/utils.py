from itertools import tee, count
import numpy as np


def create_index_map(index_lst):
    return dict(zip(index_lst, count()))


def unzip_pair_iter(it):
    it1, it2 = tee(it)
    first_it = (a for a, b in it1)
    second_it = (b for a, b in it2)
    return (first_it, second_it)


def pick_subset_by_row_index(X, index_pairs, n):
    is_tensor = len(X.shape) == 1
    if is_tensor:
        A = np.zeros(n, dtype=object)
    else:
        _, m = X.shape
        A = np.zeros((n, m), dtype=X.dtype)
    for i, j in index_pairs:
        A[i] = X[j]
    return A
