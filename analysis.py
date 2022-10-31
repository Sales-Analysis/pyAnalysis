import itertools
from collections import Counter
from typing import Dict, Union, List
from code_errors import NotFoundAnalysisError
from filemanager import read_exel
from models import ABCModels, AnalysisModel


def analysis(type_analysis: str, path: str):
    """Проверяет на модель анализа"""

    if type_analysis not in set(i.value for i in AnalysisModel):
        raise NotFoundAnalysisError

    data = read_exel(path=path)
    data = pre_data(data=data)
    if type_analysis == AnalysisModel.ABC:
        return abc_analysis(data=data)


def pre_data(data: Dict[str, List[Union[int, str, float]]]):
    result = find_duplicate_values(data=data)
    return result


def find_duplicate_values(
        data: Dict[str, List[Union[int, str, float]]]
) -> Dict[str, List[Union[int, str, float]]]:
    """Удаляет повторяющиеся строчки."""

    result = {key: [] for key in data.keys()}
    for i, v in enumerate(data[ABCModels.CODE_PLU]):
        name_analysis_position = data[ABCModels.NAME_ANALYSIS_POSITIONS]
        data_analysis = data[ABCModels.DATA_ANALYSIS]
        if (v in result[ABCModels.CODE_PLU]) and \
                (name_analysis_position[i] in result[ABCModels.NAME_ANALYSIS_POSITIONS]) and \
                (data_analysis[i] in result[ABCModels.DATA_ANALYSIS]):
            continue
        result[ABCModels.CODE_PLU].append(v)
        result[ABCModels.NAME_ANALYSIS_POSITIONS].append(
            data[ABCModels.NAME_ANALYSIS_POSITIONS][i]
        )
        result[ABCModels.DATA_ANALYSIS].append(data[ABCModels.DATA_ANALYSIS][i])
    return result


def join_duplicate(
        data: Dict[str, List[Union[int, str, float]]]
) -> Dict[str, List[Union[int, str, float]]]:
    """Объединяет повторяющиеся имена со значениями"""
    result = data
    name_analysis_position = data[ABCModels.NAME_ANALYSIS_POSITIONS]
    data_analysis = data[ABCModels.DATA_ANALYSIS]
    count_name_analysis_position = Counter(result[ABCModels.NAME_ANALYSIS_POSITIONS])
    number_repetitions_name_analysis_position = 0
    for i, v in enumerate(data[ABCModels.CODE_PLU]):
        if ((name_analysis_position[i] in count_name_analysis_position) and
                count_name_analysis_position.get(name_analysis_position[i]) > 1):
            if number_repetitions_name_analysis_position == 0:
                number_repetitions_name_analysis_position += 1
                continue
            # вычисляет индекс в колонке анализируемых позиций, с которой будем складывать
            for j, k in enumerate(result[ABCModels.NAME_ANALYSIS_POSITIONS]):
                if name_analysis_position[i] == k:
                    summa_repeat = result[ABCModels.DATA_ANALYSIS][j] + data[ABCModels.DATA_ANALYSIS][i]
                    result[ABCModels.DATA_ANALYSIS].append(summa_repeat)
                    del result[ABCModels.DATA_ANALYSIS][j]
                    number_repetitions_name_analysis_position = 0
    return result


def abc_analysis(data: Dict[str, List[Union[int, str, float]]]):
    """Делает расчет abc анализа."""

    a = ABCAnalysis(data=data)
    a.sorted
    a.share
    a.accumulated_share
    a.category
    a.round
    result = a.result()
    return result


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
