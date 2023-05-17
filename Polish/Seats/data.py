import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Polish_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

df6=pd.DataFrame(df[9])
data23 = df6.drop(["Polling Firm/Link", "Sample Size", "Majority"], axis=1)
headers = ['Date','United Right','Civic Coalition','The Left','Polish Coalition','Poland 2050','Confederation','Others']
parties = ['United Right','Civic Coalition','The Left','Polish Coalition','Poland 2050','Confederation','Others']
threeway = ['Polish Coalition','Poland 2050']
data23.columns = headers
print(data23)
data23[parties] = data23[parties].astype(float)
data23['Third Way']=np.where(data23['Polish Coalition']<40, data23['Polish Coalition']+data23['Poland 2050'], data23['Polish Coalition'])
data23=data23.drop(threeway, axis=1)

df7=pd.DataFrame(df[10])
data22 = df7.drop(["Polling Firm/Link", "Sample Size", "Majority", "Kukiz'15"], axis=1)
headers = ['Date', 'United Right', 'Civic Coalition', 'The Left', 'Polish Coalition', 'Confederation', 'Poland 2050', 'Others']
parties = ['United Right', 'Civic Coalition', 'The Left', 'Polish Coalition', 'Confederation', 'Poland 2050', 'Others']
data22.columns = headers
data22.drop(data22.tail(1).index,inplace=True)
print(data22)

df8=pd.DataFrame(df[11])
data21 = df8.drop(["Polling Firm/Link", "Sample Size", "Majority"], axis=1)
data21.columns = headers
data21.drop(data21.index[[-1,-3]],inplace=True)
print(data21)

# df.drop(df.columns[-1], axis=1, inplace=True)


data = pd.concat([data23,data22,data21])
p = re.compile(r'\[[a-z]+\]')
for z in parties:
        data[z] = [p.sub('', x) for x in data[z].astype(str)]
        data[z] = data[z].astype('float').astype(str)
data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))



print(data)
data.to_csv('Polish/Seats/poll.csv', index=False)

UO = ['Civic Coalition', 'The Left', 'Polish Coalition', 'Poland 2050', 'Third Way']
R = ['United Right', 'Confederation']

data[parties] = data[parties].astype(float)
data['United Opposition (KO + Lewica + PSL + PL2050'] = data[UO].sum(axis=1)
data['Right Wing (PiS + Konfederacja)'] = data[R].sum(axis=1)
data = data.drop(UO + R, axis=1)

data.to_csv('Polish/Seats/poll2.csv', index=False)
