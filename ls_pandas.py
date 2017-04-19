# coding:utf-8
import os
import sys
from pandas import Series,  DataFrame
import pandas as pd
import numpy as np
df253 = pd.read_csv('binlog253.000', sep=' ', names=['time', 'type', 'file'])
# print df253.columns
a = set(df253['file'])

df83 = pd.read_csv('83xiugai', sep=' ', names=['file'])
# print df83.columns
b = set(df83['file'])
# print a - b
# print b -a
c = list(b - a)

df831 = pd.read_csv('binlog83.000', sep=' ', names=['time', 'type', 'file'])
re = df831[df831['file'].isin(c)]
# re = re1[re1['type'].isin(['A','B','C'])]

df = re.groupby(['file', 'type']).count().reset_index()
df_str = df.to_string()
print df_str
print df_str
with open('result', 'w+') as f:
    f.write(df_str)
    f.close()
# aa = df[df['type'].isin(['A','B','C'])]`
# print help(df['type'])
# print aa
