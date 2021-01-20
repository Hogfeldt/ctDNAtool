import logging
from scipy.sparse import issparse
from .utils import pickle_read, pickle_write

logger = logging.getLogger()


def astype(dtype, sample):
    if dtype == sample.dtype:
        return sample
    if sample.is_sparse:
        for i in range(sample.data.shape[0]):
            sample.data[i] = sample.data[i].astype(dtype)
    else:
        sample.data = sample.data.astype(dtype)
    return sample


class Data:
    def __init__(self, data, region_ids, bam_report):
        self.data = data
        self.region_ids = region_ids
        self.bam_report = bam_report
        self.is_sparse, self.dtype = self.__determine_structure_and_dtype(data)

    @staticmethod
    def read(file_path):
        return pickle_read(file_path)

    @staticmethod
    def write(data, file_path):
        pickle_write(data, file_path)

    @staticmethod
    def __determine_structure_and_dtype(data):
        is_sparse = issparse(data[0])
        if is_sparse:
            dtype = data[0].dtype
        else:
            dtype = data.dtype
        return (is_sparse, dtype)

    def __str__(self):
        return f"is sparse: {self.is_sparse}, data shape {self.data.shape}"
