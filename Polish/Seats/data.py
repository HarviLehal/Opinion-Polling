import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Polish_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

df7=pd.DataFrame(df[9])
data22 = df7.drop(["Polling Firm/Link", "Sample Size", "Majority", "Kukiz'15"], axis=1)
headers = ['Date', 'United Right', 'Civic Coalition', 'The Left', 'Polish Coalition', 'Confederation', 'Poland 2050', 'Others']
parties = ['United Right', 'Civic Coalition', 'The Left', 'Polish Coalition', 'Confederation', 'Poland 2050', 'Others']
data22.columns = headers
data22.drop(data22.tail(1).index,inplace=True)
print(data22)

df8=pd.DataFrame(df[10])
data21 = df8.drop(["Polling Firm/Link", "Sample Size", "Majority"], axis=1)
data21.columns = headers
data21.drop(data21.index[[-1,-3]],inplace=True)
print(data21)

# df.drop(df.columns[-1], axis=1, inplace=True)


data = pd.concat([data22,data21])

for z in parties:
        data[z] = [x.replace('[av]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[ba]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[bb]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[bc]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[bd]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[be]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[bf]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[aw]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[t]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[ax]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[ay]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[az]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[u]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[v]','') for x in data[z].astype(str)]
        data[z] = [x.replace('[w]','') for x in data[z].astype(str)]
        data[z] = data[z].astype('float').astype(str)
data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x))

print(data)
data.to_csv('Polish/Seats/poll.csv', index=False)
