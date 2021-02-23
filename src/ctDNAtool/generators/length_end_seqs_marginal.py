import numpy as np
import logging

from .bed import load_bed_file
from .bam import BAM
from .utils import fetch_seq
from ..data import Data
from ..py2bit_context import Py2bitContext

logger = logging.getLogger()

base_pair_offset = {"A": 0, "T": 1, "C": 2, "G": 3}


def length_end_seqs_marginal(
    bam_file, bed_file, ref_genome_file, output_file, max_length=500, flank=3, mapq=20
):
    """Create a tensor where the first dim. represents a region from the bed file,
    the second dim. represent read lengths from 1 to max_length and the third dim.
    represents the the marginal end sequence count at the fragment ends, taken
    from the reference genome.

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
    :param flank: Determines how many base pairs are examined in each end.
    type flank: Int
    :param mapq: map quality. Ignores all reads below the threshold.
    :type mapq: Int
    :returns:  None
    """
    region_lst = load_bed_file(bed_file)
    bam = BAM(bam_file)
    id_lst = list()
    flanks_size = flank * 2 * 2 * 4
    tensor = np.zeros((len(region_lst), max_length, flanks_size), dtype=np.uint32)

    with Py2bitContext(ref_genome_file) as tb:
        chromosome_lengths = tb.chroms()
        for region_index, region in enumerate(region_lst):
            id_lst.append(region.region_id)
            for read in bam.pair_generator(
                region.chrom, region.start, region.end, mapq
            ):
                length = read.length
                if (
                    length <= max_length
                    and chromosome_lengths[region.chrom] >= (read.end + flank)
                    and 0 <= (read.start - flank)
                ):
                    seq = fetch_seq(tb, region.chrom, read.start, read.end, flank)
                    if "N" in seq:
                        continue

                    _read_sequence_to_tensor(length, region_index, seq, tensor)
                    _log_current_position(length, region_index, seq, tensor)

        Data.write(Data(tensor, id_lst, bam.report), output_file)


def _read_sequence_to_tensor(length, region_index, seq, tensor):
    for bp_index, base_pair in enumerate(seq):
        offset = bp_index * 4 + base_pair_offset[base_pair]
        tensor[region_index][length - 1][offset] += 1


def _log_current_position(length, region_index, seq, tensor):
    logger.debug(f"region index {region_index}")
    logger.debug(f"length {length}")
    logger.debug(
        f"shape of tensor at region and size {tensor[region_index][length - 1].shape}"
    )
    logger.debug(f"content {tensor[region_index][length - 1]}")
    logger.debug(f"sequence {seq}")
