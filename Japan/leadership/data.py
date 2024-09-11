# import pandas as pd # library for data analysis
# import requests # library to handle requests
# from bs4 import BeautifulSoup # library to parse HTML documents
# import numpy as np
# import dateparser
# import re
# 
# wikiurl="https://en.wikipedia.org/wiki/2024_Liberal_Democratic_Party_(Japan)_leadership_election"
# table_class="wikitable sortable jquery-tablesorter"
# response=requests.get(wikiurl)
# print(response.status_code)
# soup = BeautifulSoup(response.text, 'html.parser')
# tables = soup.find_all('table',class_="wikitable")
# df=pd.read_html(str(tables))
# p = re.compile(r'\[[a-z]+\]')
# 
# headers = ['Date','Ishiba','Koizumi','Kono','Takaichi','Suga','Kamikawa','Kishida*','Noda','Motegi','Other','Undecided']
# parties = ['Ishiba','Koizumi','Kono','Takaichi','Suga','Kamikawa','Kishida*','Noda','Motegi','Other','Undecided']
# d = {}
# 
# for i in range(1):
#   d[i]=pd.DataFrame(df[-2])
#   d[i]=d[i].drop(["Sample size[vague]","Polling firm"], axis=1)
#   d[i].columns = headers
#   d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
#   d[i].Date2.fillna(d[i].Date, inplace=True)
#   d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
#   d[i]['Date'] = d[i]['Date2']
#   d[i] = d[i].drop(['Date2'], axis=1)
#   d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
#   d[i] = d[i][d[i]['Kishida*'] != d[i]['Undecided']]
#   # d[i] = d[i][d[i]['Approve'] == d[i]['Undecided']]
#   for z in parties:
#     d[i][z] = d[i][z].astype('string')
#   for z in parties:
#     d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
#     d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
#     d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
#   for z in parties:
#     d[i][z] = d[i][z].astype('float')
# 
# 
# 
# D = pd.concat(d.values(), ignore_index=True)
# 
# 
# D.to_csv('Japan/leadership/poll.csv', index=False)
# 
# 
# 
# D['Undecided'].fillna(0, inplace=True)
# D['total']=D[parties].sum(axis=1)
# 
# D['decided']=D['total']-D['Undecided']
# 
# print(D)
# parties = ['Ishiba','Koizumi','Kono','Takaichi','Suga','Kamikawa','Kishida*','Noda','Motegi','Other']
# D[parties] = D[parties].div(D['decided'], axis=0)*100
# 
# D = D.drop(["decided","total","Undecided"], axis=1)
# 
# D.to_csv('Japan/leadership/poll2.csv', index=False)
# 
# 
# 
# 
# 










import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2024_Liberal_Democratic_Party_(Japan)_leadership_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','Ishiba','Koizumi','Kono','Takaichi','Kamikawa','Kobayashi','Motegi','Hayashi','Kato','Aoyama','Other','Undecided']
parties = ['Ishiba','Koizumi','Kono','Takaichi','Kamikawa','Kobayashi','Motegi','Hayashi','Kato','Aoyama','Other','Undecided']
d = {}

for i in range(1):
  d[i]=pd.DataFrame(df[-3])
  d[i]=d[i].drop(["Sample size[vague]","Polling firm"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Ishiba'] != d[i]['Other']]
  # d[i] = d[i][d[i]['Approve'] == d[i]['Undecided']]
  for z in parties:
    d[i][z] = d[i][z].astype('string')
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
  for z in parties:
    d[i][z] = d[i][z].astype('float')



D = pd.concat(d.values(), ignore_index=True)


D.to_csv('Japan/leadership/poll_new.csv', index=False)



D['Undecided'].fillna(0, inplace=True)
D['total']=D[parties].sum(axis=1)

D['decided']=D['total']-D['Undecided']

print(D)
parties = ['Ishiba','Koizumi','Kono','Takaichi','Kamikawa','Kobayashi','Motegi','Hayashi','Kato','Aoyama','Other']
D[parties] = D[parties].div(D['decided'], axis=0)*100

D = D.drop(["decided","total","Undecided"], axis=1)

D.to_csv('Japan/leadership/poll2_new.csv', index=False)

