import numpy as np

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
    nonzero = data.nonzero()
    seq_pairs = zip(np.array(data[nonzero])[0], nonzero[1])
    counts = np.zeros((4, 2 * flank))
    for n, kmer in seq_pairs:
        # End sequence
        for i in reversed(range(2 * flank)):
            nucl = kmer % 4
            counts[nucl, i] += n
            kmer //= 4
        # Start sequence
        for i in reversed(range(2 * flank)):
            nucl = kmer % 4
            counts[nucl, i] += n
            kmer //= 4
    freqs = counts / counts.sum(axis=0)
    return sample_id, counts, freqs
