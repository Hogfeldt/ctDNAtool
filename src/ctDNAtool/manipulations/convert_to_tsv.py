from ..data import Data
from ..utils import tsv_writer


def convert_to_tsv_length(pickle_file, output_file, lower_bound, upper_bound):
    """This function takes a pickle file containing a Data instance and writes the contents to a tsv file

    param: pickle_file: Pickle file to convert.
    type: str
    param: output_file: Output file.
    type: str
    param: lower_bound: Determines the minimum length to include in output.
    Must be positive.
    type: int
    param: upper_bound: Determines the maximum length to include in output.
    Must be equal to or larger than lower bound.
    type: int
    returns: None
    """
    data = Data.read(pickle_file)
    if data.region_ids[0] == "region_sum":
        data.data = [data.data]

    assert upper_bound > lower_bound, "Higher bound should be higher than lower bound"
    assert len(data.data[0]) >= upper_bound - 1, "Upper bound out of range"

    with open(output_file, "w") as fp:
        writer = tsv_writer(fp)

        lengths = generate_lengths(lower_bound, upper_bound)
        writer.writerow(["Region ID"] + lengths)

        for region_id, row in zip(data.region_ids, data.data):
            row_from_range = _get_row_from_range(row, lower_bound, upper_bound)
            writer.writerow([region_id] + row_from_range)


def _get_row_from_range(row, lower, upper):
    return list(map(str, row[lower - 1 : upper]))


def generate_lengths(lower_bound, upper_bound):
    return list(map(str, range(lower_bound, upper_bound)))
