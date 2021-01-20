from .utils import pickle_read, pickle_write


class CombinedData:
    def __init__(self, IDs, data):
        self.IDs = IDs
        self.data = data

    @staticmethod
    def read(file_path):
        file = pickle_read(file_path)
        return file

    @staticmethod
    def write(data, file_path):
        pickle_write(data, file_path)

    def __str__(self):
        return "".join(self.IDs)
