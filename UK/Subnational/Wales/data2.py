import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser
import numpy as np

wikiurl="https://en.wikipedia.org/wiki/Next_Senedd_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))


headers = ['Date', 'Lab', 'Con', 'Plaid Cymru', 'Green', 'Lib Dem', 'AWA', 'Reform']
parties = ['Lab', 'Con', 'Plaid Cymru', 'Green', 'Lib Dem', 'AWA', 'Reform']
d = {}
for i in range(2):
  d[i]=pd.DataFrame(df[i+1])
  if i==0:
    d[i] = d[i].drop(["Pollster", "Client", "Sample size", "Others", "Lead"], axis=1)
  else:
    d[i] = d[i].drop(["Pollster", "Client", "Sample size", "Others", "Lead", "UKIP"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Lab'] != d[i]['Green']]
  for z in parties:
      d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z].astype(str)]
      d[i][z] = [x.replace('TBA',str(np.nan)) for x in d[i][z].astype(str)]
      d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z].astype(str)]
      d[i][z] = [x.replace('?',str(np.nan)) for x in d[i][z].astype(str)]
      d[i][z] = d[i][z].str.strip('%')
      d[i][z] = d[i][z].astype('float')
  d[i].drop(d[i].index[[-1]],inplace=True)

D = pd.concat(d.values(), ignore_index=True)
D.to_csv('UK/Subnational/Wales/poll_Senedd.csv', index=False)
