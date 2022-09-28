import pandas as pd
import pytest
from filemanager import read_file, FileIsEmptyError, FileIsEmptyValueError


@pytest.fixture
def data_exel():
    data = pd.DataFrame([1, 2, 3])
    return data


def test_read_file(data_exel):
    path = "./data/data_test.xlsx"
    reading_file = read_file(path=path)
    pd.testing.assert_frame_equal(data_exel, reading_file)


def test_file_is_empty():
    path = "./data/empty_exel.xlsx"
    with pytest.raises(FileIsEmptyError, match="file is empty"):
        read_file(path=path)


def test_empty_values_in_file():
    path = "./data/empty_value.xlsx"
    with pytest.raises(FileIsEmptyValueError, match="there is an empty value"):
        read_file(path=path)
