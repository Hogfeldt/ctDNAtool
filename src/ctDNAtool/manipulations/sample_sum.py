from functools import reduce, partial
import numpy as np
import logging

from ..data import Data, astype

logger = logging.getLogger()


def add_if_eq_region(x, y):
    if x.region_ids != y.region_ids:
        # TODO: There should be some exception handling
        logger.warning("region ids does not match!")
    else:
        x.data += y.data
        return x


def sample_sum(sample_files, output_file, uint32=False):
    """This function will given a list of sample files, load in the
    samples one by one and collapse them upon each other value by value.
    The final sample will be stored in the output file.

    :param sample_files: List of sample files paths
    :type sample_files: List(str)
    :param output_file: File path to the output file
    :type output_file: str
    :param uint32: If False numpy.dtype will be preserved, if True numpy.dtype will be changed to uint32
    :type uint32: boolean
    :returns:  None
    """
    first_sample = Data.read(sample_files[0])
    astype_func = partial(astype, np.uint32 if uint32 else first_sample.dtype)
    summary_sample = reduce(
        add_if_eq_region, map(astype_func, map(Data.read, sample_files))
    )
    Data.write(summary_sample, output_file)
