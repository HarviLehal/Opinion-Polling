import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
print(df[0])


df0=pd.DataFrame(df[0])
data23 = df0.drop(["Pollster", "Client", "Area", "Others", "Lead"], axis=1)
headers = ['Date', 'Sample size', 'Con', 'Lab', 'Lib Dem', 'SNP', 'Green', 'Reform']
parties = ['Con', 'Lab', 'Lib Dem', 'SNP', 'Green', 'Reform']
data23.columns = headers
data23['Date'] = [x.strip()[-6:] for x in data23['Date']]
data23['Date'] = [x.replace('–','') for x in data23['Date']]
data23['Date'] = [x+' 2023' for x in data23['Date']]
for z in parties:
    data23[z] = [x.replace('–','-') for x in data23[z]]
    data23[z] = [x.replace('TBC','-') for x in data23[z]]
    data23[z] = [x.replace('?','-') for x in data23[z]]
    data23[z] = [x.replace('[a]','') for x in data23[z]]
data23 = data23[data23['Sample size'] != data23['Con']]
print(data23)


df1=pd.DataFrame(df[1])
data22 = df1.drop(["Pollster", "Client", "Area", "Others", "Lead"], axis=1)
data22.columns = headers
data22['Date'] = [x.strip()[-6:] for x in data22['Date']]
data22['Date'] = [x.replace('–','') for x in data22['Date']]
data22['Date'] = [x+' 2022' for x in data22['Date']]
for z in parties:
    data22[z] = [x.replace('–','-') for x in data22[z]]
    data22[z] = [x.replace('TBC','-') for x in data22[z]]
    data22[z] = [x.replace('?','-') for x in data22[z]]
    data22[z] = [x.replace('[a]','') for x in data22[z]]
data22 = data22[data22['Sample size'] != data22['Con']]
print(data22)


df2=pd.DataFrame(df[2])
print(df2)
data21 = df2.drop(["Pollster", "Client", "Area", "Others", "Lead"], axis=1)
data21.columns = headers
data21['Date'] = [x.strip()[-6:] for x in data21['Date']]
data21['Date'] = [x.replace('–','') for x in data21['Date']]
data21['Date'] = [x+' 2021' for x in data21['Date']]

for z in parties:
    data21[z] = [x.replace('–','-') for x in data21[z]]
    data21[z] = [x.replace('TBC','-') for x in data21[z]]
    data21[z] = [x.replace('?','-') for x in data21[z]]
    data21[z] = [x.replace('[a]','') for x in data21[z]]
data21 = data21[data21['Sample size'] != data21['Con']]
print(data21)


df3=pd.DataFrame(df[3])
print(df3)
data20 = df3.drop(["Pollster", "Client", "Area", "Others", "Lead"], axis=1)
data20.columns = headers
data20['Date'] = [x.strip()[-6:] for x in data20['Date']]
data20['Date'] = [x.replace('–','') for x in data20['Date']]
data20['Date'] = [x+' 2020' for x in data20['Date']]

for z in parties:
    data20[z] = [x.replace('–','-') for x in data20[z]]
    data20[z] = [x.replace('TBC','-') for x in data20[z]]
    data20[z] = [x.replace('?','-') for x in data20[z]]
    data20[z] = [x.replace('[a]','') for x in data20[z]]
data20 = data20[data20['Sample size'] != data20['Con']]
print(data20)


data = pd.concat([data23,data22,data21,data20])
data.drop(data.index[[-2]],inplace=True)
data['Date'] = data['Date'].replace(['c 2019 2020'], '12 Dec 2019')

data = data.drop(["Sample size"], axis=1)
print(data)
data.to_csv('UK/general_polling/poll.csv', index=False)
