import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Next_Irish_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

data22=pd.DataFrame(df[2])
data22=data22.drop(['Sample size','Polling firm / Commissioner','O/I[nb 1]'],axis=1)
headers = ['Date','SF','FF','FG','GP','Lab','SD','PBP-S','Aon']
parties = ['SF','FF','FG','GP','Lab','SD','PBP-S','Aon']
data22.columns = headers

data22.Date = data22.Date.apply(lambda x: dateparser.parse(x))
for z in parties:
  data22[z] = [x.replace('[nb 2]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[nb 3]','') for x in data22[z].astype(str)]
print(data22)

data22.to_csv('Irish_Elections/poll.csv', index=False)
