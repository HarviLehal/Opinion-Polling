import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

data2=pd.DataFrame(df[1])
data2=data2.drop(["Pollster", "Sample size"], axis=1)

headers = ['Date','s1','s2','s3','r1','r2','r3','f1','f2','f3','d1','d2','d3','c1','c2','c3','a1','a2','a3']
parties = ['s1','s2','r1','r2','f1','f2','d1','d2','c1','c2','a1','a2']
drops = ['s3','r3','f3','d3','c3','a3']

data2.columns = headers
data2=data2.drop(drops, axis=1)

data2['Date2'] = data2['Date'].str.split('–').str[1]
data2.Date2.fillna(data2['Date'].str.split('-').str[1], inplace=True)
data2.Date2.fillna(data2.Date, inplace=True)
# data2['Date2'] = [x+ str(2024-i) for x in data2['Date2'].astype(str)]
data2['Date'] = data2['Date2']
data2 = data2.drop(['Date2'], axis=1)
data2.Date=data2.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
for z in parties:
  data2[z] = [x.replace('-',str(np.NaN)) for x in data2[z]]
  data2[z] = [x.replace('—',str(np.NaN)) for x in data2[z]]
  data2[z] = [x.replace('–',str(np.NaN)) for x in data2[z]]
  data2[z] = [x.replace('TBC',str(np.NaN)) for x in data2[z]]
  data2[z] = [x.replace('TBA',str(np.NaN)) for x in data2[z]]
  data2[z] = [x.replace('?',str(np.NaN)) for x in data2[z]]
  data2[z] = data2[z].astype(str)
  data2[z] = data2[z].str.strip('%')
  data2[z] = data2[z].astype('float')

data2

# Separate approval-disapproval ratings by leader into separate tables

data_starmer = data2[['Date','s1','s2']]
data_sunak = data2[['Date','r1','r2']]
data_farage = data2[['Date','f1','f2']]
data_davey = data2[['Date','d1','d2']]
data_denyer = data2[['Date','c1','c2']]
data_adams = data2[['Date','a1','a2']]

# Rename columns
data_starmer.columns = ['Date','Approval','Disapproval']
data_sunak.columns = ['Date','Approval','Disapproval']
data_farage.columns = ['Date','Approval','Disapproval']
data_davey.columns = ['Date','Approval','Disapproval']
data_denyer.columns = ['Date','Approval','Disapproval']
data_adams.columns = ['Date','Approval','Disapproval']

# Calculate net approval in data2 and remove approval-disapproval columns
data= data2[['Date']]
data['Starmer'] = data_starmer['Approval'] - data_starmer['Disapproval']
data['Sunak'] = data_sunak['Approval'] - data_sunak['Disapproval']
data['Farage'] = data_farage['Approval'] - data_farage['Disapproval']
data['Davey'] = data_davey['Approval'] - data_davey['Disapproval']
data['Denyer'] = data_denyer['Approval'] - data_denyer['Disapproval']
data['Adams'] = data_adams['Approval'] - data_adams['Disapproval']

data

data.to_csv('UK/leadership_approval/net_approval.csv', index=False)
data_starmer.to_csv('UK/leadership_approval/starmer_approval.csv', index=False)
data_sunak.to_csv('UK/leadership_approval/sunak_approval.csv', index=False)
data_farage.to_csv('UK/leadership_approval/farage_approval.csv', index=False)
data_davey.to_csv('UK/leadership_approval/davey_approval.csv', index=False)
data_denyer.to_csv('UK/leadership_approval/denyer_approval.csv', index=False)
data_adams.to_csv('UK/leadership_approval/adams_approval.csv', index=False)
