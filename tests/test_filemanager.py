import pandas as pd
import pytest
from code_errors import (
    FileIsEmptyError,
    FileIsEmptyValueError,
)
from filemanager import read_file
from validators import validators_read_file


class TestGroup:
    @pytest.fixture
    def data_exel(self):
        data = pd.DataFrame([1, 2, 3])
        return data

    def test_read_file(self, data_exel):
        path = "./data/data_test.xlsx"
        reading_file = read_file(path=path, header=None)
        pd.testing.assert_frame_equal(data_exel, reading_file)

    def test_file_is_empty(self):
        path = "./data/empty_exel.xlsx"
        data = pd.read_excel(path, header=None)
        with pytest.raises(FileIsEmptyError):
            validators_read_file(data=data)

    def test_empty_values_in_file(self):
        path = "./data/empty_value.xlsx"
        data = pd.read_excel(path, header=None)
        with pytest.raises(FileIsEmptyValueError):
            validators_read_file(data=data)
