import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re
from io import StringIO


wikiurl="https://es.wikipedia.org/wiki/Elecciones_al_Parlamento_de_Catalu%C3%B1a_de_2024"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['1','Date','2','3','PSC','ERC','Junts','VOX','Comuns','CUP','Cs','PP','4','5','6','AC','7','8']
parties = ['PSC','ERC','Junts','VOX','Comuns','CUP','Cs','PP','AC']
drops = ['1','2','3','4','5','6','7','8']

headers = ['1','Date','2','3','PSC','ERC','Junts','VOX','Comuns','CUP','Cs','PP','AC','4','5']
parties = ['PSC','ERC','Junts','VOX','Comuns','CUP','Cs','PP','AC']
drops = ['1','2','3','4','5']

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[5])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i][d[i]['Date'] != '23 Jul 2023']
  d[i] = d[i][d[i]['Date'] != '28 May 2023']
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['PSC'] != d[i]['Cs']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str()) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]

D = pd.concat(d.values(), ignore_index=True)
D = D.replace(r'^\s*$', np.NaN, regex=True)
D[parties] = D[parties].astype(float)
D.drop(D.index[[-1,-3]],inplace=True)
D=D.dropna(subset=['PSC'])
D = D[D['Date'] != np.max(D['Date'])]

new_row = pd.DataFrame({'Date': '12 May 2024', 'PSC':27.95,'ERC':13.68,'Junts':21.62,'VOX':7.96,'Comuns':5.81,'CUP':4.09,'Cs':0.72,'PP':10.97,'AC':3.79}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D.to_csv('Spain/Catalunya/poll.csv', index=False)

Ind = ['ERC','Junts','CUP','AC']
Fed = ['PSC','VOX','Comuns','Cs','PP']
D['Pro-Independence (ERC + Junts + CUP + AC)'] = D[Ind].sum(axis=1)
D['Rest (PSC + VOX + Comuns + Cs + PP)'] = D[Fed].sum(axis=1)
D = D.drop(Ind + Fed, axis=1)

D.to_csv('Spain/Catalunya/poll2.csv', index=False)





d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[5])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i][d[i]['Date'] != '23 Jul 2023']
  d[i] = d[i][d[i]['Date'] != '28 May 2023']
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['PSC'] != d[i]['Cs']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[1]
    d[i][z] = [x.split('/')[1] if len(x.split('/')) > 1 else x for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–',str()) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]

D = pd.concat(d.values(), ignore_index=True)
D = D.replace(r'^\s*$', np.NaN, regex=True)
D[parties] = D[parties].astype(float)
D.drop(D.index[[-1,-3]],inplace=True)
D=D.dropna(subset=['PSC'])
D = D[D['Date'] != np.max(D['Date'])]

new_row = pd.DataFrame({'Date': '12 May 2024', 'PSC':42,'ERC':20,'Junts':35,'VOX':11,'Comuns':6,'CUP':4,'Cs':0,'PP':15,'AC':2}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

# D.to_csv('Spain/Catalunya/seats.csv', index=False)

e = {}
for i in range(1):
  e[i]=pd.DataFrame(df[5])
  e[i].columns = headers
  e[i]=e[i].drop(drops, axis=1)
  e[i] = e[i][e[i]['Date'] != '23 Jul 2023']
  e[i] = e[i][e[i]['Date'] != '28 May 2023']
  e[i]['Date2'] = e[i]['Date'].str.split('–').str[1]
  e[i].Date2.fillna(e[i].Date, inplace=True)
  e[i]['Date2'] = [x for x in e[i]['Date2'].astype(str)]
  e[i]['Date'] = e[i]['Date2']
  e[i] = e[i].drop(['Date2'], axis=1)
  e[i].Date=e[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  e[i] = e[i][e[i]['PSC'] != e[i]['Cs']]
  for z in parties:
    e[i][z] = [p.sub('', x) for x in e[i][z].astype(str)]
    e[i][z] = e[i][z].str.split(' ').str[1]
    e[i][z] = [x.split('/')[0] if len(x.split('/')) > 1 else x for x in e[i][z].astype(str)]
    e[i][z] = [x.replace('–',str()) for x in e[i][z].astype(str)]
    e[i][z] = [x.replace('?',str(np.NaN)) for x in e[i][z].astype(str)]

E = pd.concat(e.values(), ignore_index=True)
E = E.replace(r'^\s*$', np.NaN, regex=True)
E[parties] = E[parties].astype(float)
E.drop(E.index[[-1,-3]],inplace=True)
E=E.dropna(subset=['PSC'])
E = E[E['Date'] != np.max(E['Date'])]


G = pd.concat([D,E], ignore_index=True)
G = G.drop_duplicates()

G.to_csv('Spain/Catalunya/seats.csv', index=False)

Ind = ['ERC','Junts','CUP','AC']
Fed = ['PSC','VOX','Comuns','Cs','PP']
G['Pro-Independence (ERC + Junts + CUP + AC)'] = G[Ind].sum(axis=1)
G['Rest (PSC + VOX + Comuns + Cs + PP)'] = G[Fed].sum(axis=1)
G = G.drop(Ind + Fed, axis=1)

G.to_csv('Spain/Catalunya/seats2.csv', index=False)


G = pd.concat([D,E], ignore_index=True)
G = G.drop_duplicates()

T = ['PSC','ERC','Comuns']
I = ['Junts','ERC','CUP', 'AC']
II = ['Junts','ERC','CUP']
INI= ['PSC','Comuns']
GANI = ['PSC','PP']
D = ['PP','Cs','VOX']

G['Tripartito (PSC + ERC + Comuns)'] = G[T].sum(axis=1)
G['Independentista no extrema derecha (Junts + ERC + CUP)'] = G[II].sum(axis=1)
G['Independentista (Junts + ERC + CUP + AC)'] = G[I].sum(axis=1)
G['Izquierda no independentista (PSC + Comuns)'] = G[INI].sum(axis=1)
G['Gran alianza no independentista (PSC + PP)'] = G[GANI].sum(axis=1)
G['Derecha (PP + VOX + Cs)'] = G[D].sum(axis=1)
G = G.drop(T + I + II + INI + GANI + D, axis=1)
G.to_csv('Spain/Catalunya/seats3.csv', index=False)


