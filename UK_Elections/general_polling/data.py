import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser


# NEXT GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))


headers = ['Date', 'Con', 'Lab', 'Lib Dem', 'SNP', 'Green', 'Reform']
parties = ['Con', 'Lab', 'Lib Dem', 'SNP', 'Green', 'Reform']
d = {}
for i in range(4):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Pollster", "Client", "Area", "Others", "Lead", "Sample size"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  d[i] = d[i][d[i]['Con'] != d[i]['Green']]
  for z in parties:
    d[i][z] = [x.replace('TBC','') for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–','') for x in d[i][z].astype(str)]


D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[-1]],inplace=True)
D.loc[len(D.index)-1,['Date']] = dateparser.parse('12 Dec 2019')


# 2019 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2019_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
ef=pd.read_html(str(tables))


headers = ['Date', 'Con', 'Lab', 'Lib Dem', 'SNP', 'Green', 'Reform', 'UKIP', 'Change UK']
parties = ['Con', 'Lab', 'Lib Dem', 'SNP', 'Green', 'Reform', 'UKIP', 'Change UK']
e = {}
e[0]=pd.DataFrame(ef[0])
e[0]=e[0].drop(["Pollster/client(s)", "Area", "Other", "Plaid Cymru", "Lead", "Sample size"], axis=1)
e[0].columns = headers
e[0]['Date2'] = e[0]['Date'].str.split('–').str[1]
e[0].Date2.fillna(e[0].Date, inplace=True)
e[0]['Date2'] = [x+ str(2019) for x in e[0]['Date2'].astype(str)]
e[0]['Date'] = e[0]['Date2']
e[0] = e[0].drop(['Date2'], axis=1)
e[0].Date=e[0].Date.astype(str).apply(lambda x: dateparser.parse(x))
e[0] = e[0][e[0]['Con'] != e[0]['Green']]
for z in parties:
  e[0][z] = [x.replace('TBC','') for x in e[0][z].astype(str)]
  e[0][z] = [x.replace('%','') for x in e[0][z].astype(str)]
  e[0][z] = [x.replace('–','') for x in e[0][z].astype(str)]
  
headers = ['Date', 'Con', 'Lab', 'Lib Dem', 'SNP', 'UKIP', 'Green']
parties = ['Con', 'Lab', 'Lib Dem', 'SNP', 'UKIP', 'Green']

for i in range(2):
  e[i+1]=pd.DataFrame(ef[i+1])
  e[i+1]=e[i+1].drop(["Pollster/client(s)","Area", "Other", "Plaid Cymru", "Lead", "Sample size"], axis=1)
  e[i+1].columns = headers
  e[i+1]['Date2'] = e[i+1]['Date'].str.split('–').str[1]
  e[i+1].Date2.fillna(e[i+1].Date, inplace=True)
  e[i+1]['Date2'] = [x+ str(2018-i) for x in e[i+1]['Date2'].astype(str)]
  e[i+1]['Date'] = e[i+1]['Date2']
  e[i+1] = e[i+1].drop(['Date2'], axis=1)
  e[i+1].Date=e[i+1].Date.astype(str).apply(lambda x: dateparser.parse(x))
  e[i+1] = e[i+1][e[i+1]['Con'] != e[i+1]['Green']]
  for z in parties:
    e[i+1][z] = [x.replace('TBC','') for x in e[i+1][z].astype(str)]
    e[i+1][z] = [x.replace('%','') for x in e[i+1][z].astype(str)]
    e[i+1][z] = [x.replace('–','') for x in e[i+1][z].astype(str)]

E = pd.concat(e.values(), ignore_index=True)
E.drop(E.index[[0,1,-1]],inplace=True)


# 2017 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2017_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
ff=pd.read_html(str(tables))

headers = ['Date', 'Con', 'Lab', 'UKIP', 'Lib Dem', 'SNP', 'Green']
parties = ['Con', 'Lab', 'UKIP', 'Lib Dem', 'SNP', 'Green']
f = {}
for i in range(3):
  f[i]=pd.DataFrame(ff[i])
  f[i]=f[i].drop(["Polling organisation/client", "Others", "Lead", "Sample size"], axis=1)
  f[i].columns = headers
  f[i]['Date2'] = f[i]['Date'].str.split('–').str[1]
  f[i].Date2.fillna(f[i].Date, inplace=True)
  f[i]['Date2'] = [x+ str(2017-i) for x in f[i]['Date2'].astype(str)]
  f[i]['Date'] = f[i]['Date2']
  f[i] = f[i].drop(['Date2'], axis=1)
  f[i].Date=f[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  f[i] = f[i][f[i]['Con'] != f[i]['Green']]
  for z in parties:
    f[i][z] = [x.replace('TBC','') for x in f[i][z].astype(str)]
    f[i][z] = [x.replace('%','') for x in f[i][z].astype(str)]
    f[i][z] = [x.replace('[a]','') for x in f[i][z].astype(str)]
    f[i][z] = [x.replace('[b]','') for x in f[i][z].astype(str)]
    f[i][z] = [x.replace('–','') for x in f[i][z].astype(str)]

F = pd.concat(f.values(), ignore_index=True)
F.drop(F.index[[0]],inplace=True)


# 2015 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2015_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
gf=pd.read_html(str(tables))

headers = ['Date', 'Con', 'Lab', 'Lib Dem', 'UKIP', 'Green']
parties = ['Con', 'Lab', 'Lib Dem', 'UKIP', 'Green']
g = {}
for i in range(3):
  g[i]=pd.DataFrame(gf[i])
  g[i]=g[i].drop(["Polling organisation/client", "Others", "Lead", "Sample size"], axis=1)
  g[i].columns = headers
  g[i]['Date2'] = g[i]['Date'].str.split('–').str[1]
  g[i].Date2.fillna(g[i].Date, inplace=True)
  g[i]['Date2'] = [x+ str(2015-i) for x in g[i]['Date2'].astype(str)]
  g[i]['Date'] = g[i]['Date2']
  g[i] = g[i].drop(['Date2'], axis=1)
  g[i].Date=g[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  g[i] = g[i][g[i]['Con'] != g[i]['Green']]
  for z in parties:
    g[i][z] = [x.replace('%','') for x in g[i][z].astype(str)]
    g[i][z] = [x.replace('–','') for x in g[i][z].astype(str)]
    
wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2015_United_Kingdom_general_election_(2010–2012)"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
gf2=pd.read_html(str(tables))

headers = ['Date', 'Con', 'Lab', 'Lib Dem', 'UKIP']
parties = ['Con', 'Lab', 'Lib Dem', 'UKIP']


g[4]=pd.DataFrame(gf2[0])
g[4]=g[4].drop(["Polling organisation/client", "Others", "Lead", "Sample size", "Green"], axis=1)
g[4].columns = headers
g[4]['Date2'] = g[4]['Date'].str.split('–').str[1]
g[4].Date2.fillna(g[4].Date, inplace=True)
g[4]['Date2'] = [x+ str(2012) for x in g[4]['Date2'].astype(str)]
g[4]['Date'] = g[4]['Date2']
g[4] = g[4].drop(['Date2'], axis=1)
g[4].Date=g[4].Date.astype(str).apply(lambda x: dateparser.parse(x))
g[4] = g[4][g[4]['Con'] != g[4]['Lib Dem']]
for z in parties:
  g[4][z] = [x.replace('%','') for x in g[4][z].astype(str)]
  g[4][z] = [x.replace('–','') for x in g[4][z].astype(str)]
  

headers = ['Date', 'Con', 'Lab', 'Lib Dem']
parties = ['Con', 'Lab', 'Lib Dem']


for i in range(2):
  g[i+5]=pd.DataFrame(gf2[i+1])
  g[i+5]=g[i+5].drop(["Polling organisation/client", "Others", "Lead", "Sample size", "Green", "UKIP"], axis=1)
  g[i+5].columns = headers
  g[i+5]['Date2'] = g[i+5]['Date'].str.split('–').str[1]
  g[i+5].Date2.fillna(g[i+5].Date, inplace=True)
  g[i+5]['Date2'] = [x+ str(2011-i) for x in g[i+5]['Date2'].astype(str)]
  g[i+5]['Date'] = g[i+5]['Date2']
  g[i+5] = g[i+5].drop(['Date2'], axis=1)
  g[i+5].Date=g[i+5].Date.astype(str).apply(lambda x: dateparser.parse(x))
  g[i+5] = g[i+5][g[i+5]['Con'] != g[i+5]['Lib Dem']]
  for z in parties:
    g[i+5][z] = [x.replace('%','') for x in g[i+5][z].astype(str)]
    g[i+5][z] = [x.replace('–','') for x in g[i+5][z].astype(str)]
    
G = pd.concat(g.values(), ignore_index=True)
G.drop(G.index[[0,1]],inplace=True)


# 2010 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2010_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
hf=pd.read_html(str(tables))

headers = ['Date', 'Lab', 'Con', 'Lib Dem']
parties = ['Lab', 'Con', 'Lib Dem']

h = {}
for i in range(4):
  h[i]=pd.DataFrame(hf[i])
  h[i]=h[i].drop(["Client", "Pollster", "Others", "Lead", "Sample size"], axis=1)
  h[i].columns = headers
  h[i]['Date2'] = h[i]['Date'].str.split('–').str[1]
  h[i].Date2.fillna(h[i].Date, inplace=True)
  h[i]['Date2'] = [x+ str(2010-i) for x in h[i]['Date2'].astype(str)]
  h[i]['Date'] = h[i]['Date2']
  h[i] = h[i].drop(['Date2'], axis=1)
  h[i].Date=h[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  h[i] = h[i][h[i]['Lab'] != h[i]['Lib Dem']]
  for z in parties:
    h[i][z] = [x.replace('%',' ') for x in h[i][z].astype(str)]

for i in range(2):
  h[i+4]=pd.DataFrame(hf[i+4])
  h[i+4]=h[i+4].drop(["Polling Organisation / Client", "Others", "Lead", "Sample size"], axis=1)
  h[i+4].columns = headers
  h[i+4]['Date2'] = h[i+4]['Date'].str.split('–').str[1]
  h[i+4].Date2.fillna(h[i+4].Date, inplace=True)
  h[i+4]['Date2'] = [x+ str(2006-i) for x in h[i+4]['Date2'].astype(str)]
  h[i+4]['Date'] = h[i+4]['Date2']
  h[i+4] = h[i+4].drop(['Date2'], axis=1)
  h[i+4].Date=h[i+4].Date.astype(str).apply(lambda x: dateparser.parse(x))
  h[i+4] = h[i+4][h[i+4]['Lab'] != h[i+4]['Lib Dem']]
  for z in parties:
    h[i+4][z] = [x.replace('%',' ') for x in h[i+4][z].astype(str)]

H = pd.concat(h.values(), ignore_index=True)
H.drop(H.index[[0]],inplace=True)


# 2005 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2005_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
jf=pd.read_html(str(tables))


j = {}
for i in range(5):
  j[i]=pd.DataFrame(jf[i])
  j[i]=j[i].drop(["Client", "Pollster", "Others", "Lead", "Sample size"], axis=1)
  j[i].columns = headers
  j[i]['Date2'] = j[i]['Date'].str.split('–').str[1]
  j[i].Date2.fillna(j[i].Date, inplace=True)
  j[i]['Date2'] = [x+ str(2005-i) for x in j[i]['Date2'].astype(str)]
  j[i]['Date'] = j[i]['Date2']
  j[i] = j[i].drop(['Date2'], axis=1)
  j[i].Date=j[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  j[i] = j[i][j[i]['Lab'] != j[i]['Lib Dem']]
  for z in parties:
    j[i][z] = [x.replace('%',' ') for x in j[i][z].astype(str)]
    
J = pd.concat(j.values(), ignore_index=True)
J.drop(J.index[[0]],inplace=True)


# 2001 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2001_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
kf=pd.read_html(str(tables))


k = {}
for i in range(5):
  k[i]=pd.DataFrame(kf[i+1])
  k[i]=k[i].drop(["Client", "Pollster", "Others", "Lead", "Sample size"], axis=1)
  k[i].columns = headers
  k[i]['Date2'] = k[i]['Date'].str.split('–').str[1]
  k[i].Date2.fillna(k[i].Date, inplace=True)
  k[i]['Date2'] = [x+ str(2001-i) for x in k[i]['Date2'].astype(str)]
  k[i]['Date'] = k[i]['Date2']
  k[i] = k[i].drop(['Date2'], axis=1)
  k[i].Date=k[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  k[i] = k[i][k[i]['Lab'] != k[i]['Lib Dem']]
  for z in parties:
    k[i][z] = [x.replace('%',' ') for x in k[i][z].astype(str)]
    
K = pd.concat(k.values(), ignore_index=True)
K.drop(K.index[[0]],inplace=True)


# 2001 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1997_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
lf=pd.read_html(str(tables))

headers = ['Date', 'Con', 'Lab', 'Lib Dem']
parties = ['Con', 'Lab', 'Lib Dem']

l = {}
for i in range(6):
  l[i]=pd.DataFrame(lf[i])
  l[i]=l[i].drop(["Pollster/Client", "Lead"], axis=1)
  l[i].columns = headers
  l[i]['Date2'] = l[i]['Date'].str.split('–').str[1]
  l[i].Date2.fillna(l[i].Date, inplace=True)
  l[i]['Date2'] = [x+ str(1997-i) for x in l[i]['Date2'].astype(str)]
  l[i]['Date'] = l[i]['Date2']
  l[i] = l[i].drop(['Date2'], axis=1)
  l[i].Date=l[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  l[i] = l[i][l[i]['Lab'] != l[i]['Lib Dem']]
  for z in parties:
    l[i][z] = [x.replace('%',' ') for x in l[i][z].astype(str)]

L = pd.concat(l.values(), ignore_index=True)
L.drop(L.index[[0]],inplace=True)




data = pd.concat([D,E,F,G,H,J,K,L])
data.to_csv('UK_Elections/general_polling/poll.csv', index=False)
