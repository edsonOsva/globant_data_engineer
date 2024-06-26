import pandas as pd
from datetime import datetime

df = pd.read_csv('C:/Users/edson.perez/Desktop/hired_employees (3) (2) (1).csv', header=None)
print(df.head())


df2 = df.fillna({4: 1})
print(df2.head())

now = datetime.now()
print(now)

pass