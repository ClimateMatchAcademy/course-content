
# select data for the month of interest
data = ds.precip_error.sel(time='1979-01-01', method='nearest')

# initate plot
fig = plt.figure(figsize=(9,6))

# set map projection
ax = plt.axes(projection=ccrs.Robinson())

# add coastal lines to indicate land/ocean
ax.coastlines()

# add grid lines for latitude and longitute
ax.gridlines()

# add the precipitation data for
_ = data.plot(ax=ax, transform=ccrs.PlateCarree(),
          cbar_kwargs=dict(shrink=0.4, label='GPCP Monthly Precipitation Error\n(mm/day)'))