'''
This file will plot a gaussian distribution of the polling data for each party from the csv file for the UK general election for the last 14 days.
'''
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import poisson
import seaborn as sns
import numpy as np
import dateparser


# Read the csv file
# data = pd.read_csv('UK/general_polling/poll.csv')
data = pd.read_csv('UK/constituency_results/harborough_results/data.csv')

data = data*100




# Get the polling data for the last 14 days
# Get the polling data for each party
conservative = data['Con'].values
labour = data['Lab'].values
lib_dem = data['Lib Dem'].values
Other = data['Other'].values
green = data['Green'].values
reform = data['Reform'].values
# drop all nan values
conservative = conservative[~np.isnan(conservative)]
labour = labour[~np.isnan(labour)]
lib_dem = lib_dem[~np.isnan(lib_dem)]
Other = Other[~np.isnan(Other)]
green = green[~np.isnan(green)]
reform = reform[~np.isnan(reform)]

# Plot the gaussian distribution for each party
plt.figure(figsize=(12,6))
plt.title('Gaussian Distributions of the Seat Projection Polling for Harborough, Oadby and Wigston')
plt.xlabel('Percentage')
plt.ylabel('Density')

# Plot the gaussian distribution for Conservative
mu, std = norm.fit(conservative)
# xmin, xmax = plt.xlim()
x = np.linspace(0, 100, 1000)
p_c_o = norm.pdf(x, mu, std)
# remove p_c values below 0.001 and the corresponding x values so that the plot is not cluttered but still shows the distribution in the correct range
p_c = p_c_o[p_c_o > 0.0001]
x_c = x[p_c_o > 0.0001]
# remove specific x values that correspond to the p_c values that were removed, so that the plot is still in the correct x range

plt.plot(x_c, p_c, linewidth=2, label='Conservative', color= "#0077b6")
plt.fill_between(x_c, p_c, where=(x_c >= mu-1.65*std) & (x_c <= mu+1.65*std), color="#0077b6", alpha=0.5)

# Plot the gaussian distribution for Labour
mu, std = norm.fit(labour)
# xmin, xmax = plt.xlim()
p_l_0 = norm.pdf(x, mu, std)
p_l = p_l_0[p_l_0 > 0.0001]
x_l = x[p_l_0 > 0.0001]
plt.plot(x_l, p_l, linewidth=2, label='Labour', color= "#c70000")
plt.fill_between(x_l, p_l, where=(x_l >= mu-1.65*std) & (x_l <= mu+1.65*std), color="#c70000", alpha=0.5)

# Plot the gaussian distribution for the Liberal Democrats
mu, std = norm.fit(lib_dem)
# xmin, xmax = plt.xlim()
p_ld_o = norm.pdf(x, mu, std)
p_ld = p_ld_o[p_ld_o > 0.0001]
x_ld = x[p_ld_o > 0.0001]
plt.plot(x_ld, p_ld, linewidth=2, label='Liberal Democrats', color= "#e05e00")
plt.fill_between(x_ld, p_ld, where=(x_ld >= mu-1.65*std) & (x_ld <= mu+1.65*std), color="#e05e00", alpha=0.5)

# Plot the poisson distribution for the Other
mu, std = norm.fit(Other)
# xmin, xmax = plt.xlim()
p_Other_o = norm.pdf(x, mu, std)
p_Other = p_Other_o[p_Other_o > 0.0001]
x_Other = x[p_Other_o > 0.0001]
plt.plot(x_Other, p_Other, linewidth=2, label='Other', color= "#000000")
plt.fill_between(x_Other, p_Other, where=(x_Other >= mu-1.65*std) & (x_Other <= mu+1.65*std), color="#000000", alpha=0.5)
print(mu)
print(Other.mean())
print(std)
print(Other.std())


# Plot the gaussian distribution for the Green Party
mu, std = norm.fit(green)
if std == 0:
  std=1
# xmin, xmax = plt.xlim()
p_g_o = norm.pdf(x, mu, std)
p_g = p_g_o[p_g_o > 0.0001]
x_g = x[p_g_o > 0.0001]
plt.plot(x_g, p_g, linewidth=2, label='Green Party', color= "#528D6B")
plt.fill_between(x_g, p_g, where=(x_g >= mu-1.65*std) & (x_g <= mu+1.65*std), color="#528D6B", alpha=0.5)

# Plot the gaussian distribution for the Reform Party
mu, std = norm.fit(reform)
# xmin, xmax = plt.xlim()
p_r_o = norm.pdf(x, mu, std)
p_r = p_r_o[p_r_o > 0.0001]
x_r = x[p_r_o > 0.0001]
plt.plot(x_r, p_r, linewidth=2, label='Reform Party', color= "#12B6CF")
plt.fill_between(x_r, p_r, where=(x_r >= mu-1.65*std) & (x_r <= mu+1.65*std), color="#12B6CF", alpha=0.5)

plt.grid()
# show x ticks in percentage for every 1% and rotate 90 degrees
plt.xticks(np.arange(0, 61, 1))
plt.yticks(np.arange(0, 1, 0.1))
plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
plt.gca().set_xticklabels(['{:.0f}%'.format(x) for x in plt.gca().get_xticks()])
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}%'.format(x*100)))
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}%'.format(x)))
plt.gca().tick_params(axis='x', rotation=-90)
plt.gca().tick_params(axis='y', rotation=0)

# plot the mean value of each party as a label at the top of each gaussian distribution with the 95% confidence interval in brackets below it
plt.text(conservative.mean(), p_c.max()+0.01, f'{conservative.mean():.2f}% \n ({conservative.mean()-1.65*conservative.std():.2f}%, {conservative.mean()+1.65*conservative.std():.2f}%)', color= "#0077b6", ha='center')
plt.text(labour.mean(), p_l.max()+0.01, f'{labour.mean():.2f}% \n ({labour.mean()-1.65*labour.std():.2f}%, {labour.mean()+1.65*labour.std():.2f}%)', color= "#c70000", ha='center')
plt.text(lib_dem.mean(), p_ld.max()+0.11, f'{lib_dem.mean():.2f}% \n ({lib_dem.mean()-1.65*lib_dem.std():.2f}%, {lib_dem.mean()+1.65*lib_dem.std():.2f}%)', color= "#e05e00", ha='center')
plt.text(Other.mean(), p_Other.max()+0.01, f'{Other.mean():.2f}% \n ({Other.mean()-1.65*Other.std():.2f}%, {Other.mean()+1.65*Other.std():.2f}%)', color= "#000000", ha='center')
plt.text(green.mean(), p_g.max()+0.01, f'{green.mean():.2f}% \n ({green.mean()-1.65*green.std():.2f}%, {green.mean()+1.65*green.std():.2f}%)', color= "#528D6B", ha='center')
plt.text(reform.mean(), p_r.max()+0.01, f'{reform.mean():.2f}% \n ({reform.mean()-1.65*reform.std():.2f}%, {reform.mean()+1.65*reform.std():.2f}%)', color= "#12B6CF", ha='center')

plt.legend()
# tight layout but make sure axis ticks start at 0 and 0
plt.tight_layout()
plt.ylim(0, 1)
plt.xlim(0, 60)
plt.savefig('UK/constituency_results/harborough_results/distribution.png')
