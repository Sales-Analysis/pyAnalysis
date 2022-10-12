import pandas as pd
import pytest
from filemanager import (
    read_file,
    FileIsEmptyError,
    FileIsEmptyValueError,
    validators,
)


@pytest.fixture
def data_exel():
    data = pd.DataFrame([1, 2, 3])
    return data


def test_read_file(data_exel):
    path = "./data/data_test.xlsx"
    reading_file = read_file(path=path, header=None)
    pd.testing.assert_frame_equal(data_exel, reading_file)


def test_file_is_empty():
    path = "./data/empty_exel.xlsx"
    data = pd.read_excel(path, header=None)
    with pytest.raises(FileIsEmptyError, match="File is empty."):
        validators(data=data)


def test_empty_values_in_file():
    path = "./data/empty_value.xlsx"
    data = pd.read_excel(path, header=None)
    with pytest.raises(FileIsEmptyValueError, match="There is an empty value."):
        validators(data=data)

