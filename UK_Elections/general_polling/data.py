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


# 1997 GENERAL ELECTION

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
    l[i][z] = [x.replace('%','') for x in l[i][z].astype(str)]

L = pd.concat(l.values(), ignore_index=True)
L.drop(L.index[[0]],inplace=True)


# 1992 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1992_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
mf=pd.read_html(str(tables))

headers = ['Date', 'Con', 'Lab', 'Lib Dem']
parties = ['Con', 'Lab', 'Lib Dem']

m = {}
for i in range(2):
  m[i]=pd.DataFrame(mf[i])
  m[i]=m[i].drop(["Pollster","Client", "Lead"], axis=1)
  m[i].columns = headers
  m[i]['Date2'] = m[i]['Date'].str.split('–').str[1]
  m[i].Date2.fillna(m[i].Date, inplace=True)
  m[i]['Date2'] = [x+ str(1992-i) for x in m[i]['Date2'].astype(str)]
  m[i]['Date'] = m[i]['Date2']
  m[i] = m[i].drop(['Date2'], axis=1)
  m[i].Date=m[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  m[i] = m[i][m[i]['Lab'] != m[i]['Lib Dem']]
  for z in parties:
    m[i][z] = [x.replace('%','') for x in m[i][z].astype(str)]

for i in range(3):
  m[i+2]=pd.DataFrame(mf[i+2])
  m[i+2]=m[i+2].drop(["Pollster","Client", "Lead","SDP"], axis=1)
  m[i+2].columns = headers
  m[i+2]['Date2'] = m[i+2]['Date'].str.split('–').str[1]
  m[i+2].Date2.fillna(m[i+2].Date, inplace=True)
  m[i+2]['Date2'] = [x+ str(1990-i) for x in m[i+2]['Date2'].astype(str)]
  m[i+2]['Date'] = m[i+2]['Date2']
  m[i+2] = m[i+2].drop(['Date2'], axis=1)
  m[i+2].Date=m[i+2].Date.astype(str).apply(lambda x: dateparser.parse(x))
  m[i+2] = m[i+2][m[i+2]['Lab'] != m[i+2]['Lib Dem']]
  for z in parties:
    m[i+2][z] = [x.replace('%','') for x in m[i+2][z].astype(str)]

m[5]=pd.DataFrame(mf[5])
m[5]=m[5].drop(["Pollster","Client", "Lead"], axis=1)
m[5].columns = headers
m[5]['Date2'] = m[5]['Date'].str.split('–').str[1]
m[5].Date2.fillna(m[5].Date, inplace=True)
m[5]['Date2'] = [x+ str(1987) for x in m[5]['Date2'].astype(str)]
m[5]['Date'] = m[5]['Date2']
m[5] = m[5].drop(['Date2'], axis=1)
m[5].Date=m[5].Date.astype(str).apply(lambda x: dateparser.parse(x))
m[5] = m[5][m[5]['Lab'] != m[5]['Lib Dem']]
for z in parties:
  m[5][z] = [x.replace('%','') for x in m[5][z].astype(str)]

M = pd.concat(m.values(), ignore_index=True)
M.drop(M.index[[0]],inplace=True)


# 1987 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1987_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
nf=pd.read_html(str(tables))

headers = ['Date', 'Con', 'Lab', 'Lib Dem']
parties = ['Con', 'Lab', 'Lib Dem']

n = {}
for i in range(5):
  n[i]=pd.DataFrame(nf[i])
  n[i]=n[i].drop(["Pollster","Client", "Lead"], axis=1)
  n[i].columns = headers
  n[i]['Date2'] = n[i]['Date'].str.split('–').str[1]
  n[i].Date2.fillna(n[i].Date, inplace=True)
  n[i]['Date2'] = [x+ str(1987-i) for x in n[i]['Date2'].astype(str)]
  n[i]['Date'] = n[i]['Date2']
  n[i] = n[i].drop(['Date2'], axis=1)
  n[i].Date=n[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  n[i] = n[i][n[i]['Lab'] != n[i]['Lib Dem']]
  for z in parties:
    n[i][z] = [x.replace('%','') for x in n[i][z].astype(str)]

N = pd.concat(n.values(), ignore_index=True)
N.drop(N.index[[0]],inplace=True)


# 1983 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1983_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
of=pd.read_html(str(tables))

headers = ['Date', 'Con', 'Lab', 'Lib Dem']
parties = ['Con', 'Lab', 'Lib Dem']

o = {}
for i in range(5):
  o[i]=pd.DataFrame(of[i])
  o[i]=o[i].drop(["Pollster","Client", "Lead"], axis=1)
  o[i].columns = headers
  o[i]['Date2'] = o[i]['Date'].str.split('–').str[1]
  o[i].Date2.fillna(o[i].Date, inplace=True)
  o[i]['Date2'] = [x+ str(1983-i) for x in o[i]['Date2'].astype(str)]
  o[i]['Date'] = o[i]['Date2']
  o[i] = o[i].drop(['Date2'], axis=1)
  o[i].Date=o[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  o[i] = o[i][o[i]['Lab'] != o[i]['Lib Dem']]
  for z in parties:
    o[i][z] = [x.replace('%','') for x in o[i][z].astype(str)]

O = pd.concat(o.values(), ignore_index=True)
O.drop(O.index[[0]],inplace=True)


# 1979 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1979_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
pf=pd.read_html(str(tables))

headers = ['Date', 'Lab', 'Con', 'Lib Dem']
parties = ['Lab', 'Con', 'Lib Dem']

p = {}
for i in range(6):
  p[i]=pd.DataFrame(pf[i])
  p[i]=p[i].drop(["Pollster","Client", "Lead"], axis=1)
  p[i].columns = headers
  p[i]['Date2'] = p[i]['Date'].str.split('–').str[1]
  p[i].Date2.fillna(p[i].Date, inplace=True)
  p[i]['Date2'] = [x+ str(1979-i) for x in p[i]['Date2'].astype(str)]
  p[i]['Date'] = p[i]['Date2']
  p[i] = p[i].drop(['Date2'], axis=1)
  p[i].Date=p[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  p[i] = p[i][p[i]['Lab'] != p[i]['Lib Dem']]
  for z in parties:
    p[i][z] = [x.replace('%','') for x in p[i][z].astype(str)]

P = pd.concat(p.values(), ignore_index=True)
P.drop(P.index[[0]],inplace=True)


# 1974 GENERAL ELECTIONs

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1974_United_Kingdom_general_elections"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
qf=pd.read_html(str(tables))

headers = ['Date', 'Con',  'Lab','Lib Dem']
parties = [ 'Con', 'Lab', 'Lib Dem']

q = {}

q[0]=pd.DataFrame(qf[0])
q[0]=q[0].drop(["Pollster","Client", "Lead"], axis=1)
q[0].columns = headers
q[0]['Date2'] = q[0]['Date'].str.split('–').str[1]
q[0].Date2.fillna(q[0].Date, inplace=True)
q[0]['Date2'] = [x+ str(1974) for x in q[0]['Date2'].astype(str)]
q[0]['Date'] = q[0]['Date2']
q[0] = q[0].drop(['Date2'], axis=1)
q[0].Date=q[0].Date.astype(str).apply(lambda x: dateparser.parse(x))
q[0] = q[0][q[0]['Lab'] != q[0]['Lib Dem']]
for z in parties:
  q[0][z] = [x.replace('%','') for x in q[0][z].astype(str)]
    
for i in range(5):
  q[i+1]=pd.DataFrame(qf[i+1])
  q[i+1]=q[i+1].drop(["Pollster","Client", "Lead"], axis=1)
  q[i+1].columns = headers
  q[i+1]['Date2'] = q[i+1]['Date'].str.split('–').str[1]
  q[i+1].Date2.fillna(q[i+1].Date, inplace=True)
  q[i+1]['Date2'] = [x+ str(1974-i) for x in q[i+1]['Date2'].astype(str)]
  q[i+1]['Date'] = q[i+1]['Date2']
  q[i+1] = q[i+1].drop(['Date2'], axis=1)
  q[i+1].Date=q[i+1].Date.astype(str).apply(lambda x: dateparser.parse(x))
  q[i+1] = q[i+1][q[i+1]['Lab'] != q[i+1]['Lib Dem']]
  for z in parties:
    q[i+1][z] = [x.replace('%','') for x in q[i+1][z].astype(str)]

Q = pd.concat(q.values(), ignore_index=True)
Q.drop(Q.index[[0]],inplace=True)


# 1970 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1970_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
q2f=pd.read_html(str(tables))

headers = ['Date', 'Lab', 'Con', 'Lib Dem']
parties = ['Lab', 'Con', 'Lib Dem']

q2 = {}

for i in range(5):
  q2[i]=pd.DataFrame(q2f[i])
  q2[i]=q2[i].drop(["Polling Organisation", "Lead"], axis=1)
  q2[i].columns = headers
  q2[i]['Date2'] = q2[i]['Date'].str.split('–').str[1]
  q2[i].Date2.fillna(q2[i].Date, inplace=True)
  q2[i]['Date2'] = [x+ str(1970-i) for x in q2[i]['Date2'].astype(str)]
  q2[i]['Date'] = q2[i]['Date2']
  q2[i] = q2[i].drop(['Date2'], axis=1)
  q2[i].Date=q2[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  q2[i] = q2[i][q2[i]['Lab'] != q2[i]['Lib Dem']]
  for z in parties:
    q2[i][z] = [x.replace('%','') for x in q2[i][z].astype(str)]

Q2 = pd.concat(q2.values(), ignore_index=True)
Q2.drop(Q2.index[[0]],inplace=True)



# 1966 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1966_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
rf=pd.read_html(str(tables))

headers = ['Date', 'Lab', 'Con', 'Lib Dem']
parties = ['Lab', 'Con', 'Lib Dem']

r = {}

for i in range(3):
  r[i]=pd.DataFrame(rf[i])
  r[i]=r[i].drop(["Polling Organisation", "Lead"], axis=1)
  r[i].columns = headers
  r[i]['Date2'] = r[i]['Date'].str.split('–').str[1]
  r[i].Date2.fillna(r[i].Date, inplace=True)
  r[i]['Date2'] = [x+ str(1966-i) for x in r[i]['Date2'].astype(str)]
  r[i]['Date'] = r[i]['Date2']
  r[i] = r[i].drop(['Date2'], axis=1)
  r[i].Date=r[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  r[i] = r[i][r[i]['Lab'] != r[i]['Lib Dem']]
  for z in parties:
    r[i][z] = [x.replace('%','') for x in r[i][z].astype(str)]

R = pd.concat(r.values(), ignore_index=True)
R.drop(R.index[[0]],inplace=True)


# 1964 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1964_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
sf=pd.read_html(str(tables))

headers = ['Date', 'Con',  'Lab','Lib Dem']
parties = [ 'Con', 'Lab', 'Lib Dem']

s = {}

for i in range(6):
  s[i]=pd.DataFrame(sf[i])
  s[i]=s[i].drop(["Polling Organisation", "Lead"], axis=1)
  s[i].columns = headers
  s[i]['Date2'] = s[i]['Date'].str.split('–').str[1]
  s[i].Date2.fillna(s[i].Date, inplace=True)
  s[i]['Date2'] = [x+ str(1964-i) for x in s[i]['Date2'].astype(str)]
  s[i]['Date'] = s[i]['Date2']
  s[i] = s[i].drop(['Date2'], axis=1)
  s[i].Date=s[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  s[i] = s[i][s[i]['Lab'] != s[i]['Lib Dem']]
  for z in parties:
    s[i][z] = [x.replace('%','') for x in s[i][z].astype(str)]

S = pd.concat(s.values(), ignore_index=True)
S.drop(S.index[[0]],inplace=True)


# 1959 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1959_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
tf=pd.read_html(str(tables))

headers = ['Date', 'Con',  'Lab','Lib Dem']
parties = [ 'Con', 'Lab', 'Lib Dem']

t = {}

for i in range(5):
  t[i]=pd.DataFrame(tf[i])
  t[i]=t[i].drop(["Polling Organisation", "Lead"], axis=1)
  t[i].columns = headers
  t[i]['Date2'] = t[i]['Date'].str.split('–').str[1]
  t[i].Date2.fillna(t[i].Date, inplace=True)
  t[i]['Date2'] = [x+ str(1959-i) for x in t[i]['Date2'].astype(str)]
  t[i]['Date'] = t[i]['Date2']
  t[i] = t[i].drop(['Date2'], axis=1)
  t[i].Date=t[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  t[i] = t[i][t[i]['Lab'] != t[i]['Lib Dem']]
  for z in parties:
    t[i][z] = [x.replace('%','') for x in t[i][z].astype(str)]

T = pd.concat(t.values(), ignore_index=True)
T.drop(T.index[[0]],inplace=True)


# 1955 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1955_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
uf=pd.read_html(str(tables))

headers = ['Date', 'Lab', 'Con', 'Lib Dem']
parties = ['Lab', 'Con', 'Lib Dem']

u = {}

for i in range(5):
  u[i]=pd.DataFrame(uf[i])
  u[i]=u[i].drop(["Pollster","Client", "Lead"], axis=1)
  u[i].columns = headers
  u[i]['Date2'] = u[i]['Date'].str.split('–').str[1]
  u[i].Date2.fillna(u[i].Date, inplace=True)
  u[i]['Date2'] = [x+ str(1955-i) for x in u[i]['Date2'].astype(str)]
  u[i]['Date'] = u[i]['Date2']
  u[i] = u[i].drop(['Date2'], axis=1)
  u[i].Date=u[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  u[i] = u[i][u[i]['Lab'] != u[i]['Lib Dem']]
  for z in parties:
    u[i][z] = [x.replace('%','') for x in u[i][z].astype(str)]

U = pd.concat(u.values(), ignore_index=True)
U.drop(U.index[[0]],inplace=True)


# 1951 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1951_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
vf=pd.read_html(str(tables))

headers = ['Date', 'Lab', 'Con', 'Lib Dem']
parties = ['Lab', 'Con', 'Lib Dem']

v = {}

for i in range(2):
  v[i]=pd.DataFrame(vf[i])
  v[i]=v[i].drop(["Pollster","Client", "Lead"], axis=1)
  v[i].columns = headers
  v[i]['Date2'] = v[i]['Date'].str.split('–').str[1]
  v[i].Date2.fillna(v[i].Date, inplace=True)
  v[i]['Date2'] = [x+ str(1951-i) for x in v[i]['Date2'].astype(str)]
  v[i]['Date'] = v[i]['Date2']
  v[i] = v[i].drop(['Date2'], axis=1)
  v[i].Date=v[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  v[i] = v[i][v[i]['Lab'] != v[i]['Lib Dem']]
  for z in parties:
    v[i][z] = [x.replace('%','') for x in v[i][z].astype(str)]

V = pd.concat(v.values(), ignore_index=True)
V.drop(V.index[[0]],inplace=True)


# 1950 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1950_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
wf=pd.read_html(str(tables))

headers = ['Date', 'Lab', 'Con', 'Lib Dem']
parties = ['Lab', 'Con', 'Lib Dem']

w = {}

for i in range(5):
  w[i]=pd.DataFrame(wf[i])
  w[i]=w[i].drop(["Pollster","Client", "Lead"], axis=1)
  w[i].columns = headers
  w[i]['Date2'] = w[i]['Date'].str.split('–').str[1]
  w[i].Date2.fillna(w[i].Date, inplace=True)
  w[i]['Date2'] = [x+ str(1950-i) for x in w[i]['Date2'].astype(str)]
  w[i]['Date'] = w[i]['Date2']
  w[i] = w[i].drop(['Date2'], axis=1)
  w[i].Date=w[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  w[i] = w[i][w[i]['Lab'] != w[i]['Lib Dem']]
  for z in parties:
    w[i][z] = [x.replace('%','') for x in w[i][z].astype(str)]

W = pd.concat(w.values(), ignore_index=True)
W.drop(W.index[[0,-1]],inplace=True)


# 1945 GENERAL ELECTION

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1945_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
yf=pd.read_html(str(tables))

headers = ['Date', 'Con',  'Lab','Lib Dem']
parties = [ 'Con', 'Lab', 'Lib Dem']

y = {}

y[0]=pd.DataFrame(yf[0])
y[0]=y[0].drop(["Pollster","Client", "Lead"], axis=1)
y[0].columns = headers
y[0].Date=y[0].Date.astype(str).apply(lambda x: dateparser.parse(x))
y[0] = y[0][y[0]['Lab'] != y[0]['Lib Dem']]
for z in parties:
  y[0][z] = [x.replace('%','') for x in y[0][z].astype(str)]

Y = pd.concat(y.values(), ignore_index=True)
Y.drop(Y.index[[-1]],inplace=True)




data = pd.concat([D,E,F,G,H,J,K,L,M,N,O,P,Q,Q2,R,S,T,U,V,W,Y])
data.to_csv('UK_Elections/general_polling/poll.csv', index=False)
