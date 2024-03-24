import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_and_seat_projections_for_the_2024_European_Parliament_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
# Parse each table into a DataFrame
# Parse each table into a DataFrame
for table in tables:
    # Initialize an empty list to hold the data for the rows
    data = []
    # Loop through each row in the table
    for row in table.find_all('tr'):
        # Extract the data from each cell in the row
        row_data = []
        for cell in row.find_all(['th', 'td']):
            # Append the cell's text to the row data
            row_data.append(cell.get_text(strip=True))
        # Append the row data to the table data
        data.append(row_data)
    # Convert the table data to a DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    break  # Exit the loop after parsing the first table

# Now df contains the DataFrame for the first table on the page

p = re.compile(r'\[[a-z]+\]'  )

data2=pd.DataFrame(df)
data2=data2.drop(["Organisation", "Area", "Lead"], axis=1)

headers = ['Date','SEATS','Left','S&D','G/EFA','Renew','EPP','ECR','ID','NI','Other']
parties = ['SEATS','Left','S&D','G/EFA','Renew','EPP','ECR','ID','NI','Other']
data2.columns = headers
data2.drop(data2.index[[0]],inplace=True)
data2.Date = data2.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

data2 = data2[data2['EPP'] != data2['NI']]

data2 =data2.dropna(subset=['Date'])

for z in parties:
  data2[z] = [p.sub('', x) for x in data2[z].astype(str)]
  data2[z] = [x.replace('–',str(np.NaN)) for x in data2[z].astype(str)]
  data2[z] = [x.replace('–',str(np.NaN)) for x in data2[z].astype(str)]
data2 =data2.dropna(subset=['SEATS'])

data2 = data2[pd.to_numeric(data2['SEATS'], errors='coerce').notnull()]
for z in parties:
  data2[z] = [x.replace('None',str(np.NaN)) for x in data2[z].astype(str)]
data2 = data2.replace(r'^\s*$', str(np.NaN), regex=True)

data2[parties] = data2[parties].astype(float)

data2 = data2[data2['SEATS'] != 751]
data2=data2.drop(["SEATS"], axis=1)
data2 = data2.reset_index(drop=True)
data2.loc[len(data2.index)-1,['Date']] = '26 May 2019'
data2.Date = data2.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))



data2.to_csv('Europe/poll.csv', index=False)


