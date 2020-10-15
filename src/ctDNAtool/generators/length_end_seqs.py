import numpy as np
from scipy.sparse import dok_matrix, csr_matrix
import py2bit
from functools import reduce
from operator import add

from .bed import load_bed_file
from .bam import BAM
from ..data import Data

nucleotide_to_digit = {"A": "0", "T": "1", "G": "2", "C": "3"}


def seq_to_index(seq):
    return int(reduce(add, map(nucleotide_to_digit.get, seq)), base=4)


def fetch_seq(tb, chrom, start, end, flank):
    start_seq = tb.sequence(chrom, start - flank, start + flank)
    end_seq = tb.sequence(chrom, end - flank, end + flank)
    return (start_seq + end_seq).upper()


def length_end_seqs(
    bam_file, bed_file, ref_genome_file, output_file, max_length=500, flank=1
):
    """Create a tensor where the first dim. represents a region from the bed file,
    the second dim. represent read lengths from 0 to max_length and the third dim.
    represents the the concatenation of the sequenses at the fragment ends, taken
    from the reference genome, endcoded as an index. Then length of an end sequence
    is 2 times the flank parameter.

    :param bam_file: File path to the bam sample file
    :type bam_file: str
    :param bed_file: File path to the bed file, which can be compiled by the preprocessing function
    :type bed_file: str
    :param output_file: File path to the output file
    :type output_file: str
    :param ref_genome_file: File path to the reference genome given as a 2bit file.
    :type ref_genome_file: str
    :param max_length: Maximum read length to be counted
    :type max_length: int > 0
    :returns:  None
    """
    region_lst = load_bed_file(bed_file)
    bam = BAM(bam_file)
    id_lst = list()
    tensor = np.empty((len(region_lst),), dtype=np.object)
    N_seqs = 4 ** (4 * flank) + 1  # the last bin is for sequences containing N
    try:
        tb = py2bit.open(ref_genome_file)
        for i, region in enumerate(region_lst):
            matrix = dok_matrix((max_length, N_seqs), dtype=np.uint16)
            for reading in bam.pair_generator(region.chrom, region.start, region.end):
                start = int(reading[1])
                end = int(reading[2])
                length = abs(end - start)
                if length < max_length:
                    seq = fetch_seq(tb, region.chrom, start, end, flank)
                    if "N" in seq:
                        matrix[length, -1] += 1
                    else:
                        matrix[length, seq_to_index(seq)] += 1
            tensor[i] = csr_matrix(matrix)
            id_lst.append(region.region_id)
        Data.write(Data(tensor, id_lst), output_file)
    finally:
        tb.close()
