import pandas as pd
import pytest
from filemanager import read_file


@pytest.fixture
def data_exel():
    data = pd.DataFrame([1, 2, 3])
    return data


def test_read_file(data_exel):
    path = "./data/data_test.xlsx"
    reading_file = read_file(path=path)
    pd.testing.assert_frame_equal(data_exel, reading_file)


