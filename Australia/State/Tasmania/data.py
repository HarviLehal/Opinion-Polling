import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Next_Tasmanian_state_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))


headers=['Date','Firm','Liberal', 'Labor', 'Green', 'JLN', 'Other','1','2']
parties = ['Liberal', 'Labor', 'Green', 'JLN', 'Other']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[2])
  d[i].columns = headers
  d[i]=d[i].drop(['Firm','1','2'], axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Labor'] != d[i]['Other']]

D = pd.concat(d.values(), ignore_index=True)
D.to_csv('Australia/State/Tasmania/poll.csv', index=False)
