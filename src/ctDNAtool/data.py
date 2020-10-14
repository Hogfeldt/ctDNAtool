import pickle
from scipy.sparse import issparse


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
    def __init__(self, data, region_ids):
        self.data = data
        self.region_ids = region_ids
        self.is_sparse, self.dtype = self.__determine_structure_and_dtype(data)

    @staticmethod
    def read(file_path):
        with open(file_path, "rb") as fp:
            return pickle.load(fp)

    @staticmethod
    def write(data, file_path):
        with open(file_path, "wb") as fp:
            pickle.dump(data, fp)

    def __determine_structure_and_dtype(data):
        is_sparse = issparse(data[0])
        if is_sparse:
            dtype = data[0].dtype
        else:
            dtype = data.dtype
        return (is_sparse, dtype)
