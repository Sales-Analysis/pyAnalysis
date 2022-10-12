import pandas as pd
from typing import Optional
from code_errors import (
    FileIsEmptyError,
    FileIsEmptyValueError,
)


def read_file(path: str, header: Optional[int] = 0) -> pd.DataFrame:
    data = pd.read_excel(path, header=header)
    try:
        validators(data=data)
    except Exception as err:
        raise Exception(err)
    return data


def validators(data: pd.DataFrame) -> None:
    if data.empty:
        raise FileIsEmptyError("File is empty.")
    if data.isnull().any().any():
        raise FileIsEmptyValueError("There is an empty value.")
