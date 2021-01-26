import numpy as np


def summaries_data(data, flank):
    """This function will given a Data instance and flank find flank amount of base pairs on each end of the sample
    and return count of each base pair and frequency of each base pair

    :param data instance containing data
    :type Data
    :param flank amount of base pairs on each end of the sample
    :type flank Integer
    """
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
    return counts, freqs
