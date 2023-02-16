import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_next_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

print(df[25])
df0=pd.DataFrame(df[25])
sunak22 = df0.drop(["Pollster/client", "Area", "Sample size", "Lead"], axis=1)
headers = ['Date', 'Starmer', 'Sunak', 'Unsure']
parties = ['Starmer', 'Sunak', 'Unsure']
sunak22.columns = headers
sunak22['Date'] = [x.strip()[-6:] for x in sunak22['Date']]
sunak22['Date'] = [x.replace('–','') for x in sunak22['Date']]
sunak22['Date'] = [x+' 2022' for x in sunak22['Date']]
print(sunak22)

print(df[26])
df1=pd.DataFrame(df[26])
sunak21 = df1.drop(["Pollster/client", "Area", "Sample size", "Lead"], axis=1)
headers = ['Date', 'Starmer', 'Sunak', 'Unsure']
parties = ['Starmer', 'Sunak', 'Unsure']
sunak21.columns = headers
sunak21['Date'] = [x.strip()[-6:] for x in sunak21['Date']]
sunak21['Date'] = [x.replace('–','') for x in sunak21['Date']]
sunak21['Date'] = [x+' 2021' for x in sunak21['Date']]
print(sunak21)

print(df[27])
df2=pd.DataFrame(df[27])
sunak20 = df2.drop(["Pollster/client", "Area", "Sample size", "Lead"], axis=1)
headers = ['Date', 'Starmer', 'Sunak', 'Unsure']
parties = ['Starmer', 'Sunak', 'Unsure']
sunak20.columns = headers
sunak20['Date'] = [x.strip()[-6:] for x in sunak20['Date']]
sunak20['Date'] = [x.replace('–','') for x in sunak20['Date']]
sunak20['Date'] = [x+' 2020' for x in sunak20['Date']]
print(sunak20)

print(df[28])
df3=pd.DataFrame(df[28])
truss = df3.drop(["Pollster/client", "Area", "Sample size", "Lead", "None of these"], axis=1)
truss.drop([5] , axis=0, inplace=True)
truss = truss[['Date(s) conducted', 'Liz Truss','Keir Starmer','Unsure']]
headers = ['Date', 'Truss', 'Starmer', 'Unsure']
parties = ['Truss', 'Starmer', 'Unsure']
truss.columns = headers
truss['Date'] = [x.strip()[-6:] for x in truss['Date']]
truss['Date'] = [x.replace('–','') for x in truss['Date']]
truss['Date'] = [x+' 2022' for x in truss['Date']]
print(truss)

print(df[29])
df4=pd.DataFrame(df[29])
boris22 = df4.drop(["Pollster/client", "Area", "Refused", "Sample size", "Lead", "None of these"], axis=1)
# boris22.drop([5] , axis=0, inplace=True)
# boris22 = truss22[['Date(s) conducted', 'Liz Truss','Keir Starmer','Unsure']]
headers = ['Date', 'Johnson', 'Starmer', 'Unsure']
parties = ['Johnson', 'Starmer', 'Unsure']
boris22.columns = headers
boris22['Date'] = [x.strip()[-6:] for x in boris22['Date']]
boris22['Date'] = [x.replace('–','') for x in boris22['Date']]
boris22['Date'] = [x+' 2022' for x in boris22['Date']]
print(boris22)

print(df[30])
df5=pd.DataFrame(df[30])
boris21 = df5.drop(["Pollster/client", "Area", "Refused", "Sample size", "Lead", "None of these"], axis=1)
# boris22.drop([5] , axis=0, inplace=True)
# boris22 = truss22[['Date(s) conducted', 'Liz Truss','Keir Starmer','Unsure']]
headers = ['Date', 'Johnson', 'Starmer', 'Unsure']
parties = ['Johnson', 'Starmer', 'Unsure']
boris21.columns = headers
boris21['Date'] = [x.strip()[-6:] for x in boris21['Date']]
boris21['Date'] = [x.replace('–','') for x in boris21['Date']]
boris21['Date'] = [x+' 2021' for x in boris21['Date']]
print(boris21)

print(df[31])
df6=pd.DataFrame(df[31])
boris20 = df6.drop(["Pollster/client", "Area", "Refused", "Sample size", "Lead", "None of these"], axis=1)
# boris22.drop([5] , axis=0, inplace=True)
# boris22 = truss22[['Date(s) conducted', 'Liz Truss','Keir Starmer','Unsure']]
headers = ['Date', 'Johnson', 'Starmer', 'Unsure']
parties = ['Johnson', 'Starmer', 'Unsure']
boris20.columns = headers
boris20['Date'] = [x.strip()[-6:] for x in boris20['Date']]
boris20['Date'] = [x.replace('–','') for x in boris20['Date']]
boris20['Date'] = [x+' 2020' for x in boris20['Date']]
print(boris20)


boris = pd.concat([boris22,boris21,boris20])
print(boris)
sunak = pd.concat([sunak22,sunak21,sunak20])
print(sunak)

sunak.to_csv('UK/leadership_approval/sunak.csv', index=False)
boris.to_csv('UK/leadership_approval/boris.csv', index=False)
truss.to_csv('UK/leadership_approval/truss.csv', index=False)
