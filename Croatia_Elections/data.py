import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser
import numpy as np

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Croatian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

df0=pd.DataFrame(df[1])
data22 = df0.drop(["Polling firm","Votes","Lead", "Undecided", "BM 365","Centar","RF", "NS R", "HNS", "KH","IDS","HSS","HSU","HS", "Others"], axis=1)
headers = ['Date', 'HDZ', 'SDP', 'DP', 'Most', 'Možemo!', 'Fokus', 'SD']
parties = ['HDZ', 'SDP', 'DP', 'Most', 'Možemo!', 'Fokus', 'SD']
data22.columns = headers

data22 = data22[data22['HDZ'] != data22['Fokus']]
data22['Date'] = data22.Date.apply(lambda x: dateparser.parse(x))

for z in parties:
  data22[z] = [x.replace('[a]','') for x in data22[z]]
  data22[z] = [x.replace('[b]','') for x in data22[z]]
  data22[z] = [x.replace('[c]','') for x in data22[z]]
  data22[z] = [x.replace('[d]','') for x in data22[z]]
  data22[z] = [x.replace('[e]','') for x in data22[z]]
  data22[z] = [x.replace('[f]','') for x in data22[z]]
  data22[z] = [x.replace('[g]','') for x in data22[z]]
  data22[z] = [x.replace('[h]','') for x in data22[z]]
  data22[z] = [x.replace('[i]','') for x in data22[z]]
  data22[z] = [x.replace('[j]','') for x in data22[z]]
  data22[z] = [x.replace('[k]','') for x in data22[z]]
  data22[z] = [x.replace('[l]','') for x in data22[z]]
  data22[z] = [x.replace('[m]','') for x in data22[z]]
  data22[z] = [x.replace('[n]','') for x in data22[z]]
  data22[z] = [x.replace('[o]','') for x in data22[z]]


print(data22)
data22.to_csv('Croatia_Elections/poll.csv', index=False)

# FIXED GRAPH

df0=pd.DataFrame(df[1])
data22 = df0.drop(["Polling firm","Votes","Lead", "Undecided"], axis=1)
headers = ['Date', 'HDZ', 'SDP', 'DP', 'Most', 'Možemo!', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14']
parties = ['HDZ', 'SDP', 'DP', 'Most', 'Možemo!', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14']
Other = ['o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14']

data22.columns = headers

data22 = data22[data22['HDZ'] != data22['o3']]
data22['Date'] = data22.Date.apply(lambda x: dateparser.parse(x))

for z in parties:
  data22[z] = [x.replace('[a]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[b]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[c]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[d]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[e]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[f]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[g]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[h]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[i]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[j]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[k]','') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[l]','0') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[m]','0') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[n]','0') for x in data22[z].astype(str)]
  data22[z] = [x.replace('[o]','0') for x in data22[z].astype(str)]
  data22[z] = [x.replace('–','0') for x in data22[z].astype(str)]
  data22[z] = [x.replace('-','0') for x in data22[z].astype(str)]

data22[parties] = data22[parties].astype(float)
data22['o2']=np.where(data22['o2'] == data22['o3'], 0, data22['o2'])
data22['o3']=np.where(data22['o3'] == data22['o4'], 0, data22['o3'])
data22['o1']=np.where(data22['Možemo!'] == data22['o1'], 0, data22['o1'])
data22['Other'] = data22[Other].sum(axis=1)

data22 = data22.drop(Other, axis=1)
parties = ['HDZ', 'SDP', 'DP', 'Most', 'Možemo!', 'Other']

data22[parties] = data22[parties].div(data22[parties].sum(axis=1), axis=0)

print(data22)
data22.to_csv('Croatia_Elections/poll2.csv', index=False)
