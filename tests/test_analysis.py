import pytest
from analysis import ABCAnalysis, abc_analysis, find_duplicate_values, join_duplicate
from filemanager import read_exel
from models import ABCModels


def test_sorted(data_input, data_result):
    a = ABCAnalysis(data=data_input)
    a.sorted
    result = a.result()
    assert result[ABCModels.CODE_PLU] == data_result[ABCModels.CODE_PLU]
    assert result[ABCModels.NAME_ANALYSIS_POSITIONS] == data_result[ABCModels.NAME_ANALYSIS_POSITIONS]
    assert result[ABCModels.DATA_ANALYSIS] == data_result[ABCModels.DATA_ANALYSIS]


def test_share(data_input, data_result):
    a = ABCAnalysis(data=data_input)
    a.sorted
    a.share
    result = a.result()
    assert result[ABCModels.SHARE] == [
        54.644808743169406,
        27.322404371584703,
        10.92896174863388,
        4.371584699453552,
        2.73224043715847
    ]


def test_accum_share(data_input, data_result):
    a = ABCAnalysis(data=data_input)
    a.sorted
    a.share
    a.accumulated_share
    a.round
    result = a.result()
    assert result[ABCModels.ACCUMULATED_SHARE] == data_result[ABCModels.ACCUMULATED_SHARE]


def test_class_abc(data_input, data_result):
    a = ABCAnalysis(data=data_input)
    a.sorted
    a.share
    a.accumulated_share
    a.category
    a.round
    result = a.result()
    assert result == data_result


def test_abc_analysis(data_result):
    path = "../tests/data/abc_test.xlsx"
    data = read_exel(path=path)
    result = abc_analysis(data=data)
    assert result == data_result


def test_duplicate_value(data_input, data_duplicate_value, data_duplicates):
    result, duplicates = find_duplicate_values(data=data_duplicate_value)
    assert result == data_input
    assert duplicates == data_duplicates

