#!/usr/bin/env python
# coding: utf-8

# # Computations and Masks with Xarray

# ---

# ## Overview
# 
# In this tutorial, we will cover the following topics:
# 
# 1. Performing basic arithmetic on `DataArrays` and `Datasets`
# 2. Performing aggregation (i.e., reduction) along single or multiple dimensions of a `DataArray` or `Dataset`
# 3. Computing climatologies and anomalies of data using Xarray's "split-apply-combine" approach, via the `.groupby()` method
# 4. Performing weighted-reduction operations along single or multiple dimensions of a `DataArray` or `Dataset`
# 5. Providing a broad overview of Xarray's data-masking capability
# 6. Using the `.where()` method to mask Xarray data

# ## Prerequisites
# 
# 
# | Concepts | Importance | Notes |
# | --- | --- | --- |
# | [Introduction to Xarray](xarray-intro) | Necessary | |
# 
# 
# - **Time to learn**: 60 minutes

# ---

# ## Imports
# 
# In order to work with data and plotting, we must import NumPy, Matplotlib, and Xarray. These packages are covered in greater detail in earlier tutorials. We also import a package that allows quick download of Pythia example datasets.

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from pythia_datasets import DATASETS


# ## Data Setup
# 
# The bulk of the examples in this tutorial make use of a single dataset. This dataset contains monthly sea surface temperature (SST, call 'tos' here) data, and is obtained from the Community Earth System Model v2 (CESM2). (For this tutorial, however, the dataset will be retrieved from the Pythia example data repository.) The following example illustrates the process of retrieving this Global Climate Model dataset:

# In[ ]:


filepath = DATASETS.fetch('CESM2_sst_data.nc')
ds = xr.open_dataset(filepath)
ds


# ## Arithmetic Operations
# 
# In a similar fashion to NumPy arrays, performing an arithmetic operation on a `DataArray` will automatically perform the operation on all array values; this is known as vectorization. To illustrate the process of vectorization, the following example converts the air temperature data from units of degrees Celsius to units of Kelvin:

# In[ ]:


ds.tos + 273.15


# In addition, there are many other arithmetic operations that can be performed on `DataArrays`. In this example, we demonstrate squaring the original Celsius values of our air temperature data:

# In[ ]:


ds.tos**2


# ## Aggregation Methods 
# 
# A common practice in the field of data analysis is aggregation. Aggregation is the process of reducing data through methods such as `sum()`, `mean()`, `median()`, `min()`, and `max()`, in order to gain greater insight into the nature of large datasets. In this set of examples, we demonstrate correct usage of a select group of aggregation methods:

# Compute the mean:

# In[ ]:


ds.tos.mean()


# Notice that we did not specify the `dim` keyword argument; this means that the function was applied over all of the dataset's dimensions. In other words, the aggregation method computed the mean of every element of the temperature dataset across every temporal and spatial data point. However, if a dimension name is used with the `dim` keyword argument, the aggregation method computes an aggregation along the given dimension. In this next example, we use aggregation to calculate the temporal mean across all spatial data; this is performed by providing the dimension name `'time'` to the `dim` keyword argument:

# In[ ]:


ds.tos.mean(dim='time').plot(size=7);


# There are many other combinations of aggregation methods and dimensions on which to perform these methods. In this example, we compute the temporal minimum:

# In[ ]:


ds.tos.min(dim=['time'])


# This example computes the spatial sum. Note that this dataset contains no altitude data; as such, the required spatial dimensions passed to the method consist only of latitude and longitude.

# In[ ]:


ds.tos.sum(dim=['lat', 'lon'])


# For the last example in this set of aggregation examples, we compute the temporal median:

# In[ ]:


ds.tos.median(dim='time')


# In addition, there are many other commonly used aggregation methods in Xarray. Some of the more popular aggregation methods are summarized in the following table:
# 
# | Aggregation              | Description                     |
# |--------------------------|---------------------------------|
# | ``count()``              | Total number of items           |
# | ``mean()``, ``median()`` | Mean and median                 |
# | ``min()``, ``max()``     | Minimum and maximum             |
# | ``std()``, ``var()``     | Standard deviation and variance |
# | ``prod()``               | Compute product of elements            |
# | ``sum()``                | Compute sum of elements                |
# | ``argmin()``, ``argmax()``| Find index of minimum and maximum value |

# ## GroupBy: Split, Apply, Combine
# 
# While we can obtain useful summaries of datasets using simple aggregation methods, it is more often the case that aggregation must be performed over coordinate labels or groups. In order to perform this type of aggregation, it is helpful to use the **split-apply-combine** workflow. Fortunately, Xarray provides this functionality for `DataArrays` and `Datasets` by means of the `groupby` operation. The following figure illustrates the split-apply-combine workflow in detail:
# 
# <img src="./images/xarray-split-apply-combine.jpeg">
# 
# Based on the above figure, you can understand the split-apply-combine process performed by `groupby`. In detail, the steps of this process are:
# 
# - The split step involves breaking up and grouping an xarray `Dataset` or `DataArray` depending on the value of the specified group key.
# - The apply step involves computing some function, usually an aggregate, transformation, or filtering, within the individual groups.
# - The combine step merges the results of these operations into an output xarray `Dataset` or `DataArray`.
# 
# In this set of examples, we will remove the seasonal cycle (also known as a climatology) from our dataset using `groupby`. There are many types of input that can be provided to `groupby`; a full list can be found in [Xarray's `groupby` user guide](https://xarray.pydata.org/en/stable/user-guide/groupby.html).

# In this first example, we plot data to illustrate the annual cycle described above. We first select the grid point closest to a specific latitude-longitude point. Once we have this grid point, we can plot a temporal series of sea-surface temperature (SST) data at that location. Reviewing the generated plot, the annual cycle of the data becomes clear.

# In[ ]:


ds.tos.sel(lon=310, lat=50, method='nearest').plot();


# ### Split
# 
# The first step of the split-apply-combine process is splitting. As described above, this step involves splitting a dataset into groups, with each group matching a group key. In this example, we split the SST data using months as a group key. Therefore, there is one resulting group for January data, one for February data, etc. This code illustrates how to perform such a split:

# In[ ]:


ds.tos.groupby(ds.time.dt.month)


# <div class="admonition alert alert-info">
# 
# In the above code example, we are extracting components of date/time data by way of the time coordinate's `.dt` attribute. This attribute is a `DatetimeAccessor` object that contains additional attributes for units of time, such as hour, day, and year. Since we are splitting the data into monthly data, we use the `month` attribute of .dt in this example. (In addition, there exists similar functionality in Pandas; see the [official documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.html) for details.)
#     
#    </div>

# In addition, there is a more concise syntax that can be used in specific instances. This syntax can be used if the variable on which the grouping is performed is already present in the dataset. The following example illustrates this syntax; it is functionally equivalent to the syntax used in the above example.

# In[ ]:


ds.tos.groupby('time.month')


# ### Apply & Combine 
# 
# Now that we have split our data into groups, the next step is to apply a calculation to the groups. There are two types of calculation that can be applied:
# 
# - aggregation: reduces the size of the group
# - transformation: preserves the group's full size
# 
# After a calculation is applied to the groups, Xarray will automatically combine the groups back into a single object, completing the split-apply-combine workflow.
# 
# 
# 
# #### Compute climatology 
# 
# 
# In this example, we use the split-apply-combine workflow to calculate the monthly climatology at every point in the dataset. Notice that we are using the `month` `DatetimeAccessor`, as described above, as well as the `.mean()` aggregation function:
# 

# In[ ]:


tos_clim = ds.tos.groupby('time.month').mean()
tos_clim


# Now that we have a `DataArray` containing the climatology data, we can plot the data in different ways. In this example, we plot the climatology at a specific latitude-longitude point:

# In[ ]:


tos_clim.sel(lon=310, lat=50, method='nearest').plot();


# In this example, we plot the zonal mean climatology:

# In[ ]:


tos_clim.mean(dim='lon').transpose().plot.contourf(levels=12, cmap='turbo');


# Finally, this example calculates and plots the difference between the climatology for January and the climatology for December:

# In[ ]:


(tos_clim.sel(month=1) - tos_clim.sel(month=12)).plot(size=6, robust=True);


# #### Compute anomaly
# 
# In this example, we compute the anomaly of the original data by removing the climatology from the data values. As shown in previous examples, the climatology is first calculated. The calculated climatology is then removed from the data using arithmetic and Xarray's `groupby` method:

# In[ ]:


gb = ds.tos.groupby('time.month')
tos_anom = gb - gb.mean(dim='time')
tos_anom


# In[ ]:


tos_anom.sel(lon=310, lat=50, method='nearest').plot();


# In this example, we compute and plot our dataset's mean global anomaly over time. In order to specify global data, we must provide both `lat` and `lon` to the `mean()` method's `dim` keyword argument:

# In[ ]:


unweighted_mean_global_anom = tos_anom.mean(dim=['lat', 'lon'])
unweighted_mean_global_anom.plot();


# <div class="admonition alert alert-warning">
#    
# 
# Many geoscientific algorithms perform operations over data contained in many different grid cells. However, if the grid cells are not equivalent in size, the operation is not scientifically valid by default. Fortunately, this can be fixed by weighting the data in each grid cell by the size of the cell. Weighting data in Xarray is simple, as Xarray has a built-in weighting method, known as [`.weighted()`](https://xarray.pydata.org/en/stable/user-guide/computation.html#weighted-array-reductions).
# 
# </div>
# 

# In this example, we again make use of the Pythia example data library to load a new CESM2 dataset. Contained in this dataset are weights corresponding to the grid cells in our anomaly data:

# In[ ]:


filepath2 = DATASETS.fetch('CESM2_grid_variables.nc')
areacello = xr.open_dataset(filepath2).areacello
areacello


# In a similar fashion to a previous example, this example calculates mean global anomaly. However, this example makes use of the `.weighted()` method and the newly loaded CESM2 dataset to weight the grid cell data as described above:

# In[ ]:


weighted_mean_global_anom = tos_anom.weighted(areacello).mean(dim=['lat', 'lon'])


# This example plots both unweighted and weighted mean data, which illustrates the degree of scientific error with unweighted data:

# In[ ]:


unweighted_mean_global_anom.plot(size=7)
weighted_mean_global_anom.plot()
plt.legend(['unweighted', 'weighted']);


# ## Other high level computation functionality
# 
# - `resample`: [This method behaves similarly to groupby, but is specialized for time dimensions, and can perform temporal upsampling and downsampling.](https://xarray.pydata.org/en/stable/user-guide/time-series.html#resampling-and-grouped-operations)
# - `rolling`: [This method is used to compute aggregation functions, such as `mean`, on moving windows of data in a dataset.](https://xarray.pydata.org/en/stable/user-guide/computation.html#rolling-window-operations)
# - `coarsen`: [This method provides generic functionality for performing downsampling operations on various types of data.](https://xarray.pydata.org/en/stable/user-guide/computation.html#coarsen-large-arrays)

# This example illustrates the resampling of a dataset's time dimension to annual frequency:

# In[ ]:


r = ds.tos.resample(time='AS')
r


# In[ ]:


r.mean()


# This example illustrates using the `rolling` method to compute averages in a moving window of 5 months of data:

# In[ ]:


m_avg = ds.tos.rolling(time=5, center=True).mean()
m_avg


# In[ ]:


lat = 50
lon = 310

m_avg.isel(lat=lat, lon=lon).plot(size=6)
ds.tos.isel(lat=lat, lon=lon).plot()
plt.legend(['5-month moving average', 'monthly data']);


# ## Masking Data
# 

# Masking of data can be performed in Xarray by providing single or multiple conditions to either Xarray's `.where()` method or a `Dataset` or `DataArray`'s `.where()` method. Data values matching the condition(s) are converted into a single example value, effectively masking them from the scientifically important data. In the following set of examples, we use the `.where()` method to mask various data values in the `tos` `DataArray`.

# For reference, we will first print our entire sea-surface temperature (SST) dataset:

# In[ ]:


ds


# ### Using `where` with one condition

# In this set of examples, we are trying to analyze data at the last temporal value in the dataset. This first example illustrates the use of `.isel()` to perform this analysis:

# In[ ]:


sample = ds.tos.isel(time=-1)
sample


# As shown in the previous example, methods like `.isel()` and `.sel()` return data of a different shape than the original data provided to them. However, `.where()` preserves the shape of the original data by masking the values with a Boolean condition. Data values for which the condition is `True` are returned identical to the values passed in. On the other hand, data values for which the condition is `False` are returned as a preset example value. (This example value defaults to `nan`, but can be set to other values as well.)
# 
# Before testing `.where()`, it is helpful to look at the [official documentation](http://xarray.pydata.org/en/stable/generated/xarray.DataArray.where.html). As stated above, the `.where()` method takes a Boolean condition. (Boolean conditions use operators such as less-than, greater-than, and equal-to, and return a value of `True` or `False`.) Most uses of `.where()` check whether or not specific data values are less than or greater than a constant value. As stated in the documentation, the data values specified in the Boolean condition of `.where()` can be any of the following:
# 
# - a `DataArray`
# - a `Dataset`
# - a function
# 
# In the following example, we make use of `.where()` to mask data with temperature values greater than `0`. Therefore, values greater than `0` are set to `nan`, as described above. (It is important to note that the Boolean condition matches values to keep, not values to mask out.)

# In[ ]:


masked_sample = sample.where(sample < 0.0)
masked_sample


# In this example, we use Matplotlib to plot the original, unmasked data, as well as the masked data created in the previous example.

# In[ ]:


fig, axes = plt.subplots(ncols=2, figsize=(19, 6))
sample.plot(ax=axes[0])
masked_sample.plot(ax=axes[1]);


# ### Using `where` with multiple conditions

# Those familiar with Boolean conditions know that such conditions can be combined by using logical operators. In the case of `.where()`, the relevant logical operators are bitwise or exclusive `'and'` (represented by the `&` symbol) and bitwise or exclusive 'or' (represented by the `|` symbol). This allows multiple masking conditions to be specified in a single use of `.where()`; however, be aware that if multiple conditions are specified in this way, each simple Boolean condition must be enclosed in parentheses. (If you are not familiar with Boolean conditions, or this section is confusing in any way, please review a detailed Boolean expression guide before continuing with the tutorial.) In this example, we provide multiple conditions to `.where()` using a more complex Boolean condition. This allows us to mask locations with temperature values less than 25, as well as locations with temperature values greater than 30. (As stated above, the Boolean condition matches values to keep, and everything else is masked out. Because we are now using more complex Boolean conditions, understanding the following example may be difficult. Please review a Boolean condition guide if needed.)

# In[ ]:


sample.where((sample > 25) & (sample < 30)).plot(size=6);


# In addition to using `DataArrays` and `Datasets` in Boolean conditions provided to `.where()`, we can also use coordinate variables. In the following example, we make use of Boolean conditions containing `latitude` and `longitude` coordinates. This greatly simplifies the masking of regions outside of the [Niño 3.4 region](https://www.ncdc.noaa.gov/teleconnections/enso/indicators/sst/):
# 
# ![](https://www.ncdc.noaa.gov/monitoring-content/teleconnections/nino-regions.gif)
# 
# 

# In[ ]:


sample.where(
    (sample.lat < 5) & (sample.lat > -5) & (sample.lon > 190) & (sample.lon < 240)
).plot(size=6);


# ### Using `where` with a custom fill value

# In the previous examples that make use of `.where()`, the masked data values are set to `nan`. However, this behavior can be modified by providing a second value, in numeric form, to `.where()`; if this numeric value is provided, it will be used instead of `nan` for masked data values. In this example, masked data values are set to `0` by providing a second value of `0` to the `.where()` method:

# In[ ]:


sample.where((sample > 25) & (sample < 30), 0).plot(size=6);


# ---

# ## Summary 
# 
# - In a similar manner to NumPy arrays, performing arithmetic on a `DataArray` affects all values simultaneously.
# - Xarray allows for simple data aggregation, over single or multiple dimensions, by way of built-in methods such as `sum()` and `mean()`.
# - Xarray supports the useful split-apply-combine workflow through the `groupby` method.
# - Xarray allows replacing (masking) of data matching specific Boolean conditions by means of the `.where()` method.
# 
# ### What's next?
# 
# The next tutorial illustrates the use of previously covered Xarray concepts in a geoscientifically relevant example: plotting the [Niño 3.4 Index](https://climatedataguide.ucar.edu/climate-data/nino-sst-indices-nino-12-3-34-4-oni-and-tni).

# ## Resources and References
# 
# - `groupby`: [Useful for binning/grouping data and applying reductions and/or transformations on those groups](https://xarray.pydata.org/en/stable/user-guide/groupby.html)
# - `resample`: [Functionality similar to groupby, specialized for time dimensions. Can be used for temporal upsampling and downsampling](https://xarray.pydata.org/en/stable/user-guide/time-series.html#resampling-and-grouped-operations)
# - `rolling`: [Useful for computing aggregations on moving windows of your dataset, e.g., computing moving averages](https://xarray.pydata.org/en/stable/user-guide/computation.html#rolling-window-operations)
# - `coarsen`: [Generic functionality for downsampling data](https://xarray.pydata.org/en/stable/user-guide/computation.html#coarsen-large-arrays)
# 
# - `weighted`: [Useful for weighting data before applying reductions](https://xarray.pydata.org/en/stable/user-guide/computation.html#weighted-array-reductions)
# 
# - [More xarray tutorials and videos](https://xarray.pydata.org/en/stable/tutorials-and-videos.html)
# - [Xarray Documentation - Masking with `where()`](https://xarray.pydata.org/en/stable/user-guide/indexing.html#masking-with-where)
