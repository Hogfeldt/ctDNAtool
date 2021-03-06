from .utils import pickle_read, pickle_write


class CombinedData:
    def __init__(self, IDs, regions_ids, data):
        self.IDs = IDs
        self.region_ids = regions_ids
        self.data = data

    @staticmethod
    def read(file_path):
        return pickle_read(file_path)

    @staticmethod
    def write(data, file_path):
        pickle_write(data, file_path)

    def __str__(self):
        return "CombinedData instance containing the following IDs: " + ", ".join(
            self.IDs
        )
