import numpy as np
import logging

from ..data import Data
from ..combined_data import CombinedData

logger = logging.getLogger()


def combine_data(output_file, pickle_files):
    """Takes a collection of pickle files containing data and combines them into one .picke file"""
    IDs = np.empty(len(pickle_files), dtype=object)
    result = []

    tmp_data = Data.read(pickle_files[0])
    IDs[0] = _get_id_from_file_path(pickle_files[0])
    region_ids = tmp_data.region_ids
    data_shape = tmp_data.data.shape
    is_sparse = tmp_data.is_sparse
    result.append(tmp_data.data)

    for index, file in enumerate(pickle_files[1:], 1):
        logger.debug(f"Combining data from file {file}")

        IDs[index] = _get_id_from_file_path(file)
        tmp_data = Data.read(file)
        result.append(tmp_data.data)

        assert (
            tmp_data.region_ids == region_ids
        ), "Region IDs does not match for all samples"
        assert tmp_data.data.shape == data_shape, "Shape of data does not match"
        assert tmp_data.is_sparse == is_sparse, "Data is_sparse does not match"

    combined_data = CombinedData(IDs, region_ids, np.array(result))
    CombinedData.write(combined_data, output_file)
    logger.debug(f"Data was combined into file {output_file}")


def _get_id_from_file_path(file_path):
    return file_path.split("/")[-1].split(".")[0]
