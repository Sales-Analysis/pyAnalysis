import pandas as pd


class FileIsEmptyError(Exception):
    """File is empty"""


class FileIsEmptyValueError(Exception):
    """there is an empty value"""


def read_file(path: str, header: [int, None] = 0) -> pd.DataFrame:
    excel_data = pd.read_excel(path, header=header)
    return excel_data


def make_exception_tests(path: str):
    input_data = read_file(path=path)
    if input_data.empty:
        raise FileIsEmptyError("file is empty")
    if input_data.isnull().any().any():
        raise FileIsEmptyValueError("there is an empty value")
