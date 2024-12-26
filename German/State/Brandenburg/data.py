import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2024_Brandenburg_state_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

df0=pd.DataFrame(df[-2])
data22 = df0.drop(["Polling firm", "Sample size","Lead"], axis=1)
headers = ['Date','SPD','AfD','CDU','Grüne','Linke','BVB/FW','FDP','BSW','Others']
parties = ['SPD','AfD','CDU','Grüne','Linke','BVB/FW','FDP','BSW','Others']
data22.columns = headers
data22['Date'] = [x.strip()[-11:] for x in data22['Date'].astype(str)]
data22['Date'] = [x.replace('–','') for x in data22['Date'].astype(str)]
data22=data22[~data22.Date.str.contains("26 Sep 2021")]
data22=data22[~data22.Date.str.contains("9 Jun 2024")]
for z in parties:
  data22[z] = [p.sub('', x) for x in data22[z].astype(str)]
  data22[z] = [x.replace('–',str(np.nan)) for x in data22[z].astype(str)]
  data22[z] = [x.replace('—',str(np.nan)) for x in data22[z].astype(str)]
data22=data22[~data22.Others.str.contains(".mw-parser-output")]
data22[parties] = data22[parties].astype(float)


data22
split_date = '10 Nov 2023'

split_date=dateparser.parse(split_date)

d={}
d[0]=data22[(pd.to_datetime(data22["Date"]) > split_date)]
d[1]=data22[(pd.to_datetime(data22["Date"]) < split_date)]

d[1]=d[1].drop(d[1][d[1]['BSW']>0].index)

data22 = pd.concat(d.values(), ignore_index=True)

print(data22)
# data22.drop(data22.index[[0]],inplace=True)
# 
# S=30.9
# A=29.2
# C=12.1
# G=4.1
# L=3.0
# BV=2.6
# F=0.8
# B=13.5
# O=100-L-A-C-S-G-F-B-BV
# 
# new_row = pd.DataFrame({'Date':'22 September 2024','SPD':S,'AfD':A,'CDU':C,'Grüne':G,'Linke':L,'BVB/FW':BV,'FDP':F,'BSW':B,'Others':O}, index=[0])
# D = pd.concat([new_row,data22]).reset_index(drop=True)
# D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

data22.to_csv('German/State/Brandenburg/poll.csv', index=False)
