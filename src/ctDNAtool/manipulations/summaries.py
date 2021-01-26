from ..manipulations.summaries_data import summaries_data
from ..data import Data


def summaries(sample_file, flank):
    """This function will given a sample and flank find flank amount of base pairs on each end of the sample
    and return sample ID, count of each base pair and frequency of each base pair

    :param sample_file File path to the matrix/tensor
    :type sample_file str
    :param flank amount of base pairs on each end of the sample
    :type flank Integer
    """
    sample_id = sample_file.split("/")[-1].replace(".pickle", "")
    data = Data.read(sample_file).data.sum(axis=0)

    counts, freqs = summaries_data(data, flank)
    return sample_id, counts, freqs
