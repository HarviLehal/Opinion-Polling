import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://fr.wikipedia.org/wiki/Liste_de_sondages_pour_les_élections_législatives_slovaques_de_2023"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables), decimal=',', thousands='.')

df0=pd.DataFrame(df[0])
data22 = df0.drop(["Sondeur", "Échantillon", 'SMK', 'Most-Híd', 'Autres'], axis=1)

headers = ['Date', 'OĽaNO', 'SMER', 'SR', 'ĽSNS', 'PS', 'SPOLU/Dem', 'SaS', 'ZĽ', 'KDH', 'SNS', 'HLAS', 'Rep']
parties = ['OĽaNO', 'SMER', 'SR', 'ĽSNS', 'PS', 'SPOLU/Dem', 'SaS', 'ZĽ', 'KDH', 'SNS', 'HLAS', 'Rep']
data22.columns = headers
# data22['Date'] = [x.strip()[-11:] for x in data22['Date'].astype(str)]
# data22['Date'] = [x.replace('–','') for x in data22['Date'].astype(str)]

data22['Date2'] = data22['Date'].str.split('-').str[1]
data22.Date2.fillna(data22.Date, inplace=True)
data22.Date = data22.Date2
data22 = data22.drop(['Date2'],axis=1)
data22.Date = data22['Date'].astype(str)
data22.Date = data22.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

for z in parties:
  data22[z] = [x.replace('–','0') for x in data22[z].astype(str)]

for i in range(len(data22)):
  if data22['SPOLU/Dem'][i]==data22['PS'][i]:
    data22['SPOLU/Dem'][i] = 'nan'

data22.drop([0], axis=0, inplace=True)

    
print(data22)
  

data22.to_csv('Slovak/poll.csv', index=False)
