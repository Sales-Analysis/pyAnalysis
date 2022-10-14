import pandas as pd
from pydantic import BaseModel
from models import (
    AnalysisModel,
    ABCModels,
)
from filemanager import read_file
from code_errors import (
    NotFoundAnalysisError,
)
from validators import validators_abc


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

def analysis(type_analysis: str, path: str) -> pd.DataFrame:
    if type_analysis not in set(i.value for i in AnalysisModel):
        raise NotFoundAnalysisError

    if type_analysis == AnalysisModel.ABC:
        return abc(path=path)


def abc(path: str) -> pd.DataFrame:
    """Делает расчет abc анализа"""
    # path = "./tests/data/abc_test.xlsx"
    data = read_file(path=path)
    data = data.sort_values(by=[ABCModels.DATA_ANALYSIS], ascending=False)
    data = share(data=data)
    data = accumulated_share(data=data)
    data = category(data=data)
    data = data.round(2)
    validators_abc(data=data)
    data = data.reset_index(drop=True)
    return data


# def good_type():
#     result = File(abc())
#     return result


def share(data: pd.DataFrame) -> pd.DataFrame:
    """Cчитает долю от анализируемой колонки в %"""
    data[ABCModels.SHARE] = data[ABCModels.DATA_ANALYSIS] / (data[ABCModels.DATA_ANALYSIS].sum()) * 100
    return data


def accumulated_share(data: pd.DataFrame) -> pd.DataFrame:
    """Считает накопленную долю в %"""
    data[ABCModels.ACCUMULATED_SHARE] = data[ABCModels.SHARE].cumsum()
    return data


def category(data: pd.DataFrame) -> pd.DataFrame:
    """Разбивает по категориям a,b,c в зависимости от накопленной доли"""
    data.loc[data[ABCModels.ACCUMULATED_SHARE] < 80, ABCModels.CATEGORY] = 'A'
    data.loc[(data[ABCModels.ACCUMULATED_SHARE] >= 80) & (data[ABCModels.ACCUMULATED_SHARE] < 95),
             ABCModels.CATEGORY] = 'B'
    data.loc[data[ABCModels.ACCUMULATED_SHARE] >= 95, ABCModels.CATEGORY] = 'C'
    return data



