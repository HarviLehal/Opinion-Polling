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
for i in range(5):
  if i == 0:
      headers.append('KPÖ')
      headers.append('BIER')
  elif i == 1:
      headers.remove('BIER')
      headers.remove('KPÖ')
      headers.append('MFG')
      headers.append('BIER')
  elif i == 2:
      headers.remove('BIER')
  elif i == 3:
      headers.remove('MFG')
  elif i == 4:
      headers.append('HC')
  d[i]=pd.DataFrame(df[i])
  print(d[i])
  d[i]=d[i].drop(["Polling firm", "Sample size", "Method", "Others", "Lead"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['ÖVP'] != d[i]['NEOS']]

d[4].drop(d[4].index[[-1]],inplace=True)
  

D = pd.concat(d.values(), ignore_index=True)

D = D[D.Date.notnull()]


parties = ['ÖVP','SPÖ','FPÖ','Grüne','NEOS','BIER','KPÖ','MFG','HC']
for z in parties:
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  D[z] = [x.replace('–',str(np.NaN)) for x in D[z].astype(str)]
  D[z] = [x.replace('—',str(np.NaN)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)

D.to_csv('Austrian/poll.csv', index=False)

D=D.drop(["MFG", "HC"], axis=1)
D.to_csv('Austrian/poll2.csv', index=False)





# 
# parties = ['ÖVP','SPÖ','FPÖ','Grüne','NEOS','BIER','KPÖ','MFG','HC']
# RG    = ['SPÖ','Grüne']
# GroKo = ['ÖVP','SPÖ']
# Kenia = ['ÖVP','SPÖ','Grüne']
# Kiwi  = ['ÖVP','Grüne']
# Kiwip = ['ÖVP','Grüne','NEOS']
# Ibiza = ['ÖVP','FPÖ']
# Links = ['SPÖ','Grüne','NEOS','KPÖ','BIER']
# Recht = ['ÖVP','FPÖ','MFG','HC']
# 
# D['Rot-Grün'] = D[RG].sum(axis=1)       # RG  (Maroon) #770004
# D['GroKo'] = D[GroKo].sum(axis=1)       # RB  (Black) #10305B
# D['Kenia'] = D[Kenia].sum(axis=1)       # RGY (Red) #DD1529
# D['Kiwi'] = D[Kiwi].sum(axis=1)         # BGY (Green) #509A3A
# D['Kiwi Plus'] = D[Kiwip].sum(axis=1)   # BRY (Yellow) #FBBE00
# D['Ibiza'] = D[Ibiza].sum(axis=1)       # BRG (Orange) #E5963F
# D['Links'] = D[Links].sum(axis=1)       # BG  (Kiwi Green) #8EE53F
# D['Rechts'] = D[Recht].sum(axis=1)      # BBr (AfD blue) #0489DB
# D = D.drop(parties, axis=1)
# 
# D.to_csv('Austrian/poll3.csv', index=False)



parties  = ['ÖVP','SPÖ','FPÖ','Grüne','NEOS','BIER','KPÖ']
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

D.to_csv('Austrian/poll3.csv', index=False)
