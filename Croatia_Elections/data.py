import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Croatian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

df0=pd.DataFrame(df[1])
data22 = df0.drop(["Polling firm","Votes","Lead", "Undecided", "BM 365","Centar","RF", "NS R", "HNS", "KH","IDS","HSS","HSU","HS", "Others"], axis=1)
headers = ['Date', 'HDZ', 'SDP', 'DP', 'Most', 'Možemo', 'Fokus', 'SD']
parties = ['HDZ', 'SDP', 'DP', 'Most', 'Možemo', 'Fokus', 'SD']
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


print(data22)
data22.to_csv('Croatia_Elections/poll.csv', index=False)
