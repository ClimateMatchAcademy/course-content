%matplotlib inline

def global_mean(ds:xr.Dataset) -> xr.Dataset:
    """Global average, weighted by the cell area"""
    return ds.weighted(ds.areacello.fillna(0)).mean(['x', 'y'], keep_attrs=True)

# average every dataset in the tree globally
dt_gm = dt_with_area.map_over_subtree(global_mean)


with plt.xkcd():
  for experiment in ['historical', 'ssp126', 'ssp585']:
      da = dt_gm['TaiESM1'][experiment].ds.tos
      da.plot(label=experiment)
  plt.title('Global Mean SST from TaiESM1')
  plt.ylabel('Global Mean SST [$^\circ$C]')
  plt.xlabel('Year')
  plt.legend()

plt.show()