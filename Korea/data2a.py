import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2025_South_Korean_presidential_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
p = re.compile(r'\[[a-z]+\]')
df=pd.read_html(str(tables))

headers = ['Date','1','2','3','Lee Jae-myung','Kim Moon-soo','Lee Jun-seok','Kwon Yeong-guk','Koo Joo-wa*','Hwang Kyo-ahn*','Song Jin-ho','Other','4','5']
parties = ['Lee Jae-myung','Kim Moon-soo','Lee Jun-seok','Kwon Yeong-guk','Koo Joo-wa*','Hwang Kyo-ahn*','Song Jin-ho','Other']
drops = ['1','2','3','4','5']
d = {}

for i in range(1):
  d[i]=pd.DataFrame(df[0])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Lee Jun-seok'] != d[i]['Lee Jae-myung']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = d[i][z].astype('float').astype(str)

D = pd.concat(d.values(), ignore_index=True)
# D.drop(D.index[[-1]],inplace=True)

c={}
c[0] = D[:1]
c[1] = D[1:]
c[1] = c[1][(pd.to_datetime(c[1]["Date"])<dateparser.parse("3 June 2025"))]
D = pd.concat(c.values(), ignore_index=True)

D.to_csv('Korea/poll2a.csv', index=False)
