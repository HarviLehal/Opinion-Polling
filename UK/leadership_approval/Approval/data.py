import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_next_United_Kingdom_general_election"
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
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Pollster/client", "Sample size", "Net approval", "Question wording"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  
D = pd.concat(d.values(), ignore_index=True)

for z in parties:
  D[z] = [x.replace('–',str(np.NaN)) for x in D[z].astype(str)]
  D[z] = [x.replace('—',str(np.NaN)) for x in D[z].astype(str)]
  D[z] = D[z].str.strip('%')
D[parties] = D[parties].astype(float)

idk = ['neither1',"neither2"]
D['Neither'] = D[idk].sum(axis=1)
D = D.drop(idk, axis=1)

D.to_csv('UK/leadership_approval/Approval/sunak.csv', index=False)


# Keir Starmer

headers = ['Date', 'Approve', 'Disapprove', 'neither1',"neither2"]
parties = ['Approve', 'Disapprove', 'neither1',"neither2"]
d = {}
for i in range(5):
  d[i]=pd.DataFrame(df[i+3])
  d[i]=d[i].drop(["Pollster/client", "Sample size", "Net approval", "Question wording"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  
D = pd.concat(d.values(), ignore_index=True)
# for z in parties:
#   D[z] = [p.sub('', x) for x in D[z].astype(str)]
for z in parties:
  D[z] = [x.replace('–',str(np.NaN)) for x in D[z].astype(str)]
  D[z] = [x.replace('—',str(np.NaN)) for x in D[z].astype(str)]
  D[z] = D[z].str.strip('%')
D[parties] = D[parties].astype(float)

idk = ['neither1',"neither2"]
D['Neither'] = D[idk].sum(axis=1)
D = D.drop(idk, axis=1)

D.to_csv('UK/leadership_approval/Approval/starmer.csv', index=False)


# # LIZ TRUSS
# 
# headers = ['Date', 'Approve', 'Disapprove', 'neither1',"neither2"]
# parties = ['Approve', 'Disapprove', 'neither1',"neither2"]
# d = {}
# for i in range(1):
#   d[i]=pd.DataFrame(df[15])
#   d[i]=d[i].drop(["Pollster/client", "Sample size", "Net approval", "Question wording"], axis=1)
#   d[i].columns = headers
#   d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
#   d[i].Date2.fillna(d[i].Date, inplace=True)
#   d[i]['Date2'] = [x+ str(2022-i) for x in d[i]['Date2'].astype(str)]
#   d[i]['Date'] = d[i]['Date2']
#   d[i] = d[i].drop(['Date2'], axis=1)
#   d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
#   
# D = pd.concat(d.values(), ignore_index=True)
# # for z in parties:
# #   D[z] = [p.sub('', x) for x in D[z].astype(str)]
# for z in parties:
#   D[z] = [x.replace('–',str(np.NaN)) for x in D[z].astype(str)]
#   D[z] = [x.replace('—',str(np.NaN)) for x in D[z].astype(str)]
#   D[z] = D[z].str.strip('%')
# D[parties] = D[parties].astype(float)
# 
# idk = ['neither1',"neither2"]
# D['Neither'] = D[idk].sum(axis=1)
# D = D.drop(idk, axis=1)
# 
# D.to_csv('UK/leadership_approval/Approval/truss.csv', index=False)
# 
# 
# 
# BORIS JOHNSON
# 
# 
# headers = ['Date', 'Approve', 'Disapprove', 'neither1',"neither2"]
# parties = ['Approve', 'Disapprove', 'neither1',"neither2"]
# d = {}
# for i in range(4):
#   d[i]=pd.DataFrame(df[i+16])
#   d[i]=d[i].drop(["Pollster/client", "Sample size", "Net approval", "Question wording"], axis=1)
#   d[i].columns = headers
#   d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
#   d[i].Date2.fillna(d[i].Date, inplace=True)
#   d[i]['Date2'] = [x+ str(2022-i) for x in d[i]['Date2'].astype(str)]
#   d[i]['Date'] = d[i]['Date2']
#   d[i] = d[i].drop(['Date2'], axis=1)
#   d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
# 
# 
# 
# wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_2019_United_Kingdom_general_election"
# table_class="wikitable sortable jquery-tablesorter"
# response=requests.get(wikiurl)
# print(response.status_code)
# soup = BeautifulSoup(response.text, 'html.parser')
# tables = soup.find_all('table',class_="wikitable")
# df=pd.read_html(str(tables))
# p = re.compile(r'\[[a-z]+\]')
# 
# for j in range(1):
#   i = j+5
#   d[i]=pd.DataFrame(df[0])
#   d[i]=d[i].drop(["Polling organisation/client", "Sample size", "Net approval", "Question wording"], axis=1)
#   d[i].columns = headers
#   d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
#   d[i].Date2.fillna(d[i].Date, inplace=True)
#   d[i]['Date2'] = [x+ str(2019) for x in d[i]['Date2'].astype(str)]
#   d[i]['Date'] = d[i]['Date2']
#   d[i] = d[i].drop(['Date2'], axis=1)
#   d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
# 
# 
# D = pd.concat(d.values(), ignore_index=True)
# for z in parties:
#   D[z] = [x.replace('–',str(np.NaN)) for x in D[z].astype(str)]
#   D[z] = [x.replace('—',str(np.NaN)) for x in D[z].astype(str)]
#   D[z] = D[z].str.strip('%')
#   D[z] = D[z].str.strip('<')
# D[parties] = D[parties].astype(float)
# 
# idk = ['neither1',"neither2"]
# D['Neither'] = D[idk].sum(axis=1)
# D = D.drop(idk, axis=1)
# 
# D.to_csv('UK/leadership_approval/Approval/boris.csv', index=False)
# 
# 
# # JEREMY CORBYN
# 
# wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_next_United_Kingdom_general_election"
# table_class="wikitable sortable jquery-tablesorter"
# response=requests.get(wikiurl)
# print(response.status_code)
# soup = BeautifulSoup(response.text, 'html.parser')
# tables = soup.find_all('table',class_="wikitable")
# df=pd.read_html(str(tables))
# p = re.compile(r'\[[a-z]+\]')
# 
# headers = ['Date', 'Approve', 'Disapprove', 'neither1',"neither2"]
# parties = ['Approve', 'Disapprove', 'neither1',"neither2"]
# d = {}
# for i in range(2):
#   d[i]=pd.DataFrame(df[i+25])
#   d[i]=d[i].drop(["Pollster/client", "Sample size", "Net approval", "Question wording"], axis=1)
#   d[i].columns = headers
#   d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
#   d[i].Date2.fillna(d[i].Date, inplace=True)
#   d[i]['Date2'] = [x+ str(2020-i) for x in d[i]['Date2'].astype(str)]
#   d[i]['Date'] = d[i]['Date2']
#   d[i] = d[i].drop(['Date2'], axis=1)
#   d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
# 
# 
# wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_2019_United_Kingdom_general_election"
# table_class="wikitable sortable jquery-tablesorter"
# response=requests.get(wikiurl)
# print(response.status_code)
# soup = BeautifulSoup(response.text, 'html.parser')
# tables = soup.find_all('table',class_="wikitable")
# df=pd.read_html(str(tables))
# p = re.compile(r'\[[a-z]+\]')
# 
# for j in range(3):
#   i = j+2
#   d[i]=pd.DataFrame(df[j+1])
#   d[i]=d[i].drop(["Polling organisation/client", "Sample size", "Net approval", "Question wording"], axis=1)
#   d[i].columns = headers
#   d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
#   d[i].Date2.fillna(d[i].Date, inplace=True)
#   d[i]['Date2'] = [x+ str(2019-j) for x in d[i]['Date2'].astype(str)]
#   d[i]['Date'] = d[i]['Date2']
#   d[i] = d[i].drop(['Date2'], axis=1)
#   d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
# 
# 
# D = pd.concat(d.values(), ignore_index=True)
# for z in parties:
#   D[z] = [x.replace('–',str(np.NaN)) for x in D[z].astype(str)]
#   D[z] = [x.replace('—',str(np.NaN)) for x in D[z].astype(str)]
#   D[z] = D[z].str.strip('%')
#   D[z] = D[z].str.strip('<')
# D[parties] = D[parties].astype(float)
# 
# idk = ['neither1',"neither2"]
# D['Neither'] = D[idk].sum(axis=1)
# D = D.drop(idk, axis=1)
# 
# D.to_csv('UK/leadership_approval/Approval/corbyn.csv', index=False)
