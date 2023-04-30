
def plot_historical_ssp126_combined(dt):
    for model in dt.keys():
        datasets = []
        for experiment in ['historical', 'ssp126']:
            datasets.append(dt[model][experiment].ds.tos)

        # For each of the models, concatenate its historical and future data
        da_combined = xr.concat(datasets, dim='time')
        # plot annual averages
        da_combined.coarsen(time=12).mean().plot(label=model)

with plt.xkcd():
  plot_historical_ssp126_combined(dt_gm)

  plt.title('Global Mean SST from five CMIP6 models (annually smoothed)')
  plt.ylabel('Global Mean SST [$^\circ$C]')
  plt.xlabel('Year')
  plt.legend()