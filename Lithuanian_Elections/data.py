import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

wikiurl="https://en.wikipedia.org/wiki/2024_Lithuanian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

df0=pd.DataFrame(df[2])
data22 = df0.drop(["Pollster","Sample size","Lead"], axis=1)
headers = ['Date', 'TS–LKD', 'LVŽS', 'DP', 'LSDP', 'LP', 'LRLS', 'LLRA', 'LRP', 'LCP', 'LT', 'DSVL']
parties = ['TS–LKD', 'LVŽS', 'DP', 'LSDP', 'LP', 'LRLS', 'LLRA', 'LRP', 'LCP', 'LT', 'DSVL']
data22.columns = headers

data22['Date'] = [x.replace('[a]','') for x in data22['Date'].astype(str)]
data22['Date'] = [x.replace('[b]','') for x in data22['Date'].astype(str)]
data22['Date'] = [x.strip()[-11:] for x in data22['Date'].astype(str)]
data22['Date'] = [x.replace('–','') for x in data22['Date'].astype(str)]
data22.loc[len(data22.index)-1,['Date']] = '11 Oct 2020'
data22['Date'] = data22.Date.apply(lambda x: dateparser.parse(x))

# for z in parties:
#   data22[z] = [x.replace('–','0') for x in data22[z].astype(str)]



print(data22)
data22.to_csv('Lithuanian_Elections/poll.csv', index=False)
