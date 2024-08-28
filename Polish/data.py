import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Polish_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

# 2023 part 1

data24=pd.DataFrame(df[2])
data24=data24.drop(['Polling firm/Link','Sample size','Others','Don\'t know','Lead','Nonpartisan Local Government Activists','There is One Poland'],axis=1)

headers = ['Date','PiS','KO','Trzecia Droga','Lewica','Konfederacja']
parties = ['PiS','KO','Trzecia Droga','Lewica','Konfederacja']
data24.columns = headers
data24.drop(data24.index[[-1,-2,-3,]],inplace=True)
data24=data24[data24['Date'] != '7 Apr']
data24=data24[data24['Date'] != '9 Jun	']
data24['Date'] = [p.sub('', x) for x in data24['Date']]
data24['Date2'] = data24['Date'].str.split('–').str[1]
data24.Date2.fillna(data24['Date'].str.split('-').str[1], inplace=True)
data24.Date2.fillna(data24.Date, inplace=True)
data24.Date = data24.Date2
data24 = data24.drop(['Date2'],axis=1)
data24.Date = data24['Date'].astype(str)
data24['Date'] = [x+' 2024' for x in data24['Date']]
data24.Date = data24.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data24 = data24[data24['PiS'] != data24['Lewica']]
for z in parties:
  data24[z] = [p.sub('', x) for x in data24[z].astype(str)]
  data24[z] = data24[z].astype('float').astype(str)
data24[parties] = data24[parties].astype(float)
# data24['Trzecia Droga']=np.where(data24['Koalicja']==data24['PL2050'],data24['PL2050'],np.nan)
# threeway = ['Koalicja','PL2050']
# data24=data24.drop(threeway, axis=1)


# 2023

data23=pd.DataFrame(df[3])
data23=data23.drop(['Polling firm/Link','Sample size','Others','Don\'t know','Lead','Nonpartisan Local Government Activists','There is One Poland'],axis=1)

headers = ['Date','PiS','KO','Trzecia Droga','Lewica','Konfederacja']
parties = ['PiS','KO','Trzecia Droga','Lewica','Konfederacja']
data23.columns = headers
data23.drop(data23.index[[-1,-3,]],inplace=True)
# data23['Date'] = [p.sub('', x) for x in data23['Date']]
data23['Date2'] = data23['Date'].str.split('–').str[1]
data23.Date2.fillna(data23['Date'].str.split('-').str[1], inplace=True)
data23.Date2.fillna(data23.Date, inplace=True)
data23.Date = data23.Date2
data23 = data23.drop(['Date2'],axis=1)
data23.Date = data23['Date'].astype(str)
data23['Date'] = [x+' 2023' for x in data23['Date']]
data23.Date = data23.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data23 = data23[data23['PiS'] != data23['Lewica']]
for z in parties:
  data23[z] = [p.sub('', x) for x in data23[z].astype(str)]
  data23[z] = data23[z].astype('float').astype(str)
data23[parties] = data23[parties].astype(float)
# data23['Trzecia Droga']=np.where(data23['Koalicja']==data23['PL2050'],data23['PL2050'],data23['Koalicja']+data23['PL2050'])
# threeway = ['Koalicja','PL2050']
# data23=data23.drop(threeway, axis=1)


data = pd.concat([data24,data23])
data=data[['Date','PiS','KO','Trzecia Droga','Lewica','Konfederacja']]
data.to_csv('Polish/poll.csv', index=False)



parties = ['PiS','KO','Lewica','Konfederacja', 'Trzecia Droga']
UO = ['KO', 'Lewica', 'Trzecia Droga']
R = ['PiS', 'Konfederacja']
data[parties] = data[parties].astype(float)
data['Government (KO + Lewica + Trzecia Droga)'] = data[UO].sum(axis=1)
data['Opposition (PiS + Konfederacja)'] = data[R].sum(axis=1)
data = data.drop(UO + R, axis=1)

data.to_csv('Polish/poll2.csv', index=False)


