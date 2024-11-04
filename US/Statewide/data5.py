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


def extract_latest_date(date_range):
    parts = date_range.split(' ')
    parts2 = parts[1].split('–')
    if len(parts2) == 1:
        parts2 = parts[1].split('−')
    if len(parts2) == 1:
        parts2 = ['blank', parts[1]]
    if len(parts) == 3:
        return parts2[1] + ' ' + parts[0] + ' ' + parts[-1]
    else:
        return parts[4] + ' ' + parts[3] + ' ' + parts[-1]

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

# states = ['Iowa']
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
    parties = ['Harris', 'Trump']
    d = {}
    for i in range(len(df)):
        if state == "Minnesota":
            z = 'Kamala Harris DFL'
        elif state == "North Dakota":
            z = 'Kamala Harris Democratic-NPL'
        else:
            z = 'Kamala Harris Democratic'
        if z in df[i].columns:
            y = 'Dates updated'
            if y in df[i].columns:
                i +=1
            d[i] = pd.DataFrame(df[i])
            d[i] = d[i].drop(["Margin of error"], axis=1)

            # Drop Rows with Poll Sources that contain the word Rasmussen or Trafalgar
            # d[i] = d[i][~d[i]['Poll source'].str.contains('Rasmussen' ,na=False)]
            # d[i] = d[i][~d[i]['Poll source'].str.contains('Trafalgar' ,na=False)]
            # d[i] = d[i][~d[i]['Poll source'].str.contains('McLaughlin ' ,na=False)]
            d[i] = d[i][~d[i]['Poll source'].str.contains('\\(R\\)' ,na=False)]
            d[i] = d[i][~d[i]['Poll source'].str.contains('Emerson' ,na=False)]
            d[i] = d[i][~d[i]['Poll source'].str.contains('AtlasIntel' ,na=False)]
            d[i] = d[i][~d[i]['Poll source'].str.contains('Patriot Polling' ,na=False)]
            d[i] = d[i][~d[i]['Poll source'].str.contains('\\(D\\)' ,na=False)]
            d[i] = d[i].drop(["Poll source"], axis=1)

            # psub the column headers to remove the citation numbers
            for z in d[i].columns:
                d[i].rename(columns={z: p.sub('', z)}, inplace=True)
            d[i] = d[i].drop("Sample size", axis=1)
            d[i] = d[i].iloc[:, :3]
            # rename the columns to the headers we want
            # if 
            d[i].rename(columns={d[i].columns[0]: 'Date'}, inplace=True)
            z = 'Kamala Harris Democratic'
            z1 = 'Kamala Harris DFL'
            z2 = 'Donald Trump Republican'
            z3 = 'Donald J. Trump Republican'
            z4 = 'Kamala Harris Democratic-NPL'
            if z in d[i].columns:
                d[i].rename(columns={z: 'Harris'}, inplace=True)
            if z1 in d[i].columns:
                d[i].rename(columns={z1: 'Harris'}, inplace=True)
            if z2 in d[i].columns:
                d[i].rename(columns={z2: 'Trump'}, inplace=True)
            if z3 in d[i].columns:
                d[i].rename(columns={z3: 'Trump'}, inplace=True)
            if z4 in d[i].columns:
                d[i].rename(columns={z4: 'Harris'}, inplace=True)
            for z in parties:
                d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
                d[i][z] = [x.replace('-', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('—', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('–', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('TBC', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('TBA', str(np.NaN)) for x in d[i][z]]
                d[i][z] = [x.replace('?', str(np.NaN)) for x in d[i][z]]
            d[i]['Date2'] = [extract_latest_date(x) for x in d[i]['Date']]
            d[i]['Date2'] = [x.replace(',','') for x in d[i]['Date2']]
            d[i]['Date'] = d[i]['Date2']
            d[i] = d[i].drop(['Date2'], axis=1)
            d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
        if len(d) == 2:
            break
    if len(d) == 0:
        return pd.DataFrame()
    else:
            D = pd.concat(d.values(), ignore_index=True)
    # only keep the first table of the dictionary, which might not be 0
    for z in parties:
        D[z] = D[z].astype(str)
        D[z] = D[z].str.strip('%')
        # D[z] = D[z].astype('float')
        D[z] = pd.to_numeric(D[z], errors='coerce')
    
    # drop rows where both Harris and Trump are NaN
    D = D.dropna(subset=['Harris', 'Trump'], how='all')
    D = D.dropna(subset=['Trump'], how='all')
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
# polls[polls['State'] == 'Iowa']








# ONLY THE POLLED STATES

# drop all polls before Biden's withdrawal on July 21, 2024
dropout = dateparser.parse('July 01, 2024', settings={'PREFER_DAY_OF_MONTH': 'first'})
polls = polls[polls['Date'] >= dropout]

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware','District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


# create list of max d


# Class a winner based on the 14 day average since the most recent poll for each state
dates = polls.groupby('State')['Date'].max()
dates
fourteen_days_before = dates - pd.Timedelta(days=3)

# check polls for Nevada

averages = pd.DataFrame(columns=['State', 'Harris', 'Trump', 'Winner'])
for state in states:
    if state not in polls['State'].unique():
        continue
    averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Harris': [polls[(polls['State']== state) & (polls['Date'] >= fourteen_days_before[state])]['Harris'].mean().round(10)], 'Trump': [polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Trump'].mean().round(10)]})])    
    if averages[averages['State'] == state]['Harris'].values[0] > averages[averages['State'] == state]['Trump'].values[0]:
        averages.loc[averages['State'] == state, 'Winner'] = 'Harris'
    elif averages[averages['State'] == state]['Harris'].values[0] == averages[averages['State'] == state]['Trump'].values[0]:
        averages.loc[averages['State'] == state, 'Winner'] = 'Tie'
    else:
        averages.loc[averages['State'] == state, 'Winner'] = 'Trump'

poll_averages = averages
# round the polling averages to 2 decimal places


Red_States = ['Alabama', 'Arkansas', 'Idaho', 'Indiana','Kansas','Kentucky','Louisiana','Mississippi','Missouri','Montana','Nebraska','North Dakota','Oklahoma','South Carolina','South Dakota','Tennessee','Utah','West Virginia','Wyoming']
# Red_States.extend(['Alaska','Texas','Florida','Ohio','Iowa','North Carolina'])
Blue_States = ['California','Connecticut','Delaware','District of Columbia','Hawaii','Illinois','Maryland','Massachusetts','New York','Rhode Island','Vermont','Washington']
# Blue_States.extend(['Colorado','New Jersey','New Mexico','Oregon','Virginia','Minnesota','New Hampshire'])
Swing_States = []

for state in states:
    if state not in Red_States and state not in Blue_States:
        Swing_States.append(state)

# Assume Blue States will go to Harris and Red States will go to Trump and set the rest to Tie, as long as they are not in the averages dataframe

for state in states:
    if state not in averages['State'].values:
        if state in Blue_States:
            averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['Harris']})])
        elif state in Red_States:
            averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['Trump']})])
        else:
            # averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['Tie']})])
            averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['No Polling Data']})])

# Add winner 2 where Tie and No Polling Data are the same for the map
averages['Winner2'] = averages['Winner']
averages.loc[averages['Winner'] == 'No Polling Data', 'Winner2'] = 'Tie'

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
Harris_votes = averages[averages['Winner'] == 'Harris']['votes'].sum()
trump_votes = averages[averages['Winner'] == 'Trump']['votes'].sum()
tie_votes = averages[averages['Winner'] == 'Tie']['votes'].sum()
no_data = averages[averages['Winner'] == 'No Polling Data']['votes'].sum()

# I have added the cb_2018_us_state_500k files into the same folder as this file
usa = gpd.read_file(os.path.join(os.path.dirname(__file__), 'cb_2018_us_state_500k.shp'))
# AttributeError: The geopandas.dataset has been deprecated and was removed in GeoPandas 1.0. You can get the original 'naturalearth_lowres' data from https://www.naturalearthdata.com/downloads/110m-cultural-vectors/.
# so we will load
usa.loc[usa['NAME'] == 'Hawai‘i', 'NAME'] = 'Hawaii'
usa.loc[usa['NAME'] == 'Alaska', 'NAME'] = 'Alaska'

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

usa.plot(column='Winner2', ax=ax, legend=True, cmap='bwr', edgecolor='black')
# plt.title('2024 US Presidential Election Polling taking the most recent poll for each state', fontsize=16, fontname='Times New Roman', fontweight='bold')
plt.title('2024 US Presidential Election Polling taking the 3 day average from the most recent poll for each state', fontsize=16, fontname='Times New Roman', fontweight='bold')
# make state outlines black
usa.boundary.plot(ax=ax, color='black', linewidth=0.5)
plt.axis('off')
plt.xlim(-150, -55)
plt.ylim(20, 50)
plt.text(-137, 45, f'Harris: {Harris_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='blue')
plt.text(-137, 42.5, f'Tied: {tie_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='white')
plt.text(-137, 40, f'Trump: {trump_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='red')
# plt.text(-137, 37.5, f'No Polling: {no_data}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='#333333')

plt.legend().remove()
# change background color to grey

# usa[usa['Winner'] == 'No Polling Data'].plot(ax=ax, color='#333333')

fig.patch.set_facecolor('darkgrey')
plt.savefig(os.path.join(os.path.dirname(__file__), 'polling_map_New_Version.png'), bbox_inches='tight', dpi= 1000)

# print the range of dates for the polling data from the dates and fourteen_days_before dataframes, in %B %d, %Y format

state_abbr = {}

for state in states:
    state_abbr[state] = usa[usa['NAME'] == state]['STUSPS'].values[0]

for state in states:
    if state not in polls['State'].unique():
        continue
    print(f'{state_abbr[state]}: {dates[state].strftime("%d %b %Y")}')

for state in states:
    if state not in polls['State'].unique():
        continue
    print(f'{state_abbr[state]}: {fourteen_days_before[state].strftime("%d")}-{dates[state].strftime("%d %b %Y")}')

# Calculate Harris lead in each state
averages['Lead'] = averages['Harris'] - averages['Trump']

# find largest lead for scaling

max = np.max(np.abs(averages['Lead']))
# max = np.max(averages['Lead'])
# min = np.min(averages['Lead'])
# round max up to nearest even number and min down to nearest even number
max = np.ceil(max*100)/100
min = -max


from matplotlib.colors import TwoSlopeNorm
norm = TwoSlopeNorm(vmin=min, vcenter=0, vmax=max)


# Change to 1 for Blue States, -1 for Red States, 0 for Swing States if there is a NaN value

# for state in states:
#     if pd.isna(averages[averages['State'] == state]['Lead'].values[0]) == False:
#         pass
#     elif state in Blue_States:
#         averages.loc[averages['State'] == state, 'Lead'] = max+0.1
#     elif state in Red_States:
#         averages.loc[averages['State'] == state, 'Lead'] = -max-0.1
#     else:
#         averages.loc[averages['State'] == state, 'Lead'] = 0

#set limits to be the rounding up of the max value to nearest 0.01
# lim = np.round(max+0.1, 2)
# if max+0.1 > lim:
#     lim += 0.01

# all states without polling data will be classes as No Polling Data
for state in states:
    if pd.isna(averages[averages['State'] == state]['Lead'].values[0]) == False:
        pass
    else:
        averages.loc[averages['State'] == state, 'Winner'] = 'No Polling Data'

# save averages to a pickle file
averages.to_pickle(os.path.join(os.path.dirname(__file__), 'polling_averages.pkl'))

# Create Map of Harris Lead
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from shapely.geometry import Point
import os

usa = gpd.read_file(os.path.join(os.path.dirname(__file__), 'cb_2018_us_state_500k.shp'))
usa.loc[usa['NAME'] == 'Hawai‘i', 'NAME'] = 'Hawaii'
usa.loc[usa['NAME'] == 'Alaska', 'NAME'] = 'Alaska'

states.append('District of Columbia')
states.append('Hawaii')

usa = usa[usa.NAME.isin(states)]
usa = usa.merge(averages, left_on='NAME', right_on='State')

usa.loc[usa['NAME'] == 'Hawaii', 'geometry'] = usa[usa['NAME'] == 'Hawaii']['geometry'].translate(xoff=40, yoff=7.5)
usa.loc[usa['NAME'] == 'Alaska', 'geometry'] = usa[usa['NAME'] == 'Alaska']['geometry'].translate(xoff=-50, yoff=-35)
usa.loc[usa['NAME'] == 'Alaska', 'geometry'] = usa[usa['NAME'] == 'Alaska']['geometry'].scale(xfact=0.5, yfact=0.5)
usa.loc[usa['NAME'] == 'Hawaii', 'geometry'] = usa[usa['NAME'] == 'Hawaii']['geometry'].scale(xfact=1.5, yfact=1.5)

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
usa.plot(column='Lead', ax=ax, legend=True, cmap='bwr_r', edgecolor='black', norm=norm)
plt.title('2024 US Presidential Election Polling Harris Lead', fontsize=16, fontname='Times New Roman', fontweight='bold')
# make state outlines black
usa.boundary.plot(ax=ax, color='black', linewidth=0.5)
plt.axis('off')
plt.xlim(-150, -55)
plt.ylim(20, 50)
plt.legend().remove()
# change colorbar axis ticks to be in percentage format and have ticks at ever 1% interval and in Times New Roman font
cbar = ax.get_figure().get_axes()[1]
cbar.set_yticks(np.arange(min,max,0.02))
cbar.set_yticklabels([f'{x*100:.0f}%' for x in np.arange(min,max,0.02)], fontname='Times New Roman')
# resize colorbar to quarter the height
cbar.set_position([0.7, 0.25, 0.03, 0.5])

# Fill in states with no polling data with dark grey
usa[usa['Winner'] == 'No Polling Data'].plot(ax=ax, color='#333333')



# remove the colorbar legend
# cax = fig.get_axes()[1]
# cax.remove()

# change background color to grey
fig.patch.set_facecolor('darkgrey')
plt.savefig(os.path.join(os.path.dirname(__file__), 'polling_map_Harris_Lead.png'), bbox_inches='tight', dpi= 1000)









# ALL STATES PREDICTED

# drop all polls before Biden's withdrawal on July 21, 2024
dropout = dateparser.parse('July 01, 2024', settings={'PREFER_DAY_OF_MONTH': 'first'})
polls = polls[polls['Date'] >= dropout]

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware','District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


# create list of max d


# Class a winner based on the 14 day average since the most recent poll for each state
dates = polls.groupby('State')['Date'].max()
dates
fourteen_days_before = dates - pd.Timedelta(days=3)

averages = pd.DataFrame(columns=['State', 'Harris', 'Trump', 'Winner'])
for state in states:
    if state not in polls['State'].unique():
        continue
    # averages = averages.append({'State': state, 'Harris': polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Harris'].mean(), 'Trump': polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Trump'].mean()}, ignore_index=True)
    # causes error AttributeError: 'DataFrame' object has no attribute 'append' so replace with following line that works for pandas dataframes
    averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Harris': [polls[(polls['State']== state) & (polls['Date'] >= fourteen_days_before[state])]['Harris'].mean().round(10)], 'Trump': [polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Trump'].mean().round(10)]})])    
    if averages[averages['State'] == state]['Harris'].values[0] > averages[averages['State'] == state]['Trump'].values[0]:
        averages.loc[averages['State'] == state, 'Winner'] = 'Harris'
    elif averages[averages['State'] == state]['Harris'].values[0] == averages[averages['State'] == state]['Trump'].values[0]:
        averages.loc[averages['State'] == state, 'Winner'] = 'Tie'
    else:
        averages.loc[averages['State'] == state, 'Winner'] = 'Trump'
poll_averages = averages

Red_States = ['Alabama', 'Arkansas', 'Idaho', 'Indiana','Kansas','Kentucky','Louisiana','Mississippi','Missouri','Montana','Nebraska','North Dakota','Oklahoma','South Carolina','South Dakota','Tennessee','Utah','West Virginia','Wyoming']
Red_States.extend(['Alaska','Texas','Florida','Ohio','Iowa','North Carolina'])
Blue_States = ['California','Connecticut','Delaware','District of Columbia','Hawaii','Illinois','Maryland','Massachusetts','New York','Rhode Island','Vermont','Washington']
Blue_States.extend(['Colorado','New Jersey','New Mexico','Oregon','Virginia','Minnesota','New Hampshire'])
Swing_States = []

for state in states:
    if state not in Red_States and state not in Blue_States:
        Swing_States.append(state)

# Assume Blue States will go to Harris and Red States will go to Trump and set the rest to Tie, as long as they are not in the averages dataframe

for state in states:
    if state not in averages['State'].values:
        if state in Blue_States:
            averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['Harris']})])
        elif state in Red_States:
            averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['Trump']})])
        else:
            # averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['Tie']})])
            averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['No Polling Data']})])

# Add winner 2 where Tie and No Polling Data are the same for the map
averages['Winner2'] = averages['Winner']
averages.loc[averages['Winner'] == 'No Polling Data', 'Winner2'] = 'Tie'

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
Harris_votes = averages[averages['Winner'] == 'Harris']['votes'].sum()
trump_votes = averages[averages['Winner'] == 'Trump']['votes'].sum()
tie_votes = averages[averages['Winner'] == 'Tie']['votes'].sum()
no_data = averages[averages['Winner'] == 'No Polling Data']['votes'].sum()

# I have added the cb_2018_us_state_500k files into the same folder as this file
usa = gpd.read_file(os.path.join(os.path.dirname(__file__), 'cb_2018_us_state_500k.shp'))
# AttributeError: The geopandas.dataset has been deprecated and was removed in GeoPandas 1.0. You can get the original 'naturalearth_lowres' data from https://www.naturalearthdata.com/downloads/110m-cultural-vectors/.
# so we will load
usa.loc[usa['NAME'] == 'Hawai‘i', 'NAME'] = 'Hawaii'
usa.loc[usa['NAME'] == 'Alaska', 'NAME'] = 'Alaska'

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

usa.plot(column='Winner2', ax=ax, legend=True, cmap='bwr', edgecolor='black')
# plt.title('2024 US Presidential Election Polling taking the most recent poll for each state (States without polling projected)', fontsize=16, fontname='Times New Roman', fontweight='bold')
plt.title('2024 US Presidential Election Polling taking the 3 day average from the most recent poll for each state', fontsize=16, fontname='Times New Roman', fontweight='bold')
# make state outlines black
usa.boundary.plot(ax=ax, color='black', linewidth=0.5)
plt.axis('off')
plt.xlim(-150, -55)
plt.ylim(20, 50)
plt.text(-137, 45, f'Harris: {Harris_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='blue')
plt.text(-137, 42.5, f'Tied: {tie_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='white')
plt.text(-137, 40, f'Trump: {trump_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='red')
plt.legend().remove()
# change background color to grey
fig.patch.set_facecolor('darkgrey')
plt.savefig(os.path.join(os.path.dirname(__file__), 'polling_map_New_Version_2.png'), bbox_inches='tight', dpi= 1000)


averages['Lead'] = averages['Harris'] - averages['Trump']
averages = averages.sort_values('Lead', ascending=False)
for state in averages['State']:
    if state not in polls['State'].unique():
        continue
    # print up to 2 significant figures 
    if round(averages[averages['State'] == state]['Lead'].values[0], 3) == 0:
        print(f'{state_abbr[state]}: {100*averages[averages["State"] == state]["Lead"].values[0]:.4f}%')
    elif round(averages[averages['State'] == state]['Lead'].values[0], 100) == 0:
        print(f'{state_abbr[state]}: TIE')

    else:
        print(f'{state_abbr[state]}: {100*averages[averages["State"] == state]["Lead"].values[0]:.2f}%')


# load 2020 error csv
error = pd.read_csv(os.path.join(os.path.dirname(__file__), '2020_error2.csv'))

# merge error with averages
averages = averages.merge(error, left_on='State', right_on='State')

# calculate the adjusted lead for each state unless the state has no polling data

for state in states:
    if state not in averages['State'].values:
        continue
    averages.loc[averages['State'] == state, 'Adjusted_Lead'] = averages[averages['State'] == state]['Lead'].values[0] + averages[averages['State'] == state]['Error'].values[0]

# adjusted winners

for state in states:
    if state not in averages['State'].values:
        continue
    if averages[averages['State'] == state]['Adjusted_Lead'].values[0] > 0:
        averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Harris'
    elif averages[averages['State'] == state]['Adjusted_Lead'].values[0] == 0:
        averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Tie'
    elif averages[averages['State'] == state]['Adjusted_Lead'].values[0] < 0:
        averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Trump'
    else:
        if state in Blue_States:
            averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Harris'
        elif state in Red_States:
            averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Trump'
        else:
            averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Tie'
            
# create map of adjusted winner

Harris_votes = averages[averages['Adjusted_Winner'] == 'Harris']['votes'].sum()
trump_votes = averages[averages['Adjusted_Winner'] == 'Trump']['votes'].sum()
tie_votes = averages[averages['Adjusted_Winner'] == 'Tie']['votes'].sum()
no_data = averages[averages['Adjusted_Winner'] == 'No Polling Data']['votes'].sum()

usa = gpd.read_file(os.path.join(os.path.dirname(__file__), 'cb_2018_us_state_500k.shp'))
usa.loc[usa['NAME'] == 'Hawai‘i', 'NAME'] = 'Hawaii'
usa.loc[usa['NAME'] == 'Alaska', 'NAME'] = 'Alaska'

states.append('District of Columbia')
states.append('Hawaii')

usa = usa[usa.NAME.isin(states)]
usa = usa.merge(averages, left_on='NAME', right_on='State')

usa.loc[usa['NAME'] == 'Hawaii', 'geometry'] = usa[usa['NAME'] == 'Hawaii']['geometry'].translate(xoff=40, yoff=7.5)
usa.loc[usa['NAME'] == 'Alaska', 'geometry'] = usa[usa['NAME'] == 'Alaska']['geometry'].translate(xoff=-50, yoff=-35)
usa.loc[usa['NAME'] == 'Alaska', 'geometry'] = usa[usa['NAME'] == 'Alaska']['geometry'].scale(xfact=0.5, yfact=0.5)
usa.loc[usa['NAME'] == 'Hawaii', 'geometry'] = usa[usa['NAME'] == 'Hawaii']['geometry'].scale(xfact=1.5, yfact=1.5)

fig, ax = plt.subplots(1, 1, figsize=(15, 10))

usa.plot(column='Adjusted_Winner', ax=ax, legend=True, cmap='bwr', edgecolor='black')
# plt.title('2024 US Presidential Election Polling taking the most recent poll for each state (States without polling projected)', fontsize=16, fontname='Times New Roman', fontweight='bold')
plt.title('2024 US Presidential Election Polling taking the 3 day average from the most recent poll for each state (Adjusted for 2020 Error)', fontsize=16, fontname='Times New Roman', fontweight='bold')
# make state outlines black
usa.boundary.plot(ax=ax, color='black', linewidth=0.5)
plt.axis('off')
plt.xlim(-150, -55)
plt.ylim(20, 50)
plt.text(-137, 45, f'Harris: {Harris_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='blue')
plt.text(-137, 42.5, f'Tied: {tie_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='white')
plt.text(-137, 40, f'Trump: {trump_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='red')

plt.legend().remove()

# change background color to grey
fig.patch.set_facecolor('darkgrey')
plt.savefig(os.path.join(os.path.dirname(__file__), 'polling_map_Adjusted_Winner2.png'), bbox_inches='tight', dpi= 1000)


# REVERSE

averages['Lead'] = averages['Harris'] - averages['Trump']
averages = averages.sort_values('Lead', ascending=False)
for state in averages['State']:
    if state not in polls['State'].unique():
        continue
    # print up to 2 significant figures 
    if round(averages[averages['State'] == state]['Lead'].values[0], 3) == 0:
        print(f'{state_abbr[state]}: {100*averages[averages["State"] == state]["Lead"].values[0]:.4f}%')
    elif round(averages[averages['State'] == state]['Lead'].values[0], 100) == 0:
        print(f'{state_abbr[state]}: TIE')

    else:
        print(f'{state_abbr[state]}: {100*averages[averages["State"] == state]["Lead"].values[0]:.2f}%')



# calculate the adjusted lead for each state unless the state has no polling data

for state in states:
    if state not in averages['State'].values:
        continue
    averages.loc[averages['State'] == state, 'Adjusted_Lead'] = averages[averages['State'] == state]['Lead'].values[0] - averages[averages['State'] == state]['Error'].values[0]

# adjusted winners

for state in states:
    if state not in averages['State'].values:
        continue
    if averages[averages['State'] == state]['Adjusted_Lead'].values[0] > 0:
        averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Harris'
    elif averages[averages['State'] == state]['Adjusted_Lead'].values[0] == 0:
        averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Tie'
    elif averages[averages['State'] == state]['Adjusted_Lead'].values[0] < 0:
        averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Trump'
    else:
        if state in Blue_States:
            averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Harris'
        elif state in Red_States:
            averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Trump'
        else:
            averages.loc[averages['State'] == state, 'Adjusted_Winner'] = 'Tie'
            
# create map of adjusted winner

Harris_votes = averages[averages['Adjusted_Winner'] == 'Harris']['votes'].sum()
trump_votes = averages[averages['Adjusted_Winner'] == 'Trump']['votes'].sum()
tie_votes = averages[averages['Adjusted_Winner'] == 'Tie']['votes'].sum()
no_data = averages[averages['Adjusted_Winner'] == 'No Polling Data']['votes'].sum()

usa = gpd.read_file(os.path.join(os.path.dirname(__file__), 'cb_2018_us_state_500k.shp'))
usa.loc[usa['NAME'] == 'Hawai‘i', 'NAME'] = 'Hawaii'
usa.loc[usa['NAME'] == 'Alaska', 'NAME'] = 'Alaska'

states.append('District of Columbia')
states.append('Hawaii')

usa = usa[usa.NAME.isin(states)]
usa = usa.merge(averages, left_on='NAME', right_on='State')

usa.loc[usa['NAME'] == 'Hawaii', 'geometry'] = usa[usa['NAME'] == 'Hawaii']['geometry'].translate(xoff=40, yoff=7.5)
usa.loc[usa['NAME'] == 'Alaska', 'geometry'] = usa[usa['NAME'] == 'Alaska']['geometry'].translate(xoff=-50, yoff=-35)
usa.loc[usa['NAME'] == 'Alaska', 'geometry'] = usa[usa['NAME'] == 'Alaska']['geometry'].scale(xfact=0.5, yfact=0.5)
usa.loc[usa['NAME'] == 'Hawaii', 'geometry'] = usa[usa['NAME'] == 'Hawaii']['geometry'].scale(xfact=1.5, yfact=1.5)

fig, ax = plt.subplots(1, 1, figsize=(15, 10))

usa.plot(column='Adjusted_Winner', ax=ax, legend=True, cmap='bwr', edgecolor='black')
# plt.title('2024 US Presidential Election Polling taking the most recent poll for each state (States without polling projected)', fontsize=16, fontname='Times New Roman', fontweight='bold')
plt.title('2024 US Presidential Election Polling taking the 3 day average from the most recent poll for each state (Reverse Error)', fontsize=16, fontname='Times New Roman', fontweight='bold')
# make state outlines black
usa.boundary.plot(ax=ax, color='black', linewidth=0.5)
plt.axis('off')
plt.xlim(-150, -55)
plt.ylim(20, 50)
plt.text(-137, 45, f'Harris: {Harris_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='blue')
plt.text(-137, 42.5, f'Tied: {tie_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='white')
plt.text(-137, 40, f'Trump: {trump_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='red')

plt.legend().remove()

# change background color to grey
fig.patch.set_facecolor('darkgrey')
plt.savefig(os.path.join(os.path.dirname(__file__), 'polling_map_Adjusted_Winner_REVERSE.png'), bbox_inches='tight', dpi= 1000)



averages = pd.DataFrame(columns=['State', 'Harris', 'Trump', 'Winner'])
for state in states:
    if state not in polls['State'].unique():
        continue
    # averages = averages.append({'State': state, 'Harris': polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Harris'].mean(), 'Trump': polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Trump'].mean()}, ignore_index=True)
    # causes error AttributeError: 'DataFrame' object has no attribute 'append' so replace with following line that works for pandas dataframes
    averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Harris': [polls[(polls['State']== state) & (polls['Date'] >= fourteen_days_before[state])]['Harris'].mean().round(2)], 'Trump': [polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Trump'].mean().round(2)]})])    
    if averages[averages['State'] == state]['Harris'].values[0] > averages[averages['State'] == state]['Trump'].values[0]:
        averages.loc[averages['State'] == state, 'Winner'] = 'Harris'
    elif averages[averages['State'] == state]['Harris'].values[0] == averages[averages['State'] == state]['Trump'].values[0]:
        averages.loc[averages['State'] == state, 'Winner'] = 'Tie'
    else:
        averages.loc[averages['State'] == state, 'Winner'] = 'Trump'
poll_averages = averages

Red_States = ['Alabama', 'Arkansas', 'Idaho', 'Indiana','Kansas','Kentucky','Louisiana','Mississippi','Missouri','Montana','Nebraska','North Dakota','Oklahoma','South Carolina','South Dakota','Tennessee','Utah','West Virginia','Wyoming']
Red_States.extend(['Alaska','Texas','Florida','Ohio','Iowa','North Carolina'])
Blue_States = ['California','Connecticut','Delaware','District of Columbia','Hawaii','Illinois','Maryland','Massachusetts','New York','Rhode Island','Vermont','Washington']
Blue_States.extend(['Colorado','New Jersey','New Mexico','Oregon','Virginia','Minnesota','New Hampshire'])
Swing_States = []

for state in states:
    if state not in Red_States and state not in Blue_States:
        Swing_States.append(state)

# Assume Blue States will go to Harris and Red States will go to Trump and set the rest to Tie, as long as they are not in the averages dataframe

for state in states:
    if state not in averages['State'].values:
        if state in Blue_States:
            averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['Harris']})])
        elif state in Red_States:
            averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['Trump']})])
        else:
            # averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['Tie']})])
            averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Winner': ['No Polling Data']})])

# Add winner 2 where Tie and No Polling Data are the same for the map
averages['Winner2'] = averages['Winner']
averages.loc[averages['Winner'] == 'No Polling Data', 'Winner2'] = 'Tie'

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
Harris_votes = averages[averages['Winner'] == 'Harris']['votes'].sum()
trump_votes = averages[averages['Winner'] == 'Trump']['votes'].sum()
tie_votes = averages[averages['Winner'] == 'Tie']['votes'].sum()
no_data = averages[averages['Winner'] == 'No Polling Data']['votes'].sum()

# I have added the cb_2018_us_state_500k files into the same folder as this file
usa = gpd.read_file(os.path.join(os.path.dirname(__file__), 'cb_2018_us_state_500k.shp'))
# AttributeError: The geopandas.dataset has been deprecated and was removed in GeoPandas 1.0. You can get the original 'naturalearth_lowres' data from https://www.naturalearthdata.com/downloads/110m-cultural-vectors/.
# so we will load
usa.loc[usa['NAME'] == 'Hawai‘i', 'NAME'] = 'Hawaii'
usa.loc[usa['NAME'] == 'Alaska', 'NAME'] = 'Alaska'

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

usa.plot(column='Winner2', ax=ax, legend=True, cmap='bwr', edgecolor='black')
# plt.title('2024 US Presidential Election Polling taking the most recent poll for each state (States without polling projected)', fontsize=16, fontname='Times New Roman', fontweight='bold')
plt.title('2024 US Presidential Election Polling taking the 3 day average from the most recent poll for each state (Rounded to nearest %)', fontsize=16, fontname='Times New Roman', fontweight='bold')
# make state outlines black
usa.boundary.plot(ax=ax, color='black', linewidth=0.5)
plt.axis('off')
plt.xlim(-150, -55)
plt.ylim(20, 50)
plt.text(-137, 45, f'Harris: {Harris_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='blue')
plt.text(-137, 42.5, f'Tied: {tie_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='white')
plt.text(-137, 40, f'Trump: {trump_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='red')
plt.legend().remove()
# change background color to grey
fig.patch.set_facecolor('darkgrey')
plt.savefig(os.path.join(os.path.dirname(__file__), 'polling_map_New_Version_2(rounded).png'), bbox_inches='tight', dpi= 1000)

