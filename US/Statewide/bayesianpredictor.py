'''
    This file is used to simulate the US elections using the polling averages for each state
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from scipy.stats import norm
from tqdm import tqdm

Red_States = ['Alabama', 'Arkansas', 'Idaho', 'Indiana','Kansas','Kentucky','Louisiana','Mississippi','Missouri','Montana','Nebraska','North Dakota','Oklahoma','South Carolina','South Dakota','Tennessee','Utah','West Virginia','Wyoming']
Red_States.extend(['Alaska','Texas','Florida','Ohio','Iowa','North Carolina'])
Blue_States = ['California','Connecticut','Delaware','District of Columbia','Hawaii','Illinois','Maryland','Massachusetts','New York','Rhode Island','Vermont','Washington']
Blue_States.extend(['Colorado','New Jersey','New Mexico','Oregon','Virginia','Minnesota','New Hampshire'])

# Load the pickle file
df = pd.read_pickle('US/Statewide/polling_averages.pkl')

# take the polls 

# Function to simulate the election

def simulate_election(df, n_simulations, sigma=0.1):
    results = []
    # Initialize the number of electoral votes for each candidate
    electoral_votes = {'Harris': 0, 'Trump': 0}
    # Loop through each state
    for iter in tqdm(range(n_simulations)):
        for i in range(len(df)):
            # exclude states with No Polling Data in Winner column
            if df.iloc[i]['Winner'] == 'No Polling Data':
                if df.iloc[i]['State'] in Red_States:
                    electoral_votes['Trump'] += df.iloc[i]['votes']

                elif df.iloc[i]['State'] in Blue_States:
                    electoral_votes['Harris'] += df.iloc[i]['votes']
            else:
                # Get the state name
                state = df.iloc[i]['State']
                # using the polling average, simulate the election with a random walk
                # Get the polling average
                harris_poll = df.iloc[i]['Harris']
                trump_poll = df.iloc[i]['Trump']
                # Simulate the election
                harris_votes = np.random.normal(harris_poll, sigma)
                trump_votes = np.random.normal(trump_poll, sigma)
                # Update the electoral votes
                if harris_votes > trump_votes:
                    electoral_votes['Harris'] += df.iloc[i]['votes']
                else:
                    electoral_votes['Trump'] += df.iloc[i]['votes']
        results.append(electoral_votes.copy())
        electoral_votes = {'Harris': 0, 'Trump': 0}
        
    return results

# margin of error in polls tends to be 5% so convert to standard deviation

N = 100000
sigma = 0.05
# Run the simulation
results = simulate_election(df, n_simulations=N, sigma=sigma)

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)
# Calculate the probability of winning
harris_wins = (results_df['Harris'] > 269).mean()
trump_wins = (results_df['Trump'] > 269).mean()
# convert to percentage
harris_wins = harris_wins * 100
trump_wins = trump_wins * 100

# Plot the results
plt.figure(figsize=(10, 6))
plt.axvline(x=269, color='black', linestyle='--')
# use same bins for both histograms
# united results
union = []
for i in range(len(results_df)):
    union.append(results_df.iloc[i]['Harris'])
    union.append(results_df.iloc[i]['Trump'])
bins = np.histogram_bin_edges(union, bins=50)
sns.histplot(results_df['Harris'], kde=True, color='blue', label='Harris', alpha=0.5, bins=bins)
sns.histplot(results_df['Trump'], kde=True, color='red', label='Trump', alpha=0.5, bins=bins)
# add win probability text
min = np.min(union)
max = np.max(union)

plt.text(max-80, 5000, f'P(Harris Wins) = {harris_wins:.2f}%', fontsize=12, color='blue') 
plt.text(min+10, 5000, f'P(Trump Wins) = {trump_wins:.2f}%', fontsize=12, color='red')
plt.xlabel('Electoral Votes')
plt.ylabel('Frequency')
plt.title(f'Simulated US Election Results using 7-day Polling Averages, $N=100,000$ & $\sigma=0.05$')
plt.legend()
plt.show()
