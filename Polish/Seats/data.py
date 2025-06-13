import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser
import re
import numpy as np

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Polish_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

data=pd.DataFrame(df[6])
headers = ['1','Date','2','PiS','KO','Trzecia Droga','Lewica','Konfederacja','6','3','4','5','7']
parties = ['PiS','KO','Trzecia Droga','Lewica','Konfederacja']
drops = ['1','2','3','4','5','6','7']

data.columns = headers
data=data.drop(drops, axis=1)

for z in parties:
  data[z] = [p.sub('', x) for x in data[z].astype(str)]
  data[z] = pd.to_numeric(data[z], errors='coerce')
data = data.dropna(subset=['PiS'])


data['Date'] = [p.sub('', x) for x in data['Date'].astype(str)]
data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

data.to_csv('Polish/Seats/poll.csv', index=False)

parties = ['PiS','KO','Lewica','Konfederacja', 'Trzecia Droga']
UO = ['KO', 'Lewica', 'Trzecia Droga']
R = ['PiS', 'Konfederacja']
data[parties] = data[parties].astype(float)
data['Government (KO + Lewica + Trzecia Droga)'] = data[UO].sum(axis=1)
data['Opposition (PiS + Konfederacja)'] = data[R].sum(axis=1)
data = data.drop(UO + R, axis=1)

data.to_csv('Polish/Seats/poll2.csv', index=False)


