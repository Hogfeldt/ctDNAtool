import csv
import numpy as np


def tsv_writer(fp):
    """ Given a file obj return csv.writer with delimiter '\t' """
    return csv.writer(fp, delimiter="\t")


def tsv_reader(fp):
    """ Given a file obj return csv.reader with delimiter '\t' """
    return csv.reader(fp, delimiter="\t")


def determine_index_file_name(output_file):
    if output_file.split(".")[-1] == "npy":
        return output_file.replace(".npy", ".index")
    else:
        return output_file + ".index"


def write_index_file(output_file, index_lst):
    with open(determine_index_file_name(output_file), "w") as fp:
        writer = tsv_writer(fp)
        writer.writerow(("#index", "id"))
        for row_info in index_lst:
            writer.writerow(row_info)


def write_matrix_and_index_file(output_file, matrix, index_lst):
    write_index_file(output_file, index_lst)
    np.save(output_file, matrix)
