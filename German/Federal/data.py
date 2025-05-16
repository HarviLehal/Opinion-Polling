import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_German_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','Union','AfD','SPD','Grüne','Linke','BSW','FDP','Others']
parties = ['Union','AfD','SPD','Grüne','Linke','BSW','FDP','Others']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[0])
  d[i]=d[i].drop(["Polling firm", "Sample size", "Abs.", "Lead"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['SPD'] != d[i]['Linke']]

D = pd.concat(d.values(), ignore_index=True)

parties = ['Union','AfD','SPD','Grüne','Linke','BSW','FDP','Others']
# parties = ['SPD','Union','Grüne','FDP','AfD','Linke']
for z in parties:
    D[z] = [p.sub('', x) for x in D[z].astype(str)]
    D[z] = [x.replace('–',str(np.nan)) for x in D[z].astype(str)]
    D[z] = [x.replace('—',str(np.nan)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)

D.to_csv('German/Federal/poll.csv', index=False)

for z in parties:
  D[z] = np.where(5>D[z],np.nan,D[z])
D.loc[len(D.index)-1,['BSW']] = np.nan

D = D.drop('Others',axis=1)
parties = ['Union','AfD','SPD','Grüne','Linke','BSW','FDP']
Gov = ['SPD','Union']
Opp = [p for p in parties if p not in Gov]
D['Government'] = D[Gov].sum(axis=1)
D['Opposition'] = D[Opp].sum(axis=1)
D = D.drop(Gov + Opp, axis=1)
D.to_csv('German/Federal/poll2.csv', index=False)


D = pd.concat(d.values(), ignore_index=True)

parties = ['Union','AfD','SPD','Grüne','Linke','BSW','FDP','Others']
# parties = ['SPD','Union','Grüne','FDP','AfD','Linke']
for z in parties:
    D[z] = [p.sub('', x) for x in D[z].astype(str)]
    D[z] = [x.replace('–',str(np.nan)) for x in D[z].astype(str)]
    D[z] = [x.replace('—',str(np.nan)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)

for z in parties:
  D[z] = np.where(5>D[z],np.nan,D[z])
D = D.drop('Others',axis=1)
D.loc[len(D.index)-1,['BSW']] = np.nan
parties = ['Union','AfD','SPD','Grüne','Linke','BSW','FDP']

RG              = ['SPD','Grüne']
R2G             = ['SPD','Linke','Grüne']
GroKo           = ['Union','SPD']
Jamaika         = ['Union','Grüne','FDP']
Deutschland     = ['Union','SPD','FDP']
Kenia           = ['Union','SPD','Grüne']
Kiwi            = ['Union','Grüne']
Rechts          = ['Union','AfD']
Kemmerich       = ['Union','AfD','FDP']
Brombeer        = ['Union','BSW','SPD']
# Mehrheit        = ['SPD','Union','Grüne','FDP','AfD']
parties = ['Union','AfD','SPD','Grüne','Linke','BSW','FDP']
# 
D[parties] = D[parties].astype(float)
D['Rot²-Grün'] = D[R2G].sum(axis=1)               # RGY (Red) #DD1529
D['GroKo'] = D[GroKo].sum(axis=1)               # RB  (Black) #10305B
D['Rot-Grün'] = D[RG].sum(axis=1)               # RG  (Maroon) #770004
D['Jamaika'] = D[Jamaika].sum(axis=1)           # BGY (Green) #509A3A
D['Deutschland'] = D[Deutschland].sum(axis=1)   # BRY (Yellow) #FBBE00
D['Kenia'] = D[Kenia].sum(axis=1)               # BRG (Orange) #E5963F
D['Kiwi'] = D[Kiwi].sum(axis=1)                 # BG  (Kiwi Green) #8EE53F
D['Rechts'] = D[Rechts].sum(axis=1)            # BBr (AfD blue) #0489DB
D['Kemmerich'] = D[Kemmerich].sum(axis=1)       # BBr (Brown) #AA692F
D['Brombeer'] = D[Brombeer].sum(axis=1)       # BBr (Brown) #AA692F
# D['Mehrheit'] = D[parties].sum(axis=1)/2
D = D.drop(parties, axis=1)
# 
D.to_csv('German/Federal/poll3.csv', index=False)
# 
# 
D = pd.concat(d.values(), ignore_index=True)
D = D.drop('Others',axis=1)
parties = ['Union','AfD','SPD','Grüne','Linke','BSW','FDP']
for z in parties:
    D[z] = [p.sub('', x) for x in D[z].astype(str)]
    D[z] = [x.replace('–',str(np.nan)) for x in D[z].astype(str)]
    D[z] = [x.replace('—',str(np.nan)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)
for z in parties:
  D[z] = np.where(5>D[z],np.nan,D[z])
D.loc[len(D.index)-1,['BSW']] = np.nan
D['Mehrheit'] = D[parties].sum(axis=1)
# divide by 2 to get the true majority required
D['Mehrheit'] = D['Mehrheit']/2
D.drop(parties, axis=1, inplace=True)
D.to_csv('German/Federal/poll4.csv', index=False)
