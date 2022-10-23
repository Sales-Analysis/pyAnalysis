# import numpy as np
# import pandas as pd
#
# from models import ABCModels
# from code_errors import (
#     FileNotNumericValueError,
#     FileNegativeValueError,
#     SumValuesIsNot100Error,
#     AccumulatedValuesNotCorrect,
#     CategoryIncorrectError,
#     FileIsEmptyError,
#     FileIsEmptyValueError,
# )
#
#
# def validators_abc(data: pd.DataFrame) -> None:
#     """Проводит валидацию на предмет ошибок"""
#     if not data[ABCModels.DATA_ANALYSIS].apply(np.isreal).all():
#         raise FileNotNumericValueError
#     if (data[ABCModels.DATA_ANALYSIS] < 0).any():
#         raise FileNegativeValueError
#     if data[ABCModels.SHARE].values.sum() <= 99.99:
#         raise SumValuesIsNot100Error
#     if not (99.99 < data[ABCModels.ACCUMULATED_SHARE].iloc[-1] < 100.01):
#         raise AccumulatedValuesNotCorrect
#     if not data[ABCModels.CATEGORY].isin([symbol for symbol in "ABC"]).all():
#         raise CategoryIncorrectError
#
#
# def validators_read_file(data: pd.DataFrame) -> None:
#     if data.empty:
#         raise FileIsEmptyError
#     if data.isnull().any().any():
#         raise FileIsEmptyValueError
