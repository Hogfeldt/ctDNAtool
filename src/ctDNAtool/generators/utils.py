from functools import reduce
from operator import add

nucleotide_to_digit = {"A": "0", "T": "1", "G": "2", "C": "3"}


def seq_to_index(seq):
    if "N" in seq:
        return -1
    else:
        return int(reduce(add, map(nucleotide_to_digit.get, seq)), base=4)


def fetch_seq(tb, chrom, start, end, flank):
    start_seq = tb.sequence(chrom, start - flank, start + flank)
    end_seq = tb.sequence(chrom, end - flank, end + flank)
    return (start_seq + end_seq).upper()


def fetch_seqs(tb, chrom, start, end, flank):
    start_seq = tb.sequence(chrom, start - flank, start + flank).upper()
    end_seq = tb.sequence(chrom, end - flank, end + flank).upper()
    return (start_seq, end_seq)
