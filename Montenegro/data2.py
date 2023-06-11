import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re


# wikiurl="https://en.wikipedia.org/wiki/2023_Montenegrin_parliamentary_election"
# table_class="wikitable sortable jquery-tablesorter"
# response=requests.get(wikiurl)
# print(response.status_code)
# soup = BeautifulSoup(response.text, 'html.parser')
# tables = soup.find_all('table',class_="wikitable")
# df=pd.read_html(str(tables))
# p = re.compile(r'\[[a-z]+\]')
# 
# data22=pd.DataFrame(df[2])
# data22 = data22.drop(['Polling firm/source','Others','Lead'],axis=1)
# 
# headers = ['Date','DPS','SD','UDSh','DF','PzP','Prava','DHP','UCG','SNP','Demos','DCG','CnB','BS','SDP','ASh','Forca','PES!'
# ]
# parties = ['DPS','SD','UDSh','DF','PzP','Prava','DHP','UCG','SNP','Demos','DCG','CnB','BS','SDP','ASh','Forca','PES!'
# ]
# data22.columns = headers
# 
# 
# data22['Date2'] = data22['Date'].str.split('–').str[1]
# data22.Date2.fillna(data22['Date'].str.split('-').str[1], inplace=True)
# data22.Date2.fillna(data22.Date, inplace=True)
# data22.Date = data22.Date2
# data22 = data22.drop(['Date2'],axis=1)
# data22.Date = data22['Date'].astype(str)
# data22.Date = data22.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
# 
# for z in parties:
#   data22[z] = [p.sub('', x) for x in data22[z].astype(str)]
#   data22[z] = [x.replace('–',str(np.NaN)) for x in data22[z]]
#   data22[z] = [x.replace('<1','0.4') for x in data22[z]]
#   data22[z] = [x.replace('w.DPS',str(np.NaN)) for x in data22[z]]
#   data22[z] = data22[z].astype('float').astype(str)
#   
#   
# data22[parties] = data22[parties].astype(float)
# 
# # DPS-SD-UDSh FIX
# data22['SD'][data22['SD']==data22['DPS']]=np.nan
# data22['UDSh'][data22['UDSh']==data22['DPS']]=np.nan
# 
# # DF-PzP-Prava-DHP-UCG-SNP FIX
# data22['PzP'][data22['PzP']==data22['DF']]=np.nan
# data22['Prava'][data22['Prava']==data22['DF']]=np.nan
# data22['DHP'][data22['DHP']==data22['DF']]=np.nan
# data22['UCG'][data22['UCG']==data22['DF']]=np.nan
# data22['SNP'][data22['SNP']==data22['DF']]=np.nan
# 
# data22 = data22.drop(['UDSh','PzP','Prava','DHP','UCG','Demos','Forca'],axis=1)
# 
# 
# data22.to_csv('Montenegro/poll2.csv', index=False)


df = pd.read_csv('Montenegro/poll2.csv')
new_row1 = pd.DataFrame({'Date':'28 May 2023','DPS':22.1,'SD':np.nan,'DF':15.3 ,'SNP':2.4,'DCG':np.nan,'CnB':np.nan,'DCG-URA':12.9,'BS':4.3,'SDP':np.nan,'ASh':np.nan,'PES!':32.5},index=[0])

new_row = pd.DataFrame({'Date':'11 June 2023','DPS':23.8,'SD':np.nan,'DF':14.8 ,'SNP':3.3,'DCG':np.nan,'CnB':np.nan,'DCG-URA':12.3,'BS':6.9,'SDP':2.8,'ASh':1.4,'PES!':25.6},index=[0])
D = pd.concat([new_row1,df]).reset_index(drop=True)
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D.rename(columns={"DF": "ZBCG"}, inplace=True)
D.rename(columns={"CnB": "URA"}, inplace=True)
D.rename(columns={"SNP": "SNP-Demos"}, inplace=True)
D['new'] = D['URA']+D['DCG']
D['new'].fillna(D['DCG-URA'], inplace=True)
D=D.drop(['URA','DCG','DCG-URA'],axis=1)
D.rename(columns={"new": "DCG-URA"}, inplace=True)

D.to_csv('Montenegro/poll3.csv', index=False)
