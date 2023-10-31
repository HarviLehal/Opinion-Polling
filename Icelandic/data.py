import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Next_Icelandic_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

data22=pd.DataFrame(df[2])

headers = ['1','Date','2','3','D','B','V','S','F','P','C','M','J','4','5']
parties = ['D','B','V','S','F','P','C','M','J']
data22.columns = headers
data22 = data22.drop(['1','2','3','4','5'], axis=1)


data22['Date2'] = data22['Date'].str.split('–').str[1]
data22.Date2.fillna(data22['Date'].str.split('-').str[1], inplace=True)
data22.Date2.fillna(data22.Date, inplace=True)
data22.Date = data22.Date2
data22 = data22.drop(['Date2'],axis=1)
data22.Date = data22['Date'].astype(str)
data22.Date = data22.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

print(data22)

data22.to_csv('Icelandic/poll.csv', index=False)
data22[parties] = data22[parties].astype(float)

Left = ['V','S','P','F','J']
Right = ['D','B','M']

data22['Left (VSPFJ)'] = data22[Left].sum(axis=1)
data22['Right (DBM)'] = data22[Right].sum(axis=1)
data22 = data22.drop(Left + Right, axis=1)

data22.to_csv('Icelandic/poll2.csv', index=False)
