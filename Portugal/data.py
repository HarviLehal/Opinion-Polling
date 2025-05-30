import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Portuguese_legislative_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


# 2024

headers = ['Date','AD','PS','Chega','IL','BE','CDU','LIVRE','PAN','Others']
parties = ['AD','PS','Chega','IL','BE','CDU','LIVRE','PAN','Others']

d={}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(['Polling firm/Link','Sample size','Turnout','Lead'], axis=1)
  d[i].columns = headers
  if i == 0:
    d[i]=d[i][d[i]['Date'] != '9 Jun 2024']
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.nan)) for x in d[i][z]]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i]['Date']=d[i]['Date'].astype(str)
  d[i]=d[i][~d[i].Date.str.contains("18 May 2025")]
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i]=d[i].dropna(subset=['AD'])


D = pd.concat(d.values(), ignore_index=True)

AD=32.10+0.62
PS=23.38
CH=22.56
IL=5.53
BE=2
CD=3.03
PA=1.36
LI=4.20
O=100-AD-PS-CH-IL-BE-CD-PA-LI

new_row = pd.DataFrame({'Date': '18 May 2025', 'AD':AD , 'PS':PS , 'Chega':CH, 'IL':IL, 'BE':BE, 'CDU':CD,'PAN':PA,'LIVRE':LI,'Others':O}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D.to_csv('Portugal/poll.csv', index=False)

