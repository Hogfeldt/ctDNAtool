import numpy as np
import logging

from ..data import Data
from ..combined_data import CombinedData

logger = logging.getLogger()


def combine_data(output_file, pickle_files):
    """Takes a collection of pickle files containing data and combines them into one object"""

    IDs = np.empty(len(pickle_files), dtype=object)
    data = np.empty(len(pickle_files), dtype=Data)

    for index, file in enumerate(pickle_files):
        logger.debug(f"Combining data from file {file}")
        IDs[index] = _get_id_from_file_path(file)
        data[index] = Data.read(file)

    combined_data = CombinedData(IDs, data)
    CombinedData.write(combined_data, output_file)
    logger.debug(f"Data was combine into file {output_file}")
    print(combined_data)


def _get_id_from_file_path(file_path):
    return file_path.split("/")[-1].split(".")[0]
