from functools import reduce

import pandas as pd
from typing import Dict, Union, List
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
    # data = read_file(path=path)
    # data = data.sort_values(by=[ABCModels.DATA_ANALYSIS], ascending=False)
    # data = share(data=data)
    # data = accumulated_share(data=data)
    # data = category(data=data)
    # data = data.round(2)
    validators_abc(data=data)
    data = data.reset_index(drop=True)
    return data


# def good_type():
#     result = File(abc())
#     return result


# def share(data: pd.DataFrame) -> pd.DataFrame:
#     """Cчитает долю от анализируемой колонки в %"""
#     data[ABCModels.SHARE] = data[ABCModels.DATA_ANALYSIS] / (data[ABCModels.DATA_ANALYSIS].sum()) * 100
#     return data


# def accumulated_share(data: pd.DataFrame) -> pd.DataFrame:
#     """Считает накопленную долю в %"""
#     data[ABCModels.ACCUMULATED_SHARE] = data[ABCModels.SHARE].cumsum()
#     return data


# def category(data: pd.DataFrame) -> pd.DataFrame:
#     """Разбивает по категориям a,b,c в зависимости от накопленной доли"""
#     data.loc[data[ABCModels.ACCUMULATED_SHARE] < 80, ABCModels.CATEGORY] = 'A'
#     data.loc[(data[ABCModels.ACCUMULATED_SHARE] >= 80) & (data[ABCModels.ACCUMULATED_SHARE] < 95),
#              ABCModels.CATEGORY] = 'B'
#     data.loc[data[ABCModels.ACCUMULATED_SHARE] >= 95, ABCModels.CATEGORY] = 'C'
#     return data


class ABCAnalysis:
    """ABC analysis."""
    def __init__(self, data: Dict[str, List[Union[int, str, float]]]):
        self.data = data

    def result(self):
        return self.data

    @property
    def sorted(self):
        values: List[Union[int, float]] = self.data[ABCModels.DATA_ANALYSIS].copy()
        values.sort(reverse=True)
        result = {}
        for key in self.data.keys():
            if key == ABCModels.DATA_ANALYSIS:
                result[key] = values
                continue
            arr = []
            for value in values:
                index = self.data[ABCModels.DATA_ANALYSIS.value].index(value)
                arr.append(self.data[key][index])
            result[key] = arr
        self.data = result

    @property
    def share(self):
        """Cчитает долю от анализируемой колонки в %"""
        sum_analysis_numbers: Union[int, float] = sum(self.data[ABCModels.DATA_ANALYSIS.value])
        arr: List[Union[int, float]] = []
        for analysis_number in self.data[ABCModels.DATA_ANALYSIS.value]:
            s = analysis_number / sum_analysis_numbers * 100
            arr.append(s)
        self.data[ABCModels.SHARE.value] = arr

    @property
    def accumulated_share(self):
        """Считает накопленную долю в %"""
        arr: List[Union[int, float]] = []
        accum_numbers = 0
        for number_share in self.data[ABCModels.SHARE.value]:
            accum_numbers += number_share
            arr.append(accum_numbers)
        self.data[ABCModels.ACCUMULATED_SHARE.value] = arr

    @property
    def category(self):
        """Разбивает по категориям a,b,c в зависимости от накопленной доли"""
        arr: List[str] = []
        for accum_numb in self.data[ABCModels.ACCUMULATED_SHARE.value]:
            if accum_numb < 80:
                arr.append("A")
            elif 80 <= accum_numb < 95:
                arr.append("B")
            elif accum_numb >= 95:
                arr.append("C")
        self.data[ABCModels.CATEGORY.value] = arr

    @property
    def round(self):
        arr: List[Union[int, float]] = []
        arr2: List[Union[int, float]] = []
        for value_share in self.data[ABCModels.SHARE.value]:
            arr.append(round(value_share, 2))
        self.data[ABCModels.SHARE.value] = arr
        for value_share in self.data[ABCModels.ACCUMULATED_SHARE.value]:
            arr2.append(round(value_share, 2))
        self.data[ABCModels.ACCUMULATED_SHARE.value] = arr2
