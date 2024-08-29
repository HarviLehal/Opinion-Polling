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

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

# states = ['Georgia']
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
    # some tables also show more than just Harris and Trump, so we need to remove them
    # also not every table is polling data, so we need to remove those as well, the first column of all polling tables is poll source, so we can use that to filter out the non polling tables
    # Also, Harris only comes first in the columns in states where he won the 2020 election, so use if statement to set headers accordingly
    if state in ['Arizona','California','Colorado', 'Connecticut', 'Delaware', 'Georgia', 'Hawaii', 'Illinois', 'Maine', 'Maryland', 'Massachusetts','Michigan','Minnesota','Nevada','New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'Oregon','Pennsylvania', 'Rhode Island', 'Vermont', 'Virginia', 'Washington','Wisconsin']:
        headers = ['Date', 'Harris', 'Trump']
        parties = ['Harris', 'Trump']
    else:
        headers = ['Date', 'Trump', 'Harris']
        parties = ['Trump', 'Harris']
    d = {}
    for i in range(len(df)):
        if state == "Minnesota":
            z = 'Kamala Harris DFL'
        # elif state == "Nevada":
        #     z = 'Kamala Harris .mw-parser-output .nobold{font-weight:normal}Democratic'
        else:
            z = 'Kamala Harris Democratic'
        if z in df[i].columns:
            # skip first accepted table for Florida as it is not polling data
            # if state == "Florida":
                # i += 2
            y = 'Dates updated'
            if y in df[i].columns:
                i +=1
            # if state == "Michigan" or state == "Pennsylvania" or state == "Wisconsin" or state == "Arizona" or state
                # i += 1
            d[i] = pd.DataFrame(df[i])
            if state == "Delaware" or state == "Michigan" or state == "North Carolina":
                d[i] = d[i].drop(["Poll source", "Sample size[c]", "Margin of error"], axis=1)
            elif state == "Arizona" or state == "California" or state == "Florida" or state == "Georgia" or state == "Illinois" or state == "Iowa" or state == "Massachusetts" or state == "Nevada" or state == "New Hampshire" or state == "Pennsylvania" or state == "Wisconsin":
                d[i] = d[i].drop(["Poll source", "Sample size[b]", "Margin of error"], axis=1)
            elif state == "Idaho" or state == "Indiana" or state == "North Dakota" or state == "West Virginia" or state == "Wyoming":
                d[i] = d[i].drop(["Poll source", "Sample size", "Margin of error"], axis=1)
            else:
                d[i] = d[i].drop(["Poll source", "Sample size[a]", "Margin of error"], axis=1)
            # the remaining first 3 columns are the date, Harris and trump, so we can rename them but remove the other columns for other candidates by only keeping the first 3
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
            # d[i]['Date2'] = (d[i]['Date'].str.split(' ').str[0] + ' ' + d[i]['Date'].str.split('–').str[1]).astype(str)
            # d[i]['Date2'] = [x if d[i]['Date2'][j] != 'nan' else d[i]['Date'][j] for j, x in enumerate(d[i]['Date2'])]
            d[i]['Date2'] = [extract_latest_date(x) for x in d[i]['Date']]
            d[i]['Date'] = d[i]['Date2']
            d[i] = d[i].drop(['Date2'], axis=1)
            d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
            # d[i] = d[i][d[i]['Harris'] != d[i]['Trump']]
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
        # D[z] = D[z].astype('float')
        D[z] = pd.to_numeric(D[z], errors='coerce')
    
    # drop rows where both Harris and Trump are NaN
    D = D.dropna(subset=['Harris', 'Trump'], how='all')
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








# ONLY THE POLLED STATES

# drop all polls before Biden's withdrawal on July 21, 2024
dropout = dateparser.parse('July 01, 2024', settings={'PREFER_DAY_OF_MONTH': 'first'})
polls = polls[polls['Date'] >= dropout]

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware','District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


# create list of max d


# Class a winner based on the 14 day average since the most recent poll for each state
dates = polls.groupby('State')['Date'].max()
dates
fourteen_days_before = dates - pd.Timedelta(days=7)

# check polls for Nevada
# polls[polls['State'] == 'Nevada']

averages = pd.DataFrame(columns=['State', 'Harris', 'Trump', 'Winner'])
for state in states:
    if state not in polls['State'].unique():
        continue
    # averages = averages.append({'State': state, 'Harris': polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Harris'].mean(), 'Trump': polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Trump'].mean()}, ignore_index=True)
    # causes error AttributeError: 'DataFrame' object has no attribute 'append' so replace with following line that works for pandas dataframes
    averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Harris': [polls[(polls['State']== state) & (polls['Date'] >= fourteen_days_before[state])]['Harris'].mean()], 'Trump': [polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Trump'].mean()]})])    
    if averages[averages['State'] == state]['Harris'].values[0] > averages[averages['State'] == state]['Trump'].values[0]:
        averages.loc[averages['State'] == state, 'Winner'] = 'Harris'
    elif averages[averages['State'] == state]['Harris'].values[0] == averages[averages['State'] == state]['Trump'].values[0]:
        averages.loc[averages['State'] == state, 'Winner'] = 'Tie'
    else:
        averages.loc[averages['State'] == state, 'Winner'] = 'Trump'
poll_averages = averages

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
plt.title('2024 US Presidential Election Polling taking the 7 day average from the most recent poll for each state', fontsize=16, fontname='Times New Roman', fontweight='bold')
# make state outlines black
usa.boundary.plot(ax=ax, color='black', linewidth=0.5)
plt.axis('off')
plt.xlim(-150, -55)
plt.ylim(20, 50)
plt.text(-137, 45, f'Harris: {Harris_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='blue')
plt.text(-137, 42.5, f'Tied: {tie_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='white')
plt.text(-137, 40, f'Trump: {trump_votes}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='red')
plt.text(-137, 37.5, f'No Polling: {no_data}', fontsize=12, fontname='Times New Roman', fontweight='bold', color='#333333')

plt.legend().remove()
# change background color to grey

usa[usa['Winner'] == 'No Polling Data'].plot(ax=ax, color='#333333')

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
fourteen_days_before = dates - pd.Timedelta(days=7)

averages = pd.DataFrame(columns=['State', 'Harris', 'Trump', 'Winner'])
for state in states:
    if state not in polls['State'].unique():
        continue
    # averages = averages.append({'State': state, 'Harris': polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Harris'].mean(), 'Trump': polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Trump'].mean()}, ignore_index=True)
    # causes error AttributeError: 'DataFrame' object has no attribute 'append' so replace with following line that works for pandas dataframes
    averages = pd.concat([averages, pd.DataFrame({'State': [state], 'Harris': [polls[(polls['State']== state) & (polls['Date'] >= fourteen_days_before[state])]['Harris'].mean()], 'Trump': [polls[(polls['State'] == state) & (polls['Date'] >= fourteen_days_before[state])]['Trump'].mean()]})])    
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
plt.title('2024 US Presidential Election Polling taking the 7 day average from the most recent poll for each state (States without polling projected)', fontsize=16, fontname='Times New Roman', fontweight='bold')
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

# print(polls[polls['State'] == 'Georgia'])