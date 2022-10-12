from enum import Enum


class AnalysisModel(str, Enum):
    ABC = 'ABC'


class ABCModels(str, Enum):
    CODE_PLU = 'код идентификатор PLU'
    NAME_ANALYSIS_POSITIONS = 'наименование анализируемых позиций'
    DATA_ANALYSIS = 'данные по анализируемому критерию (продажи/оборот/прибыль)'
    SHARE = 'Доля'
    ACCUMULATED_SHARE = 'Аккум.доля'
    CATEGORY = 'Категория'
