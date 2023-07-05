%matplotlib inline

for experiment, color in zip(['historical', 'ssp126', 'ssp585'], ['C0', 'C1', 'C2']):
    datasets = []
    for model in dt_gm_anomaly.keys():
        annual_sst = dt_gm_anomaly[model][experiment].ds.tos.coarsen(time=12).mean().assign_coords(source_id=model)
        datasets.append(annual_sst.sel(time=slice(None, '2100')).load()) # the french model has a long running member for ssp126
    da = xr.concat(datasets, dim='source_id', join='override').squeeze()
    x = da.time.data
    # Calculate the lower bound of the likely range
    da_lower = da.squeeze().quantile(0.17, dim='source_id')
    # Calculate the upper bound of the likely range
    da_upper = da.squeeze().quantile(0.83, dim='source_id')
    # plt.fill_between(range(x), da_lower, da_upper,  alpha=0.5, color=color)
    # Calculate the multi-model mean at each time within each experiment
    _ = da.mean('source_id').plot(color=color, label=experiment)
plt.title('Global Mean SST Anomaly from five-member CMIP6 ensemble (base period: 1950 to 1980)')
plt.ylabel('Global Mean SST Anomaly [$^\circ$C]')
plt.xlabel('Year')
plt.legend()

plt.show()