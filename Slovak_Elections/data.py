import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Slovak_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

df0=pd.DataFrame(df[0])
data22 = df0.drop(["Polling firm", "Sample size", "Others", "DV","SNS","Others","ALI","Unnamed: 12_level_0","Unnamed: 21_level_0"], axis=1)
headers = ['Date', 'OĽaNO', 'SMER-SD', 'SR', 'ĽSNS', 'PS', 'SPOLU', 'SaS', 'ZĽ', 'KDH', 'HLAS-SD', 'REP']
parties = ['OĽaNO', 'SMER-SD', 'SR', 'ĽSNS', 'PS', 'SPOLU', 'SaS', 'ZĽ', 'KDH', 'HLAS-SD', 'REP']
data22.columns = headers
data22 = data22[data22['OĽaNO'] != data22['SMER-SD']]
data22['Date'] = [x.strip()[-11:] for x in data22['Date'].astype(str)]
data22['Date'] = [x.replace('–','') for x in data22['Date'].astype(str)]

data22.drop(data22.tail(5).index,inplace=True)
for z in parties:
  data22[z] = data22[z].str.split('%').str[0]
print(data22)
data22.to_csv('Slovak_Elections//poll.csv', index=False)
