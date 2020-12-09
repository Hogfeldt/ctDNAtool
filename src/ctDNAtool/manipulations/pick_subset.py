from functools import partial
from itertools import count

from .utils import create_index_map, unzip_pair_iter, pick_subset_by_row_index
from ..data import Data


def get_id_index_pair_iters_from_ids(index_map, ids):
    pair_iter = map(
        partial(lambda index_map, row_id: (row_id, index_map[row_id]), index_map), ids
    )
    ids_iter, index_iter = unzip_pair_iter(pair_iter)
    new_index_id_pairs = zip(count(), ids_iter)
    new_old_index_pairs = zip(count(), index_iter)
    return (new_index_id_pairs, new_old_index_pairs)


def pick_subset(sample_file, output_file, ids):
    """Given a matrix/tensor and a list of row identifiers, create a
    new matrix/tensor which is a row-wise subset of the given matrix/tensor.

    :param sample_file: File path to the input sample
    :type sample_file: str
    :param output_file: File path to the output matrix
    :type output_file: str
    :param ids: List of row identifiers for the input matrix
    :type ids: List[str]
    :returns:  None
    """
    sample = Data.read(sample_file)
    index_map = create_index_map(sample.region_ids)
    new_index_id_pairs, new_old_index_pairs = get_id_index_pair_iters_from_ids(
        index_map, ids
    )
    sub_sample = pick_subset_by_row_index(sample, new_old_index_pairs, len(ids))
    Data.write(Data(sub_sample, new_index_id_pairs, None), output_file)
