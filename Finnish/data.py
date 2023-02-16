import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Finnish_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

data22=pd.DataFrame(df[0])
data22 = data22.drop(['Polling firm','Sample size','Others','Lead','.mw-parser-output .tooltip-dotted{border-bottom:1px dotted;cursor:help}Gov.','Opp.','Unnamed: 16_level_0','Unnamed: 19_level_0','Unnamed: 17_level_0','Unnamed: 18_level_0','Unnamed: 20_level_0','Unnamed: 21_level_0','Unnamed: 22_level_0','Unnamed: 23_level_0'],axis=1)
headers = ['Date','SDP','PS','KOK','KESK','VIHR','VAS','SFP','KD','LIIK']
parties = ['SDP','PS','KOK','KESK','VIHR','VAS','SFP','KD','LIIK']
data22.columns = headers


data22['Date2'] = data22['Date'].str.split('–').str[1]
data22.Date2.fillna(data22['Date'].str.split('-').str[1], inplace=True)
data22.Date2.fillna(data22.Date, inplace=True)
data22.Date = data22.Date2
data22 = data22.drop(['Date2'],axis=1)
data22.Date = data22['Date'].astype(str)
data22=data22[~data22.Date.str.contains("26 May 2019")]
data22=data22[~data22.Date.str.contains("13 Jun 2021")]
data22=data22[~data22.Date.str.contains("23 Jan 2022")]
data22=data22[~data22.Date.str.contains("24 Feb 2022")]
data22.Date = data22.Date.apply(lambda x: dateparser.parse(x))
data22.drop(data22.index[[0]],inplace=True)


data22.to_csv('Finnish/poll.csv', index=False)

# COALITION!

for z in parties:
    data22[z] = [x.replace('–','0') for x in data22[z].astype(str)]
data22[parties] = data22[parties].astype(float)
Gov=['SDP','KESK','VIHR','VAS','SFP']
data22['Government'] = data22[Gov].sum(axis=1)
data22['Opposition'] = 100-data22['Government']
data22 = data22.drop(parties, axis=1)
data22.to_csv('Finnish/poll2.csv', index=False)
