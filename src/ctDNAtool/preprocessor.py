import attr
import re
import csv
import py2bit
from enum import Enum, auto

from .transcript_annotation import (
    pull_tx_id,
    pull_ensemble_gene_id,
    pull_ccds_id,
    pull_tx_type,
)
from .tss import TranscriptionStartSite, get_header


@attr.s
class Tx_annotation:
    chrom = attr.ib()
    start = attr.ib()
    end = attr.ib()
    strand = attr.ib()
    additionals = attr.ib()


def is_chrome_autosome(chrom):
    return re.match(r"chr\d", chrom) is not None


def get_transcript_annotations(file_path):
    with open(file_path, "r") as file_obj:
        for line in file_obj:
            if line[0] == "#":  # line is comment
                continue
            anno = line.replace("\n", "").split()
            if anno[2] != "transcript":  # line is not a transcript
                continue
            if is_chrome_autosome(anno[0]):
                anno_obj = Tx_annotation(
                    anno[0], int(anno[3]), int(anno[4]), anno[6], anno[8]
                )
                yield anno_obj


def determine_TSS_and_format_data(tx_anno):
    if tx_anno.strand == "+":
        TSS = tx_anno.start
    elif tx_anno.strand == "-":
        TSS = tx_anno.end
    else:
        raise Exception("Strand annotation is neither '+' nor '-'")
    tss_id = "_".join((tx_anno.chrom, str(TSS)))
    return TranscriptionStartSite(
        tss_id,
        tx_anno.chrom,
        TSS,
        tx_anno.strand,
        [pull_tx_id(tx_anno)],
        pull_ensemble_gene_id(tx_anno),
        pull_ccds_id(tx_anno),
        [pull_tx_type(tx_anno)],
    )


class Chromosomes(Enum):
    AUTOSOMES = auto()
    AUTOSOMES_X = auto()


def preprocess_bin_genome_Mbp(
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
        bed_writer = csv.writer(fp, delimiter="\t")
        bed_writer.writerow(["#chrom", "start", "end", "name", "score", "strand"])
        regexp = None
        if chromosomes == Chromosomes.AUTOSOMES:
            regexp = "chr[3-9]$|chr1[0-9]?$|chr2[0-2]?$"
        elif chromosomes == Chromosomes.AUTOSOMES_X:
            regexp = "chr[3-9]$|chr1[0-9]?$|chr2[0-2]?$|chrX$"
        for chr_name in chroms.keys():
            if re.match(regexp, chr_name):
                length = int(chroms[chr_name])
                pos_pairs = zip(
                    range(0, length, bin_size), range(bin_size, length, bin_size)
                )
                for start, end in pos_pairs:
                    bed_writer.writerow(
                        [chr_name, start, end, "{}_{}".format(chr_name, start), 0, "+"]
                    )
    return output_file


def preprocess(input_file, region_size, bed_file, tss_file):
    """This function will given a gencode annotation file, find all transcripts
    and determine the Transcription Start Site (TSS) for the transcript.
    Information about the TSS will be stored in the tss file with metadata
    and a bed file which can be used as input for the generator.

    :param input_file: File path to the gencode annotation file
    :type input_file: str
    :param region_size: Size of the region with the TSS in the center which
                        should be stored in the bed file
    :type region_size: int >= 0
    :param bed_file: File path to the bed file
    :type bed_file: str
    :param tss_file: File path to the tss file
    :type tss_file: str
    :returns:  None
    """
    tx_annotations = get_transcript_annotations(input_file)
    TSS_dict = dict()
    for tx_anno in tx_annotations:
        tss = determine_TSS_and_format_data(tx_anno)
        if tss.tss_id in TSS_dict:
            if tss.tx_types[0] not in TSS_dict[tss.tss_id].tx_types:
                TSS_dict[tss.tss_id].tx_types += tss.tx_types
            TSS_dict[tss.tss_id].tx_ids += tss.tx_ids
        else:
            TSS_dict[tss.tss_id] = tss
    with open(bed_file, "w") as fp_bed:
        bed_writer = csv.writer(fp_bed, delimiter="\t")
        bed_writer.writerow(["#chrom", "start", "end", "name", "score", "strand"])
        k = int(region_size / 2)
        with open(tss_file, "w") as fp_tss:
            fp_tss.write("#%s\n" % get_header())
            for tss_id in TSS_dict.keys():
                tss = TSS_dict[tss_id]
                region_start = tss.tss - k
                if region_start < 0:
                    continue
                region_end = tss.tss + k
                bed_writer.writerow(
                    [tss.chrom, region_start, region_end, tss_id, 0, tss.strand]
                )
                fp_tss.write("%s\n" % str(TSS_dict[tss_id]))
    return (bed_file, tss_file)
