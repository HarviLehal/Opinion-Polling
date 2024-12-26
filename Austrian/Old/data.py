import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Austrian_legislative_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['Date','ÖVP','SPÖ','FPÖ','Grüne','NEOS']
parties = ['ÖVP','SPÖ','FPÖ','Grüne','NEOS']
d = {}
for i in range(6):
  if i == 0:
      headers.append('KPÖ')
      headers.append('KEINE')
      headers.append('BIER')
      headers.append('LMP')
  if i == 1:
      headers.remove('LMP')
      headers.remove('KEINE')
  elif i == 2:
      headers.remove('BIER')
      headers.remove('KPÖ')
      headers.append('MFG')
      headers.append('BIER')
  elif i == 3:
      headers.remove('BIER')
  elif i == 4:
      headers.remove('MFG')
  elif i == 5:
      headers.append('HC')
  d[i]=pd.DataFrame(df[i])
  print(d[i])
  d[i]=d[i].drop(["Polling firm", "Sample size", "Method", "Others", "Lead"], axis=1)
  # if i==0:
    # d[i]=d[i].drop(["KEINE", "LMP"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['ÖVP'] != d[i]['NEOS']]
  if i != 5:
    d[i].drop(d[i].index[[-1]],inplace=True)

D = pd.concat(d.values(), ignore_index=True)
D.loc[len(D.index)-1,['KPÖ']] = 2.06
D.loc[len(D.index)-1,['BIER']] = 0.1
D.drop(D.index[[0,1]],inplace=True)

D = D[D.Date.notnull()]


parties = ['ÖVP','SPÖ','FPÖ','Grüne','NEOS','KPÖ','KEINE','BIER','LMP','MFG','HC']
for z in parties:
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  D[z] = [x.replace('–',str(np.nan)) for x in D[z].astype(str)]
  D[z] = [x.replace('—',str(np.nan)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)
D=D.drop(["MFG", "HC",'KEINE','LMP'], axis=1)


V=26.3
S=21.0
F=28.8
G=8.3
N=9.2
K=2.4
B=2.0
O=100-V-S-F-G-N-K-B

new_row = pd.DataFrame({'Date':'29 September 2024','ÖVP':V,'SPÖ':S,'FPÖ':F,'Grüne':G,'NEOS':N,'KPÖ':K,'BIER':B}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D.to_csv('Austrian/poll.csv', index=False)





parties  = ['ÖVP','SPÖ','FPÖ','Grüne','NEOS','KPÖ','BIER']

for z in parties:
  D[z] = D[z].apply(lambda x: x if x > 4 else 0)

Ampel    = ['SPÖ','Grüne','NEOS']
Ampelp   = ['SPÖ','Grüne','NEOS','BIER','KPÖ']
Groko    = ['SPÖ','ÖVP']
Kiwi     = ['ÖVP','Grüne']
LibRecht = ['ÖVP','NEOS']
Dirndl   = ['ÖVP','NEOS','Grüne']
Ibiza    = ['ÖVP','FPÖ']

D['Ampel (SGN)'] = D[Ampel].sum(axis=1)       # RG  (Maroon) #770004
D['Ampel Plus (SGNBK)'] = D[Ampelp].sum(axis=1) # RB  (Black) #10305B
D['Groko (SÖ)'] = D[Groko].sum(axis=1)       # RGY (Red) #DD1529
D['Kiwi (ÖG)'] = D[Kiwi].sum(axis=1)         # BGY (Green) #509A3A
D['Liberale Rechts (ÖN)'] = D[LibRecht].sum(axis=1)   # BRY (Yellow) #FBBE00
D['Dirndl (ÖNG)'] = D[Dirndl].sum(axis=1)       # BRG (Orange) #E5963F
D['Ibiza (ÖF)'] = D[Ibiza].sum(axis=1)       # BG  (Kiwi Green) #8EE53F
D = D.drop(parties, axis=1)

D.to_csv('Austrian/poll2.csv', index=False)



D = pd.concat(d.values(), ignore_index=True)
D.loc[len(D.index)-1,['KPÖ']] = 2.06
D.loc[len(D.index)-1,['BIER']] = 0.1
D.drop(D.index[[0,1]],inplace=True)

D = D[D.Date.notnull()]


parties = ['ÖVP','SPÖ','FPÖ','Grüne','NEOS','KPÖ','KEINE','BIER','LMP','MFG','HC']
for z in parties:
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  D[z] = [x.replace('–',str(np.nan)) for x in D[z].astype(str)]
  D[z] = [x.replace('—',str(np.nan)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)
D=D.drop(["MFG", "HC",'KEINE','LMP'], axis=1)
parties  = ['ÖVP','SPÖ','FPÖ','Grüne','NEOS','KPÖ','BIER']

new_row = pd.DataFrame({'Date':'29 September 2024','ÖVP':V,'SPÖ':S,'FPÖ':F,'Grüne':G,'NEOS':N,'KPÖ':K,'BIER':B}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

# take the sum of all parties with more than 5% in each poll to get the total percentage of valid votes
for z in parties:
  D[z] = D[z].apply(lambda x: x if x > 4 else 0)
D['Mehrheit'] = D[parties].sum(axis=1)
# divide by 2 to get the true majority required
D['Mehrheit'] = D['Mehrheit']/2
D.drop(parties, axis=1, inplace=True)
D.to_csv('Austrian/poll3.csv', index=False)
