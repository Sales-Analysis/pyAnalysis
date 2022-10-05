import pandas as pd
import numpy as np
from enum import Enum
from filemanager import read_file


class ABCData(str, Enum):
    CODE_PLU = 'код идентификатор PLU'
    NAME_ANALYSIS_POSITIONS = 'наименование анализируемых позиций'
    DATA_ANALYSIS = 'данные по анализируемому критерию (продажи/оборот/прибыль)'


class FileNotNumericValueError(Exception):
    """there is a not numeric value"""


class FileNegativeValueError(Exception):
    """there is a negative value"""


def abc() -> pd.DataFrame:
    path = "./tests/data/abc_test.xlsx"
    data = read_file(path=path)
    validators(data=data)
    data = data.sort_values(by=[ABCData.DATA_ANALYSIS], ascending=False)
    data['Доля'] = data[ABCData.DATA_ANALYSIS] / (data[ABCData.DATA_ANALYSIS].sum()) * 100
    data['Аккум.доля'] = data['Доля'].cumsum()
    data["Категория"] = ' '
    data.loc[data['Аккум.доля'] < 80, 'Категория'] = 'A'
    data.loc[(data['Аккум.доля'] >= 80) & (data['Аккум.доля'] < 95), 'Категория'] = 'B'
    data.loc[data['Аккум.доля'] >= 95, 'Категория'] = 'C'
    data = data.round(2)
    return data


def validators(data: pd.DataFrame) -> None:
    if not data[ABCData.DATA_ANALYSIS].apply(np.isreal).all():
        raise FileNotNumericValueError("there is a not numeric value")
    if (data[ABCData.DATA_ANALYSIS] < 0).any():
        raise FileNegativeValueError("there is a negative value")
