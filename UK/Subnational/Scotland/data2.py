import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser
import numpy as np

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Scottish_Parliament_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

df0=pd.DataFrame(df[1])
data23 = df0.drop(["Pollster", "Client", "Sample size", "Others", "Lead"], axis=1)
headers = ['Date', 'SNP', 'Con', 'Lab', 'Green', 'Lib Dem', "Reform"]
parties = ['SNP', 'Con', 'Lab', 'Green', 'Lib Dem', "Reform"]
data23.columns = headers
data23['Date2'] = data23['Date'].str.split('–').str[1]
data23.Date2.fillna(data23.Date, inplace=True)
# data23['Date2'] = [x+ str(2023-i) for x in data23['Date2'].astype(str)]
data23['Date'] = data23['Date2']
data23 = data23.drop(['Date2'], axis=1)
data23.Date=data23.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
for z in parties:
  data23[z] = [x.replace('–',str(np.NaN)) for x in data23[z].astype(str)]
  data23[z] = [x.replace('TBA',str(np.NaN)) for x in data23[z].astype(str)]
  data23[z] = [x.replace('?',str(np.NaN)) for x in data23[z].astype(str)]
  data23[z] = [x.replace('-',str(np.NaN)) for x in data23[z].astype(str)]
data23 = data23[data23['Lib Dem'] != data23['SNP']]
print(data23)

for z in parties:
  data23[z] = data23[z].astype(str)
  data23[z] = data23[z].str.strip('%')
  data23[z] = data23[z].astype('float')

data23.to_csv('UK/Subnational/Scotland/poll2.csv', index=False)



df0=pd.DataFrame(df[0])
data23 = df0.drop(["Pollster", "Client", "Sample size", "Others", "Lead"], axis=1)
headers = ['Date', 'SNP', 'Con', 'Lab', 'Lib Dem', 'Green']
parties = ['SNP', 'Con', 'Lab', 'Lib Dem', 'Green']
data23.columns = headers
data23['Date2'] = data23['Date'].str.split('–').str[1]
data23.Date2.fillna(data23.Date, inplace=True)
# data23['Date2'] = [x+ str(2023-i) for x in data23['Date2'].astype(str)]
data23['Date'] = data23['Date2']
data23 = data23.drop(['Date2'], axis=1)
data23.Date=data23.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
for z in parties:
    data23[z] = [x.replace('–',str(np.NaN)) for x in data23[z].astype(str)]
    data23[z] = [x.replace('TBA',str(np.NaN)) for x in data23[z].astype(str)]
    data23[z] = [x.replace('?',str(np.NaN)) for x in data23[z].astype(str)]
    data23[z] = [x.replace('-',str(np.NaN)) for x in data23[z].astype(str)]
data23 = data23[data23['Lib Dem'] != data23['SNP']]
print(data23)

for z in parties:
  data23[z] = data23[z].astype(str)
  data23[z] = data23[z].str.strip('%')
  data23[z] = data23[z].astype('float')

data23.to_csv('UK/Subnational/Scotland/poll3.csv', index=False)

