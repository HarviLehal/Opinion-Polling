import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Polish_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

# 2023 part 1

data24=pd.DataFrame(df[0])
data24=data24.drop(['Polling firm/Link','Sample size','Others','Don\'t know','Lead','Nonpartisan Local Gov. Activists','There is One Poland'],axis=1)

headers = ['Date','PiS','KO','Lewica','Koalicja','PL2050','Konfederacja']
parties = ['PiS','KO','Lewica','Koalicja','PL2050','Konfederacja']
data24.columns = headers
data24['Date'] = [p.sub('', x) for x in data24['Date']]
data24['Date2'] = data24['Date'].str.split('–').str[1]
data24.Date2.fillna(data24['Date'].str.split('-').str[1], inplace=True)
data24.Date2.fillna(data24.Date, inplace=True)
data24.Date = data24.Date2
data24 = data24.drop(['Date2'],axis=1)
data24.Date = data24['Date'].astype(str)
data24['Date'] = [x+' 2023' for x in data24['Date']]
data24.Date = data24.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data24 = data24[data24['PiS'] != data24['Lewica']]
for z in parties:
  data24[z] = [p.sub('', x) for x in data24[z].astype(str)]
  data24[z] = data24[z].astype('float').astype(str)
data24[parties] = data24[parties].astype(float)
data24['Trzecia Droga']=np.where(data24['Koalicja']==data24['PL2050'],data24['PL2050'],data24['PL2050']+data24['Koalicja'])
threeway = ['Koalicja','PL2050']
data24=data24.drop(threeway, axis=1)
data24.drop(data24.index[[0,2,]],inplace=True)


# 2023

data23=pd.DataFrame(df[1])
data23=data23.drop(['Polling firm/Link','Sample size','Kukiz\'15','AGROunia','Others / Don\'t know','Lead','Independents & Local Gov. Activists'],axis=1)

headers = ['Date','PiS','KO','Agreement','Koalicja','PL2050','Konfederacja','Lewica']
parties = ['PiS','KO','Agreement','Koalicja','PL2050','Konfederacja','Lewica']
data23.columns = headers
data23=data23.drop(['Agreement'],axis=1)
parties = ['PiS','KO','Koalicja','PL2050','Konfederacja','Lewica']
data23['Date'] = [p.sub('', x) for x in data23['Date']]
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
data23['Trzecia Droga']=np.where(data23['Koalicja']==data23['PL2050'],data23['PL2050'],np.nan)
threeway = ['Polish Coalition','Poland 2050']

# for z in threeway:
data23['Koalicja'][data23['Koalicja']==data23['Trzecia Droga']]=np.nan
data23['PL2050'][data23['Trzecia Droga']==data23['PL2050']]=np.nan




# 2022

data22=pd.DataFrame(df[2])
data22=data22.drop(['Polling firm/Link','Sample size','Agreement','Kukiz\'15','AGROunia','Others / Don\'t know','Lead'],axis=1)

headers = ['Date','PiS','KO','Lewica','Koalicja','Konfederacja','PL2050']
parties = ['PiS','KO','Lewica','Koalicja','Konfederacja','PL2050']
data22.columns = headers

data22['Date2'] = data22['Date'].str.split('–').str[1]
data22.Date2.fillna(data22['Date'].str.split('-').str[1], inplace=True)
data22.Date2.fillna(data22.Date, inplace=True)
data22.Date = data22.Date2
data22 = data22.drop(['Date2'],axis=1)
data22.Date = data22['Date'].astype(str)
data22['Date'] = [x+' 2022' for x in data22['Date']]
data22.Date = data22.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data22 = data22[data22['PiS'] != data22['Lewica']]
for z in parties:
  data22[z] = [p.sub('', x) for x in data22[z].astype(str)]
  data22[z] = data22[z].astype('float').astype(str)




# 2021

data21=pd.DataFrame(df[3])
data21=data21.drop(['Polling firm/Link','Sample size','Agreement','Kukiz\'15','Others / Don\'t know','Lead','Unnamed: 13_level_0'],axis=1)

headers = ['Date','PiS','KO','Lewica','Koalicja','Konfederacja','PL2050']
parties = ['PiS','KO','Lewica','Koalicja','Konfederacja','PL2050']
data21.columns = headers

data21['Date2'] = data21['Date'].str.split('–').str[1]
data21.Date2.fillna(data21['Date'].str.split('-').str[1], inplace=True)
data21.Date2.fillna(data21.Date, inplace=True)
data21.Date = data21.Date2
data21 = data21.drop(['Date2'],axis=1)
data21.Date = data21['Date'].astype(str)
data21['Date'] = [x+' 2021' for x in data21['Date']]
data21.Date = data21.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data21 = data21[data21['PiS'] != data21['Lewica']]

for z in parties:
  data21[z] = [p.sub('', x) for x in data21[z].astype(str)]
  data21[z] = data21[z].astype('float').astype(str)





# 2020

data20=pd.DataFrame(df[4])
data20=data20.drop(['Polling firm/Link','Sample size','Kukiz\'15','Others / Don\'t know','Lead'],axis=1)

headers = ['Date','PiS','KO1','KO2','Lewica','Koalicja','Konfederacja','PL2050']
parties = ['PiS','KO1','KO2','Lewica','Koalicja','Konfederacja','PL2050']
data20.columns = headers
KO=['KO1','KO2']
data20 = data20[data20['PiS'] != data20['Lewica']]
data20['Date2'] = data20['Date'].str.split('–').str[1]
data20.Date2.fillna(data20['Date'].str.split('-').str[1], inplace=True)
data20.Date2.fillna(data20.Date, inplace=True)
data20.Date = data20.Date2
data20 = data20.drop(['Date2'],axis=1)
data20.Date = data20['Date'].astype(str)
data20['Date'] = [x+' 2020' for x in data20['Date']]
data20=data20[~data20.Date.str.contains("12 Jul 2020")]
data20=data20[~data20.Date.str.contains("28 Jun 2020")]
data20.Date = data20.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data20 = data20[data20['PiS'] != data20['Lewica']]

for z in parties:
  data20[z] = [p.sub('', x) for x in data20[z].astype(str)]
  data20[z] = [x.replace('–','0') for x in data20[z].astype(str)]
  data20[z] = [x.replace('-','0') for x in data20[z].astype(str)]
  data20[z] = data20[z].astype('float').astype(str)

data20[KO]=data20[KO].astype('float')
data20['KO'] = np.where(data20['KO1'] == data20['KO2'],data20['KO2'],data20[KO].sum(axis=1))
data20 = data20.drop(KO, axis=1)





# 2019

data19=pd.DataFrame(df[5])
data19=data19.drop(['Polling firm/Link','Sample size','Others / Don\'t know','Lead','Unnamed: 10_level_0','Unnamed: 11_level_0','Unnamed: 12_level_0','Unnamed: 13_level_0'],axis=1)

headers = ['Date','PiS','KO','Lewica','Koalicja','Konfederacja']
parties = ['PiS','KO','Lewica','Koalicja','Konfederacja']
data19.columns = headers

data19['Date2'] = data19['Date'].str.split('–').str[1]
data19.Date2.fillna(data19['Date'].str.split('-').str[1], inplace=True)
data19.Date2.fillna(data19.Date, inplace=True)
data19.Date = data19.Date2
data19 = data19.drop(['Date2'],axis=1)
data19.Date = data19['Date'].astype(str)
data19['Date'] = [x+' 2019' for x in data19['Date']]
data19.Date = data19.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data19.drop(data19.index[[-1,-3,]],inplace=True)
data19 = data19[data19['PiS'] != data19['Lewica']]
for z in parties:
  data19[z] = [p.sub('', x) for x in data19[z].astype(str)]
  data19[z] = data19[z].astype('float').astype(str)






data = pd.concat([data24,data23,data22,data21,data20,data19])
data = data[data['PiS'] != data['Lewica']]



data.to_csv('Polish/Votes/poll.csv', index=False)

parties = ['PiS','KO','Lewica','Koalicja','PL2050','Konfederacja', 'Trzecia Droga']
UO = ['KO', 'Lewica', 'Koalicja', 'PL2050', 'Trzecia Droga']
R = ['PiS', 'Konfederacja']
data[parties] = data[parties].astype(float)
data['United Opposition (KO + Lewica + Trzecia Droga)'] = data[UO].sum(axis=1)
data['Right Wing (PiS + Konfederacja)'] = data[R].sum(axis=1)
data = data.drop(UO + R, axis=1)

data.to_csv('Polish/Votes/poll2.csv', index=False)
