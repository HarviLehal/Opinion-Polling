import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2025_Portuguese_legislative_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


# 2024

headers = ['1','Date','2','3','AD','PS','Chega','IL','BE','CDU','LIVRE','PAN','Others','4']
parties = ['AD','PS','Chega','IL','BE','CDU','LIVRE','PAN','Others']
drops = ['1','2','3','4']
d={}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
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

AD=31.20+0.58
PS=22.83
CH=22.76
IL=5.36
BE=1.99
CD=2.91
PA=1.38
LI=5.36
O=100-AD-PS-CH-IL-BE-CD-PA-LI

new_row = pd.DataFrame({'Date': '18 May 2025', 'AD':AD , 'PS':PS , 'Chega':CH, 'IL':IL, 'BE':BE, 'CDU':CD,'LIVRE':LI,'PAN':PA,'Others':O}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

# c={}
# c[0] = D[:1]
# c[1] = D[1:]
# c[1] = c[1][(pd.to_datetime(c[1]["Date"])<dateparser.parse("18 May 2025"))]
# D = pd.concat(c.values(), ignore_index=True)

D.to_csv('Portugal/poll.csv', index=False)

