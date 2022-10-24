import itertools
from typing import Dict, Union, List

from code_errors import NotFoundAnalysisError
from filemanager import read_exel
from models import ABCModels, AnalysisModel


class ABCAnalysis:
    """ABC analysis."""

    def __init__(self, data: Dict[str, List[Union[int, str, float]]]):
        self.data = data

    def result(self):
        return self.data

    @property
    def sorted(self):
        """Сортирует входные анализируемые данные в порядке убывания."""
        values: List[Union[int, float]] = self.data[ABCModels.DATA_ANALYSIS].copy()
        values.sort(reverse=True)
        result: Dict[str, List[Union[int, str, float]]] = {}
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
        sum_numbers: Union[int, float] = sum(self.data[ABCModels.DATA_ANALYSIS.value])
        arr: List[Union[int, float]] = []
        for analysis_number in self.data[ABCModels.DATA_ANALYSIS.value]:
            s = analysis_number / sum_numbers * 100
            arr.append(s)
        self.data[ABCModels.SHARE.value] = arr

    @property
    def accumulated_share(self):
        """Считает накопленную долю в %"""
        self.data[ABCModels.ACCUMULATED_SHARE.value] = [
            i for i in itertools.accumulate(self.data[ABCModels.SHARE.value])
        ]

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
        self.data[ABCModels.SHARE.value] = [
            round(i, 2) for i in self.data[ABCModels.SHARE.value]
        ]
        self.data[ABCModels.ACCUMULATED_SHARE.value] = [
            round(i, 2) for i in self.data[ABCModels.ACCUMULATED_SHARE.value]
        ]


def analysis(type_analysis: str, path: str):
    """Проверяет на модель анализа"""
    if type_analysis not in set(i.value for i in AnalysisModel):
        raise NotFoundAnalysisError

    if type_analysis == AnalysisModel.ABC:
        return abc_analysis(path=path)


def abc_analysis(path: str):
    """Делает расчет abc анализа"""
    data = read_exel(path=path)
    a = ABCAnalysis(data=data)
    a.sorted
    a.share
    a.accumulated_share
    a.category
    a.round
    result = a.result()
    return result
