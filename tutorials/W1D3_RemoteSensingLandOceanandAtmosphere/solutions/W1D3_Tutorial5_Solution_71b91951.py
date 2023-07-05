
# calculate 24-month rolling mean
grid_rolling_24m = grid_month.rolling(time=24, center=True).mean()

# plot all three time series together with different colors
fig = plt.figure(figsize=(12,6))
grid_month.plot(label='Monthly anomaly')
grid_rolling.plot(color='k', label='12-mon rolling mean')
grid_rolling_24m.plot(color='r', label='24-mon rolling mean')
plt.axhline(y=0, color='y', linestyle='-')
plt.ylabel('Precipitation Anomaly (mm/day)')
plt.legend()
# remove the automatically generated title
plt.title('')