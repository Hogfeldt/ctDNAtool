import numpy as np

from .bam import BAM
from .bed import load_bed_file
from ..data import Data


def length_matrix(bam_file, bed_file, output_file, max_length=500):
    """Creates a matrix where each row represents a region from the bed file
    and the columns are read lengths from 0 to max_length.
    The size of the matrix is (n x max_length) where n is the number of regions
    in the bed file.
    Data is read length counts, so that a_ij is the number of reads in region i,
    with length j.

    :param bam_file: File path to the bam sample file
    :type bam_file: str
    :param bed_file: File path to the bed file, which can be compiled by the preprocessing function
    :type bed_file: str
    :param output_file: File path to the output file
    :type output_file: str
    :param max_length: Maximum read length to be counted
    :type max_length: int > 0
    :returns:  None
    """
    region_lst = load_bed_file(bed_file)
    matrix = np.zeros((len(region_lst), max_length), dtype=np.uint16)
    bam = BAM(bam_file)
    id_lst = list()
    for i, region in enumerate(region_lst):
        for reading in bam.pair_generator(region.chrom, region.start, region.end):
            start = int(reading[1])
            end = int(reading[2])
            length = abs(end - start)
            if length < max_length:
                matrix[i, length] += 1
        id_lst.append(region.region_id)
    Data.write(Data(matrix, id_lst), output_file)
