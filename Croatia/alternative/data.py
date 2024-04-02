import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser
import numpy as np
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Croatian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

df0=pd.DataFrame(df[-2])
data22 = df0.drop(["Polling firm","Votes","Lead"], axis=1)
headers = ['Date','HDZ','SDP','DP','Most','Možemo!','RF','Centar1','Centar2','Fokus','KH','HNS','IDS','HSS','HSU','HS','SD','Others','Undecided']
parties = ['HDZ','SDP','DP','Most','Možemo!','RF','Centar1','Centar2','Fokus','KH','HNS','IDS','HSS','HSU','HS','SD','Others','Undecided']
data22.columns = headers

data22 = data22[data22['HDZ'] != data22['Fokus']]
data22=data22.reset_index(drop=True)
data22['Date'] = data22.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

for z in parties:
  data22[z] = [p.sub('', x) for x in data22[z].astype(str)]
  data22[z] = [x.replace('–',str(np.NaN)) for x in data22[z]]
  data22[z] = [x.replace('-',str(np.NaN)) for x in data22[z]]
  # data22[z] = [x.replace(-,str(np.NaN)) for x in data22[z]]
  
for z in parties:
  data22[z] = data22[z].astype('float')

data22['Centar']=np.where(data22['Centar1'] != data22['Centar2'], data22['Centar1']+data22['Centar2'], data22['Centar1'])
data22 = data22.drop(["Centar1","Centar2"], axis=1)


headers = ['Date','HDZ','SDP','DP','Most','Možemo!','RF','Centar','Fokus','KH','HNS','IDS','HSS','HSU','HS','SD','Others','Undecided']
parties = ['HDZ','SDP','DP','Most','Možemo!','RF','Centar','Fokus','KH','HNS','IDS','HSS','HSU','HS','SD','Others','Undecided']
data22=data22.reindex(columns=headers)
data22.loc[len(data22.index)-1,['RF']] = np.NaN
data22.loc[len(data22.index)-2,['RF']] = np.NaN
data22.loc[len(data22.index)-1,['Fokus']] = np.NaN

data22.to_csv('Croatia/alternative/poll.csv', index=False)



data22['Undecided'].fillna(0, inplace=True)
data22['total']=data22[parties].sum(axis=1)

data22['decided']=data22['total']-data22['Undecided']

print(data22)
parties = ['HDZ','SDP','DP','Most','Možemo!','RF','Centar','Fokus','KH','HNS','IDS','HSS','HSU','HS','SD','Others']
data22[parties] = data22[parties].div(data22['decided'], axis=0)*100

data22 = data22.drop(["decided","total","Undecided"], axis=1)

data22.to_csv('Croatia/alternative/poll2.csv', index=False)
