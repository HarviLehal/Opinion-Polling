import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

wikiurl="https://en.wikipedia.org/wiki/2023_Ceuta_Assembly_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

df0=pd.DataFrame(df[0])
data22 = df0.drop(["Polling firm/Commissioner", "Sample size", "Turnout", "Lead"], axis=1)
headers = ['Date', 'PP', 'PSOE', 'VOX', 'MDyC', 'Caballas', 'Cs', 'CY!' ,'CA']
parties = ['PP', 'PSOE', 'VOX', 'MDyC', 'Caballas', 'Cs', 'CY!' ,'CA']
data22.columns = headers
data22.drop(data22.index[[-1,-3,-4]],inplace=True)
data22['Date'] = [x.strip()[-11:] for x in data22['Date'].astype(str)]
data22['Date'] = [x.replace('–','') for x in data22['Date'].astype(str)]

for z in parties:
  data22[z] = [x.replace('?','0') for x in data22[z].astype(str)]
  data22[z] = [x.replace('–','0') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[a]','0') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[c]','0') for x in data22[z].astype(str)]
  data22[z] = data22[z].str.split(' ').str[0]


data22[parties] = data22[parties].astype(float)

print(data22)
data22.to_csv('Spanish_Elections/Ceuta/poll.csv', index=False)
