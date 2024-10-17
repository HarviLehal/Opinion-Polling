import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re
p = re.compile(r'\[[a-z]+\]')
headers = ['Date','2','3','Harris','Trump','4']
parties = ['Harris','Trump']
drops = ['2','3','4']
split_date = '21 July 2024'
split_date=dateparser.parse(split_date)

def extract_latest_date(date_range):
    parts = date_range.split('–')
    start_date = parts[0].strip()
    end_date = parts[-1].strip()
    if any(char.isdigit() for char in end_date) and not any(char.isalpha() for char in end_date):
        month = ''.join(filter(str.isalpha, start_date))
        end_date = month + ' ' + end_date
    return end_date

wikiurl="https://en.wikipedia.org/wiki/2024_United_States_presidential_election_in_Pennsylvania"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[4])
  d[i] = d[i][~d[i]['Poll source'].str.contains('(R)' ,na=False)]
  d[i] = d[i][~d[i]['Poll source'].str.contains('(D)' ,na=False)]
  d[i] = d[i].drop(["Poll source"], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = [extract_latest_date(x) for x in d[i]['Date']]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))


D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  D[z] = [x.replace('–',str(np.NaN)) for x in D[z]]
  D[z] = [x.replace('—',str(np.NaN)) for x in D[z]]
  D[z] = D[z].str.strip('%')
  D[z] = pd.to_numeric(D[z], errors='coerce')
D=D.dropna(subset=['Harris'])
D=D[(pd.to_datetime(D["Date"]) > split_date)]
D['total']=D[parties].sum(axis=1)
D['Harris'] = D['Harris']/D['total']
D['Trump'] = D['Trump']/D['total']
D = D.drop(['total'], axis=1)

D.to_csv('US/Presidential/States/PA.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/2024_United_States_presidential_election_in_Nevada"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[5])
  d[i] = d[i][~d[i]['Poll source'].str.contains('(R)' ,na=False)]
  d[i] = d[i][~d[i]['Poll source'].str.contains('(D)' ,na=False)]
  d[i] = d[i].drop(["Poll source"], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = [extract_latest_date(x) for x in d[i]['Date']]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))


D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  D[z] = [x.replace('–',str(np.NaN)) for x in D[z]]
  D[z] = [x.replace('—',str(np.NaN)) for x in D[z]]
  D[z] = D[z].str.strip('%')
  D[z] = pd.to_numeric(D[z], errors='coerce')
D=D.dropna(subset=['Harris'])
D=D[(pd.to_datetime(D["Date"]) > split_date)]
D['total']=D[parties].sum(axis=1)
D['Harris'] = D['Harris']/D['total']
D['Trump'] = D['Trump']/D['total']
D = D.drop(['total'], axis=1)

D.to_csv('US/Presidential/States/NV.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/2024_United_States_presidential_election_in_Wisconsin"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[4])
  d[i] = d[i][~d[i]['Poll source'].str.contains('(R)' ,na=False)]
  d[i] = d[i][~d[i]['Poll source'].str.contains('(D)' ,na=False)]
  d[i] = d[i].drop(["Poll source"], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = [extract_latest_date(x) for x in d[i]['Date']]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))


D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  D[z] = [x.replace('–',str(np.NaN)) for x in D[z]]
  D[z] = [x.replace('—',str(np.NaN)) for x in D[z]]
  D[z] = D[z].str.strip('%')
  D[z] = pd.to_numeric(D[z], errors='coerce')
D=D.dropna(subset=['Harris'])
D=D[(pd.to_datetime(D["Date"]) > split_date)]
D['total']=D[parties].sum(axis=1)
D['Harris'] = D['Harris']/D['total']
D['Trump'] = D['Trump']/D['total']
D = D.drop(['total'], axis=1)

D.to_csv('US/Presidential/States/WI.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/2024_United_States_presidential_election_in_Michigan"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[5])
  d[i] = d[i][~d[i]['Poll source'].str.contains('(R)' ,na=False)]
  d[i] = d[i][~d[i]['Poll source'].str.contains('(D)' ,na=False)]
  d[i] = d[i].drop(["Poll source"], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = [extract_latest_date(x) for x in d[i]['Date']]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))


D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  D[z] = [x.replace('–',str(np.NaN)) for x in D[z]]
  D[z] = [x.replace('—',str(np.NaN)) for x in D[z]]
  D[z] = D[z].str.strip('%')
  D[z] = pd.to_numeric(D[z], errors='coerce')
D=D.dropna(subset=['Harris'])
D=D[(pd.to_datetime(D["Date"]) > split_date)]
D['total']=D[parties].sum(axis=1)
D['Harris'] = D['Harris']/D['total']
D['Trump'] = D['Trump']/D['total']
D = D.drop(['total'], axis=1)

D.to_csv('US/Presidential/States/MI.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/2024_United_States_presidential_election_in_Georgia"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[4])
  d[i] = d[i][~d[i]['Poll source'].str.contains('(R)' ,na=False)]
  d[i] = d[i][~d[i]['Poll source'].str.contains('(D)' ,na=False)]
  d[i] = d[i].drop(["Poll source"], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = [extract_latest_date(x) for x in d[i]['Date']]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))


D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  D[z] = [x.replace('–',str(np.NaN)) for x in D[z]]
  D[z] = [x.replace('—',str(np.NaN)) for x in D[z]]
  D[z] = D[z].str.strip('%')
  D[z] = pd.to_numeric(D[z], errors='coerce')
D=D.dropna(subset=['Harris'])
D=D[(pd.to_datetime(D["Date"]) > split_date)]
D['total']=D[parties].sum(axis=1)
D['Harris'] = D['Harris']/D['total']
D['Trump'] = D['Trump']/D['total']
D = D.drop(['total'], axis=1)

D.to_csv('US/Presidential/States/GA.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/2024_United_States_presidential_election_in_North_Carolina"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
headers = ['Date','2','3','Trump','Harris','4']

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[5])
  d[i] = d[i][~d[i]['Poll source'].str.contains('(R)' ,na=False)]
  d[i] = d[i][~d[i]['Poll source'].str.contains('(D)' ,na=False)]
  d[i] = d[i].drop(["Poll source"], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = [extract_latest_date(x) for x in d[i]['Date']]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))


D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  D[z] = [x.replace('–',str(np.NaN)) for x in D[z]]
  D[z] = [x.replace('—',str(np.NaN)) for x in D[z]]
  D[z] = D[z].str.strip('%')
  D[z] = pd.to_numeric(D[z], errors='coerce')
D=D.dropna(subset=['Harris'])
D=D[(pd.to_datetime(D["Date"]) > split_date)]
D['total']=D[parties].sum(axis=1)
D['Harris'] = D['Harris']/D['total']
D['Trump'] = D['Trump']/D['total']
D = D.drop(['total'], axis=1)

D.to_csv('US/Presidential/States/NC.csv', index=False)

