
from pandas import *
xls = ExcelFile('exceltopython.xlsx')
data = xls.parse(xls.sheet_names[0])
datavalues = data.to_dict()
print(datavalues)
for key in datavalues:
    print(key)
print('hi')
filename = 'exceltopython.xlsx'
import pandas as pd
df = pd.read_excel('exceltopython.xlsx')
l1 = []
print(l1)
for index, row in df.iterrows():
    l1.append(row.to_list())
print(l1)

print(totalamount)
df = pd.read_excel('exceltopython.xlsx')
l1 = []
print(l1)
for index, row in df.iterrows():
    l1.append(row.to_list())
print(l1)
dbframes = exceldata.objects.all()
print(dbframes)