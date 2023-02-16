import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Polish_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))


# 2023

data23=pd.DataFrame(df[0])
data23=data23.drop(['Polling firm/Link','Sample size','Agreement','Kukiz\'15','AGROunia','Others / Don\'t know','Lead'],axis=1)

headers = ['Date','PiS','KO','Lewica','Koalicja','Konfederacja','PL2050']
parties = ['PiS','KO','Lewica','Koalicja','Konfederacja','PL2050']
data23.columns = headers

data23['Date2'] = data23['Date'].str.split('–').str[1]
data23.Date2.fillna(data23['Date'].str.split('-').str[1], inplace=True)
data23.Date2.fillna(data23.Date, inplace=True)
data23.Date = data23.Date2
data23 = data23.drop(['Date2'],axis=1)
data23.Date = data23['Date'].astype(str)
data23['Date'] = [x+' 2023' for x in data23['Date']]
data23.Date = data23.Date.apply(lambda x: dateparser.parse(x))


# 2022

data22=pd.DataFrame(df[1])
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
data22.Date = data22.Date.apply(lambda x: dateparser.parse(x))


# 2021

data21=pd.DataFrame(df[2])
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
data21.Date = data21.Date.apply(lambda x: dateparser.parse(x))
for z in parties:
  data21[z] = [x.replace('[i]','') for x in data21[z].astype(str)]
  data21[z] = [x.replace('[m]','') for x in data21[z].astype(str)]
  data21[z] = [x.replace('[r]','') for x in data21[z].astype(str)]
  data21[z] = [x.replace('[i]','') for x in data21[z].astype(str)]
  data21[z] = [x.replace('[u]','') for x in data21[z].astype(str)]
  data21[z] = [x.replace('[v]','') for x in data21[z].astype(str)]
  data21[z] = [x.replace('[w]','') for x in data21[z].astype(str)]


# 2020

data20=pd.DataFrame(df[3])
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
data20.Date = data20.Date.apply(lambda x: dateparser.parse(x))

for z in parties:
  data20[z] = [x.replace('[ac]','') for x in data20[z].astype(str)]
  data20[z] = [x.replace('[ad]','') for x in data20[z].astype(str)]
  data20[z] = [x.replace('–','0') for x in data20[z].astype(str)]
  data20[z] = [x.replace('-','0') for x in data20[z].astype(str)]
data20[parties] = data20[parties].astype(float)

data20['KO'] = np.where(data20['KO1'] == data20['KO2'],data20['KO2'],data20[KO].sum(axis=1))
data20 = data20.drop(KO, axis=1)


# 2019

data19=pd.DataFrame(df[4])
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
data19.Date = data19.Date.apply(lambda x: dateparser.parse(x))
data19.drop(data19.index[[-1,-3,]],inplace=True)



data = pd.concat([data23,data22,data21,data20,data19])
data = data[data['PiS'] != data['Lewica']]



data.to_csv('Polish/Votes/poll.csv', index=False)
