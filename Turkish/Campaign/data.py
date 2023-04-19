import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Turkish_presidential_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

# 2023 POLLS

df0=pd.DataFrame(df[0])
data = df0.drop(['Polling firm','Published by','Sample size', 'Others','Lead'], axis=1)
headers = ['Date', 'Erdoğan', 'Kılıçdaroğlu', 'Oğan', 'İnce']
parties = ['Erdoğan', 'Kılıçdaroğlu', 'Oğan', 'İnce']
data.columns = headers
data = data[data['Erdoğan'] != data['İnce']]
data['Date2'] = data['Date'].str.split('-').str[1]
data.Date2.fillna(data.Date, inplace=True)
data['Date2'] = [x+' 2023' for x in data['Date2'].astype(str)]
data['Date'] = data['Date2']
data = data.drop(['Date2'], axis=1)

print(data)


data.Date = data.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
print(data)
data.to_csv('Turkish/Campaign/poll.csv', index=False)
