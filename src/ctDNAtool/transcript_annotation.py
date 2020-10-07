import attr
import re


@attr.s
class Tx_annotation:
    chrom = attr.ib()
    start = attr.ib()
    end = attr.ib()
    strand = attr.ib()
    additionals = attr.ib()


def is_chrome_autosome(chrom):
    return re.match(r"chr\d", chrom) != None


def pull_tx_id(anno_obj):
    return anno_obj.additionals.split(";")[0].split(".")[0].replace("ID=", "")


def pull_ensemble_gene_id(anno_obj):
    return anno_obj.additionals.split(";")[2].split(".")[0].replace("gene_id=", "")


def pull_ccds_id(anno_obj):
    if "CCDS" in anno_obj.additionals:
        add_list = anno_obj.additionals.split(";")
        for add in add_list:
            if "ccdsid=" in add:
                return add.replace("ccdsid=", "")
    return None


def pull_tx_type(anno_obj):
    return anno_obj.additionals.split(";")[7].replace("transcript_type=", "")


def load_transcript_annotations_iter(annotation_path):
    with open(annotation_path, "r") as fp:
        for line in fp.read().split("\n"):
            if line != "":
                anno = line.split()
                anno_obj = Tx_annotation(
                    anno[0], int(anno[3]), int(anno[4]), anno[6], anno[8]
                )
                if is_chrome_autosome(anno_obj.chrom):  # Filter out none autosomes
                    yield anno_obj


def load_transcript_annotations(annotation_path):
    annotations = dict()
    with open(annotation_path, "r") as fp:
        for line in fp.read().split("\n"):
            if line != "":
                anno = line.split()
                anno_obj = Tx_annotation(
                    anno[0], int(anno[3]), int(anno[4]), anno[6], anno[8]
                )
                if is_chrome_autosome(anno_obj.chrom):  # Filter out none autosomes
                    tx_id = pull_tx_id(anno_obj)
                    annotations[tx_id] = anno_obj
    return annotations
