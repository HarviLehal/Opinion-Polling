import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/44th_Manitoba_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

def extract_latest_date(date_range):
    parts = date_range.split('–')
    start_date = parts[0].strip()
    end_date = parts[-1].strip()
    if any(char.isdigit() for char in end_date) and not any(char.isalpha() for char in end_date):
        month = ''.join(filter(str.isalpha, start_date))
        end_date = month + ' ' + end_date
    return end_date

headers = ['1','Date','2','NDP','PC','Libéral','Keystone','Vert','Autres','3','4','5','6']
parties = ['NPD','PC','Libéral','Keystone','Vert','Autres']
headers = ['1','Date','2','NDP','PC','Liberal','Keystone','Green','Others','3','4','5','6']
parties = ['NDP','PC','Liberal','Keystone','Green','Others']
drops = ['1','2','3','4','5','6']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])

  d[i]['Date2'] = [extract_latest_date(x) for x in d[i]['Date']]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['PC'])
  d[i] = d[i].dropna(subset=['Date'])

# d[0]['Date'].replace({pd.NaT: "0 days"}, inplace=True)



D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].str.strip('%')
  D[z] = pd.to_numeric(D[z], errors='coerce')

  

D.to_csv('Canada/Provincial/Manitoba/poll.csv', index=False)
