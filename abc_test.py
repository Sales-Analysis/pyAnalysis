from pathlib import *
import pandas as pd

path = Path.home() / "Desktop" / "abc_test.xlsx"
excel_data = pd.read_excel(io=path, engine='openpyxl')

print(excel_data)
