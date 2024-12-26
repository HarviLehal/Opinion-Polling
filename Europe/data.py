import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_and_seat_projections_for_the_2024_European_Parliament_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

data2=pd.DataFrame(df[2])
data2=data2.drop(["Organisation", "Area", "Lead"], axis=1)

headers = ['Date','SEATS','Left','S&D','G/EFA','Renew','EPP','ECR','ID','NI','Other']
parties = ['SEATS','Left','S&D','G/EFA','Renew','EPP','ECR','ID','NI','Other']
data2.columns = headers
data2.drop(data2.index[[0]],inplace=True)
data2.Date = data2.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

data2 = data2[data2['EPP'] != data2['NI']]

data2 =data2.dropna(subset=['Date'])

for z in parties:
  data2[z] = [p.sub('', x) for x in data2[z].astype(str)]
  data2[z] = [x.replace('–',str(np.nan)) for x in data2[z].astype(str)]
  data2[z] = [x.replace('–',str(np.nan)) for x in data2[z].astype(str)]
data2 =data2.dropna(subset=['SEATS'])

data2 = data2[pd.to_numeric(data2['SEATS'], errors='coerce').notnull()]
for z in parties:
  data2[z] = [x.replace('None',str(np.nan)) for x in data2[z].astype(str)]
data2 = data2.replace(r'^\s*$', str(np.nan), regex=True)

data2[parties] = data2[parties].astype(float)

data2 = data2[data2['SEATS'] != 751]
data2=data2.drop(["SEATS"], axis=1)
data2 = data2.reset_index(drop=True)
data2.loc[len(data2.index)-1,['Date']] = '26 May 2019'
data2.Date = data2.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))



data2.to_csv('Europe/poll.csv', index=False)







