import re


def is_autosome(chrom):
    return re.match(r"chr[3-9]$|chr1[0-9]?$|chr2[0-2]?$", chrom) is not None


def is_autosome_or_x(chrom):
    return re.match(r"chr[3-9]$|chr1[0-9]?$|chr2[0-2]?$|chrX$", chrom) is not None
