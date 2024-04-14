wikiurl="https://en.wikipedia.org/wiki/2023_Bulgarian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['drop1','Date','drop2','GERB','PP','DB','DPS','V','BSP','BV','drop3','ITN','Levitsata','drop4','Other','drop5','drop6']
parties = ['GERB','PP','DB','DPS','V','BSP','BV','ITN','Levitsata','Other']
drops = ['drop1','drop2','drop3','drop4','drop5','drop6']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-4])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['GERB'] != d[i]['Levitsata']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]
    
D = pd.concat(d.values(), ignore_index=True)
D[parties] = D[parties].astype(float)

D['PP-DB']=np.where(D['PP']==D['DB'],D['PP'],np.NaN)
D['PP']=np.where(D['PP']==D['DB'],np.NaN,D['PP'])
D['DB']=np.where(D['DB']>10,np.NaN,D['DB'])

D=D[['Date','GERB','PP-DB','PP','DB','DPS','V','BSP','BV','ITN','Levitsata','Other']]
D
D.to_csv('Bulgaria/poll2.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/2022_Bulgarian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['drop1','Date','drop2','PP','DB','GERB','DPS','BSP','ITN','V','Levitsata','drop3','BV','Other','drop4','drop5']
parties = ['GERB','PP','DB','DPS','V','BSP','BV','ITN','Levitsata','Other']
drops = ['drop1','drop2','drop3','drop4','drop5']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-4])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['GERB'] != d[i]['Levitsata']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]
    
D = pd.concat(d.values(), ignore_index=True)
D[parties] = D[parties].astype(float)
D = D[D.Date.notnull()]
D
D.to_csv('Bulgaria/poll3.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/2021_Bulgarian_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['drop1','Date','drop2','drop3','drop4','ITN','GERB','BSP','DB','DPS','ISMV','drop5','V','PP','Other','drop6','drop7']
parties = ['ITN','GERB','BSP','DB','DPS','ISMV','V','PP','Other']
drops = ['drop1','drop2','drop3','drop4','drop5','drop6','drop7']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-8])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('−').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['GERB'] != d[i]['ISMV']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]
    
D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
D = D[D.Date.notnull()]
D
D.to_csv('Bulgaria/poll4.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/July_2021_Bulgarian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['drop1','Date','drop2','GERB','ITN','BSP','DPS','DB','ISMV','drop3','drop4','drop5','V','drop6','drop7','drop8','Other','drop9']
parties = ['GERB','ITN','BSP','DPS','DB','ISMV','V','Other']
drops = ['drop1','drop2','drop3','drop4','drop5','drop6','drop7','drop8','drop9']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-3])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('−').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['GERB'] != d[i]['ISMV']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]
    
D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
D = D[D.Date.notnull()]
D
D.to_csv('Bulgaria/poll5.csv', index=False)



wikiurl="https://en.wikipedia.org/wiki/April_2021_Bulgarian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['drop1','Date','drop2','drop3','GERB','BSP','DPS','OP','DB','drop4','ITN','ISMV','Other','drop5']
parties = ['GERB','BSP','DPS','OP','DB','ITN','ISMV','Other']
drops = ['drop1','drop2','drop3','drop4','drop5']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-4])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('−').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['GERB'] != d[i]['ISMV']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]
    
D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
D = D[D.Date.notnull()]
D
D.to_csv('Bulgaria/poll6.csv', index=False)
