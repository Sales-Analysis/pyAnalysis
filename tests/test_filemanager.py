import pytest
from filemanager import read_exel, read_csv
from code_errors import FileIsEmptyError, HeaderNotFoundError


class TestGroup:
    def test_read_exel(self, data_input):
        path = "./data/abc_test.xlsx"
        reading_file = read_exel(path=path)
        assert reading_file.CODE_PLU == data_input['код идентификатор PLU']
        assert reading_file.NAME_ANALYSIS_POSITIONS == data_input['наименование анализируемых позиций']
        assert reading_file.DATA_ANALYSIS == data_input['данные по анализируемому критерию (продажи/оборот/прибыль)']

    def test_file_is_empty(self):
        path = "./data/empty_exel.xlsx"
        with pytest.raises(FileIsEmptyError):
            read_exel(path=path)

    def test_file_value_is_empty(self):
        path = "./data/only_header.xlsx"
        with pytest.raises(FileIsEmptyError):
            read_exel(path=path)


class TestCsv:
    def test_reading_csv(self, data_input_csv):
        path = "./data/abc_test.csv"
        reading_file = read_csv(path=path)
        assert data_input_csv == reading_file

    def test_file_is_empty(self):
        path = "./data/empty_csv.csv"
        with pytest.raises(HeaderNotFoundError):
            read_csv(path=path)

    def test_empty_row(self, data_input_csv):
        path = "./data/data_input_empty_rows.csv"
        reading_file = read_csv(path=path)
        assert data_input_csv == reading_file

    def test_file_value_is_empty(self):
        path = "./data/only_header_csv.csv"
        with pytest.raises(FileIsEmptyError):
            read_csv(path=path)
