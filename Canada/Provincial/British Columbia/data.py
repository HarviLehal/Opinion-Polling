import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/43rd_British_Columbia_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

headers = ['Date','NDP','BCU','Green','Con']
headers = ['1','2','Date','3','NDP','BCU','Green','Con','4','5','6','7','8']
parties = ['NDP','BCU','Green','Con']
drops = ['1','2','3','4','5','6','7','8']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  # d[i]=d[i].drop(["Polling firm","Client","Source","Others","Margin of error","Sample size","Polling method","Lead"], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  for j in range(len(d[i])):
    if d[i].Date2[j][0].isdigit():
      d[i]['Date2'][j] = d[i]['Date'][j][:3] + d[i]['Date2'][j]
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['NDP'] != d[i]['Green']]
  

# d[0]['Date'].replace({pd.NaT: "0 days"}, inplace=True)



D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = [x.replace('–',str(np.nan)) for x in D[z]]
  D[z] = [x.replace('—',str(np.nan)) for x in D[z]]
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
  
D = D.dropna(subset=['Date'])

D.to_csv('Canada/Provincial/British Columbia/poll.csv', index=False)

split_date = '21 September 2024'
split_date=dateparser.parse(split_date)
z=D.tail(1)
D=D[(pd.to_datetime(D["Date"]) > split_date)]
D = pd.concat([D,z], ignore_index=True)
# D=D.drop(['BCU'], axis=1)

D.to_csv('Canada/Provincial/British Columbia/poll2.csv', index=False)
