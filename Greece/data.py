import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Greek_legislative_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

headers = ['Date','ΝΔ','ΣΥΡΙΖΑ','ΠΑΣΟΚ','KKE','ΣΠ','ΕΛ','Νίκη','ΠΕ','ΜέΡΑ25','ΦΛ','ΝΑ','Δημο','Κασσελάκης']
# headers = [r'Date', r'ΝΔ', r'ΣΥΡΙΖΑ', r'ΠΑΣΟΚ', r'KKE', r'ΣΠ', r'ΕΛ', r'Νίκη', r'ΠΕ', r'ΜέΡΑ25', r'ΦΛ', r'ΝΑ', r'Δημο',r'Κασσελάκης']

# parties = [r'ΝΔ', r'ΣΥΡΙΖΑ', r'ΠΑΣΟΚ', r'KKE', r'ΣΠ', r'ΕΛ', r'Νίκη', r'ΠΕ', r'ΜέΡΑ25', r'ΦΛ', r'ΝΑ', r'Δημο',r'Κασσελάκης']
parties = ['ΝΔ','ΣΥΡΙΖΑ','ΠΑΣΟΚ','KKE','ΣΠ','ΕΛ','Νίκη','ΠΕ','ΜέΡΑ25','ΦΛ','ΝΑ','Δημο','Κασσελάκης']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Polling firm/commissioner","Sample size","Lead"], axis=1)
  d[i].columns = headers
  print(type(d[i]['Date']))
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date = d[i]['Date'].astype(str)
  d[i]=d[i][~d[i].Date.str.contains("9 Jun 2024")]
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  # d[i] = d[i][d[i]['ΝΔ'] != d[i]['KKE']]
  for z in parties:
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['ΝΔ'])


D = pd.concat(d.values(), ignore_index=True)
# new_row = pd.DataFrame({'Date': '25 June 2023', 'ΝΔ':40.43 , 'ΣΥΡΙΖΑ':17.83 , 'ΠΑΣΟΚ':12.23 , 'KKE':7.49,'Σπαρτιάτες':4.71,'ΕΛ':4.49,'Νίκη':3.74,'ΠΕ':3.15,'ΜέΡΑ25':2.42}, index=[0])
# D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D=D.drop(["Δημο"], axis=1)

D.to_csv('Greece/poll.csv', index=False)
