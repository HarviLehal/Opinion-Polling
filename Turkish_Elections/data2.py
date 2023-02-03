import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser

wikiurl="https://tr.wikipedia.org/wiki/2023_Türkiye_cumhurbaşkanlığı_seçimi_için_yapılan_anketler"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables), decimal=',', thousands='.')

# 2023 POLLS

df0=pd.DataFrame(df[0])
data23 = df0.drop(['Anket şirketi',	'Örneklem', 'Özdağ ZP','Fark','Erbakan YRP','Diğerleri'], axis=1)
headers = ['Date', 'Erdoğan', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'HDP3', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu', 'İnce']
parties = ['Erdoğan', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'HDP3', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu', 'İnce']
CHP = ['CHP1', 'CHP2', 'CHP3']
HDP = ['HDP1', 'HDP2', 'HDP3']
data23.columns = headers
data23['Date2'] = data23['Date'].str.split('–').str[1]
# data23['Date'] = ['15 ' + x for x in data23['Date'].astype(str)]
data23.Date2.fillna(data23.Date, inplace=True)
data23['Date2'] = [x+' 2023' for x in data23['Date2'].astype(str)]
data23['Date'] = data23['Date2']
data23 = data23.drop(['Date2'], axis=1)

for z in parties:
    data23[z] = [x.replace('–','0') for x in data23[z].astype(str)]
data23[parties] = data23[parties].astype(float)
data23['CHP Total'] = data23[CHP].sum(axis=1)
data23['HDP Total'] = data23[HDP].sum(axis=1)
data23 = data23.drop(CHP + HDP, axis=1)
print(data23)


# 2022 POLLS

df1=pd.DataFrame(df[1])
data22 = df1.drop(['Anket şirketi',	'Örneklem', 'Özdağ ZP','Fark','Diğerleri'], axis=1)
headers = ['Date', 'Erdoğan', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu', 'İnce']
parties = ['Erdoğan', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu', 'İnce']
HDP = ['HDP1', 'HDP2']
data22.columns = headers  
data22['Date2'] = data22['Date'].str.split('–').str[1]
# data22['Date'] = ['15 ' + x for x in data22['Date'].astype(str)]
data22.Date2.fillna(data22.Date, inplace=True)
data22['Date2'] = [x+' 2022' for x in data22['Date2'].astype(str)]
data22['Date'] = data22['Date2']
data22 = data22.drop(['Date2'], axis=1)

for z in parties:
    data22[z] = [x.replace('12,4[no 1]','6.2') for x in data22[z].astype(str)]
    data22[z] = [x.replace('–','0') for x in data22[z].astype(str)]
data22[parties] = data22[parties].astype(float)
data22['CHP Total'] = data22[CHP].sum(axis=1)
data22['HDP Total'] = data22[HDP].sum(axis=1)
data22 = data22.drop(CHP + HDP, axis=1)
print(data22)


# 2021 POLLS

df2=pd.DataFrame(df[2])
data21 = df2.drop(['Anket şirketi',	'Örneklem', 'Diğerleri','Fark',], axis=1)
headers = ['Date', 'Erdoğan', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'HDP3', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu', 'İnce']
parties = ['Erdoğan', 'CHP1', 'CHP2', 'CHP3', 'HDP1', 'HDP2', 'HDP3', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu', 'İnce']
HDP = ['HDP1', 'HDP2', 'HDP3']
data21.columns = headers  
data21 = data21[data21['Erdoğan'] != data21['Bahçeli']]
data21['Date2'] = data21['Date'].str.split('–').str[1]
# data21['Date'] = ['15 ' + x for x in data21['Date'].astype(str)]
data21.Date2.fillna(data21.Date, inplace=True)
data21['Date2'] = [x+' 2021' for x in data21['Date2'].astype(str)]
data21['Date'] = data21['Date2']
data21 = data21.drop(['Date2'], axis=1)

for z in parties:
    data21[z] = [x.replace('–','0') for x in data21[z].astype(str)]
data21[parties] = data21[parties].astype(float)
data21['CHP Total'] = data21[CHP].sum(axis=1)
data21['HDP Total'] = data21[HDP].sum(axis=1)
data21 = data21.drop(CHP + HDP, axis=1)

data21.Date = data21.Date.apply(lambda x: dateparser.parse(x))
print(data21)


# 2021 POLLS

df3=pd.DataFrame(df[3])
data20 = df3.drop(['Anket şirketi',	'Örneklem', 'Diğerleri','Fark',], axis=1)
headers = ['Date', 'Erdoğan', 'CHP1', 'CHP2', 'CHP3', 'CHP4', 'HDP1', 'HDP2', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu']
parties = ['Erdoğan', 'CHP1', 'CHP2', 'CHP3', 'CHP4', 'HDP1', 'HDP2', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu']
CHP = ['CHP1', 'CHP2', 'CHP3', 'CHP4']
HDP = ['HDP1', 'HDP2']
data20.columns = headers  
data20 = data20[data20['Erdoğan'] != data20['Bahçeli']]
data20['Date2'] = data20['Date'].str.split('–').str[1]
# data20['Date'] = ['15 ' + x for x in data20['Date'].astype(str)]
data20.Date2.fillna(data20.Date, inplace=True)
data20['Date2'] = [x+' 2020' for x in data20['Date2'].astype(str)]
data20['Date'] = data20['Date2']
data20 = data20.drop(['Date2'], axis=1)

for z in parties:
    data20[z] = [x.replace('–','0') for x in data20[z].astype(str)]
data20[parties] = data20[parties].astype(float)
data20['CHP Total'] = data20[CHP].sum(axis=1)
data20['HDP Total'] = data20[HDP].sum(axis=1)
data20 = data20.drop(CHP + HDP, axis=1)
parties = ['Erdoğan', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu','CHP Total', 'HDP Total']
for z in parties:
  data20[z] = data20[z].apply(lambda x: x/4 if x > 100 else x)


print(data20)


df4=pd.DataFrame(df[4])
data19 = df4.drop(['Anket şirketi',	'Örneklem', 'Diğerleri','Fark',], axis=1)
headers = ['Date', 'Erdoğan', 'CHP1', 'CHP2', 'CHP3', 'CHP4', 'HDP Total', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu']
parties = ['Erdoğan', 'CHP1', 'CHP2', 'CHP3', 'CHP4', 'HDP Total', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu']
CHP = ['CHP1', 'CHP2', 'CHP3', 'CHP4']
data19.columns = headers  
data19 = data19[data19['Erdoğan'] != data19['Bahçeli']]
data19['Date2'] = data19['Date'].str.split('–').str[1]
# data19['Date'] = ['15 ' + x for x in data19['Date'].astype(str)]
data19.Date2.fillna(data19.Date, inplace=True)
data19['Date2'] = [x+' 2019' for x in data19['Date2'].astype(str)]
data19['Date'] = data19['Date2']
data19 = data19.drop(['Date2'], axis=1)

for z in parties:
    data19[z] = [x.replace('–','0') for x in data19[z].astype(str)]
    data19[z] = [x.replace('30,6[no 4]','30.6') for x in data19[z].astype(str)]
    data19[z] = [x.replace('56,7[no 3]','56.7') for x in data19[z].astype(str)]
    data19[z] = [x.replace('52,6[no 3]','52.6') for x in data19[z].astype(str)]

data19[parties] = data19[parties].astype(float)
data19['CHP Total'] = data19[CHP].sum(axis=1)
data19 = data19.drop(CHP, axis=1)
parties = ['Erdoğan', 'Akşener', 'Bahçeli', 'Babacan', 'Davutoğlu', 'Karamollaoğlu','CHP Total', 'HDP Total']
for z in parties:
  data19[z] = data19[z].apply(lambda x: x/4 if x > 100 else x)
data19.loc[len(data19.index)-1,['Date']] = '30 Haziran 2018'
data19.loc[len(data19.index),['Date']] = '24 Haziran 2018'

print(data19)




data = pd.concat([data23,data22,data21,data20,data19])
data.Date = data.Date.astype(str).apply(lambda x: dateparser.parse(x))
print(data)
data.to_csv('Turkish_Elections/poll2.csv', index=False)
