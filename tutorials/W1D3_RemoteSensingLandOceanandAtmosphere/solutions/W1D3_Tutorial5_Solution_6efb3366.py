
# calculate unweighted global mean
global_unweighted_mean = precip_anom.mean(('latitude', 'longitude'))

# calculate different between weighted and unweighted global mean
global_diff = global_weighted_mean - global_unweighted_mean

# plot the time series of the difference
fig = plt.figure(figsize=(12,6))
global_diff.rolling(time=12, center=True).mean(('latitude', 'longitude')).plot(color='k', label='12-mon rolling mean')
plt.axhline(y=0, color='y', linestyle='-')
plt.ylabel('Weighted Mean - Unweighted Mean')
plt.legend()