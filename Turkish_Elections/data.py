import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Turkish_presidential_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

df0=pd.DataFrame(df[0])
data22 = df0.drop(["Polling firm", "Sample size","Others", "Lead"], axis=1)
headers = ['Dates conducted', 'AKP', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'HDP3', 'IYI', 'SAADET', 'MHP', 'DEVA', 'GP', 'MP']
parties = ['AKP', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'HDP3', 'IYI', 'SAADET', 'MHP', 'DEVA', 'GP', 'MP']
CHP = ['CHP1', 'CHP2', 'CHP3']
HDP = ['HDP1', 'HDP2', 'HDP3']
data22.columns = headers
data22.AKP = data22.AKP.astype('float').astype(str)
data22['Dates conducted'] = [x.strip()[-6:] for x in data22['Dates conducted']]
data22['Dates conducted'] = [x.replace('–','') for x in data22['Dates conducted']]
data22['Dates conducted'] = [x+' 2022' for x in data22['Dates conducted']]

for z in parties:
    data22[z] = [x.replace('–','0') for x in data22[z]]
data22[parties] = data22[parties].astype(float)
data22['CHP'] = data22[CHP].sum(axis=1)
data22['HDP'] = data22[HDP].sum(axis=1)
data22 = data22.drop(CHP + HDP, axis=1)
print(data22)


df1=pd.DataFrame(df[1])
data21 = df1.drop(["Polling firm", "Sample size","Others", "Lead"], axis=1)
headers = ['Dates conducted', 'AKP', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'HDP3', 'IYI', 'SAADET', 'MHP', 'DEVA', 'GP', 'MP']
parties = ['AKP', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'HDP3', 'IYI', 'SAADET', 'MHP', 'DEVA', 'GP', 'MP']
CHP = ['CHP1', 'CHP2', 'CHP3']
HDP = ['HDP1', 'HDP2', 'HDP3']
data21.columns = headers
data21.AKP = data21.AKP.astype('float').astype(str)
data21['Dates conducted'] = [x.strip()[-6:] for x in data21['Dates conducted']]
data21['Dates conducted'] = [x.replace('–','') for x in data21['Dates conducted']]
data21['Dates conducted'] = [x+' 2021' for x in data21['Dates conducted']]

for z in parties:
    data21[z] = [x.replace('–','0') for x in data21[z]]
data21[parties] = data21[parties].astype(float)
data21['CHP'] = data21[CHP].sum(axis=1)
data21['HDP'] = data21[HDP].sum(axis=1)
data21 = data21.drop(CHP + HDP, axis=1)
print(data21)



df2=pd.DataFrame(df[2])
data20 = df2.drop(["Polling firm", "Sample size","Others", "Lead"], axis=1)
headers = ['Dates conducted', 'AKP', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'IYI', 'SAADET', 'MHP', 'DEVA', 'GP', 'MP']
parties = ['AKP', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'IYI', 'SAADET', 'MHP', 'DEVA', 'GP', 'MP']
CHP = ['CHP1', 'CHP2', 'CHP3']
HDP = ['HDP1', 'HDP2']
data20.columns = headers
data20.AKP = data20.AKP.astype('float').astype(str)
data20.CHP1 = data20.CHP1.astype('float').astype(str)
data20['Dates conducted'] = [x.strip()[-6:] for x in data20['Dates conducted']]
data20['Dates conducted'] = [x.replace('–','') for x in data20['Dates conducted']]
data20['Dates conducted'] = [x+' 2020' for x in data20['Dates conducted']]

for z in parties:
    data20[z] = [x.replace('–','0') for x in data20[z]]
data20[parties] = data20[parties].astype(float)
data20['CHP'] = data20[CHP].sum(axis=1)
data20['HDP'] = data20[HDP].sum(axis=1)
data20 = data20.drop(CHP + HDP, axis=1)
data20.loc[len(data20.index)-2,['CHP']] = 35.1
print(data20)

df3=pd.DataFrame(df[3])
data19 = df3.drop(["Polling firm", "Sample size","Others", "Lead"], axis=1)
headers = ['Dates conducted', 'AKP', 'CHP1', 'CHP2', 'CHP3', 'HDP', 'IYI', 'SAADET', 'MHP', 'DEVA', 'GP', 'MP']
parties = ['AKP', 'CHP1', 'CHP2', 'CHP3', 'HDP', 'IYI', 'SAADET', 'MHP', 'DEVA', 'GP', 'MP']
CHP = ['CHP1', 'CHP2', 'CHP3']
data19.columns = headers
data19 = data19[data19['AKP'] != data19['Dates conducted']]
for z in parties:
    data19[z] = [x.replace('-','0') for x in data19[z].astype(str)]
    data19[z] = [x.replace('–','0') for x in data19[z].astype(str)]
    data19[z] = [x.replace('—','0') for x in data19[z].astype(str)]
    data19[z] = [x.replace('[nb 3]','') for x in data19[z].astype(str)]
    data19[z] = [x.replace('[nb 2]','') for x in data19[z].astype(str)]
data19.AKP = data19.AKP.astype('float').astype(str)
data19.CHP1 = data19.CHP1.astype('float').astype(str)
data19['Dates conducted'] = [x.strip()[-6:] for x in data19['Dates conducted']]
data19['Dates conducted'] = [x.replace('–','') for x in data19['Dates conducted']]
data19['Dates conducted'] = [x+' 2019' for x in data19['Dates conducted']]
data19.loc[len(data19.index)-1,['Dates conducted']] = 'Jul 2018'
data19.loc[len(data19.index),['Dates conducted']] = '24 Jun 2018'

data19[parties] = data19[parties].astype(float)
data19['CHP'] = data19[CHP].sum(axis=1)
data19 = data19.drop(CHP, axis=1)
data19.loc[len(data19.index),['CHP']] = 30.6
data19.loc[len(data19.index)-1,['CHP']] = 27.7

print(data19)



data = pd.concat([data22,data21,data20,data19])
data = data.rename(columns={'Dates conducted':'Date'})
print(data)
data.to_csv('Turkish_Elections/poll.csv', index=False)
