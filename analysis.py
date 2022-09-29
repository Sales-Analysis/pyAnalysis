import pandas as pd
import numpy as np
from filemanager import read_file


class FileNotNumericValueError(Exception):
    """there is a not numeric value"""


def abc() -> pd.DataFrame:
    path = "./tests/data/abc_test.xlsx"
    data = read_file(path=path)
    # file.apply(pd.to_numeric, errors='coerce')
    names_columns = data.columns.values.tolist()
    analysis_columns = names_columns[2]
    data.sort_values(by=[analysis_columns], ascending=False)
    data['Доля'] = data[analysis_columns] / (data[analysis_columns].sum()) * 100
    data['Аккум.доля'] = data['Доля'].cumsum()
    data["Категория"] = ' '
    data.loc[data['Аккум.доля'] <= 80, 'Категория'] = 'A'
    data.loc[(data['Аккум.доля'] > 80) & (data['Аккум.доля'] <= 95), 'Категория'] = 'B'
    data.loc[data['Аккум.доля'] > 95, 'Категория'] = 'C'
    return data


def validators(data: pd.DataFrame) -> None:
    if not data.apply(np.isreal).all():
        raise FileNotNumericValueError("there is a not numeric value")


if __name__ == '__main__':
    abc()