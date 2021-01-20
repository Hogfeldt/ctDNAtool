import csv
import pickle
import logging

logger = logging.getLogger()


def tsv_writer(fp):
    """ Given a file obj return csv.writer with delimiter '\t' """
    return csv.writer(fp, delimiter="\t")


def tsv_reader(fp):
    """ Given a file obj return csv.reader with delimiter '\t' """
    return csv.reader(fp, delimiter="\t")


def pickle_read(file_path):
    """ Given a file path return an object """
    with open(file_path, "rb") as fp:
        return pickle.load(fp)


def pickle_write(data, file_path):
    """ Given a file path and data object dump a .pickle file """
    with open(file_path, "wb") as fp:
        logger.debug(f"Writing data to {file_path}")
        pickle.dump(data, fp)

