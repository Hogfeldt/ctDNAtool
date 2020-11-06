import numpy as np
import py2bit

from .bed import load_bed_file
from .bam import BAM
from .utils import seq_to_index, fetch_seq
from ..data import Data


def mate_length_end_seqs(
    bam_file, bed_file, ref_genome_file, output_file, max_length=500, flank=1
):
    """Create a tensor where the first dim. represents a whether a read came from
    the first or the second mate, the second dim. represent read lengths from 0 to
    max_length and the third dim. represents the the concatenation of the sequenses
    at the fragment ends, taken from the reference genome, endcoded as an index.
    Then length of an end sequence is 2 times the flank parameter.

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
    id_lst = ["start_is_first_mate", "start_is_second_mate"]
    N_seqs = 4 ** (4 * flank) + 1  # the last bin is for sequences containing N
    T = np.zeros((2, max_length, N_seqs))
    try:
        tb = py2bit.open(ref_genome_file)
        for i, region in enumerate(region_lst):
            for read in bam.pair_generator(region.chrom, region.start, region.end):
                length = abs(read.end - read.start)
                if length < max_length:
                    seq = fetch_seq(tb, region.chrom, read.start, read.end, flank)
                    mate = 0 if read.start_is_first else 1
                    T[mate, length, seq_to_index(seq)] += 1
        Data.write(Data(T, id_lst), output_file)
    finally:
        tb.close()
