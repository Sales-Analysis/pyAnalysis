import pandas as pd
import pytest
from analysis import (
    FileNotNumericValueError,
    validators,
    FileNegativeValueError,
)


def test_not_numeric_value_in_file():
    path = "./data/not_numeric.xlsx"
    data = pd.read_excel(path, header=0)
    with pytest.raises(FileNotNumericValueError, match="there is a not numeric value"):
        validators(data=data)


def test_negative_value_in_file():
    path = "./data/negative_value.xlsx"
    data = pd.read_excel(path, header=0)
    with pytest.raises(FileNegativeValueError, match="there is a negative value"):
        validators(data=data)
