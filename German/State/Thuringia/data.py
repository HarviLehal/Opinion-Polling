import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/2024_Thuringian_state_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

df0=pd.DataFrame(df[1])
data22 = df0.drop(["Polling firm", "Sample size","Lead"], axis=1)
headers = ['Date','Linke','AfD','CDU','SPD','Grüne','FDP','BSW','Others']
parties = ['Linke','AfD','CDU','SPD','Grüne','FDP','BSW','Others']
data22.columns = headers
data22['Date'] = [x.strip()[-11:] for x in data22['Date'].astype(str)]
data22['Date'] = [x.replace('–','') for x in data22['Date'].astype(str)]
data22=data22[~data22.Date.str.contains("26 Sep 2021")]
data22=data22[~data22.Date.str.contains("9 Jun 2024")]
for z in parties:
    data22[z] = [x.replace('–',str(np.nan)) for x in data22[z].astype(str)]
    data22[z] = [x.replace('—',str(np.nan)) for x in data22[z].astype(str)]
data22=data22[~data22.Others.str.contains(".mw-parser-output")]
data22[parties] = data22[parties].astype(float)


data22
split_date = '01 Jan 2024'

split_date=dateparser.parse(split_date)

d={}
d[0]=data22[(pd.to_datetime(data22["Date"]) > split_date)]
d[1]=data22[(pd.to_datetime(data22["Date"]) < split_date)]

d[1]=d[1].drop(d[1][d[1]['BSW']>0].index)

data22 = pd.concat(d.values(), ignore_index=True)

print(data22)
# 
# L=12.9
# A=32.8
# C=23.8
# S=6.1
# G=3.3
# F=1.2
# B=15.5
# O=100-L-A-C-S-G-F-B
# 
# new_row = pd.DataFrame({'Date':'01 September 2024','Linke':L,'AfD':A,'CDU':C,'SPD':S,'Grüne':G,'FDP':F,'BSW':B,'Others':O}, index=[0])
# D = pd.concat([new_row,data22]).reset_index(drop=True)
# D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

data22.to_csv('German/State/Thuringia/poll.csv', index=False)
