import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser
import re
wikiurl="https://en.wikipedia.org/wiki/2024_Lithuanian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

df0=pd.DataFrame(df[2])
data22 = df0.drop(["Pollster","Sample size","Lead"], axis=1)
headers = ['Date', 'TS–LKD', 'LVŽS', 'DP', 'LSDP', 'LP', 'LRLS', 'LLRA', 'LRP', 'LCP', 'LT', 'DSVL']
parties = ['TS–LKD', 'LVŽS', 'DP', 'LSDP', 'LP', 'LRLS', 'LLRA', 'LRP', 'LCP', 'LT', 'DSVL']
data22.columns = headers

for z in headers:
    data22[z] = [p.sub('', x) for x in data22[z].astype(str)]
# data22['Date'] = [x.replace('[a]','') for x in data22['Date'].astype(str)]
# data22['Date'] = [x.replace('[b]','') for x in data22['Date'].astype(str)]
# data22['Date'] = [x.replace('[c]','') for x in data22['Date'].astype(str)]
# data22['Date'] = [x.replace('[d]','') for x in data22['Date'].astype(str)]
# data22['Date'] = [x.replace('[e]','') for x in data22['Date'].astype(str)]
# data22['Date'] = [x.replace('[f]','') for x in data22['Date'].astype(str)]
data22['Date2'] = data22['Date'].str.split('–').str[1]
data22.Date2.fillna(data22['Date'].str.split('-').str[1], inplace=True)
data22.Date2.fillna(data22.Date, inplace=True)
data22.Date = data22.Date2
data22 = data22.drop(['Date2'],axis=1)
data22.Date = data22['Date'].astype(str)
data22.loc[len(data22.index)-1,['Date']] = '11 October 2020'
data22.Date = data22.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

# for z in parties:
#   data22[z] = [x.replace('–','0') for x in data22[z].astype(str)]



print(data22)
data22.to_csv('Lithuanian/poll.csv', index=False)
