import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://is.wikipedia.org/wiki/N%C3%A6stu_al%C3%BEingiskosningar"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables), decimal=',', thousands='.')

data22=pd.DataFrame(df[-1])

headers = ['1','Date','2','3','S','D','C','F','M','B','J','P','V','4','5']
parties = ['S','D','C','F','M','B','J','P','V']
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
data22 = data22.dropna(subset=['Date'])
for z in parties:
    data22[z] = [p.sub('', x) for x in data22[z].astype(str)]
    data22[z] = pd.to_numeric(data22[z], errors='coerce')
data22 = data22.dropna(subset=['S'])

data22.to_csv('Icelandic/poll.csv', index=False)

for z in parties:
  data22[z] = data22[z].apply(lambda x: x if x > 5 else 0)

Gov = ['S','C','F']
Right = ['D','B','M']
Left = ['V','P','J']
data22['Gov (SCF)'] = data22[Gov].sum(axis=1)
data22['Right (DBM)'] = data22[Right].sum(axis=1)
data22['Left (VPJ)'] = data22[Left].sum(axis=1)
data22 = data22.drop(Gov + Left + Right, axis=1)

data22.to_csv('Icelandic/poll2.csv', index=False)
