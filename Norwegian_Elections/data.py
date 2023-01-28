import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2025_Norwegian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

headers = ['Date','R','SV','MDG','Ap','Sp','V','KrF','H','FrP']
parties = ['R','SV','MDG','Ap','Sp','V','KrF','H','FrP']
d = {}
for i in range(3):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Polling firm", "Sample size", "Resp.", "Others", "Lead"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  d[i] = d[i][d[i]['KrF'] != d[i]['H']]

for i in range(2):
  d[i].drop(d[i].index[[-1]],inplace=True)

D = pd.concat(d.values(), ignore_index=True)
D.to_csv('Norwegian_Elections/poll.csv', index=False)
