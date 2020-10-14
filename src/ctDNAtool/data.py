import pickle

class Data:
    def __init__(self, data, region_ids):
        self.data = data
        self.region_ids = region_ids

    @staticmethod
    def read(file_path):
        with open(file_path, 'rb') as fp:
            return pickle.load(fp)

    @staticmethod
    def write(data, file_path):
        with open(file_path, 'wb') as fp:
            pickle.dump(data, fp)
