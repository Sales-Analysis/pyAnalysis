import pandas as pd


class FileIsEmptyError(Exception):
    """File is empty"""


class FileIsEmptyValueError(Exception):
    """there is an empty value"""


def read_file(path: str, header: int = None) -> pd.DataFrame:
    excel_data = pd.read_excel(path, header=header)
    if excel_data.empty:
        raise FileIsEmptyError("file is empty")
    if excel_data.isnull().any().any():
        raise FileIsEmptyValueError("there is an empty value")
    return excel_data
