import pandas as pd


def read_file(path: str, header: int = None):
    excel_data = pd.read_excel(path, header=header)
    return excel_data
