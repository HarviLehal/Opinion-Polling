import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2025_German_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(5):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j][0])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[0,2,3,-1]],axis=1)
  parties = heads[4:-1]
  if "FW" in heads:
    d[i].drop(["FW"], axis=1)
    parties.remove("FW")
  d[i].rename(columns={d[i].columns[0]: "Date" }, inplace = True)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  if i < 4:
    d[i].drop(d[i].index[[-1]],inplace=True)
  
D = pd.concat(d.values(), ignore_index=True)
D.to_csv('German/Federal/Historic/poll_25.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2021_German_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(5):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j][0])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[0,2,3,-1]],axis=1)
  parties = heads[4:-1]
  if "FW" in heads:
    d[i].drop(["FW"], axis=1)
    parties.remove("FW")
  d[i].rename(columns={d[i].columns[0]: "Date" }, inplace = True)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  if i < 4:
    d[i].drop(d[i].index[[-1]],inplace=True)
  
D = pd.concat(d.values(), ignore_index=True)
D.to_csv('German/Federal/Historic/poll_21.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2017_German_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(5):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j][0])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  if i == 2:
    d[i]=d[i].drop(d[i].columns[[0,-1]],axis=1)
    parties = heads[2:-1]
  elif i<2:
    d[i]=d[i].drop(d[i].columns[[0,2,3,-1]],axis=1)
    parties = heads[4:-1]
  else:
    d[i]=d[i].drop(d[i].columns[[0,2,-1]],axis=1)
    parties = heads[3:-1]
  d[i].rename(columns={d[i].columns[0]: "Date" }, inplace = True)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  if i < 4:
    d[i].drop(d[i].index[[-1]],inplace=True)
  
D = pd.concat(d.values(), ignore_index=True)
D.to_csv('German/Federal/Historic/poll_17.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2013_German_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(5):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j][0])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1]],axis=1)
  parties = heads[2:-1]
  d[i].rename(columns={d[i].columns[0]: "Date" }, inplace = True)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D = pd.concat(d.values(), ignore_index=True)
D.to_csv('German/Federal/Historic/poll_13.csv', index=False)


# 2009



wikiurl = "https://www.wahlrecht.de/umfragen/allensbach/2009.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3]],axis=1)
  parties = heads[1:-3]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D0 = pd.concat(d.values(), ignore_index=True)


wikiurl = "https://www.wahlrecht.de/umfragen/gms/projektion-2009.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3]],axis=1)
  parties = heads[1:-3]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D1 = pd.concat(d.values(), ignore_index=True)


wikiurl = "https://www.wahlrecht.de/umfragen/emnid/2013.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3,-5,-6]],axis=1)
  parties = heads[2:7]+[heads[-4]]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D = pd.concat(d.values(), ignore_index=True)

split_date = '28 September 2009'
split_date=dateparser.parse(split_date)
D2=D[(pd.to_datetime(D["Date"]) < split_date)]


wikiurl = "https://www.wahlrecht.de/umfragen/forsa/2013.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3,-5,-6]],axis=1)
  parties = heads[2:7]+[heads[-4]]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D = pd.concat(d.values(), ignore_index=True)

split_date = '28 September 2009'
split_date=dateparser.parse(split_date)
D3=D[(pd.to_datetime(D["Date"]) < split_date)]


wikiurl = "https://www.wahlrecht.de/umfragen/dimap/2013.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3,-5,-6]],axis=1)
  parties = heads[2:7]+[heads[-4]]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D = pd.concat(d.values(), ignore_index=True)

split_date = '28 September 2009'
split_date=dateparser.parse(split_date)
D4=D[(pd.to_datetime(D["Date"]) < split_date)]


p = re.compile(r'\[[a-z]+\]')
base_url = "https://www.wahlrecht.de/umfragen/emnid/{}.htm"
start_year = 2008
end_year = 2005  # change as needed

dfs = {}
var_counter = 5

for year in range(start_year, end_year - 1, -1):
    url = base_url.format(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table', class_="wilko")
    df_list = pd.read_html(str(tables))
    
    df = pd.DataFrame(df_list[0])
    heads = list(df.columns)
    df = df.drop(df.columns[[1, -1, -2, -3]], axis=1)
    parties = heads[1:-3]
    
    df.rename(columns={
        df.columns[0]: "Date",
        df.columns[1]: "Union",
        df.columns[3]: "Grüne",
        df.columns[5]: "Linke",
        df.columns[-1]: "Others"
    }, inplace=True)
    
    df['Date'] = df['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).apply(lambda x: p.sub('', x)).str.replace('%','').str.replace(',','.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Date'])
    if 'SPD' in df.columns:
        df = df.dropna(subset=['SPD'])
    
    dfs[f'D{var_counter}'] = df
    var_counter += 1

D5, D6, D7, D8 = dfs['D5'], dfs['D6'], dfs['D7'], dfs['D8']


p = re.compile(r'\[[a-z]+\]')
base_url = "https://www.wahlrecht.de/umfragen/forsa/{}.htm"
start_year = 2008
end_year = 2005  # change as needed

dfs = {}
var_counter = 9

for year in range(start_year, end_year - 1, -1):
    url = base_url.format(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table', class_="wilko")
    df_list = pd.read_html(str(tables))
    
    df = pd.DataFrame(df_list[0])
    heads = list(df.columns)
    df = df.drop(df.columns[[1, -1, -2, -3]], axis=1)
    parties = heads[1:-3]
    
    df.rename(columns={
        df.columns[0]: "Date",
        df.columns[1]: "Union",
        df.columns[3]: "Grüne",
        df.columns[5]: "Linke",
        df.columns[-1]: "Others"
    }, inplace=True)
    
    df['Date'] = df['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).apply(lambda x: p.sub('', x)).str.replace('%','').str.replace(',','.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Date'])
    if 'SPD' in df.columns:
        df = df.dropna(subset=['SPD'])
    
    dfs[f'D{var_counter}'] = df
    var_counter += 1

D9, D10, D11, D12 = dfs['D9'], dfs['D10'], dfs['D11'], dfs['D12']


p = re.compile(r'\[[a-z]+\]')
base_url = "https://www.wahlrecht.de/umfragen/dimap/{}.htm"
start_year = 2008
end_year = 2005  # change as needed

dfs = {}
var_counter = 13

for year in range(start_year, end_year - 1, -1):
    url = base_url.format(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table', class_="wilko")
    df_list = pd.read_html(str(tables))
    
    df = pd.DataFrame(df_list[0])
    heads = list(df.columns)
    df = df.drop(df.columns[[1, -1, -2, -3]], axis=1)
    parties = heads[1:-3]
    
    df.rename(columns={
        df.columns[0]: "Date",
        df.columns[1]: "Union",
        df.columns[3]: "Grüne",
        df.columns[5]: "Linke",
        df.columns[-1]: "Others"
    }, inplace=True)
    
    df['Date'] = df['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).apply(lambda x: p.sub('', x)).str.replace('%','').str.replace(',','.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Date'])
    if 'SPD' in df.columns:
        df = df.dropna(subset=['SPD'])
    
    dfs[f'D{var_counter}'] = df
    var_counter += 1

D13, D14, D15, D16 = dfs['D13'], dfs['D14'], dfs['D15'], dfs['D16']


wikiurl = "https://www.wahlrecht.de/umfragen/politbarometer/politbarometer-2009.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3]],axis=1)
  parties = heads[1:-3]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D17 = pd.concat(d.values(), ignore_index=True)

dfs_to_concat = [globals()[f'D{i}'] for i in range(18) if f'D{i}' in globals()]
D_all = pd.concat(dfs_to_concat, ignore_index=True)

split_date = '28 September 2009'
split_date=dateparser.parse(split_date)
D_all=D_all[(pd.to_datetime(D_all["Date"]) < split_date)]
split_date = '17 September 2005'
split_date=dateparser.parse(split_date)
D_all=D_all[(pd.to_datetime(D_all["Date"]) > split_date)]


D_all.to_csv('German/Federal/Historic/poll_09.csv', index=False)


# 2005

wikiurl = "https://www.wahlrecht.de/umfragen/allensbach/2005.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3]],axis=1)
  parties = heads[1:-3]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D0 = pd.concat(d.values(), ignore_index=True)

wikiurl = "https://www.wahlrecht.de/umfragen/politbarometer/politbarometer-2005.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3]],axis=1)
  parties = heads[1:-3]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D1 = pd.concat(d.values(), ignore_index=True)

wikiurl = "https://www.wahlrecht.de/umfragen/gms/projektion-2009.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3]],axis=1)
  parties = heads[1:-3]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D2 = pd.concat(d.values(), ignore_index=True)


p = re.compile(r'\[[a-z]+\]')
base_url = "https://www.wahlrecht.de/umfragen/emnid/{}.htm"
start_year = 2005
end_year = 2002  # change as needed

dfs = {}
var_counter = 3

for year in range(start_year, end_year - 1, -1):
    url = base_url.format(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table', class_="wilko")
    df_list = pd.read_html(str(tables))
    
    df = pd.DataFrame(df_list[0])
    heads = list(df.columns)
    df = df.drop(df.columns[[1, -1, -2, -3]], axis=1)
    parties = heads[1:-3]
    
    df.rename(columns={
        df.columns[0]: "Date",
        df.columns[1]: "Union",
        df.columns[3]: "Grüne",
        df.columns[5]: "Linke",
        df.columns[-1]: "Others"
    }, inplace=True)
    
    df['Date'] = df['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).apply(lambda x: p.sub('', x)).str.replace('%','').str.replace(',','.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Date'])
    if 'SPD' in df.columns:
        df = df.dropna(subset=['SPD'])
    
    dfs[f'D{var_counter}'] = df
    var_counter += 1

D3, D4, D5, D6 = dfs['D3'], dfs['D4'], dfs['D5'], dfs['D6']


p = re.compile(r'\[[a-z]+\]')
base_url = "https://www.wahlrecht.de/umfragen/forsa/{}.htm"
start_year = 2005
end_year = 2002  # change as needed

dfs = {}
var_counter = 7

for year in range(start_year, end_year - 1, -1):
    url = base_url.format(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table', class_="wilko")
    df_list = pd.read_html(str(tables))
    
    df = pd.DataFrame(df_list[0])
    heads = list(df.columns)
    df = df.drop(df.columns[[1, -1, -2, -3]], axis=1)
    parties = heads[1:-3]
    
    df.rename(columns={
        df.columns[0]: "Date",
        df.columns[1]: "Union",
        df.columns[3]: "Grüne",
        df.columns[5]: "Linke",
        df.columns[-1]: "Others"
    }, inplace=True)
    
    df['Date'] = df['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).apply(lambda x: p.sub('', x)).str.replace('%','').str.replace(',','.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Date'])
    if 'SPD' in df.columns:
        df = df.dropna(subset=['SPD'])
    
    dfs[f'D{var_counter}'] = df
    var_counter += 1

D7, D8, D9, D10 = dfs['D7'], dfs['D8'], dfs['D9'], dfs['D10']


p = re.compile(r'\[[a-z]+\]')
base_url = "https://www.wahlrecht.de/umfragen/dimap/{}.htm"
start_year = 2005
end_year = 2002  # change as needed

dfs = {}
var_counter = 11

for year in range(start_year, end_year - 1, -1):
    url = base_url.format(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table', class_="wilko")
    df_list = pd.read_html(str(tables))
    
    df = pd.DataFrame(df_list[0])
    heads = list(df.columns)
    df = df.drop(df.columns[[1, -1, -2, -3]], axis=1)
    parties = heads[1:-3]
    
    df.rename(columns={
        df.columns[0]: "Date",
        df.columns[1]: "Union",
        df.columns[3]: "Grüne",
        df.columns[5]: "Linke",
        df.columns[-1]: "Others"
    }, inplace=True)
    
    df['Date'] = df['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).apply(lambda x: p.sub('', x)).str.replace('%','').str.replace(',','.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Date'])
    if 'SPD' in df.columns:
        df = df.dropna(subset=['SPD'])
    
    dfs[f'D{var_counter}'] = df
    var_counter += 1

D11, D12, D13, D14 = dfs['D11'], dfs['D12'], dfs['D13'], dfs['D14']


dfs_to_concat = [globals()[f'D{i}'] for i in range(15) if f'D{i}' in globals()]
D_all = pd.concat(dfs_to_concat, ignore_index=True)

split_date = '19 September 2005'
split_date=dateparser.parse(split_date)
D_all=D_all[(pd.to_datetime(D_all["Date"]) < split_date)]
split_date = '21 September 2002'
split_date=dateparser.parse(split_date)
D_all=D_all[(pd.to_datetime(D_all["Date"]) > split_date)]
D_all.to_csv('German/Federal/Historic/poll_05.csv', index=False)



# 2002

wikiurl = "https://www.wahlrecht.de/umfragen/allensbach/2002.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3,-5]],axis=1)
  parties = heads[1:-5] +[heads[-4]]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D0 = pd.concat(d.values(), ignore_index=True)


wikiurl = "https://www.wahlrecht.de/umfragen/politbarometer/politbarometer-2002.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3]],axis=1)
  parties = heads[1:-3]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D1 = pd.concat(d.values(), ignore_index=True)


p = re.compile(r'\[[a-z]+\]')
base_url = "https://www.wahlrecht.de/umfragen/emnid/{}.htm"
start_year = 2002
end_year = 1998  # change as needed

dfs = {}
var_counter = 2

for year in range(start_year, end_year - 1, -1):
    url = base_url.format(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table', class_="wilko")
    df_list = pd.read_html(str(tables))
    
    df = pd.DataFrame(df_list[0])
    heads = list(df.columns)
    if year < 2000:
      df = df.drop(df.columns[[1, -2]], axis=1)
      parties = heads[1:-2] + [heads[-1]]
    else:
      df = df.drop(df.columns[[1, -1, -2, -3]], axis=1)
      parties = heads[1:-3]
    df.rename(columns={
        df.columns[0]: "Date",
        df.columns[1]: "Union",
        df.columns[3]: "Grüne",
        df.columns[-2]: "Linke",
        df.columns[-1]: "Others"
    }, inplace=True)
    
    df['Date'] = df['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).apply(lambda x: p.sub('', x)).str.replace('%','').str.replace(',','.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Date'])
    if 'SPD' in df.columns:
        df = df.dropna(subset=['SPD'])
    
    dfs[f'D{var_counter}'] = df
    var_counter += 1

D2, D3, D4, D5, D6= dfs['D2'], dfs['D3'], dfs['D4'], dfs['D5'], dfs['D6']


p = re.compile(r'\[[a-z]+\]')
base_url = "https://www.wahlrecht.de/umfragen/forsa/{}.htm"
start_year = 2002
end_year = 1998  # change as needed

dfs = {}
var_counter = 7

for year in range(start_year, end_year - 1, -1):
    url = base_url.format(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table', class_="wilko")
    df_list = pd.read_html(str(tables))
    
    df = pd.DataFrame(df_list[0])
    heads = list(df.columns)
    if year == 2002:
      df = df.drop(df.columns[[1, -1, -2, -3]], axis=1)
      parties = heads[1:-3]
    elif year == 1998:
      df = df.drop(df.columns[[1, -2]], axis=1)
      parties = heads[1:-2] + [heads[-1]]
    else:
      df = df.drop(df.columns[[1]], axis=1)
      parties = heads[1:]
    df.rename(columns={
        df.columns[0]: "Date",
        df.columns[1]: "Union",
        df.columns[3]: "Grüne",
        df.columns[-2]: "Linke",
        df.columns[-1]: "Others"
    }, inplace=True)
    
    df['Date'] = df['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).apply(lambda x: p.sub('', x)).str.replace('%','').str.replace(',','.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Date'])
    if 'SPD' in df.columns:
        df = df.dropna(subset=['SPD'])
    
    dfs[f'D{var_counter}'] = df
    var_counter += 1

D7, D8, D9, D10, D11= dfs['D7'], dfs['D8'], dfs['D9'], dfs['D10'], dfs['D11']


p = re.compile(r'\[[a-z]+\]')
base_url = "https://www.wahlrecht.de/umfragen/dimap/{}.htm"
start_year = 2002
end_year = 1998  # change as needed

dfs = {}
var_counter = 12

for year in range(start_year, end_year - 1, -1):
    url = base_url.format(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table', class_="wilko")
    df_list = pd.read_html(str(tables))
    
    df = pd.DataFrame(df_list[0])
    heads = list(df.columns)
    if year < 2000:
      df = df.drop(df.columns[[1, -2]], axis=1)
      parties = heads[1:-2] + [heads[-1]]
    else:
      df = df.drop(df.columns[[1, -1, -2, -3]], axis=1)
      parties = heads[1:-3]
    df.rename(columns={
        df.columns[0]: "Date",
        df.columns[1]: "Union",
        df.columns[3]: "Grüne",
        df.columns[-2]: "Linke",
        df.columns[-1]: "Others"
    }, inplace=True)
    
    df['Date'] = df['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).apply(lambda x: p.sub('', x)).str.replace('%','').str.replace(',','.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Date'])
    if 'SPD' in df.columns:
        df = df.dropna(subset=['SPD'])
    
    dfs[f'D{var_counter}'] = df
    var_counter += 1

D12, D13, D14, D15, D16= dfs['D12'], dfs['D13'], dfs['D14'], dfs['D15'], dfs['D16']


dfs_to_concat = [globals()[f'D{i}'] for i in range(17) if f'D{i}' in globals()]
D_all = pd.concat(dfs_to_concat, ignore_index=True)

split_date = '23 September 2002'
split_date=dateparser.parse(split_date)
D_all=D_all[(pd.to_datetime(D_all["Date"]) < split_date)]
split_date = '26 September 1998'
split_date=dateparser.parse(split_date)
D_all=D_all[(pd.to_datetime(D_all["Date"]) > split_date)]
D_all.to_csv('German/Federal/Historic/poll_02.csv', index=False)


# 1998




wikiurl = "https://www.wahlrecht.de/umfragen/politbarometer/politbarometer-1998.htm"
table_class = "wilko"
response = requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_="wilko")
df = pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i]=d[i].drop(d[i].columns[[1,-1,-2,-3]],axis=1)
  parties = heads[1:-3]
  d[i].rename(columns={d[i].columns[0]: "Date" ,d[i].columns[1]: "Union",d[i].columns[3]:"Grüne",d[i].columns[5]:"Linke",d[i].columns[-1]: "Others" }, inplace = True)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date'] = d[i]['Date'].astype(str).apply(lambda x: dateparser.parse(x, settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}))
  for z in d[i].columns[1:]:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z]]
    d[i][z] = [x.replace(',','.') for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['SPD'])
  
D = pd.concat(d.values(), ignore_index=True)
D.to_csv('German/Federal/Historic/poll_98.csv', index=False)
