import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_next_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

data2=pd.DataFrame(df[-2])
data2=data2.drop(["Pollster", "Sample size"], axis=1)

headers = ['Date','l1','l2','l3','c1','c2','c3','r1','r2','r3','d1','d2','d3','g1','g2','g3']
parties = ['l1','l2','c1','c2','r1','r2','d1','d2','g1','g2']
drops = ['l3','c3','r3','d3','g3']

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
  data2[z] = data2[z].astype(str)
  data2[z] = [x.replace('-',str(np.nan)) for x in data2[z]]
  data2[z] = [x.replace('—',str(np.nan)) for x in data2[z]]
  data2[z] = [x.replace('–',str(np.nan)) for x in data2[z]]
  data2[z] = [x.replace('TBC',str(np.nan)) for x in data2[z]]
  data2[z] = [x.replace('TBA',str(np.nan)) for x in data2[z]]
  data2[z] = [x.replace('?',str(np.nan)) for x in data2[z]]
  data2[z] = data2[z].astype(str)
  data2[z] = data2[z].str.strip('%')
  data2[z] = pd.to_numeric(data2[z], errors='coerce')
  data2[z] = data2[z].astype('float')

data2

data2 = data2.dropna(subset=['l1'])

# Separate approval-disapproval ratings by leader into separate tables

data_lab = data2[['Date','l1','l2']]
data_con = data2[['Date','c1','c2']]
data_ref = data2[['Date','r1','r2']]
data_lib = data2[['Date','d1','d2']]
data_grn = data2[['Date','g1','g2']]

# Rename columns
data_lab.columns = ['Date','Approval','Disapproval']
data_con.columns = ['Date','Approval','Disapproval']
data_ref.columns = ['Date','Approval','Disapproval']
data_lib.columns = ['Date','Approval','Disapproval']
data_grn.columns = ['Date','Approval','Disapproval']

# Calculate net approval in data2 and remove approval-disapproval columns
data= data2[['Date']]
data['Lab'] = (data_lab['Approval'] - data_lab['Disapproval'])/(data_lab['Approval'] + data_lab['Disapproval'])
data['Con'] = (data_con['Approval'] - data_con['Disapproval'])/(data_con['Approval'] + data_con['Disapproval'])
data['Ref'] = (data_ref['Approval'] - data_ref['Disapproval'])/(data_ref['Approval'] + data_ref['Disapproval'])
data['Lib Dem'] = (data_lib['Approval'] - data_lib['Disapproval'])/(data_lib['Approval'] + data_lib['Disapproval'])
data['Green'] = (data_grn['Approval'] - data_grn['Disapproval'])/(data_grn['Approval'] + data_grn['Disapproval'])

data


data.to_csv('UK/party_approval/net_approval.csv', index=False)



# Calculate net approval in data2 and remove approval-disapproval columns
data= data2[['Date']]
data['Lab'] = (100- data_lab['Approval'] - data_lab['Disapproval'])/100
data['Con'] = (100- data_con['Approval'] - data_con['Disapproval'])/100
data['Ref'] = (100- data_ref['Approval'] - data_ref['Disapproval'])/100
data['Lib Dem'] = (100- data_lib['Approval'] - data_lib['Disapproval'])/100
data['Green'] = (100- data_grn['Approval'] - data_grn['Disapproval'])/100

data


data.to_csv('UK/party_approval/net_approval2.csv', index=False)
