import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Next_Thuringian_state_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

df0=pd.DataFrame(df[1])
data22 = df0.drop(["Polling firm", "Sample size","Lead"], axis=1)
headers = ['Date', 'Linke', 'AfD', 'CDU', 'SPD', 'Grüne', 'FDP','Wag','Others']
parties = ['Linke', 'AfD', 'CDU', 'SPD', 'Grüne', 'FDP','Wag','Others']
data22.columns = headers
data22['Date'] = [x.strip()[-11:] for x in data22['Date'].astype(str)]
data22['Date'] = [x.replace('–','') for x in data22['Date'].astype(str)]
data22=data22[~data22.Date.str.contains("26 Sep 2021")]
for z in parties:
    data22[z] = [x.replace('–',str(np.NaN)) for x in data22[z].astype(str)]
    data22[z] = [x.replace('—',str(np.NaN)) for x in data22[z].astype(str)]
data22[parties] = data22[parties].astype(float)

data22 = data22.drop(data22[data22['Wag'] > 0].index)
data22=data22.drop('Wag', axis=1)


print(data22)
data22.to_csv('German/State/Thuringia/poll.csv', index=False)
