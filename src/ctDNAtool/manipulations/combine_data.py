import numpy as np

from ..data import Data
from ..combined_data import CombinedData


def combine_data(output_file, pickle_files):
    """Takes a collection of pickle files containing data and combines them into one object"""

    IDs = []
    data = []

    for file in pickle_files:
        IDs.append(_get_id_from_file_path(file))
        data.append(Data.read(file))

    combined_data = CombinedData(np.array(IDs), np.array(data))
    CombinedData.write(combined_data, output_file)


def _get_id_from_file_path(file_path):
    return file_path.split("/")[-1].split(".")[0]
