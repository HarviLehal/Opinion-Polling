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
# data22 = data22.groupby(level=0,axis=1).sum()
data22['CHP'] = data22[CHP].sum(axis=1)
data22['HDP'] = data22[HDP].sum(axis=1)
data22 = data22.drop(CHP + HDP, axis=1)
# data22 = data22[data22['Sample size'] != data22['Con']]
print(data22)
data22.to_csv('Turkish_Elections/poll.csv', index=False)


# df1=pd.DataFrame(df[1])
# data21 = df1.drop(["Pollster", "Client", "Area", "Others", "Lead"], axis=1)
# data21[headers] = data21[headers].apply(lambda x: x.str.replace(',',''))
# data21.columns = data21.columns.droplevel(-1)
# data21['Dates conducted'] = [x.strip()[-6:] for x in data21['Dates conducted']]
# data21['Dates conducted'] = [x.replace('–','') for x in data21['Dates conducted']]
# data21['Dates conducted'] = [x+' 2021' for x in data21['Dates conducted']]
# for z in parties:
#     data21[z] = [x.replace('–','-') for x in data21[z]]
#     data21[z] = [x.replace('TBC','-') for x in data21[z]]
#     data21[z] = [x.replace('?','-') for x in data21[z]]
#     data21[z] = [x.replace('[a]','') for x in data21[z]]
# data21 = data21[data21['Sample size'] != data21['Con']]
# print(data21)

# df2=pd.DataFrame(df[2])
# print(df2)
# data20 = df2.drop(["Pollster", "Client", "Area", "Others", "Lead"], axis=1)
# data20 = data20.rename(columns={'Brexit':'Reform'})
# data20[headers] = data20[headers].apply(lambda x: x.str.replace(',',''))
# data20.columns = data20.columns.droplevel(-1)
# data20['Dates conducted'] = [x.strip()[-6:] for x in data20['Dates conducted']]
# data20['Dates conducted'] = [x.replace('–','') for x in data20['Dates conducted']]
# data20['Dates conducted'] = [x+' 2020' for x in data20['Dates conducted']]

# for z in parties:
#     data20[z] = [x.replace('–','-') for x in data20[z]]
#     data20[z] = [x.replace('TBC','-') for x in data20[z]]
#     data20[z] = [x.replace('?','-') for x in data20[z]]
#     data20[z] = [x.replace('[a]','') for x in data20[z]]
# data20 = data20[data20['Sample size'] != data20['Con']]
# print(data20)

# data = pd.concat([data22,data21,data20])
# data = data[:-2]
# data = data.drop(["Sample size"], axis=1)
# data = data.rename(columns={'Dates conducted':'Date'})
# print(data)
# data.to_csv('UK_Elections/poll.csv', index=False)
