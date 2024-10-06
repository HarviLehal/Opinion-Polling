import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_2019_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


# RISHI SUNAK

headers = ['Date', 'Approve', 'Disapprove', 'neither1',"neither2"]
parties = ['Approve', 'Disapprove', 'neither1',"neither2"]
d = {}
for i in range(3):
  d[i]=pd.DataFrame(df[i+9])
  d[i]=d[i].drop(["Polling organisation/client", "Sample size", "Net approval", "Question wording"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2019-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  
D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = pd.to_numeric(D[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_2017_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


headers = ['Date', 'Approve', 'Disapprove', 'neither1',"neither2"]
parties = ['Approve', 'Disapprove', 'neither1',"neither2"]
d1 = {}
for i in range(2):
  d1[i]=pd.DataFrame(df[i])
  d1[i]=d1[i].drop(["Polling organisation/client", "Net approval", "Question wording"], axis=1)
  d1[i].columns = headers
  d1[i]['Date2'] = d1[i]['Date'].str.split('–').str[1]
  d1[i].Date2.fillna(d1[i]['Date'].str.split('-').str[1], inplace=True)
  d1[i].Date2.fillna(d1[i].Date, inplace=True)
  d1[i]['Date2'] = [x+ str(2017-i) for x in d1[i]['Date2'].astype(str)]
  d1[i]['Date'] = d1[i]['Date2']
  d1[i] = d1[i].drop(['Date2'], axis=1)
  d1[i].Date=d1[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D1 = pd.concat(d1.values(), ignore_index=True)
for z in parties:
  D1[z] = D1[z].astype(str)
  D1[z] = D1[z].str.strip('%')
  D1[z] = pd.to_numeric(D1[z], errors='coerce')
  


D2 = pd.concat([D,D1], ignore_index=True)
D2 = D2.dropna(subset=['Approve'])



D2=D2.drop(['neither1',"neither2"], axis=1)
parties = ['Approve', 'Disapprove']

D2['total']=D2[parties].sum(axis=1)
D2[parties] = D2[parties].div(D2['total'], axis=0)*100
D2=D2.drop(['total'], axis=1)
D2['Net Approval']=D2['Approve']-D2['Disapprove']
D2 = D2.drop(["Approve","Disapprove"], axis=1)

D2.to_csv('UK/leadership_approval/Approval/may.csv', index=False)




headers = ['Date', 'Approve', 'Disapprove', 'neither1',"neither2"]
parties = ['Approve', 'Disapprove', 'neither1',"neither2"]
d1 = {}
for i in range(2):
  d1[i]=pd.DataFrame(df[i+10])
  d1[i]=d1[i].drop(["Polling organisation/client", "Net approval", "Question wording"], axis=1)
  d1[i].columns = headers
  d1[i]['Date2'] = d1[i]['Date'].str.split('–').str[1]
  d1[i].Date2.fillna(d1[i]['Date'].str.split('-').str[1], inplace=True)
  d1[i].Date2.fillna(d1[i].Date, inplace=True)
  d1[i]['Date2'] = [x+ str(2016-i) for x in d1[i]['Date2'].astype(str)]
  d1[i]['Date'] = d1[i]['Date2']
  d1[i] = d1[i].drop(['Date2'], axis=1)
  d1[i].Date=d1[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D1 = pd.concat(d1.values(), ignore_index=True)
for z in parties:
  D1[z] = D1[z].astype(str)
  D1[z] = D1[z].str.strip('%')
  D1[z] = pd.to_numeric(D1[z], errors='coerce')
D1 = D1.dropna(subset=['Approve'])


wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_2015_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


headers = ['Date', 'Approve', 'Disapprove', 'neither1',"neither2"]
parties = ['Approve', 'Disapprove', 'neither1',"neither2"]
d2 = {}
for i in range(6):
  d2[i]=pd.DataFrame(df[i])
  d2[i]=d2[i].drop(["Polling organisation/client", "Net approval", "Question wording"], axis=1)
  d2[i].columns = headers
  d2[i]['Date2'] = d2[i]['Date'].str.split('–').str[1]
  d2[i].Date2.fillna(d2[i]['Date'].str.split('-').str[1], inplace=True)
  d2[i].Date2.fillna(d2[i].Date, inplace=True)
  d2[i]['Date2'] = [x+ str(2015-i) for x in d2[i]['Date2'].astype(str)]
  d2[i]['Date'] = d2[i]['Date2']
  d2[i] = d2[i].drop(['Date2'], axis=1)
  d2[i].Date=d2[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D2 = pd.concat(d2.values(), ignore_index=True)
for z in parties:
  D2[z] = D2[z].astype(str)
  D2[z] = D2[z].str.strip('%')
  D2[z] = pd.to_numeric(D2[z], errors='coerce')
  
  

D3 = pd.concat([D1,D2], ignore_index=True)
D3 = D3.dropna(subset=['Approve'])

D3=D3.drop(['neither1',"neither2"], axis=1)
parties = ['Approve', 'Disapprove']

D3['total']=D3[parties].sum(axis=1)
D3[parties] = D3[parties].div(D3['total'], axis=0)*100
D3=D3.drop(['total'], axis=1)
D3['Net Approval']=D3['Approve']-D3['Disapprove']
D3 = D3.drop(["Approve","Disapprove"], axis=1)


D3.to_csv('UK/leadership_approval/Approval/cameron.csv', index=False)
