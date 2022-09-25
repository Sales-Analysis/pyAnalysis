import pandas as pd


def read_file(path: str):
    excel_data = pd.read_excel(path, header=None)
    return excel_data


