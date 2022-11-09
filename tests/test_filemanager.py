import pytest
from filemanager import read_exel
from code_errors import FileIsEmptyError


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
