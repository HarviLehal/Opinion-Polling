import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2025_Tasmanian_state_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


headers=['Date','1','2','3','Liberal', 'Labor', 'Green','o1','o2', 'JLN*','o3', 'o4']
parties = ['Liberal', 'Labor', 'Green','o1','o2', 'JLN*','o3', 'o4']
drops=['1','2','3']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[0])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Labor'] != d[i]['Green']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')

D = pd.concat(d.values(), ignore_index=True)
# for z in parties:
#   D[z] = D[z].astype(str)
#   D[z] = D[z].str.strip('%')
#   D[z] = D[z].astype('float')
#         d[i][z] = pd.to_numeric(d[i][z], errors='coerce')

oth=['o1','o2']
D['Other']=D[oth].sum(axis=1)
D = D.drop(oth, axis=1)

# Lib=36.76
# Lab=29.41
# Gre=13.37
# JL=6.75
# Oth=100-Lib-Lab-Gre-JL
# 
# new_row = pd.DataFrame({'Date': '23 Mar 2024', 'Liberal':Lib, 'Labor':Lab, 'Green':Gre, 'JLN*':JL, 'Other':Oth}, index=[0])
# D = pd.concat([new_row,D]).reset_index(drop=True)
# D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D.to_csv('Australia/State/Tasmania/poll.csv', index=False)
