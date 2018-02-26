import pandas as pd
import numpy as np
import matplotlib
%%matplotlib inline

df = pd.DataFrame()
print(df)

df = pd.read_csv('week-03/data/skyhook_2017-07.csv',sep=',')

df.head()
df.shape

df.columns
df['cat'] #call certain column

A = df[df['hour']==158]
df[(df['hour']==158) & (df['count']>50)]

bastille = df[df['date'] == '2017-07-14']
hype = bastille[bastille['count']>bastille['count'].mean()]
hype['count'].describe()

df.groupby('date')['count'].describe()

df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df['weekday']=df['date_new'].apply(lambda x:x.weekday() + 1)
df['weekday'].replace(7,0,inplace=True)
