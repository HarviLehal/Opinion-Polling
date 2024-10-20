"""
Scrape statewide polling for the 2024 United States presidential election from Wikipedia.
Some states have multiple tables, so we will need to concatenate them.
Some states also have other candidates, so we will need to remove them.
# THIS IS A NEW VERSION OF THE FILE THAT WILL LOOK AT HARRIS VS TRUMP SINCE BIDEN DROPPED OUT
"""

import dateparser
import re
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


def get_state_polls(state):
    print("Getting polls for " + state)
    if state == "Washington":
        wikiurl = f"https://en.wikipedia.org/wiki/2024_United_States_presidential_election_in_{state}_(state)"
    else:
        wikiurl = f"https://en.wikipedia.org/wiki/2024_United_States_presidential_election_in_{state}"
    table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(wikiurl)
    # print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', class_="wikitable")
    df = pd.read_html(str(tables))
    p = re.compile(r'\[[a-z]+\]')
    # some states have multiple tables, so we need to concatenate them
    # some tables also show more than just Biden and Trump, so we need to remove them
    # also not every table is polling data, so we need to remove those as well, the first column of all polling tables is poll source, so we can use that to filter out the non polling tables
    # Also, Biden only comes first in the columns in states where he won the 2020 election, so use if statement to set headers accordingly
    if state in ['Arizona','California','Colorado', 'Connecticut', 'Delaware','Georgia', 'Hawaii', 'Illinois', 'Maine', 'Maryland', 'Massachusetts','Michigan','Minnesota','Nevada','New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'Oregon','Pennsylvania', 'Rhode Island', 'Vermont', 'Virginia', 'Washington','Wisconsin']:
        headers = ['Date', 'Harris', 'Trump']
        parties = ['Harris', 'Trump']
    else:
        headers = ['Date', 'Trump', 'Harris']
        parties = ['Trump', 'Harris']
    d = {}
    for i in range(len(df)):
        if 'Kamala Harris Democratic' in df[i].columns:
            # skip first accepted table for Florida as it is not polling data
            # if state == "Florida" and i == 1:
                # i += 2
            d[i] = pd.DataFrame(df[i])
            if state == "Delaware":
                d[i] = d[i].drop(["Poll source", "Sample size[c]", "Margin of error"], axis=1)
            elif state == "Florida" or state == "Illinois" or state == "Iowa" or state == "Massachusetts" or state == "Nevada" or state == "North Carolina" or state == "Florida":
                d[i] = d[i].drop(["Poll source", "Sample size[b]", "Margin of error"], axis=1)
            elif state == "Idaho" or state == "Indiana" or state == "North Dakota" or state == "West Virginia" or state == "Wyoming":
                d[i] = d[i].drop(["Poll source", "Sample size", "Margin of error"], axis=1)
            else:
                d[i] = d[i].drop(["Poll source", "Sample size[a]", "Margin of error"], axis=1)
            # the remaining first 3 columns are the date, biden and trump, so we can rename them but remove the other columns for other candidates by only keeping the first 3
            d[i] = d[i].iloc[:, :3]
            d[i].columns = headers
            for z in parties:
                d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
                d[i][z] = [x.replace('-', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('—', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('–', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('TBC', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('TBA', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('?', str(np.NaN)) for x in d[i][z]]
            d[i]['Date2'] = d[i]['Date'].str.split('–').str[0] + ' ' + d[i]['Date'].str.split(',').str[1]
            d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
            # add the year to end of the date using the second part of the split of ,
            # for x in d[i]['Date2']:
                # d[i]['Date2'] = d[i]['Date'] + ' ' + d[i]['Date'].str.split(',')[1]
            # d[i]['Date2'] = [x.split(',')[0] if len(x.split(',')) > 1 else x for x in d[i]['Date2'].astype(str)]
            # d[i].Date2.fillna(d[i].Date, inplace=True)
            # d[i]['Date2'] = [x + ' ' + str(2024) for x in d[i]['Date2'].astype(str)]
            d[i]['Date'] = d[i]['Date2']
            d[i] = d[i].drop(['Date2'], axis=1)
            d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
            # d[i] = d[i][d[i]['Biden'] != d[i]['Trump']]
            # stop loop once we have found the first polling table
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
        D[z] = D[z].astype('float')
    D['total']=D[parties].sum(axis=1)
    D['Harris'] = D['Harris']/D['total']
    D['Trump'] = D['Trump']/D['total']
    D = D.drop(['total'], axis=1)
    D['State'] = state
    return D

def get_all_polls():
    polls = pd.DataFrame()
    for state in states:
        polls = pd.concat([polls, get_state_polls(state)])
    return polls

polls = get_all_polls()

allstates = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
states = ['Arizona', 'California','Florida', 'Georgia','Michigan','Nevada', 'New Hampshire','North Carolina','Ohio','Pennsylvania','Texas', 'Virginia', 'Washington', 'Wisconsin']

# Class a winner based on the 14 day average since the most recent poll for each state
dates = polls.groupby('State')['Date'].max()
fourteen_days_before = dates - pd.Timedelta(days=14)

averages = pd.DataFrame(columns=['State', 'Harris', 'Trump', 'Winner'])
for state in states:
    # averages = averages.append({'State': state, 'Biden': polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Biden'].mean(), 'Trump': polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Trump'].mean()}, ignore_index=True)
    # causes error AttributeError: 'DataFrame' object has no attribute 'append' so replace with following line that works for pandas dataframes
    averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Harris': [polls[(polls['State']== state) & (polls['Date'] >= fourteen_days_before[state])]['Harris'].mean()], 'Trump': [polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Trump'].mean()]})])    
    if averages[averages['State'] == state]['Harris'].values[0] > averages[averages['State'] == state]['Trump'].values[0]:
        averages.loc[averages['State'] == state, 'Winner'] = 'Harris'
    elif averages[averages['State'] == state]['Harris'].values[0] == averages[averages['State'] == state]['Trump'].values[0]:
        averages.loc[averages['State'] == state, 'Winner'] = 'Tie'
    else:
        averages.loc[averages['State'] == state, 'Winner'] = 'Trump'


# Add in States with no polling data
       
# make strong republican states red and strong democrat states blue and swing states white
for state in allstates:
    if state not in states:
        if state in ['Alabama', 'Alaska', 'Arkansas', 'Idaho', 'Indiana', 'Kansas', 'Kentucky', 'Louisiana', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'North Dakota', 'Oklahoma', 'South Carolina', 'South Dakota', 'Tennessee', 'Utah', 'West Virginia', 'Wyoming']:
            averages = pd.concat([averages, pd.DataFrame({'State': [state],'Winner': ['Trump']})])
        elif state in ['California', 'Connecticut', 'Delaware', 'District of Columbia', 'Hawaii', 'Illinois', 'Maryland', 'Massachusetts', 'New York', 'Rhode Island', 'Vermont', 'Washington']:
            averages = pd.concat([averages, pd.DataFrame({'State': [state],'Winner': ['Harris']})])
        else:
            averages = pd.concat([averages, pd.DataFrame({'State': [state],'Winner': ['Tie'] })])

# Assume the District of Columbia will go to Biden as they do not have polling data
averages = pd.concat([averages, pd.DataFrame({'State': ['District of Columbia'], 'Winner': ['Harris']})])

# Also assume Hawaii will go to Biden as they do not have polling data
averages = pd.concat([averages, pd.DataFrame({'State': ['Hawaii'], 'Winner': ['Harris']})])

# add the number of electoral voters for each state
electoral_votes = pd.read_csv(os.path.join(os.path.dirname(__file__), 'electoral_votes.csv'))
averages = averages.merge(electoral_votes, left_on='State', right_on='State')


# create a map of the US with the states colored by the winner of the most recent poll
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from shapely.geometry import Point
import os

# take total number of electoral votes for each candidate
harris_votes = averages[averages['Winner'] == 'Harris']['votes'].sum()
trump_votes = averages[averages['Winner'] == 'Trump']['votes'].sum()
tie_votes = averages[averages['Winner'] == 'Tie']['votes'].sum()

# I have added the cb_2018_us_state_500k files into the same folder as this file
usa = gpd.read_file(os.path.join(os.path.dirname(__file__), 'cb_2018_us_state_500k.shp'))
# AttributeError: The geopandas.dataset has been deprecated and was removed in GeoPandas 1.0. You can get the original 'naturalearth_lowres' data from https://www.naturalearthdata.com/downloads/110m-cultural-vectors/.
# so we will load
usa.loc[usa['NAME'] == 'Hawai‘i', 'NAME'] = 'Hawaii'
usa.loc[usa['NAME'] == 'Alaska', 'NAME'] = 'Alaska'

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
states.append('District of Columbia')
states.append('Hawaii')

usa = usa[usa.NAME.isin(states)]
usa = usa.merge(averages, left_on='NAME', right_on='State')
# this is not merging properly so we need to see which states are not merging properly

# rename Hawaii to Hawaii so it works
# move Hawaii and Alaska to the bottom left
usa.loc[usa['NAME'] == 'Hawaii', 'geometry'] = usa[usa['NAME'] == 'Hawaii']['geometry'].translate(xoff=40, yoff=7.5)
usa.loc[usa['NAME'] == 'Alaska', 'geometry'] = usa[usa['NAME'] == 'Alaska']['geometry'].translate(xoff=-50, yoff=-35)
usa.loc[usa['NAME'] == 'Alaska', 'geometry'] = usa[usa['NAME'] == 'Alaska']['geometry'].scale(xfact=0.5, yfact=0.5)
usa.loc[usa['NAME'] == 'Hawaii', 'geometry'] = usa[usa['NAME'] == 'Hawaii']['geometry'].scale(xfact=1.5, yfact=1.5)

fig, ax = plt.subplots(1, 1, figsize=(15, 10))

usa.plot(column='Winner', ax=ax, legend=True, cmap='bwr', edgecolor='black')
plt.title('2024 US Presidential Election Polling taking the 14 day average from the most recent poll for each state', fontsize=16, fontname='Times New Roman', fontweight='bold')
# make state outlines black
usa.boundary.plot(ax=ax, color='black', linewidth=0.5)
plt.axis('off')
plt.xlim(-150, -55)
plt.ylim(20, 50)
plt.text(-135, 45, f'Harris: {harris_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='blue')
plt.text(-135, 42.5, f'Tie: {tie_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='white')
plt.text(-135, 40, f'Trump: {trump_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='red')
plt.legend().remove()
# change background color to grey
fig.patch.set_facecolor('darkgrey')
plt.savefig(os.path.join(os.path.dirname(__file__), 'polling_map_HARRIS.png'), bbox_inches='tight', dpi= 1000)
