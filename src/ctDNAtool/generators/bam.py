#  This class is based on the work of Tobias Røikjer,
#  parts of code is taken from his Github Repository
#  NucCa (https://github.com/TobiasRoikjer/NucCa)
import pysam
import os
import sys
import attr


@attr.s
class ReadPair:
    ref_name = attr.ib()
    start = attr.ib()
    end = attr.ib()
    start_is_first = attr.ib()
    length = attr.ib()


@attr.s
class Report:
    file_name = attr.ib()
    fetched_reads = attr.ib(default=0)
    reads_passed_qual_check = attr.ib(default=0)
    paired_reads = attr.ib(default=0)
    paired_reads_passed_qual_check = attr.ib(default=0)
    paired_reads_yielded = attr.ib(default=0)

    def __str__(self):
        return "\n".join(
            [
                "{0: ^47}",
                "-"*47,
                "Reads fetched:{1: >33}",
                "Reads passed quality check:{2: >20}",
                "Reads paired:{3: >34}",
                "Paired reads passed quality check:{4: >13}",
                "Paired reads emmitted:{5: >25}",
                "",
                "bam file: {6}"
            ]
        ).format(
            "BAM Report:",
            self.fetched_reads,
            self.reads_passed_qual_check,
            self.paired_reads,
            self.paired_reads_passed_qual_check,
            self.paired_reads_yielded,
            self.file_name,
        )


class BAM:
    def __init__(self, filename):
        bai_filename = f"{filename}.bai"

        # Check if index exists, if not create an index file
        if not os.path.exists(bai_filename):
            print(
                f"No index file found ({bai_filename}), generating...", file=sys.stderr
            )
            pysam.index(filename)

        self.bam_file = pysam.AlignmentFile(filename, "rb")
        self.report = Report(filename)

    def pair_generator(self, chrom, region_start, region_end, mapq=20):
        mem = {}

        for read in self.bam_file.fetch(
            contig=chrom, start=region_start, stop=region_end
        ):
            self.report.fetched_reads += 1
            if (
                read.is_duplicate
                or read.is_secondary
                or read.is_supplementary
                or read.mapping_quality < mapq
            ):
                continue

            query_name = read.query_name
            self.report.reads_passed_qual_check += 1

            if query_name not in mem:
                mem[query_name] = (
                    read.reference_start,
                    read.reference_end,
                    read.is_reverse,
                    read.is_read1,
                )
            else:
                mem_start, mem_end, mem_reverse, mem_is_read1 = mem[query_name]
                del mem[query_name]
                self.report.paired_reads += 1
                if (
                    mem_start is None
                    or mem_end is None
                    or read.reference_start is None
                    or read.reference_end is None
                    or read.is_reverse == mem_reverse
                ):
                    continue
                self.report.paired_reads_passed_qual_check += 1
                if read.is_reverse:
                    start = mem_start
                    end = read.reference_end
                    start_is_first = mem_is_read1
                else:
                    start = read.reference_start
                    end = mem_end
                    start_is_first = not mem_is_read1
                length = abs(read.template_length)

                if start >= end or length == 0:
                    continue
                self.report.paired_reads_yielded += 1
                yield ReadPair(
                    read.reference_name, int(start), int(end), start_is_first, length
                )

    def __str__(self):
        return str(self.report)

    def pair_generator_gabriel(self, chrom, region_start, region_end):
        mem = {}

        for read in self.bam_file.fetch(
            contig=chrom, start=region_start, stop=region_end
        ):
            if read.is_duplicate or read.is_secondary or read.is_supplementary:
                continue
            elif not read.is_paired:
                yield read.reference_name, read.reference_start, read.reference_end
                continue

            query_name = read.query_name

            if query_name not in mem:
                mem[query_name] = (read.reference_start, read.reference_end)
            else:
                mem_start, mem_end = mem[query_name]
                del mem[query_name]
                if (
                    mem_start is None
                    or mem_end is None
                    or read.reference_start is None
                    or read.reference_end is None
                ):
                    continue
                start = min(read.reference_start, mem_start)
                end = max(read.reference_end, mem_end)

                yield read.reference_name, start, end
