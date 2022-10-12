import pandas as pd
import numpy as np
from enum import Enum
from pydantic import BaseModel
from models import AnalysisModel
from filemanager import read_file
from code_errors import (
    FileNotNumericValueError,
    FileNegativeValueError,
    NotFoundAnalysisError,
    SumValuesIsNot100Error,
    AccumulatedValuesNotCorrect,
    CategoryIncorrectError,
)


class ABCData(str, Enum):
    CODE_PLU = 'код идентификатор PLU'
    NAME_ANALYSIS_POSITIONS = 'наименование анализируемых позиций'
    DATA_ANALYSIS = 'данные по анализируемому критерию (продажи/оборот/прибыль)'
    SHARE = 'Доля'
    ACCUMULATED_SHARE = 'Аккум.доля'
    CATEGORY = 'Категория'


# class File(BaseModel):
    # path = "./tests/data/abc_test.xlsx"
    # data = read_file(path=path)
    # abc(): pd.DataFrame  #??
    # data = BaseModel     #??
    # data: pd.DataFrame
    # data[ABCData.SHARE]: float
    # data[ABCData.DATA_ANALYSIS]: [float, int]  # можно так?
    # data[ABCData.ACCUMULATED_SHARE]: float
    # data[ABCData.CATEGORY]: str
    # data[ABCData.CODE_PLU]: int
    # data[ABCData.NAME_ANALYSIS_POSITIONS]: str

def analysis(path: str, type_analysis: str = 'ABC') -> pd.DataFrame:
    if type_analysis not in set(i.value for i in AnalysisModel):
        raise NotFoundAnalysisError

    if type_analysis == AnalysisModel.ABC:
        return abc(path=path)


def abc(path: str) -> pd.DataFrame:
    """делает расчет abc анализа"""
    # path = "./tests/data/abc_test.xlsx"
    data = read_file(path=path)
    data = data.sort_values(by=[ABCData.DATA_ANALYSIS], ascending=False)
    data = share(data=data)
    data = accumulated_share(data=data)
    data = category(data=data)
    data = data.round(2)
    validators(data=data)
    data = data.reset_index(drop=True)
    return data


# def good_type():
#     result = File(abc())
#     return result


def share(data: pd.DataFrame) -> pd.DataFrame:
    """считает долю от анализируемой колонки в %"""
    data[ABCData.SHARE] = data[ABCData.DATA_ANALYSIS] / (data[ABCData.DATA_ANALYSIS].sum()) * 100
    return data


def accumulated_share(data: pd.DataFrame) -> pd.DataFrame:
    """считает накопленную долю в %"""
    data[ABCData.ACCUMULATED_SHARE] = data[ABCData.SHARE].cumsum()
    return data


def category(data: pd.DataFrame) -> pd.DataFrame:
    """разбивает по категориям a,b,c в зависимости от накопленной доли"""
    data.loc[data[ABCData.ACCUMULATED_SHARE] < 80, ABCData.CATEGORY] = 'A'
    data.loc[(data[ABCData.ACCUMULATED_SHARE] >= 80) & (data[ABCData.ACCUMULATED_SHARE] < 95),
             ABCData.CATEGORY] = 'B'
    data.loc[data[ABCData.ACCUMULATED_SHARE] >= 95, ABCData.CATEGORY] = 'C'
    return data


def validators(data: pd.DataFrame) -> None:
    """проводит валидацию на предмет ошибок"""
    if not data[ABCData.DATA_ANALYSIS].apply(np.isreal).all():
        raise FileNotNumericValueError("There is a not numeric value.")
    if (data[ABCData.DATA_ANALYSIS] < 0).any():
        raise FileNegativeValueError("There is a negative value.")
    if data[ABCData.SHARE].values.sum() <= 99.99:
        raise SumValuesIsNot100Error("The sum of the values is not 100.")
    if not (99.99 < data[ABCData.ACCUMULATED_SHARE].iloc[-1] < 100.01):
        raise AccumulatedValuesNotCorrect("The accumulated share was calculated incorrectly.")
    if not data[ABCData.CATEGORY].isin([symbol for symbol in "ABC"]).all():
        raise CategoryIncorrectError("There is no such category.")
