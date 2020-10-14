import csv


def tsv_writer(fp):
    """ Given a file obj return csv.writer with delimiter '\t' """
    return csv.writer(fp, delimiter="\t")


def tsv_reader(fp):
    """ Given a file obj return csv.reader with delimiter '\t' """
    return csv.reader(fp, delimiter="\t")
