import pandas as pd
import datetime

df = pd.read_csv('data/train.csv')
df['date'] = pd.to_datetime(df['date'])

print(df['year_week'][:2])
print(type(df['year_week'][0]))
print(df.head())
df.to_csv('data/preprocessed_train.csv', index = False)