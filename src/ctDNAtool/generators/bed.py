import attr
import csv


@attr.s
class BED:
    chrom = attr.ib()
    start = attr.ib()
    end = attr.ib()
    region_id = attr.ib()
    score = attr.ib()
    strand = attr.ib()


def load_bed_file(file_path):
    region_lst = list()
    with open(file_path) as fp:
        reader = csv.reader(fp, delimiter="\t")
        for line in reader:
            if line[0].startswith("#"):
                continue
            region_lst.append(
                BED(line[0], int(line[1]), int(line[2]), line[3], int(line[4]), line[5])
            )
    return region_lst
