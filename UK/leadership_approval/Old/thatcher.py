import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re


df = pd.read_csv('UK/leadership_approval/Old/thatcher.csv')

df.columns = ['Date','1','2','Approve','Disapprove','3','4']
df.drop(['1','2','3','4'], axis=1, inplace=True)

df['total'] = df['Approve'] + df['Disapprove']
df['Approve'] = df['Approve'] / df['total'] * 100
df['Disapprove'] = df['Disapprove'] / df['total'] * 100
df.drop('total', axis=1, inplace=True)

# convert the date to datetime
df['Date'] = pd.to_datetime(df['Date'])

df.to_csv('UK/leadership_approval/Old/thatcher_adjusted.csv', index=False)
