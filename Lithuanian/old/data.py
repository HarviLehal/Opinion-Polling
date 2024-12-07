import pandas as pd # library for data analysis
import numpy as np
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser
import re
wikiurl="https://en.wikipedia.org/wiki/2024_Lithuanian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

data22=pd.DataFrame(df[-3])
headers = ['1','Date','2','TS–LKD', 'LVŽS', 'DP', 'LSDP', 'LP', 'LS', 'LLRA', 'LRP', 'TTS', 'LT', 'DSVL','NA','3','4']
parties = ['TS–LKD', 'LVŽS', 'DP', 'LSDP', 'LP', 'LS', 'LLRA', 'LRP', 'TTS', 'LT', 'DSVL','NA']
data22.columns = headers
data22 = data22.drop(["1","2","3","4"], axis=1)
headers = ['Date','TS–LKD', 'LVŽS', 'DP', 'LSDP', 'LP', 'LS', 'LLRA', 'LRP', 'TTS', 'LT', 'DSVL','NA']

for z in headers:
    data22[z] = [p.sub('', x) for x in data22[z].astype(str)]
# data22['Date'] = [x.replace('[a]','') for x in data22['Date'].astype(str)]
# data22['Date'] = [x.replace('[b]','') for x in data22['Date'].astype(str)]
# data22['Date'] = [x.replace('[c]','') for x in data22['Date'].astype(str)]
# data22['Date'] = [x.replace('[d]','') for x in data22['Date'].astype(str)]
# data22['Date'] = [x.replace('[e]','') for x in data22['Date'].astype(str)]
# data22['Date'] = [x.replace('[f]','') for x in data22['Date'].astype(str)]
data22 = data22[data22['Date'] != '5 March 2023']
data22 = data22[data22['Date'] != '9 June 2024']

data22['Date2'] = data22['Date'].str.split('–').str[1]
data22.Date2.fillna(data22['Date'].str.split('-').str[1], inplace=True)
data22.Date2.fillna(data22.Date, inplace=True)
data22.Date = data22.Date2
data22 = data22.drop(['Date2'],axis=1)
data22.Date = data22['Date'].astype(str)
data22=data22.reset_index(drop=True)
data22.drop(data22.index[[-1]],inplace=True)
data22=data22.reset_index(drop=True)
data22.loc[len(data22.index)-1,['Date']] = '11 October 2020'
data22.Date = data22.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

for z in parties:
  # data22[z] = [x.replace('–',str(np.NaN)) for x in data22[z].astype(str)]
  # data22[z] = [x.replace('−',str(np.NaN)) for x in data22[z].astype(str)]
  # data22[z] = [x.replace('−',str(np.NaN)) for x in data22[z].astype(str)]
  data22[z] = pd.to_numeric(data22[z], errors='coerce')
# data22[parties] = data22[parties].astype(float)

LSD=19.36
TS=17.96
N=14.99
DS=9.24
LS=7.70
LV=7.02
LP=4.50
LL=3.89
DP=2.20
LR=1.90
TT=1.38
LT=0.75
O=100-TS-LV-DP-LSD-LP-LS-LL-LR-TT-LT-DS-N

new_row = pd.DataFrame({'Date':'13 October 2024','TS–LKD':TS, 'LVŽS':LV, 'DP':DP, 'LSDP':LSD, 'LP':LP, 'LS':LS, 'LLRA':LL, 'LRP':LR, 'TTS':TT, 'LT':LT, 'DSVL':DS,'NA':N}, index=[0])
data22 = pd.concat([new_row,data22]).reset_index(drop=True)
data22.Date=data22.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))




print(data22)
data22.to_csv('Lithuanian/poll.csv', index=False)
