import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
indiatable=soup.find('table',{'class':"wikitable"})
df=pd.read_html(str(indiatable))
# convert list to dataframe
df=pd.DataFrame(df[0])
data = df.drop(["Pollster", "Client", "Area", "Others", "Lead"], axis=1)
# data = data.reset_index(level=[1], drop=True)
headers = ['Dates conducted', 'Sample size', 'Con', 'Lab', 'Lib Dem', 'SNP', 'Green', 'Reform']
parties = ['Con', 'Lab', 'Lib Dem', 'SNP', 'Green', 'Reform']
data[headers] = data[headers].apply(lambda x: x.str.replace(',',''))
data.columns = data.columns.droplevel(-1)
data['Dates conducted'] = [x.strip()[-6:] for x in data['Dates conducted']]
data['Dates conducted'] = [x.replace('–','') for x in data['Dates conducted']]
for z in parties:
    data[z] = [x.replace('–','-') for x in data[z]]
    data[z] = [x.replace('TBC','-') for x in data[z]]
    data[z] = [x.replace('?','-') for x in data[z]]
    data[z] = [x.replace('[a]','') for x in data[z]]
data = data[data['Sample size'] != data['Con']]
data = data.rename(columns={'Dates Conducted':'Date'})
print(data)
data.to_csv('poll.csv')
