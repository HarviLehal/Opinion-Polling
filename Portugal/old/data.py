import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2024_Portuguese_legislative_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


# 2023

data23=pd.DataFrame(df[0])
data23=data23.drop(['Polling firm/Link','Sample size','Turnout','O','Lead'],axis=1)

headers = ['Date','PS','PSD','CDS-PP','Chega','IL','BE','CDU','PAN','LIVRE']
parties = ['PS','PSD','CDS-PP','Chega','IL','BE','CDU','PAN','LIVRE']
data23.columns = headers
data23['Date2'] = data23['Date'].str.split('–').str[1]
data23.Date2.fillna(data23['Date'].str.split('-').str[1], inplace=True)
data23.Date2.fillna(data23.Date, inplace=True)
data23.Date = data23.Date2
data23 = data23.drop(['Date2'],axis=1)
data23.Date = data23['Date'].astype(str)
data23.Date = data23.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data23 = data23[data23['PS'] != data23['LIVRE']]

for z in parties:
    data23[z] = [p.sub('', x) for x in data23[z].astype(str)]
    data23[z] = data23[z].str.split(' ').str[0]
    data23[z] = [x.replace('–',str(np.nan)) for x in data23[z].astype(str)]
    data23[z] = [x.replace('?',str(np.nan)) for x in data23[z].astype(str)]

data23.drop(data23.index[[-1,-3]],inplace=True)
data23.drop(data23.index[[0,2,3,4,5,6]],inplace=True)

data23[parties] = data23[parties].astype(float)

data23['AD']=np.where(data23['PSD']==data23['CDS-PP'],data23['PSD'],np.nan)
data23['PSD']=np.where(data23['PSD']==data23['CDS-PP'],np.nan,data23['PSD'])
data23['CDS-PP']=np.where(data23['CDS-PP']==data23['AD'],np.nan,data23['CDS-PP'])


data23=data23.drop(data23[data23['AD'] > 37.5].index)

data23 = data23[['Date','PS','PSD','Chega','IL','BE','CDU','CDS-PP','PAN','LIVRE','AD']]

# new_row = pd.DataFrame({'Date': '10 March 2024', 'PS':28.7 , 'PSD':np.nan , 'Chega':18.2 , 'IL':4.9, 'BE':4.4, 'CDU':3.2,'CDS-PP':np.nan,'PAN':1.9,'LIVRE':3.0,'AD':29.8}, index=[0])
# data23 = pd.concat([new_row,data23]).reset_index(drop=True)
# data23.Date=data23.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data23.to_csv('Portugal/poll.csv', index=False)


# Alternative

data23=pd.DataFrame(df[0])
data23=data23.drop(['Polling firm/Link','Sample size','Turnout','O','Lead'],axis=1)

headers = ['Date','PS','PSD','CDS-PP','Chega','IL','BE','CDU','PAN','LIVRE']
parties = ['PS','PSD','CDS-PP','Chega','IL','BE','CDU','PAN','LIVRE']
data23.columns = headers
data23['Date2'] = data23['Date'].str.split('–').str[1]
data23.Date2.fillna(data23['Date'].str.split('-').str[1], inplace=True)
data23.Date2.fillna(data23.Date, inplace=True)
data23.Date = data23.Date2
data23 = data23.drop(['Date2'],axis=1)
data23.Date = data23['Date'].astype(str)
data23.Date = data23.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data23 = data23[data23['PS'] != data23['LIVRE']]

for z in parties:
    data23[z] = [p.sub('', x) for x in data23[z].astype(str)]
    data23[z] = data23[z].str.split(' ').str[0]
    data23[z] = [x.replace('–',str(np.nan)) for x in data23[z].astype(str)]
    data23[z] = [x.replace('?',str(np.nan)) for x in data23[z].astype(str)]

data23.drop(data23.index[[-1,-3]],inplace=True)
data23.drop(data23.index[[0,2,3,4,5,6]],inplace=True)

data23[parties] = data23[parties].astype(float)
data23['PSD']=np.where(data23['PSD']==data23['CDS-PP'],data23['PSD'],data23['PSD']+data23['CDS-PP'])
data23=data23.drop(['CDS-PP'],axis=1)
data23=data23.drop(data23[data23['PSD'] > 37.5].index)
data23 = data23[['Date','PS','PSD','Chega','IL','BE','CDU','PAN','LIVRE']]

# new_row = pd.DataFrame({'Date': '10 March 2024', 'PS':28.66 , 'PSD':29.49 , 'Chega':18.06, 'IL':5.08, 'BE':4.46, 'CDU':3.30,'PAN':1.93,'LIVRE':3.26}, index=[0])
# data23 = pd.concat([new_row,data23]).reset_index(drop=True)
# data23.Date=data23.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data23.to_csv('Portugal/poll2.csv', index=False)

