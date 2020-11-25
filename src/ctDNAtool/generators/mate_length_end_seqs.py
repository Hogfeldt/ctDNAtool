import numpy as np
import py2bit

from .bed import load_bed_file
from .bam import BAM
from .utils import seq_to_index, fetch_seqs
from ..data import Data


def mate_length_end_seqs(
    bam_file, bed_file, ref_genome_file, output_file, max_length=500, flank=1, mapq=20
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
    id_lst = ["first_mate", "second_mate"]
    N_seqs = 4 ** (2 * flank) + 1  # the last bin is for sequences containing N
    T = np.zeros((2, max_length, N_seqs), dtype=np.uint32)
    try:
        tb = py2bit.open(ref_genome_file)
        for i, region in enumerate(region_lst):
            for read in bam.pair_generator(
                region.chrom, region.start, region.end, mapq
            ):
                length = read.length
                if length < max_length:
                    start_seq, end_seq = fetch_seqs(
                        tb, region.chrom, read.start, read.end, flank
                    )
                    start_mate, end_mate = (0, 1) if read.start_is_first else (1, 0)
                    T[start_mate, length, seq_to_index(start_seq)] += 1
                    T[end_mate, length, seq_to_index(end_seq)] += 1
        Data.write(Data(T, id_lst), output_file)
    finally:
        tb.close()
