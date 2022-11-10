from enum import Enum
from typing import List, Union

from pydantic import BaseModel


class AnalysisModel(str, Enum):
    ABC = 'ABC'


class ABCModels(str, Enum):
    CODE_PLU = 'код идентификатор PLU'
    NAME_ANALYSIS_POSITIONS = 'наименование анализируемых позиций'
    DATA_ANALYSIS = 'данные по анализируемому критерию (продажи/оборот/прибыль)'
    SHARE = 'Доля'
    ACCUMULATED_SHARE = 'Аккум.доля'
    CATEGORY = 'Категория'


class InputModel(BaseModel):
    CODE_PLU: List[int]
    NAME_ANALYSIS_POSITIONS: List[str]
    DATA_ANALYSIS: List[Union[int, float]]


class OutputModel(BaseModel):
    CODE_PLU: List[int]
    NAME_ANALYSIS_POSITIONS: List[str]
    DATA_ANALYSIS: List[Union[float]]
    SHARE: List[Union[float]]
    ACCUMULATED_SHARE: List[Union[float]]
    CATEGORY: List[str]
