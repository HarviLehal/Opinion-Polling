import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_next_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))


# RISHI SUNAK

print(df[26])
headers = ['Date', 'Starmer', 'Sunak', 'Unsure']
parties = ['Starmer', 'Sunak', 'Unsure']
d = {}
for i in range(3):
  d[i]=pd.DataFrame(df[i+28])
  d[i]=d[i].drop(["Pollster/client", "Area", "Sample size", "Lead"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  
D = pd.concat(d.values(), ignore_index=True)
D = D[~(D['Date'] < '2022-10-25')]

for z in parties:
  D[z] = [x.replace('–',str(np.NaN)) for x in D[z].astype(str)]
  D[z] = [x.replace('—',str(np.NaN)) for x in D[z].astype(str)]
  D[z] = D[z].str.strip('%')
D[parties] = D[parties].astype(float)

D.to_csv('UK/leadership_approval/sunak.csv', index=False)

# 
# # LIZ TRUSS
# 
# print(df[32])
# e = {}
# headers = ['Date', 'Truss', 'Starmer', 'Unsure']
# parties = ['Truss', 'Starmer', 'Unsure']
# for i in range(1):
#   e[i]=pd.DataFrame(df[33])
#   e[i]=e[i].drop(["Pollster/client", "Area", "Sample size","None of these", "Lead"], axis=1)
#   e[i].columns = headers
#   e[i]['Date2'] = e[i]['Date'].str.split('–').str[1]
#   e[i].Date2.fillna(e[i].Date, inplace=True)
#   e[i]['Date2'] = [x+ str(2022-i) for x in e[i]['Date2'].astype(str)]
#   e[i]['Date'] = e[i]['Date2']
#   e[i] = e[i].drop(['Date2'], axis=1)
#   e[i] = e[i][e[i]['Truss'] != e[i]['Starmer']]
#   e[i].Date=e[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
#     
# E = pd.concat(e.values(), ignore_index=True)
# E = E[~(E['Date'] < '2022-09-06')]
# 
# for z in parties:
#   E[z] = [x.replace('–',str(np.NaN)) for x in E[z].astype(str)]
#   E[z] = [x.replace('—',str(np.NaN)) for x in E[z].astype(str)]
#   E[z] = E[z].str.strip('%')
# E[parties] = E[parties].astype(float)
# 
# 
# # BORIS JOHNSON
# 
# print(df[34])
# f = {}
# headers = ['Date', 'Boris', 'Starmer', 'Unsure']
# parties = ['Boris', 'Starmer', 'Unsure']
# for i in range(3):
#   f[i]=pd.DataFrame(df[i+34])
#   f[i]=f[i].drop(["Pollster/client", "Area", "Sample size","None of these","Refused","Lead"], axis=1)
#   f[i].columns = headers
#   f[i]['Date2'] = f[i]['Date'].str.split('–').str[1]
#   f[i].Date2.fillna(f[i].Date, inplace=True)
#   f[i]['Date2'] = [x+ str(2022-i) for x in f[i]['Date2'].astype(str)]
#   f[i]['Date'] = f[i]['Date2']
#   f[i] = f[i].drop(['Date2'], axis=1)
#   f[i].Date=f[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
#     
# F = pd.concat(f.values(), ignore_index=True)
# 
# for z in parties:
#   F[z] = [x.replace('–',str(np.NaN)) for x in F[z].astype(str)]
#   F[z] = [x.replace('—',str(np.NaN)) for x in F[z].astype(str)]
#   F[z] = F[z].str.strip('%')
# F[parties] = F[parties].astype(float)
# 
# 
# # JEREMY CORBYN
# wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_2019_United_Kingdom_general_election"
# table_class="wikitable sortable jquery-tablesorter"
# response=requests.get(wikiurl)
# print(response.status_code)
# soup = BeautifulSoup(response.text, 'html.parser')
# tables = soup.find_all('table',class_="wikitable")
# df=pd.read_html(str(tables))
# 
# 
# print(df[32])
# g = {}
# headers = ['Date', 'Boris', 'Corbyn', 'Unsure']
# parties = ['Boris', 'Corbyn', 'Unsure']
# for i in range(1):
#   g[i]=pd.DataFrame(df[32])
#   g[i]=g[i].drop(["Polling organisation/client","Area","Sample size","None of these","Refused","Refused","Lead"], axis=1)
#   g[i].columns = headers
#   g[i]['Date2'] = g[i]['Date'].str.split('–').str[1]
#   g[i].Date2.fillna(g[i].Date, inplace=True)
#   g[i]['Date2'] = [x+ str(2019-i) for x in g[i]['Date2'].astype(str)]
#   g[i]['Date'] = g[i]['Date2']
#   g[i] = g[i].drop(['Date2'], axis=1)
#   g[i].Date=g[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
#     
# G = pd.concat(g.values(), ignore_index=True)
# 
# for z in parties:
#   G[z] = [x.replace('–',str(np.NaN)) for x in G[z].astype(str)]
#   G[z] = [x.replace('—',str(np.NaN)) for x in G[z].astype(str)]
#   G[z] = G[z].str.strip('%')
# G[parties] = G[parties].astype(float)


# E.to_csv('UK/leadership_approval/truss.csv', index=False)
# F.to_csv('UK/leadership_approval/boris.csv', index=False)
# G.to_csv('UK/leadership_approval/corbyn.csv',index=False)
