#  This class is based on the work of Tobias Røikjer,
#  parts of code is taken from his Github Repository
#  NucCa (https://github.com/TobiasRoikjer/NucCa)
import pysam
import os
import sys
import attr


@attr.s
class Read:
    ref_name = attr.ib()
    start = attr.ib()
    end = attr.ib()
    start_is_first = attr.ib()


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

    def pair_generator(self, chrom, region_start, region_end):
        mem = {}

        for read in self.bam_file.fetch(
            contig=chrom, start=region_start, stop=region_end
        ):
            if read.is_duplicate or read.is_secondary or read.is_supplementary:
                continue

            query_name = read.query_name

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
                if (
                    mem_start is None
                    or mem_end is None
                    or read.reference_start is None
                    or read.reference_end is None
                    or read.is_reverse == mem_reverse
                ):
                    continue
                if read.is_reverse:
                    start = mem_start
                    end = read.reference_end
                    start_is_first = mem_is_read1
                else:
                    start = read.reference_start
                    end = mem_end
                    start_is_first = not mem_is_read1

                if start < end:
                    continue
                yield Read(read.reference_name, int(start), int(end), start_is_first)

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
