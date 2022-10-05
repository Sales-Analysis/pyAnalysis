import pandas as pd
from typing import List, Optional


class FileIsEmptyError(Exception):
    """File is empty"""


class FileIsEmptyValueError(Exception):
    """there is an empty value"""


def read_file(path: str, header: Optional[int] = 0) -> pd.DataFrame:
    data = pd.read_excel(path, header=header)
    try:
        validators(data=data)
    except Exception as err:
        raise Exception(err)
    return data


def validators(data: pd.DataFrame) -> None:
    if data.empty:
        raise FileIsEmptyError("file is empty")
    if data.isnull().any().any():
        raise FileIsEmptyValueError("there is an empty value")
