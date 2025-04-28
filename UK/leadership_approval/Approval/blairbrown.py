import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re


# load the csv
df = pd.read_csv('UK/leadership_approval/Approval/blair.csv')

df['total'] = df['Approve'] + df['Disapprove']
df['Approve'] = df['Approve'] / df['total'] * 100
df['Disapprove'] = df['Disapprove'] / df['total'] * 100
df['Net Approval'] = df['Approve'] - df['Disapprove']
df.drop(['total','Approve','Disapprove'], axis=1, inplace=True)
df.Date=df.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first','DATE_ORDER': 'DMY'}))

df.to_csv('UK/leadership_approval/Approval/blair_net.csv', index=False)

df2= pd.read_csv('UK/leadership_approval/Approval/brown.csv')
df2['total'] = df2['Approve'] + df2['Disapprove']
df2['Approve'] = df2['Approve'] / df2['total'] * 100
df2['Disapprove'] = df2['Disapprove'] / df2['total'] * 100
df2['Net Approval'] = df2['Approve'] - df2['Disapprove']
df2.drop(['total','Approve','Disapprove'], axis=1, inplace=True)
df2.Date=df2.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first','DATE_ORDER': 'DMY'}))

df2.to_csv('UK/leadership_approval/Approval/brown_net.csv', index=False)




# load the other 2 csvs
df = pd.read_csv('UK/leadership_approval/Approval/major.csv')

df['total'] = df['Approve'] + df['Disapprove']
df['Approve'] = df['Approve'] / df['total'] * 100
df['Disapprove'] = df['Disapprove'] / df['total'] * 100
df['Net Approval'] = df['Approve'] - df['Disapprove']
df.drop(['total','Approve','Disapprove'], axis=1, inplace=True)
df.Date=df.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first','DATE_ORDER': 'DMY'}))

df.to_csv('UK/leadership_approval/Approval/major_net.csv', index=False)

df2= pd.read_csv('UK/leadership_approval/Approval/thatcher.csv')
df2['total'] = df2['Approve'] + df2['Disapprove']
df2['Approve'] = df2['Approve'] / df2['total'] * 100
df2['Disapprove'] = df2['Disapprove'] / df2['total'] * 100
df2['Net Approval'] = df2['Approve'] - df2['Disapprove']
df2.drop(['total','Approve','Disapprove'], axis=1, inplace=True)
df2.Date=df2.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first','DATE_ORDER': 'DMY'}))

df2.to_csv('UK/leadership_approval/Approval/thatcher_net.csv', index=False)
