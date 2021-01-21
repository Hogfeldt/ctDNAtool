import numpy as np
import logging

from ..data import Data
from ..combined_data import CombinedData

logger = logging.getLogger()


def combine_data(output_file, pickle_files):
    """Takes a collection of pickle files containing data and combines them into one .picke file"""
    IDs = np.empty(len(pickle_files), dtype=object)
    region_ids = []
    data_shape = []
    data = []

    for index, file in enumerate(pickle_files):
        logger.debug(f"Combining data from file {file}")

        IDs[index] = _get_id_from_file_path(file)
        tmp_data = Data.read(file)
        data.append(tmp_data.data)

        if index == 0:
            region_ids = tmp_data.region_ids
            data_shape = tmp_data.data.shape
        else:
            assert (
                tmp_data.region_ids == region_ids
            ).all(), "Region IDs does not match for all samples"
            assert tmp_data.data.shape == data_shape, "Shape of data does not match"

    combined_data = CombinedData(IDs, region_ids, np.array(data))
    CombinedData.write(combined_data, output_file)

    logger.debug(f"Data was combined into file {output_file}")


def _get_id_from_file_path(file_path):
    return file_path.split("/")[-1].split(".")[0]
