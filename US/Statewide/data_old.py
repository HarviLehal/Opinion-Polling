"""
Scrape statewide polling for the 2024 United States presidential election from Wikipedia.
Some states have multiple tables, so we will need to concatenate them.
Some states also have other candidates, so we will need to remove them.
"""

import dateparser
import re
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
p = re.compile(r'\[[a-z]+\]')

def extract_latest_date(date_range):
    # Split the date range into parts
    parts = date_range.split('–')
    
    # Extract the start date (which includes the month)
    start_date = parts[0].strip()
    
    # Extract the end date (which might only have the day)
    end_date = parts[-1].strip()
    
    # If the end date does not contain a month, inherit it from the start date
    if any(char.isdigit() for char in end_date) and not any(char.isalpha() for char in end_date):
        # Extract the month from the start date
        month = ''.join(filter(str.isalpha, start_date))
        end_date = month + ' ' + end_date
    
    # Return the latest date with the correct format
    return end_date

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

# states = ['Georgia']
def get_state_polls(state):
    print("Getting polls for " + state)
    if state == "Washington":
        wikiurl = f"https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_{state}_(state)"
    else:
        wikiurl = f"https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_{state}"
    table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(wikiurl)
    # print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', class_="wikitable")
    df = pd.read_html(str(tables))
    p = re.compile(r'\[[a-z]+\]')
    parties = ['Trump', 'Biden']
    d = {}
    for i in range(len(df)):
        if state == "Minnesota":
            z = 'Joe Biden DFL'
        elif state == "North Dakota":
            z = 'Joe Biden Democratic-NPL'
        else:
            z = 'Joe Biden Democratic'
        if z in df[i].columns:
            # skip first accepted table for Florida as it is not polling data
            # if state == "Florida":
                # i += 2
            y = 'Source of poll aggregation'
            if y in df[i].columns:
                i +=1
            d[i] = pd.DataFrame(df[i])
            d[i] = d[i].drop(["Poll source", "Margin of error"], axis=1)
            # psub the column headers to remove the citation numbers
            for z in d[i].columns:
                d[i].rename(columns={z: p.sub('', z)}, inplace=True)

            d[i] = d[i].drop("Sample size", axis=1)
            d[i] = d[i].iloc[:, :3]
            # rename the columns to the headers we want
            # if 
            d[i].rename(columns={d[i].columns[0]: 'Date'}, inplace=True)
            z = 'Joe Biden Democratic'
            z1 = 'Joe Biden DFL'
            z2 = 'Donald Trump Republican'
            z3 = 'Donald J. Trump Republican'
            z4 = 'Joe Biden Democratic-NPL'
            if z in d[i].columns:
                d[i].rename(columns={z: 'Biden'}, inplace=True)
            if z1 in d[i].columns:
                d[i].rename(columns={z1: 'Biden'}, inplace=True)
            if z2 in d[i].columns:
                d[i].rename(columns={z2: 'Trump'}, inplace=True)
            if z3 in d[i].columns:
                d[i].rename(columns={z3: 'Trump'}, inplace=True)
            if z4 in d[i].columns:
                d[i].rename(columns={z4: 'Biden'}, inplace=True)
            # d[i].columns = headers
            for z in parties:
                d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
                d[i][z] = [x.replace('-', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('—', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('–', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('TBC', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('TBA', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('?', str(np.NaN)) for x in d[i][z]]
            d[i]['Date2'] = [extract_latest_date(x) for x in d[i]['Date']]
            d[i]['Date'] = d[i]['Date2']
            d[i] = d[i].drop(['Date2'], axis=1)
            d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
            if len(d[i]) > 0:
                break
    if len(d) > 0:
        D = pd.concat(d.values(), ignore_index=True)
    else:
        # if no polling data is found, return an empty dataframe
        return pd.DataFrame()
    # only keep the first table of the dictionary, which might not be 0
    for z in parties:
        D[z] = D[z].astype(str)
        D[z] = D[z].str.strip('%')
        # D[z] = D[z].astype('float')
        D[z] = pd.to_numeric(D[z], errors='coerce')
    
    # drop rows where both Biden and Trump are NaN
    D = D.dropna(subset=['Biden', 'Trump'], how='all')
    D['total']=D[parties].sum(axis=1)
    D['Biden'] = D['Biden']/D['total']
    D['Trump'] = D['Trump']/D['total']
    D = D.drop(['total'], axis=1)
    D['State'] = state
    return D

def get_all_polls():
    polls = pd.DataFrame()
    for state in states:
        polls = pd.concat([polls, get_state_polls(state)])
    return polls

polls_old = get_all_polls()

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware','District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


# create list of max d


# Class a winner based on the 14 day average since the most recent poll for each state
dates = polls_old.groupby('State')['Date'].max()
dates
fourteen_days_before = dates - pd.Timedelta(days=7)

averages_old = pd.DataFrame(columns=['State', 'Biden', 'Trump', 'Winner'])
for state in states:
    if state not in polls_old['State'].unique():
        continue

    averages_old = pd.concat([averages_old, pd.DataFrame({'State': [state], 'Biden': [polls_old[(polls_old['State']== state) & (polls_old['Date'] >= fourteen_days_before[state])]['Biden'].mean()], 'Trump': [polls_old[(polls_old['State'] == state) & (polls_old['Date'] >= fourteen_days_before[state])]['Trump'].mean()]})])    
    if averages_old[averages_old['State'] == state]['Biden'].values[0] > averages_old[averages_old['State'] == state]['Trump'].values[0]:
        averages_old.loc[averages_old['State'] == state, 'Winner'] = 'Biden'
    elif averages_old[averages_old['State'] == state]['Biden'].values[0] == averages_old[averages_old['State'] == state]['Trump'].values[0]:
        averages_old.loc[averages_old['State'] == state, 'Winner'] = 'Tie'
    else:
        averages_old.loc[averages_old['State'] == state, 'Winner'] = 'Trump'

poll_averages_old = averages_old

# calcualte biden lead for each state
poll_averages_old['Lead'] = poll_averages_old['Biden'] - poll_averages_old['Trump']


# # get true results for each state
# true_results = pd.read_csv('true_results.csv')

# # merge the true results with the polling averages old
# merged_old = pd.merge(poll_averages_old, true_results, on='State', how='left')

# # calculate the error for each state (difference between True Lead and Lead)

# merged_old['Error'] = merged_old['Difference'] - merged_old['Lead']

# # save only state and Error as a csv
# merged_old[['State', 'Error']].to_csv('2020_error.csv', index=False)


# get true results for each state
true_results = pd.read_csv('true_results2.csv')

# merge the true results with the polling averages old
merged_old = pd.merge(poll_averages_old, true_results, on='State', how='left')

# calculate the error for each state (difference between True Lead and Lead)

merged_old['Error'] = merged_old['Difference'] - merged_old['Lead']

# save only state and Error as a csv
merged_old[['State', 'Error']].to_csv('2020_error2.csv', index=False)