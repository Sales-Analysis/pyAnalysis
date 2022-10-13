import pandas as pd
from typing import Optional
from validators import validators_read_file


def read_file(path: str, header: Optional[int] = 0) -> pd.DataFrame:
    data = pd.read_excel(path, header=header)
    try:
        validators_read_file(data=data)
    except Exception as err:
        raise Exception(err)
    return data

