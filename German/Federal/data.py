import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_German_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

headers = ['Date','SPD','Union','Grüne','FDP','AfD','Linke','FW']
parties = ['SPD','Union','Grüne','FDP','AfD','Linke','FW']
d = {}
for i in range(5):
  if i ==0:
    # headers.append('FW')
    headers.append('BSW')
  elif i == 2:
    # headers.remove('FW')
    headers.remove('BSW')
  # elif i == 2:
    # headers.remove('FW')
  # elif i == 3:
    # headers.append('FW')
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Polling firm", "Sample size", "Abs.", "Others", "Lead"], axis=1)
  d[i].columns = headers
  # if i == 0:
  d[i]=d[i].drop(['FW'], axis=1)
      # d[i]=d[i].drop(['BSW'], axis=1)
  # if i == 1:
      # d[i]=d[i].drop(['FW'], axis=1)
  # if i == 3:
      # d[i]=d[i].drop(['FW'], axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['SPD'] != d[i]['Linke']]

for i in range(4):
  d[i].drop(d[i].index[[-1]],inplace=True)
  

D = pd.concat(d.values(), ignore_index=True)

parties = ['SPD','Union','Grüne','FDP','AfD','Linke','BSW']
# parties = ['SPD','Union','Grüne','FDP','AfD','Linke']
for z in parties:
    D[z] = [x.replace('–',str(np.nan)) for x in D[z].astype(str)]
    D[z] = [x.replace('—',str(np.nan)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)

''' REMOVE WEIRD POLL!!!!'''

D=D.drop(D[D['BSW'] ==14].index)
# D=D.drop('BSW', axis=1)

D.to_csv('German/Federal/poll.csv', index=False)
# D=D.drop('BSW', axis=1)


parties = ['SPD','Union','Grüne','FDP','AfD']
D[parties] = D[parties].astype(float)
for z in parties:
  D[z] = D[z].apply(lambda x: x if x > 5 else 0)

parties = ['SPD','Union','Grüne','FDP','AfD','Linke','BSW']

Gov = ['SPD','Grüne','FDP']
Right = ['Union', 'AfD']

D[parties] = D[parties].astype(float)
D['Government'] = D[Gov].sum(axis=1)
D['Right Wing'] = D[Right].sum(axis=1)
D = D.drop(Gov + Right, axis=1)

D.to_csv('German/Federal/poll2.csv', index=False)



D = pd.concat(d.values(), ignore_index=True)
D=D.drop('BSW', axis=1)

parties = ['SPD','Union','Grüne','FDP','AfD','Linke','BSW']
parties = ['SPD','Union','Grüne','FDP','AfD','Linke']
for z in parties:
    D[z] = [x.replace('–',str(np.nan)) for x in D[z].astype(str)]
    D[z] = [x.replace('—',str(np.nan)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)
# D=D.drop(D[D['BSW'] > 0].index)
# D=D.drop('BSW', axis=1)

for z in parties:
  D[z] = D[z].apply(lambda x: x if x > 5 else 0)

RG              = ['SPD','Grüne']
GroKo           = ['Union','SPD']
Ampel           = ['SPD','Grüne','FDP']
Jamaika         = ['Union','Grüne','FDP']
Deutschland     = ['Union','SPD','FDP']
Kenia           = ['Union','SPD','Grüne']
Kiwi            = ['Union','Grüne']
Rechts          = ['Union','AfD']
Kemmerich       = ['Union','AfD','FDP']
# Mehrheit        = ['SPD','Union','Grüne','FDP','AfD']
parties = ['SPD','Union','Grüne','FDP','AfD','Linke']

D[parties] = D[parties].astype(float)
D['Rot-Grün'] = D[RG].sum(axis=1)               # RG  (Maroon) #770004
D['GroKo'] = D[GroKo].sum(axis=1)               # RB  (Black) #10305B
D['Ampel'] = D[Ampel].sum(axis=1)               # RGY (Red) #DD1529
D['Jamaika'] = D[Jamaika].sum(axis=1)           # BGY (Green) #509A3A
D['Deutschland'] = D[Deutschland].sum(axis=1)   # BRY (Yellow) #FBBE00
D['Kenia'] = D[Kenia].sum(axis=1)               # BRG (Orange) #E5963F
D['Kiwi'] = D[Kiwi].sum(axis=1)                 # BG  (Kiwi Green) #8EE53F
D['Rechts'] = D[Rechts].sum(axis=1)            # BBr (AfD blue) #0489DB
D['Kemmerich'] = D[Kemmerich].sum(axis=1)       # BBr (Brown) #AA692F
# D['Mehrheit'] = D[Mehrheit].sum(axis=1)/2
D = D.drop(parties, axis=1)

D.to_csv('German/Federal/poll3.csv', index=False)


D = pd.concat(d.values(), ignore_index=True)
parties = ['SPD','Union','Grüne','FDP','AfD','Linke','BSW']
for z in parties:
    D[z] = [x.replace('–',str(np.nan)) for x in D[z].astype(str)]
    D[z] = [x.replace('—',str(np.nan)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)
for z in parties:
  D[z] = D[z].apply(lambda x: x if x > 5 else 0)
D['Mehrheit'] = D[parties].sum(axis=1)
# divide by 2 to get the true majority required
D['Mehrheit'] = D['Mehrheit']/2
D.drop(parties, axis=1, inplace=True)
D.to_csv('German/Federal/poll4.csv', index=False)
