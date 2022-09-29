import pandas as pd
import pytest
from analysis import (
    FileNotNumericValueError,
    validators,
)


def test_not_numeric_value_in_file():
    path = "./data/not_numeric.xlsx"
    data = pd.read_excel(path, header=None, skiprows=1)
    names_columns = data.columns.values.tolist()
    analysis_columns = names_columns[2]
    with pytest.raises(FileNotNumericValueError, match="there is a not numeric value"):
        validators(data=data[analysis_columns])
