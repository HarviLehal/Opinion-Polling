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

headers = ['1','Date','2','3','PSC','ERC','Junts','VOX','ECP','CUP','Cs','PP','4','5','6','AC','7','8']
parties = ['PSC','ERC','Junts','VOX','ECP','CUP','Cs','PP','AC']
drops = ['1','2','3','4','5','6','7','8']

headers = ['1','Date','2','3','PSC','ERC','Junts','VOX','ECP','CUP','Cs','PP','AC','4','5']
parties = ['PSC','ERC','Junts','VOX','ECP','CUP','Cs','PP','AC']
drops = ['1','2','3','4','5']

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[4])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i][d[i]['Date'] != '23 Jul 2023']
  d[i] = d[i][d[i]['Date'] != '28 de mayo de 2023']
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
D.to_csv('Spain/Catalunya/poll.csv', index=False)

Ind = ['ERC','Junts','CUP','AC']
Fed = ['PSC','VOX','ECP','Cs','PP']
D['Pro-Independence (ERC + Junts + CUP + AC)'] = D[Ind].sum(axis=1)
D['Rest (PSC + VOX + ECP + Cs + PP)'] = D[Fed].sum(axis=1)
D = D.drop(Ind + Fed, axis=1)

D.to_csv('Spain/Catalunya/poll2.csv', index=False)





d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[4])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i][d[i]['Date'] != '23 Jul 2023']
  d[i] = d[i][d[i]['Date'] != '28 de mayo de 2023']
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
D.to_csv('Spain/Catalunya/seats.csv', index=False)

Ind = ['ERC','Junts','CUP','AC']
Fed = ['PSC','VOX','ECP','Cs','PP']
D['Pro-Independence (ERC + Junts + CUP + AC)'] = D[Ind].sum(axis=1)
D['Rest (PSC + VOX + ECP + Cs + PP)'] = D[Fed].sum(axis=1)
D = D.drop(Ind + Fed, axis=1)

D.to_csv('Spain/Catalunya/seats2.csv', index=False)


# best case for Independence
D = pd.concat(d.values(), ignore_index=True)
D = D.replace(r'^\s*$', np.NaN, regex=True)
D[parties] = D[parties].astype(float)
D.drop(D.index[[-1,-3]],inplace=True)
D=D.dropna(subset=['PSC'])

Ind = ['ERC','Junts','CUP','AC']
Fed = ['PSC','VOX','ECP','Cs','PP']
D['Pro-Independence (ERC + Junts + CUP + AC)'] = D[Ind].sum(axis=1)
D['Rest (PSC + VOX + ECP + Cs + PP)'] = 134 - D['Pro-Independence (ERC + Junts + CUP + AC)']
D = D.drop(Ind + Fed, axis=1)

D.to_csv('Spain/Catalunya/seats_ind_best.csv', index=False)


D = pd.concat(d.values(), ignore_index=True)
D = D.replace(r'^\s*$', np.NaN, regex=True)
D[parties] = D[parties].astype(float)
D.drop(D.index[[-1,-3]],inplace=True)
D=D.dropna(subset=['PSC'])
Ind = ['ERC','Junts','CUP','AC']
Fed = ['PSC','VOX','ECP','Cs','PP']
D['Rest (PSC + VOX + ECP + Cs + PP)'] = D[Fed].sum(axis=1)
D['Pro-Independence (ERC + Junts + CUP + AC)'] = 134 - D['Rest (PSC + VOX + ECP + Cs + PP)']
D = D.drop(Ind + Fed, axis=1)

D.to_csv('Spain/Catalunya/seats_rest_best.csv', index=False)

# worst case for Independence



d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[4])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i][d[i]['Date'] != '23 Jul 2023']
  d[i] = d[i][d[i]['Date'] != '28 de mayo de 2023']
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
    d[i][z] = [x.split('/')[0] if len(x.split('/')) > 1 else x for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–',str()) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]

D = pd.concat(d.values(), ignore_index=True)
D = D.replace(r'^\s*$', np.NaN, regex=True)
D[parties] = D[parties].astype(float)
D.drop(D.index[[-1,-3]],inplace=True)
D=D.dropna(subset=['PSC'])
Ind = ['ERC','Junts','CUP','AC']
Fed = ['PSC','VOX','ECP','Cs','PP']
D['Pro-Independence (ERC + Junts + CUP + AC)'] = D[Ind].sum(axis=1)
D['Rest (PSC + VOX + ECP + Cs + PP)'] = 134 - D['Pro-Independence (ERC + Junts + CUP + AC)']
D = D.drop(Ind + Fed, axis=1)

D.to_csv('Spain/Catalunya/seats_ind_worst.csv', index=False)




D = pd.concat(d.values(), ignore_index=True)
D = D.replace(r'^\s*$', np.NaN, regex=True)
D[parties] = D[parties].astype(float)
D.drop(D.index[[-1,-3]],inplace=True)
D=D.dropna(subset=['PSC'])
Ind = ['ERC','Junts','CUP','AC']
Fed = ['PSC','VOX','ECP','Cs','PP']
D['Rest (PSC + VOX + ECP + Cs + PP)'] = D[Fed].sum(axis=1)
D['Pro-Independence (ERC + Junts + CUP + AC)'] = 134 - D['Rest (PSC + VOX + ECP + Cs + PP)']
D = D.drop(Ind + Fed, axis=1)

D.to_csv('Spain/Catalunya/seats_rest_worst.csv', index=False)

























d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[4])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i][d[i]['Date'] != '23 Jul 2023']
  d[i] = d[i][d[i]['Date'] != '28 de mayo de 2023']
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
    d[i][z] = [x.split('/')[0] if len(x.split('/')) > 1 else x for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–',str()) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]

D = pd.concat(d.values(), ignore_index=True)
D = D.replace(r'^\s*$', np.NaN, regex=True)
D[parties] = D[parties].astype(float)
D.drop(D.index[[-1,-3]],inplace=True)
D=D.dropna(subset=['PSC'])
Ind = ['ERC','Junts','CUP','AC']
Fed = ['PSC','VOX','ECP','Cs','PP']
D['Pro-Independence (ERC + Junts + CUP + AC)'] = D[Ind].sum(axis=1)
D['Rest (PSC + VOX + ECP + Cs + PP)'] = D[Fed].sum(axis=1)
D = D.drop(Ind + Fed, axis=1)


d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[4])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i][d[i]['Date'] != '23 Jul 2023']
  d[i] = d[i][d[i]['Date'] != '28 de mayo de 2023']
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

E = pd.concat(d.values(), ignore_index=True)
E = E.replace(r'^\s*$', np.NaN, regex=True)
E[parties] = E[parties].astype(float)
E.drop(E.index[[-1,-3]],inplace=True)
E=E.dropna(subset=['PSC'])
Ind = ['ERC','Junts','CUP','AC']
Fed = ['PSC','VOX','ECP','Cs','PP']
E['Pro-Independence (ERC + Junts + CUP + AC)'] = E[Ind].sum(axis=1)
E['Rest (PSC + VOX + ECP + Cs + PP)'] = E[Fed].sum(axis=1)
E = E.drop(Ind + Fed, axis=1)




# D is lower, E is upper so we create F as the average between D and E of each column but the date stays the same

parties = ['Pro-Independence (ERC + Junts + CUP + AC)','Rest (PSC + VOX + ECP + Cs + PP)']

F = D.copy()
F[parties] = (D[parties] + E[parties]) / 2

# check if the sum of the two columns is 135 for each row
print(F[parties].sum(axis=1))
# convert to percentages and then back to seats
totals = F[parties].sum(axis=1)
# convert to percentages and then back to seats
for party in parties:
  F[party] = F[party] / totals * 135
# check if the sum of the two columns is 135 for each row
print(F[parties].sum(axis=1))


F.to_csv('Spain/Catalunya/seats_avg.csv', index=False)








