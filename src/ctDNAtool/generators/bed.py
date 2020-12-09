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

    def __str__(self):
        return "\t".join(
            [
                self.chrom,
                str(self.start),
                str(self.end),
                self.region_id,
                str(self.score),
                self.strand,
            ]
        )


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


def write_bed_file(file_path, beds):
    output_lines = ["\t".join(["#chrom", "start", "end", "name", "score", "strand"])]
    for bed in beds:
        output_lines.append(str(bed))
    output_string = "\n".join(output_lines)
    if file_path is None:
        print(output_string)  # noqa: T001
    else:
        with open(file_path, "w") as fp:
            print(output_string, file=fp)  # noqa: T001
