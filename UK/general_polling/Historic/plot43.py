import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
from datetime import datetime
import numpy as np
import dateparser
import re

parties = ['Con','Lab','Lib Dem']
wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1945_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

df1 = pd.DataFrame(df[0])
df1.drop(['Pollster','Client','Lead'], axis=1, inplace=True)
df1.columns = ['Date','Con','Lab','Lib Dem']
df1.Date=df1.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
df1 = df1.drop(df1.index[-1])
for z in parties:
    df1[z] = [p.sub('', x) for x in df1[z].astype(str)]
    df1[z] = df1[z].str.strip('%')
    df1[z] = pd.to_numeric(df1[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1950_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(5):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster','Client','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Lab','Con','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1950-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

df2 = pd.concat(d.values(), ignore_index=True)
df2 = df2.drop(df2.index[-1])
for z in parties:
    df2[z] = [p.sub('', x) for x in df2[z].astype(str)]
    df2[z] = df2[z].str.strip('%')
    df2[z] = pd.to_numeric(df2[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1951_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(2):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster','Client','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Lab','Con','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1951-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

df3 = pd.concat(d.values(), ignore_index=True)
df3 = df3.drop(df3.index[-1])
for z in parties:
    df3[z] = [p.sub('', x) for x in df3[z].astype(str)]
    df3[z] = df3[z].str.strip('%')
    df3[z] = pd.to_numeric(df3[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1955_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(5):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster','Client','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Lab','Con','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1955-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

df4 = pd.concat(d.values(), ignore_index=True)
df4 = df4.drop(df4.index[-1])
for z in parties:
    df4[z] = [p.sub('', x) for x in df4[z].astype(str)]
    df4[z] = df4[z].str.strip('%')
    df4[z] = pd.to_numeric(df4[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1959_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(5):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Polling Organisation','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Con','Lab','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1959-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]


df5 = pd.concat(d.values(), ignore_index=True)
df5 = df5.drop(df5.index[-1])
for z in parties:
    df5[z] = [p.sub('', x) for x in df5[z].astype(str)]
    df5[z] = df5[z].str.strip('%')
    df5[z] = pd.to_numeric(df5[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1964_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(6):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Polling Organisation','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Con','Lab','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1964-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

df6 = pd.concat(d.values(), ignore_index=True)
df6 = df6.drop(df6.index[-1])#
for z in parties:
    df6[z] = [p.sub('', x) for x in df6[z].astype(str)]
    df6[z] = df6[z].str.strip('%')
    df6[z] = pd.to_numeric(df6[z], errors='coerce')


# wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1966_United_Kingdom_general_election"

# table_class="wikitable sortable jquery-tablesorter"
# response=requests.get(wikiurl)
# print(response.status_code)
# soup = BeautifulSoup(response.text, 'html.parser')
# tables = soup.find_all('table',class_="wikitable")
# df=pd.read_html(str(tables))

# d={}
# for i in range(6):
#     d[i]=pd.DataFrame(df[i])
#     d[i].drop(['Polling Organisation','Lead'], axis=1, inplace=True)
#     d[i].columns = ['Date','Con','Lab','Lib Dem']
#     d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
#     d[i].Date2.fillna(d[i].Date, inplace=True)
#     d[i]['Date2'] = [x+ str(1966-i) for x in d[i]['Date2'].astype(str)]
#     d[i]['Date'] = d[i]['Date2']
#     d[i] = d[i].drop(['Date2'], axis=1)
#     d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
#     d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

# df6 = pd.concat(d.values(), ignore_index=True)
# df6 = df6.drop(df6.index[-1])
# for z in parties:
#     df6[z] = [p.sub('', x) for x in df6[z].astype(str)]
#     df6[z] = df6[z].str.strip('%')
#     df6[z] = pd.to_numeric(df6[z], errors='coerce')

# wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1970_United_Kingdom_general_election"

# table_class="wikitable sortable jquery-tablesorter"
# response=requests.get(wikiurl)
# print(response.status_code)
# soup = BeautifulSoup(response.text, 'html.parser')
# tables = soup.find_all('table',class_="wikitable")
# df=pd.read_html(str(tables))

# d={}
# for i in range(3):
#     d[i]=pd.DataFrame(df[i])
#     d[i].drop(['Polling Organisation','Lead'], axis=1, inplace=True)
#     d[i].columns = ['Date','Con','Lab','Lib Dem']
#     d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
#     d[i].Date2.fillna(d[i].Date, inplace=True)
#     d[i]['Date2'] = [x+ str(1966-i) for x in d[i]['Date2'].astype(str)]
#     d[i]['Date'] = d[i]['Date2']
#     d[i] = d[i].drop(['Date2'], axis=1)
#     d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
#     d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

# df7 = pd.concat(d.values(), ignore_index=True)
# df7 = df7.drop(df7.index[-1])
# for z in parties:
#     df7[z] = [p.sub('', x) for x in df7[z].astype(str)]
#     df7[z] = df7[z].str.strip('%')
#     df7[z] = pd.to_numeric(df7[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1966_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(3):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Polling Organisation','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Lab','Con','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1966-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

df8 = pd.concat(d.values(), ignore_index=True)
df8 = df8.drop(df8.index[-1])
for z in parties:
    df8[z] = [p.sub('', x) for x in df8[z].astype(str)]
    df8[z] = df8[z].str.strip('%')
    df8[z] = pd.to_numeric(df8[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1970_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(5):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster','Client','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Lab','Con','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1970-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

df9 = pd.concat(d.values(), ignore_index=True)
df9 = df9.drop(df9.index[-1])
for z in parties:
    df9[z] = [p.sub('', x) for x in df9[z].astype(str)]
    df9[z] = df9[z].str.strip('%')
    df9[z] = pd.to_numeric(df9[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1974 United_Kingdom_general_elections"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(1):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster','Client','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Con','Lab','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1974-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

df10 = pd.concat(d.values(), ignore_index=True)
df10 = df10.drop(df10.index[-1])
for z in parties:
    df10[z] = [p.sub('', x) for x in df10[z].astype(str)]
    df10[z] = df10[z].str.strip('%')
    df10[z] = pd.to_numeric(df10[z], errors='coerce')

d={}
for i in range(5):
    d[i]=pd.DataFrame(df[i+1])
    d[i].drop(['Pollster','Client','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Con','Lab','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1974-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

df11 = pd.concat(d.values(), ignore_index=True)
df11 = df11.drop(df11.index[-1])
for z in parties:
    df11[z] = [p.sub('', x) for x in df11[z].astype(str)]
    df11[z] = df11[z].str.strip('%')
    df11[z] = pd.to_numeric(df11[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1979_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(6):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster','Client','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Lab','Con','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1979-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

df12 = pd.concat(d.values(), ignore_index=True)
df12 = df12.drop(df12.index[-1])
for z in parties:
    df12[z] = [p.sub('', x) for x in df12[z].astype(str)]
    df12[z] = df12[z].str.strip('%')
    df12[z] = pd.to_numeric(df12[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1983_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(5):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster','Client','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Con','Lab','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1983-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

df13 = pd.concat(d.values(), ignore_index=True)
df13 = df13.drop(df13.index[-1])
for z in parties:
    df13[z] = [p.sub('', x) for x in df13[z].astype(str)]
    df13[z] = df13[z].str.strip('%')
    df13[z] = pd.to_numeric(df13[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1987_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(5):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster','Client','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Con','Lab','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1987-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

df14 = pd.concat(d.values(), ignore_index=True)
df14 = df14.drop(df14.index[-1])
for z in parties:
    df14[z] = [p.sub('', x) for x in df14[z].astype(str)]
    df14[z] = df14[z].str.strip('%')
    df14[z] = pd.to_numeric(df14[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1992_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(6):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster','Client','Lead'], axis=1, inplace=True)
    if i == 0 or i == 1 or i == 5:
        d[i].columns = ['Date','Con','Lab','Lib Dem']
    else:
        d[i].columns = ['Date','Con','Lab','Lib Dem','SDP']
        d[i].drop(['SDP'], axis=1, inplace=True)
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1992-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]
    
df15 = pd.concat(d.values(), ignore_index=True)
df15 = df15.drop(df15.index[-1])
for z in parties:
    df15[z] = [p.sub('', x) for x in df15[z].astype(str)]
    df15[z] = df15[z].str.strip('%')
    df15[z] = pd.to_numeric(df15[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_1997_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(6):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster/Client','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Lab','Con','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(1997-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Lab'] != d[i]['Lib Dem']]

df16 = pd.concat(d.values(), ignore_index=True)
df16 = df16.drop(df16.index[-1])
for z in parties:
    df16[z] = [p.sub('', x) for x in df16[z].astype(str)]
    df16[z] = df16[z].str.strip('%')
    df16[z] = pd.to_numeric(df16[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2001_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(5):
    d[i]=pd.DataFrame(df[i+1])
    d[i].drop(['Pollster','Client','Sample size','Others','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Lab','Con','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(2001-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

df17 = pd.concat(d.values(), ignore_index=True)
df17 = df17.drop(df17.index[-1])
for z in parties:
    df17[z] = [p.sub('', x) for x in df17[z].astype(str)]
    df17[z] = df17[z].str.strip('%')
    df17[z] = pd.to_numeric(df17[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2005_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(5):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster','Client','Sample size','Others','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Lab','Con','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(2005-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Lab'] != d[i]['Lib Dem']]

df18 = pd.concat(d.values(), ignore_index=True)
df18 = df18.drop(df18.index[-1])
for z in parties:
    df18[z] = [p.sub('', x) for x in df18[z].astype(str)]
    df18[z] = df18[z].str.strip('%')
    df18[z] = pd.to_numeric(df18[z], errors='coerce')


wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2010_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(6):
    d[i]=pd.DataFrame(df[i])
    if i==4 or i==5:
        d[i].drop(['Polling Organisation / Client','Sample size','Others','Lead'], axis=1, inplace=True)
    else:
        d[i].drop(['Pollster','Client','Sample size','Others','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Lab','Con','Lib Dem']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(2010-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

df19 = pd.concat(d.values(), ignore_index=True)
df19 = df19.drop(df19.index[-1])
for z in parties:
  df19[z] = [p.sub('', x) for x in df19[z].astype(str)]
  df19[z] = df19[z].str.strip('%')
  df19[z] = pd.to_numeric(df19[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2015_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(6):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Polling organisation/client','Sample size','Others','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Con','Lab','Lib Dem','UKIP','Green']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(2015-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]

df20 = pd.concat(d.values(), ignore_index=True)
df20 = df20.drop(df20.index[-1])
parties = ['Con','Lab','Lib Dem','UKIP','Green']
for z in parties:
  df20[z] = [p.sub('', x) for x in df20[z].astype(str)]
  df20[z] = df20[z].str.strip('%')
  df20[z] = pd.to_numeric(df20[z], errors='coerce')
df20 = df20.drop(df20[(df20['Green'] > 6) & df20['UKIP'] == df20['Green']].index)

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2017_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(3):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Polling organisation/client','Sample size','Others','Lead'], axis=1, inplace=True)
    d[i].columns = ['Date','Con','Lab','UKIP','Lib Dem','SNP','Green']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(2017-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Lib Dem']]


df21 = pd.concat(d.values(), ignore_index=True)
df21 = df21.drop(df21.index[-1])
parties = ['Con','Lab','UKIP','Lib Dem','SNP','Green']
for z in parties:
  df21[z] = [p.sub('', x) for x in df21[z].astype(str)]
  df21[z] = df21[z].str.strip('%')
  df21[z] = pd.to_numeric(df21[z], errors='coerce')

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2019_United_Kingdom_general_election"

table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

d={}
for i in range(3):
    d[i]=pd.DataFrame(df[i])
    d[i].drop(['Pollster/client(s)','Area','Sample size','Other','Plaid Cymru','Lead'], axis=1, inplace=True)
    if i == 0:
        d[i].columns = ['Date','Con','Lab','Lib Dem','SNP','Green','Refrom','UKIP','Change UK']
    else:
        d[i].columns = ['Date','Con','Lab','Lib Dem','SNP','UKIP','Green']
    d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
    d[i].Date2.fillna(d[i].Date, inplace=True)
    d[i]['Date2'] = [x+ str(2019-i) for x in d[i]['Date2'].astype(str)]
    d[i]['Date'] = d[i]['Date2']
    d[i] = d[i].drop(['Date2'], axis=1)
    d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
    d[i] = d[i][d[i]['Con'] != d[i]['Green']]

df22 = pd.concat(d.values(), ignore_index=True)
df22 = df22.drop(df22.index[-1])
parties = ['Con','Lab','Lib Dem','SNP','Green','Refrom','UKIP','Change UK']
for z in parties:
    df22[z] = [p.sub('', x) for x in df22[z].astype(str)]
    df22[z] = df22[z].str.strip('%')
    df22[z] = pd.to_numeric(df22[z], errors='coerce')

# save each dataframe to a csv file
df1.to_csv('UK/general_polling/Historic/poll45.csv', index=False)
df2.to_csv('UK/general_polling/Historic/poll50.csv', index=False)
df3.to_csv('UK/general_polling/Historic/poll51.csv', index=False)
df4.to_csv('UK/general_polling/Historic/poll55.csv', index=False)
df5.to_csv('UK/general_polling/Historic/poll59.csv', index=False)
df6.to_csv('UK/general_polling/Historic/poll64.csv', index=False)
df8.to_csv('UK/general_polling/Historic/poll66.csv', index=False)
df9.to_csv('UK/general_polling/Historic/poll70.csv', index=False)
df10.to_csv('UK/general_polling/Historic/poll74.csv', index=False)
df11.to_csv('UK/general_polling/Historic/poll74_2.csv', index=False)
df12.to_csv('UK/general_polling/Historic/poll79.csv', index=False)
df13.to_csv('UK/general_polling/Historic/poll83.csv', index=False)
df14.to_csv('UK/general_polling/Historic/poll87.csv', index=False)
df15.to_csv('UK/general_polling/Historic/poll92.csv', index=False)
df16.to_csv('UK/general_polling/Historic/poll97.csv', index=False)
df17.to_csv('UK/general_polling/Historic/poll01.csv', index=False)
df18.to_csv('UK/general_polling/Historic/poll05.csv', index=False)
df19.to_csv('UK/general_polling/Historic/poll10.csv', index=False)
df20.to_csv('UK/general_polling/Historic/poll15.csv', index=False)
df21.to_csv('UK/general_polling/Historic/poll17.csv', index=False)
df22.to_csv('UK/general_polling/Historic/poll19.csv', index=False)
