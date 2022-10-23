import pandas as pd
import pytest
from analysis import (
    analysis,
    NotFoundAnalysisError,
    abc,
    ABCAnalysis
)
from code_errors import (
    FileNotNumericValueError,
    FileNegativeValueError,
    SumValuesIsNot100Error,
    AccumulatedValuesNotCorrect,
    CategoryIncorrectError,
)
from validators import validators_abc
from models import ABCModels


class TestGroup:
    def test_not_numeric_value_in_file(self):
        path = "./data/not_numeric.xlsx"
        data = pd.read_excel(path, header=0)
        with pytest.raises(FileNotNumericValueError):
            validators_abc(data=data)

    def test_negative_value_in_file(self):
        path = "./data/negative_value.xlsx"
        data = pd.read_excel(path, header=0)
        with pytest.raises(FileNegativeValueError):
            validators_abc(data=data)

    def test_value_share(self):
        path = "./data/value_in_share.xlsx"
        data = pd.read_excel(path, header=0)
        with pytest.raises(SumValuesIsNot100Error):
            validators_abc(data=data)

    def test_value_in_accumulated_share(self):
        path = "./data/value_in_accumulated_share.xlsx"
        data = pd.read_excel(path, header=0)
        with pytest.raises(AccumulatedValuesNotCorrect):
            validators_abc(data=data)

    def test_value_in_category(self):
        path = "./data/category.xlsx"
        data = pd.read_excel(path, header=0)
        with pytest.raises(CategoryIncorrectError):
            validators_abc(data=data)

    def test_analysis(self):
        a = 'ABC'
        path = '../tests/data/abc_result.xlsx'
        df = analysis(path=path, type_analysis=a)
        return df

    def test_result_analysis(self):
        path = '../tests/data/abc_test.xlsx'
        data = abc(path)
        pd.testing.assert_frame_equal(self.test_analysis(), data.reset_index(drop=True))

    def test_not_found_analysis(self):
        with pytest.raises(NotFoundAnalysisError):
            analysis(type_analysis='XXX', path="./tests/data/abc_test.xlsx")


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
