import pandas as pd
import pytest
from analysis import (
    analysis,
    validators,
    FileNotNumericValueError,
    FileNegativeValueError,
    NotFoundAnalysisError,
    SumValuesIsNot100Error,
    AccumulatedValuesNotCorrect,
    CategoryIncorrectError,
)


def test_not_numeric_value_in_file():
    path = "./data/not_numeric.xlsx"
    data = pd.read_excel(path, header=0)
    with pytest.raises(FileNotNumericValueError, match="There is a not numeric value."):
        validators(data=data)


def test_negative_value_in_file():
    path = "./data/negative_value.xlsx"
    data = pd.read_excel(path, header=0)
    with pytest.raises(FileNegativeValueError, match="There is a negative value."):
        validators(data=data)


def test_value_share():
    path = "./data/value_in_share.xlsx"
    data = pd.read_excel(path, header=0)
    with pytest.raises(SumValuesIsNot100Error, match="The sum of the values is not 100."):
        validators(data=data)


def test_value_in_accumulated_share():
    path = "./data/value_in_accumulated_share.xlsx"
    data = pd.read_excel(path, header=0)
    with pytest.raises(AccumulatedValuesNotCorrect, match="The accumulated share was calculated incorrectly."):
        validators(data=data)


def test_value_in_category():
    path = "./data/category.xlsx"
    data = pd.read_excel(path, header=0)
    with pytest.raises(CategoryIncorrectError, match="There is no such category."):
        validators(data=data)


def test_analysis():
    a = 'ABC'
    assert analysis(type_analysis=a) == a


def test_not_found_analysis():
    with pytest.raises(NotFoundAnalysisError):
        analysis(type_analysis='XXX')
