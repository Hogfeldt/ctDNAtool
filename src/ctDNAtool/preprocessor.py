import argparse
import attr
import re
import csv

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
    return re.match(r"chr\d", chrom) != None


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


def preprocess(input_file, region_size, bed_file, tss_file):
    """ This function will given a gencode annotation file, find all transcripts
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
