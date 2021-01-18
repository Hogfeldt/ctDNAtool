from ..data import Data
from ..utils import tsv_writer


def convert_to_tsv(pickle_file, output_file, length_lower_bound, length_upper_bound):
    """This function takes a pickle file containing a Data instance and writes the contents to a tsv file

    param: pickle_file: Pickle file to convert.
    type: str
    param: output_file: Output file.
    type: str
    param: length_lower_bound: Determines the minimum length to include in output.
    Must be positive.
    type: int
    param: length_upper_bound: Determines the maximum length to include in output.
    Must be equal to or larger than lower bound.
    type: int
    returns: None
    """
    data = Data.read(pickle_file)

    print(len(data.data[0]))

    assert (
        length_upper_bound > length_lower_bound
    ), "Higher bound should be higher than lower bound"
    assert length_lower_bound > 0, "Lower bound should be a positive integer"
    assert len(data.data[0]) >= length_upper_bound - 1, "Upper bound out of range"

    with open(output_file, "w") as fp:
        writer = tsv_writer(fp)

        lengths = list(map(str, range(length_lower_bound, length_upper_bound)))
        writer.writerow(["Region ID"] + lengths)

        if data.is_sparse:
            print(data.data[0])
        else:
            for region_id, row in zip(data.region_ids, data.data):
                row_range = _get_row_from_range(
                    row, length_lower_bound, length_upper_bound
                )
                writer.writerow([region_id] + row_range)
                print(len(row_range))


def _get_row_from_range(row, lower, upper):
    return list(map(str, row[lower - 1 : upper]))
