import pandas as pd
xl = pd.ExcelFile('timetable.xlsx')

print(xl.sheet_names)