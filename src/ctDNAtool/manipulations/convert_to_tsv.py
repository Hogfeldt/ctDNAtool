from ..data import Data
import logging
from ..utils import tsv_writer

logger = logging.getLogger()


def convert_to_tsv_length(pickle_file, output_file, min_length=None, max_length=None):
    """This function takes a pickle file containing containing length data and writes the contents to a tsv file.

    param: pickle_file: Pickle file to convert.
    type: str
    param: output_file: Output file.
    type: str
    param: min_length: Determines the minimum length to include in output.
    Must be positive.
    type: int
    param: max_length: Determines the maximum length to include in output.
    Must be equal to or larger than min_length.
    type: int
    returns: None
    """
    data = Data.read(pickle_file)
    if data.data.ndim == 1:
        data.data = [data.data]

    if min_length is None:
        min_length = 0

    if max_length is None:
        max_length = len(data.data[0])

    assert max_length > min_length, "max_length should be higher than min_length"
    assert len(data.data[0]) >= max_length, "max_length out of range"

    with open(output_file, "w") as fp:
        writer = tsv_writer(fp)
        logger.debug(f"Writing data to {output_file}")

        lengths = generate_lengths(min_length, max_length)
        writer.writerow(["Region ID"] + lengths)

        for region_id, row in zip(data.region_ids, data.data):
            row_from_range = _get_row_from_range(row, min_length, max_length)
            writer.writerow([region_id] + row_from_range)


def _get_row_from_range(row, min_length, max_length):
    return list(map(str, row[min_length - 1 : max_length]))


def generate_lengths(min_length, max_length):
    return list(map(str, range(min_length, max_length)))
