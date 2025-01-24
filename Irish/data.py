import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Next_Irish_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z 0-9]+\]')

data22=pd.DataFrame(df[-1])
headers = ['Date','1','2','3','4','5','FF','FG','SF','SD','Lab','Aon','II','GP','PBP-S','Ind.']
parties = ['FF','FG','SF','SD','Lab','Aon','II','GP','PBP-S','Ind.']
drops = ['1','2','3','4','5']
data22.columns = headers
data22=data22.drop(drops,axis=1)
data22.Date = data22.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
for z in parties:
    data22[z] = [p.sub('', x) for x in data22[z].astype(str)]
    data22[z] = pd.to_numeric(data22[z], errors='coerce')

print(data22)

# data22.drop(data22.index[[1]],inplace=True)


data22.to_csv('Irish/poll.csv', index=False)
