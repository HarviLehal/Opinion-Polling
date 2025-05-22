import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2027_Finnish_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

data22=pd.DataFrame(df[0])
headers = ['Date','1','2','KOK','PS','SDP','KESK','VAS','VIHR','SFP','KD','LIIK','3','4','5','6']
parties = ['KOK','PS','SDP','KESK','VAS','VIHR','SFP','KD','LIIK']
data22.columns = headers
data22 = data22.drop(['1','2','3','4','5','6'],axis=1)



data22['Date2'] = data22['Date'].str.split('–').str[1]
data22.Date2.fillna(data22['Date'].str.split('-').str[1], inplace=True)
data22.Date2.fillna(data22.Date, inplace=True)
data22.Date = data22.Date2
data22 = data22.drop(['Date2'],axis=1)
data22.Date = data22['Date'].astype(str)
data22.Date = data22.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
# data22.drop(data22.index[[0]],inplace=True)
data22 = data22[data22['KOK'] != data22['LIIK']]


data22.to_csv('Finnish/poll_new.csv', index=False)

# COALITION!

for z in parties:
    data22[z] = [x.replace('–','0') for x in data22[z].astype(str)]
data22[parties] = data22[parties].astype(float)
Gov=['KOK','PS','SFP','KD']
Opp=['SDP','KESK','VIHR','SFP','VAS']
data22['Government'] = data22[Gov].sum(axis=1)
data22['Opposition'] = data22[Opp].sum(axis=1)
data22 = data22.drop(parties, axis=1)
data22.to_csv('Finnish/poll2_new.csv', index=False)
