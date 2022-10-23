import openpyxl
from code_errors import FileIsEmptyError
from typing import Dict, Union, List


def read_exel(path: str):
    wb = openpyxl.load_workbook(path)
    worksheet = wb.worksheets[0]
    iter_rows = worksheet.iter_rows()

    try:
        header: List[str] = [cell.value for cell in next(iter_rows)]
    except StopIteration:
        raise FileIsEmptyError
    rows: List[Dict[str, List[Union[int, str, float]]]] = read_rows(header=header, rows=iter_rows)
    if not rows:
        raise FileIsEmptyError
    result = convert_dict(header=header, rows=rows)
    return result


def convert_dict(header, rows):
    """Конвертирует в один словарь"""
    result: dict[str, List[Union[int, str, float]]] = {}
    for key in header:
        arr: List[Union[int, str, float]] = []
        for into_rows in rows:
            arr.append(into_rows[key])
        result[key] = arr
    return result


def read_rows(header, rows):
    result: List[Dict[str, List[Union[int, str, float]]]] = []
    for row in rows:
        result.append(read_cells(header, cells=row))
    return result


def read_cells(header, cells):
    result: Dict[str, List[Union[int, str, float]]] = {}
    for j, cell in enumerate(cells):
        result[header[j]] = cell.value
    return result
