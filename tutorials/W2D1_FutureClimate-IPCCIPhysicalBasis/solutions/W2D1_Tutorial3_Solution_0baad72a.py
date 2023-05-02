
# Calculate anomaly to reference period
def datatree_anomaly(dt):
    dt_out = DataTree()
    for model, subtree in dt.items():
        # Find the temporal average over the desired referene period
        ref = dt[model]['historical'].ds.sel(time=slice('1950', '1980')).mean()
        dt_out[model] = subtree - ref
    return dt_out

dt_gm_anomaly = datatree_anomaly(dt_gm)

with plt.xkcd():
  plot_historical_ssp126_combined(dt_gm_anomaly)

  plt.title('Global Mean SST Anomaly from five CMIP6 models (base period: 1950 to 1980)')
  plt.ylabel('Global Mean SST Anomaly [$^\circ$C]')
  plt.xlabel('Year')
  plt.legend()