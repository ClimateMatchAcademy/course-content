#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W1D2_StateoftheClimateOceanandAtmosphereReanalysis/instructor/W1D2_Tutorial1.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W1D2_StateoftheClimateOceanandAtmosphereReanalysis/instructor/W1D2_Tutorial1.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 1: Calculating ENSO with Xarray**
# 
# 
# **Week 1, Day 2, Ocean-Atmosphere Reanalysis**
# 
# **Content creators:** Abigail Bodner, Momme Hell, Aurora Basinski
# 
# **Content reviewers:** Yosemley Bermúdez, Katrina Dobson, Danika Gupta, Maria Gonzalez, Will Gregory, Nahid Hasan, Sherry Mi, Beatriz Cosenza Muralles, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS and Google deepmind

# # **Tutorial Objectives**
# 
# In this notebook (adapted from [Project Pythia](https://foundations.projectpythia.org/core/xarray/enso-xarray.html)), you will practice using multiple tools to examine sea surface temperature (SST) and explore variations in the climate system that occur during El Nino and La Nina events. You will learn to:
# 
# 1. Load Sea Surface Temprature data from the CESM2 model
# 2. Mask data using `.where()`
# 3. Compute climatologies and anomalies using `.groupby()`
# 4. Use `.rolling()` to compute moving average
# 5. Compute, normalize, and plot the Oceanic Niño Index
# 
# After completing the tasks above, you should be able to plot [Oceanic Niño Index](https://climatedataguide.ucar.edu/climate-data/nino-sst-indices-nino-12-3-34-4-oni-and-tni) that looks similar to the figure below. The red and blue regions correspond to the phases of El Niño and La Niña respectively.
# 
# ![ONI index plot from NCAR Climate Data Guide](https://climatedataguide.ucar.edu/sites/default/files/styles/extra_large/public/2022-03/indices_oni_2_2_lg.png)
# 
# Credit: [NCAR](https://climatedataguide.ucar.edu/sites/default/files/styles/extra_large/public/2022-03/indices_oni_2_2_lg.png)
# 
# Pythia credit: Rose, B. E. J., Kent, J., Tyle, K., Clyne, J., Banihirwe, A., Camron, D., May, R., Grover, M., Ford, R. R., Paul, K., Morley, J., Eroglu, O., Kailyn, L., & Zacharias, A. (2023). Pythia Foundations (Version v2023.05.01) https://zenodo.org/record/8065851
# 
# 

# # **Setup** 
# 

# In[ ]:


# !pip install pythia_datasets
# !pip install cartopy
# !pip install geoviews


# In[ ]:


# imports
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr
from pythia_datasets import DATASETS
import cartopy.io.shapereader as shapereader
import pandas as pd
import matplotlib.dates as mdates
import geoviews as gv
import geoviews.feature as gf


# ##  Video 1:
# 

# ###  Video 1:
# 

# In[ ]:


# @title Video 1:
# tech team will add code to format and display the video


# # **Section 1: Introduction to El Niño Southern Oscillation (ENSO)**
# In W1D1 you practiced using `Xarray` to calculate a monthly climatology, climate anomalies, and a running average on monthly global Sea Surface Temperature (SST) data from the Community Earth System Model v2 (CESM2). You also used the `.where()` method to isolate SST data between **5ºN-5ºS and 190ºE-240ºE (or 170ºW-120ºW)**. This geographic region, known as the **Niño 3.4 region**, is in the tropical Pacific Ocean and is commonly used as a metric for determining the phase of the El Niño-Southern Oscillation (ENSO). ENSO is a recurring climate pattern involving changes in SST in the central and eastern tropical Pacific Ocean, which has two alternating phases:
# 
# *   **El Niño:** the phase of ENSO characterized by warmer than average SSTs in the central and eastern tropical Pacific Ocean, weakened east to west equatorial winds and increased rainfall in the eastern tropical Pacific. 
# *   **La Niña:** the phase of ENSO which is characterized by cooler than average SSTs in the central and eastern tropical Pacific Ocean, stronger east to west equatorial winds and decreased rainfall in the eastern tropical Pacific.
# 
# ## **Section 1.1: Tropical Pacific Climate Processes**
# To better understand the climate system processes that result in El Niño and La Niña events, let's first consider typical climate conditions in the tropical Pacific Ocean. Recall from W1D1, **trade winds** are winds that blow east to west just north and south of the equator (these are sometimes referred to as "easterly" winds since the winds are originating from the east and blowing toward the west). And as we discussed yesterday, the reason that the trade winds blow from east to west is related to Earth's rotation, which causes the winds in the Northern Hemisphere to curve to the right and winds in the Southern Hemisphere to curve to the left. This is known as the **Coriolis effect**. 
# 
# If Earth's rotation affects air movement, do you think it also influences surface ocean water movement? It does! As trade winds blow across the tropical Pacific Ocean, they move water because of friction at the ocean surface. But because of the Coriolis effect, surface water moves to the right of the wind direction in the Northern Hemisphere and to the left of the wind direction in the Southern Hemisphere. However, the speed and direction of water movement changes with depth. Ocean surface water moves at an angle to the wind, and the water under the surface water moves at a slightly larger angle, and the water below that turns at an even larger angle. The average direction of all this turning water is about a right angle from the wind direction. This average is known as **Ekman transport**. Since this process is driven by the trade winds, the strength of this ocean water transport varies in response to changes in the strength of the trade winds. 
# 
# 
# ## **Section 1.2: Ocean-Atmosphere Interactions During El Niño and La Niña**
# So, how does all of this relate to El Niño and La Niña? Changes in the strength of Pacific Ocean trade winds and the resulting impact on Ekman transport create variations in the tropical Pacific Ocean SST, which further results in changes to atmospheric circulation patterns and rainfall.
# 
# During an El Niño event, ***easterly trade winds are weaker***. As a result, less warm surface water is  transported to the west via Ekman transport, which causes a build-up of warm surface water in the eastern equatorial Pacific. This creates warmer than average SSTs in the eastern equatorial Pacific Ocean. The atmosphere responds to this warming with increased rising air motion and above-average rainfall in the eastern Pacific. In contrast, during a La Niña event, ***easterly trade winds are stronger***. As a result, more warm surface water is transported to the west via Ekman transport, and cool water from deeper in the ocean rises up in the eastern Pacific during a process known as upwelling. This creates cooler than average SSTs in the eastern equatorial Pacific Ocean. This cooling decreases rising air movement in the eastern Pacific, resulting in drier than average conditions. 
# 
# 
# In this tutorial, we'll examine SST temperatures to explore variations in the climate system that occur during El Niño and La Niña events. Specifically, we will plot and interpret CESM2 SST data from the Niño 3.4 region.

# # **Section 2: Calculate the Oceanic Niño Index**

# In this notebook, we are going to combine several topics and methods you've covered so far to compute the [Oceanic Niño Index](https://climatedataguide.ucar.edu/climate-data/nino-sst-indices-nino-12-3-34-4-oni-and-tni) using SST from the CESM2 submission to the [CMIP6 project](https://esgf-node.llnl.gov/projects/cmip6/). 
# 
# To calculate the Oceanic Niño Index you will:
# 
#    1. Select SST data from Niño 3.4 region of 5ºN-5ºS and 190ºE-240ºE (or 170ºW-120ºW) shown in the figure below.
#    
#    ![](https://www.ncdc.noaa.gov/monitoring-content/teleconnections/nino-regions.gif)
#    
#    2. Compute the climatology (here from 2000-2014) for the Niño 3.4 region.
#    3. Compute the monthly anomaly for the Niño 3.4 region.
#    4. Compute the area-weighted mean of the anomalies for the Niño 3.4 region to obtain a time series.
#    4. Smooth the time series of anomalies with a 3-month running mean.
#    
# Here we will briefly move through each of these steps, and tomorrow you will learn about them in more detail.

# ## **Section 2.1: Open the SST Data**

# First, open the SST and areacello datasets, and use Xarray's `merge` method to combine them into a single dataset:

# In[ ]:


# retrive (fetch) the SST data we are going to be working on
SST_path = DATASETS.fetch('CESM2_sst_data.nc')

# open the file we acquired with xarray
SST_data = xr.open_dataset(SST_path)

# remember that one degree spatial cell is not constant around the globe, each is a different size in square km.
# we need to account for this when taking averages for example

# fetch the weight for each grid cell
gridvars_path = DATASETS.fetch('CESM2_grid_variables.nc')

# open and save only the gridcell weights whose variable name is 'areacello'
# here the 'o' at the end refers to the area cells of the 'ocean' grid
areacello_data = xr.open_dataset(gridvars_path).areacello

# merge the SST and weights into one easy to use dataset - ds stands for dataset
ds_SST = xr.merge([SST_data, areacello_data])
ds_SST


# Visualize the first time point in the early 2000s. You can check this on the indexes of the variable 'time' from the ds_SST above. Note that using the `plot` function of our dataarray will automatically include this as a title when we select just the first time index.

# In[ ]:


# define the plot size
fig = plt.figure(figsize=(12, 6))

# asssign axis and define the projection -  for a round plot
ax = plt.axes(projection=ccrs.Robinson(central_longitude=180))

#add coastlines - this will issue a download warning but that is ok
ax.coastlines()

# add gridlines (lon and lat)
ax.gridlines()

# plots the first time index (0) of SST (variable name 'tos') at the first time
ds_SST.tos.isel(time=0).plot(
    ax=ax, transform=ccrs.PlateCarree(), # give our axis a map projection
    vmin=-2, vmax=30,                    # define the temp range of the colorbarfrom -2 to 30C
    cmap='coolwarm'                      # choose a colormap
)


# ### **Interactive Demo 2.1**

# You can visualize what the next few times look like in the model by using the interactive sliderbar below.

# In[ ]:


# a bit more complicated code that allows interactive plots
gv.extension('bokeh') #load Bokeh
dataset_plot = gv.Dataset(ds_SST.isel(time=slice(0,10))) # slice only the first 10 timepoint, as it is a time consuming task
images = dataset_plot.to(gv.Image, ['longitude', 'latitude'], 'tos', 'time')
images.opts(cmap='coolwarm', colorbar=True, width=600, height=400,projection=ccrs.Robinson(),clabel='Sea Surface Temperature [˚C]') * gf.coastline


# ## **Section 2.2: Select the Niño 3.4 Region**
# 
# You may have noticed that the `lon` for the SST data is organized between 0°–360°E.

# In[ ]:


ds_SST.lon


# This is different from how we typically use `longitude` (-180°–180°). How do we covert the value of longitude between two systems (0-360° v.s. -180°–180°)?
# 
# Let's use `lon2` refer to the longitude system of `0°-360°` while `lon` refers to the system of `-180°–180°`. `0°-360°` is equivalent to `0–180°, -180°–0°`.
# 
# In other words, `lon2=181°` is same as `lon=-179°`. Hence, in the western hemisphere, `lon2=lon+360`.
# 
# Therefore, the Niño 3.4 region should be (-5°–5°, 190–240°) using the `lon2` system.
# 
# Now that we have identified the longitude values we need to select, there are a couple ways to select the Niño 3.4 region. We will demonstrate how to use both below.
# 
# 1. `sel()`

# In[ ]:


# select just the Nino 3.4 region (note our longitude values are in degrees east) by slicing
tos_nino34_op1 = ds_SST.sel(lat=slice(-5, 5), lon=slice(190, 240))
tos_nino34_op1


# 2. Use `where()` and select all values within the bounds of interest

# In[ ]:


# select just the Nino 3.4 region (note our longitude values are in degrees east) by boolean conditioning
tos_nino34_op2 = ds_SST.where(
    (ds_SST.lat < 5) & (ds_SST.lat > -5) & (ds_SST.lon > 190) & (ds_SST.lon < 240), drop=True
) # use dataset where function. use boolean commands
tos_nino34_op2


# You can verify that `tos_nino34_op1` and `tos_nino34_op2` are the same by comparing the lat and lon indexes.
# 
# We only need one of these, so let us choose the second option and set that to the variable we will use moving forward.

# In[ ]:


# SST in just the Nino 3.4 region
tos_nino34=tos_nino34_op2


# Let's utilize the same code we used to plot the entire Earth, but this time focusing on the Niño 3.4 region slice only.

# In[ ]:


# define the figure size
fig = plt.figure(figsize=(12, 6))

# assign axis and projection
ax = plt.axes(projection=ccrs.Robinson(central_longitude=180))

# add coastlines
ax.coastlines()

# add gridlines (lon and lat)
ax.gridlines()

# plot as above
tos_nino34.tos.isel(time=0).plot(
    ax=ax, transform=ccrs.PlateCarree(), vmin=-2, vmax=30, cmap='coolwarm'
)

# make sure we see more areas of the earth and not only the square around Niño 3.4
ax.set_extent((120, 300, 10, -10))


# ## **Section 2.3: Compute the Climatology and Anomalies**
# 
# Now that we have selected our area, we can compute the monthly anomaly by first grouping all the data by month, then substracting the monthly climatology from each month.

# In[ ]:


# group the dataset by month
tos_nino34_mon = tos_nino34.tos.groupby('time.month')

# find the monthly climatology in the Nino 3.4 region
tos_nino34_clim = tos_nino34_mon.mean(dim='time')

# find the monthly anomaly in the Nino 3.4 region
tos_nino34_anom = tos_nino34_mon - tos_nino34_clim

# take the area weighted average of anomalies in the Nino 3.4 region
tos_nino34_anom_mean = tos_nino34_anom.weighted(tos_nino34.areacello).mean(dim=['lat', 'lon'])
tos_nino34_anom_mean


# ## **Section 2.4: Smooth the Anomaly Time Series**

# ENSO occurs on interannual timescales (a few years or more). To isolate the variability of this longer-term phenomenon on the Niño 3.4 region, we can smooth out the fluctuations due to variability on shorter timescales. To achieve this, we will apply a 3-month running mean to our time series of SST anomalies.

# In[ ]:


# smooth using a centered 3 month running mean
oni_index = tos_nino34_anom_mean.rolling(time=3, center=True).mean()


# In[ ]:


# define the plot size
fig = plt.figure(figsize=(12, 6))

# assign axis
ax = plt.axes()

# plot the monhtly data on the assigned axis
tos_nino34_anom_mean.plot(ax=ax)

# plot the smoothed data on the assigned axis
oni_index.plot(ax=ax)

# add legend
ax.legend(['monthly', '3-month running mean'])

# add ylabel
ax.set_ylabel('temprature anomalies')

#add xlabel
ax.set_xlabel('Year')


# # **Section 3: Identify El Niño and La Niña Events**

# We will highlight values in excess of $\pm$0.5, roughly corresponding to El Niño (warm) and La Niña (cold) events.

# In[ ]:


fig = plt.figure(figsize=(12, 6)) # assing figure size

plt.fill_between( #plot with color in between
    oni_index.time.data,  #x values
    oni_index.where(
        oni_index >= 0.5
    ).data, # top boundary - y values above 0.5
    0.5, # bottom boundary - 0.5
    color='red', #color
    alpha=0.9, #transparency value
)
plt.fill_between(
    oni_index.time.data,
    oni_index.where(
        oni_index <= -0.5
    ).data,
    -0.5,
    color='blue',
    alpha=0.9,
)

oni_index.plot(color='black') #plot the smoothed data
plt.axhline(0, color='black', lw=0.5) # add a black line at x=0
plt.axhline(0.5, color='black', linewidth=0.5, linestyle='dotted') # add a black line at x=0.5
plt.axhline(-0.5, color='black', linewidth=0.5, linestyle='dotted') # add a black line at x=-0.5
plt.title('Oceanic Niño Index (ONI)')


# ### Questions 3: 
# <!-- Sloane's ideas of climate content to add: -->
# Now that we've normalized the data and highlighted SST anomalies that correspond to El Niño (warm) and La Niña (cold) events, consider the following questions:
# 
# 1. How frequently do El Niño and La Niña events occur over the period of time studied here? 
# 2. When were the strongest El Niño and La Niña events over this time period? 
# 3. Considering the ocean-atmosphere interactions that cause El Niño and La Niña events, can you hypothesize potential reasons one El Niño or La Niña event may be stronger than others? 
# 

# In[ ]:


# to_remove explanation

"""
1. Based on the monthly Sea Surface Temperature (SST) data from 2000 to 2014, it appears that both the El Niño and La Niña phases (exceed +/- 0.5 ˚C) occurred roughly 4 times each over this period.
2. The strongest El Niño occurred in 2012 and the strongest La Niña occurred in 2010. Both strongest events happened in more recent years.
3. El Niño and La Niña events are primarily driven by the interactions between the ocean and the atmosphere. Their strength is impacted by factors involved in ocean-atmosphere interactions such as ocean heat content, strength of trade winds, rainfall (as explained  in the video), causing one El Niño or La Niña event to be stronger than another.
""";


# # Summary
# 
# In this tutorial, we have learned to utilize a variety of Xarray tools to examine variations in SST during El Niño and La Niña events. We've practiced loading SST data from the CESM2 model, and masking data using the `.where()` function for focused analysis. We have also computed climatologies and anomalies using the `.groupby()` function, and learned to compute moving averages using the `.rolling()` function. Finally, we have calculated, normalized, and plotted the Oceanic Niño Index (ONI), enhancing our understanding of the El Niño Southern Oscillation (ENSO) and its impacts on global climate patterns.

# # Resources
# 
# Data from this tutorial can be accessed [here](https://github.com/ProjectPythia/pythia-datasets).
