import pytest
from filemanager import read_exel
from code_errors import FileIsEmptyError


class TestGroup2:
    def test_read_exel(self, data_input):
        path = "./data/abc_test.xlsx"
        reading_file = read_exel(path=path)
        assert reading_file == data_input

    def test_file_is_empty(self):
        path = "./data/empty_exel.xlsx"
        with pytest.raises(FileIsEmptyError):
            read_exel(path=path)

    def test_file_value_is_empty(self):
        path = "./data/only_header.xlsx"
        with pytest.raises(FileIsEmptyError):
            read_exel(path=path)
