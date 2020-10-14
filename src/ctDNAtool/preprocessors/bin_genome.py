from enum import Enum, auto
import py2bit
from natsort import natsorted

from .utils import is_autosome, is_autosome_or_x
from ..utils import tsv_writer


class Chromosomes(Enum):
    AUTOSOMES = auto()
    AUTOSOMES_X = auto()


def select_chrom_test(chroms):
    CHROM_TESTS = {
        Chromosomes.AUTOSOMES: is_autosome,
        Chromosomes.AUTOSOMES_X: is_autosome_or_x,
    }
    return CHROM_TESTS.get(chroms)


def bin_genome_Mbp(
    genome_ref_file, output_file, mbp=1.0, chromosomes=Chromosomes.AUTOSOMES_X
):
    """This function will given a genome reference file in .2bit format,
    create a bed file splitting the genome in bins of size mbp.

    If the last bin of a chromosome is smaller than the given mbp,
    the bin will be thrown away

    :param genome_ref_file: File path to a .2bit file
    :type genome_ref_file: str
    :param output_file: The path to where the outputting bed file
                        is stored.
    :type output_file: str
    :param mbp: Bin size in Mbp.
    :type mbp:
    :param chromosomes: Choose wich chromosomes to include in bed file.
    :type Chromosomes:
    """
    # NOTE: If no output file path is given, the output should prob. be
    #       outputtet on stdout. Nice for piping.
    tb = py2bit.open(genome_ref_file)
    bin_size = int(mbp * 10 ** 6)
    try:
        chroms = tb.chroms()
    finally:
        tb.close()
    with open(output_file, "w") as fp:
        bed_writer = tsv_writer(fp)
        bed_writer.writerow(["#chrom", "start", "end", "name", "score", "strand"])
        for chr_name in natsorted(
            filter(chroms.keys(), key=select_chrom_test(chromosomes))
        ):
            length = int(chroms[chr_name])
            pos_pairs = zip(
                range(0, length, bin_size), range(bin_size, length, bin_size)
            )
            for start, end in pos_pairs:
                bed_writer.writerow(
                    [chr_name, start, end, "{}_{}".format(chr_name, start), 0, "+"]
                )
    return output_file
