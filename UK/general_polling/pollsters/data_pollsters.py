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
p = re.compile(r'\[[a-z 0-9]+\]')
# same as above but removes any text in brackets from the pollster column
q = re.compile(r'\(.*\)')

headers = ['Date','Pollster', 'Lab', 'Con', 'Reform', 'Lib Dem', 'Green', 'SNP', 'PC']
parties = ['Lab', 'Con', 'Reform', 'Lib Dem', 'Green', 'SNP', 'PC']
d = {}
for i in range(2):
  # i=j+1
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Client", "Area", "Others", "Lead", "Sample size"], axis=1)
  d[i].columns = headers
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.nan)) for x in d[i][z]]
  d[i]['Pollster'] = [p.sub('', x) for x in d[i]['Pollster'].astype(str)]
  d[i]['Pollster'] = [q.sub('', x) for x in d[i]['Pollster'].astype(str)]
  # d[i]['Pollster'] = d[i]['Pollster'].str.strip('(MRP)')
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Lab'] != d[i]['Green']]

D = pd.concat(d.values(), ignore_index=True)

for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
  
D.drop(D.index[[-1]],inplace=True)
D.loc[len(D.index)-1,['Date']] = '4 Jul 2024'
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

# rename all FindOutNow/ElectoralCalculus to FindOutNow only in the Pollster column
# D.loc[D['Pollster'].str.contains('Savanta ComRes'), 'Pollster'] = 'Savanta'
# remove all whitespace from the Pollster column
D['Pollster'] = D['Pollster'].str.replace(' ', '')
D.loc[D['Pollster'].str.contains('FindOutNowElectoralCalculus'), 'Pollster'] = 'FindOutNow'
D.loc[D['Pollster'].str.contains('MoreInCommon'), 'Pollster'] = 'MoreinCommon'

# Split D into a separate dataframe for each pollster
pollsters = D['Pollster'].unique()
dfs = {}
for pollster in pollsters:
    dfs[pollster] = D[D['Pollster'] == pollster]
    dfs[pollster] = dfs[pollster].sort_values(by='Date', ascending=False)
    dfs[pollster] = dfs[pollster].reset_index(drop=True)
    dfs[pollster] = dfs[pollster].drop(['Pollster'], axis=1)
  

# Save each pollster's dataframe as a csv file
for pollster in pollsters:
    dfs[pollster].to_csv(f'UK/general_polling/pollsters/polls_{pollster}.csv', index=False)
    
    
    
    
D = D[D['Pollster'] != 'FindOutNow']
D = D.drop(['Pollster'], axis=1)
D.to_csv('UK/general_polling/unbiased_polls.csv', index=False)

