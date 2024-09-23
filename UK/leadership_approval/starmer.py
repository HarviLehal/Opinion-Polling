import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re


# load the csv
df = pd.read_csv('UK/leadership_approval/starmer_approval.csv')

df2= pd.read_csv('UK/leadership_approval/Approval/starmer.csv')

df2.columns = ['Date','Approval','Disapproval','Neither']
df = pd.concat([df,df2])
df.drop('Neither', axis=1, inplace=True)

df['total'] = df['Approval'] + df['Disapproval']
df['Approval'] = df['Approval'] / df['total'] * 100
df['Disapproval'] = df['Disapproval'] / df['total'] * 100
df.drop('total', axis=1, inplace=True)

df.to_csv('UK/leadership_approval/starmer_approval_long.csv', index=False)
