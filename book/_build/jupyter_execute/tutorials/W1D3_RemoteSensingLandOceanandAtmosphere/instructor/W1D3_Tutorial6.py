#!/usr/bin/env python
# coding: utf-8

# #**Tutorial 6: Large Scale Climate Variability - ENSO**
# 
# > Indented block
# 
# > Indented block
# 
# 
# 
# 
# **Week 1, Day 3, Remote Sensing**
# 
# **Content creators:** Douglas Rao
# 
# **Content reviewers:** TBD
# 
# **Content editors:** TBD
# 
# **Production editors:** TBD
# 
# **Our 2023 Sponsors:** TBD

# #**Tutorial Objectives**
# 
# In this tutorial, you will learn the basics of the El Nino-Southern Oscillation (ENSO) - one of the most influencial large-scale climate variability that affects weather and climate.
# 
# By the end of this tutorial you will be able to:
# 
# * Understand the concept of ENSO and three different phases of the ENSO
# * Use satellite based sea surface temperature data to calculate index for ENSO monitoring
# 

# #**Setup**
# 
# 
# 
# In this section, we have:
# 
# 
# 1.   **Import cell:** imports all libraries you use in the tutorial.
# 2.   **Hidden Figure settings cell:** sets up the plotting style (copy exactly)
# 1.   **Hidden Plotting functions cell:** contains all functions used to create plots throughout the tutorial (so students don't waste time looking at boilerplate matplotlib but can here if they wish to). Please use only matplotlib for plotting for consistency.
# 2.   **Hidden Helper functions cell:** This should contain functions that students have previously used or that are very simple. Any helper functions that are being used for the first time and are important should be placed directly above the relevant text or exercise (see Section 1.1 for an example).
#     
# 
# 

# In[ ]:


#Imports

# Import only the libraries/objects that you use in this tutorial.

# If any external library has to be installed, !pip install library --quiet
# follow this order: numpy>matplotlib.
# import widgets in hidden Figure settings cell

# Properly install cartopy in colab to avoid session crash
# !apt-get install libproj-dev proj-data proj-bin --quiet
# !apt-get install libgeos-dev --quiet
# !pip install cython --quiet
# !pip install cartopy --quiet

# !apt-get -qq install python-cartopy python3-cartopy  --quiet
# !pip uninstall -y shapely  --quiet
# !pip install shapely --no-binary shapely  --quiet


# In[ ]:


import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy, cartopy.crs as ccrs


# ##  Figure settings
# 

# ###  Figure settings
# 

# In[ ]:


# @title Figure settings
import ipywidgets as widgets       # interactive display
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
plt.style.use("https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/cma.mplstyle")


# # **Section 1: El Niño-Southern Oscillation (ENSO)**
# 

# ##  Video 1: Video 1 Name
# 

# ###  Video 1: Video 1 Name
# 

# In[ ]:


# @title Video 1: Video 1 Name
#Tech team will add code to format and display the video


# One of the most commonly discussed large scale climate variability is El Niño-Southern Oscillation (ENSO). 
# 
# ENSO is one of the most important climate phenomena on Earth due to its ability to change the global atmospheric circulation, which in turn, influences temperature and precipitation across the globe. 
# 
# Though ENSO is a single climate phenomenon, it has three states, or phases, it can be in.  
# 
# - El Niño: A warming of the ocean surface, or above-average sea surface temperatures, in the central and eastern tropical Pacific Ocean.
# - La Niña: A cooling of the ocean surface, or below-average sea surface temperatures, in the central and eastern tropical Pacific Ocean.
# - Neutral: Neither El Niño or La Niña. Often tropical Pacific SSTs are generally close to average. 
# 
# In other words, we need to use sea surface temperature to study the ENSO. In this tutorial, we will use the Optimum Interpolated Sea Surface Temperature (OISST) CDR data from NOAA to calculate ENSO and reproduce the famous ENSO figure. 
# 

# ##**Section 1.1: Calculate SST Anomaly**
# 
# OISST data is originally produced at daily and 1/4° spatial resolution. To avoid the large amount of data processing, we use the monthly aggregated OISST SST data provided by NOAA Physical Systems Laboratory. 

# In[ ]:


# Option 1: Download data
# Download the monthly sea surface temperature data from NOAA Physical System
# Laboratory. The data is processed using the OISST SST Climate Data Records
# from NOAA CDR program.
# The data downloading may take 2-3 minutes to complete.
import os, requests, tarfile
fname = 'sst.mon.mean.nc'
url = "https://osf.io/6pgc2/download/"
if not os.path.isfile(fname):
  try:
    r = requests.get(url)
  except requests.ConnectionError:
    print("!!! Failed to download data !!!")
  else:
    if r.status_code != requests.codes.ok:
      print("!!! Failed to download data !!!")
    else:
      print(f"Downloading {fname}...")
      with open(fname, "wb") as fid:
        fid.write(r.content)
      print(f"Download {fname} completed!")

## Option 2: Use the data stored in the workspace
#url = 'asset/data/sst.mon.mean.nc'


# In[ ]:


ds = xr.open_dataset(fname)
ds


# The monthly OISST data is available starting from September of 1981. The ENSO is often identified using monthly SST anomaly over a defined regions. There are various different regions used to monitor and study ENSO:
# 
# - Niño 1+2 (0-10S, 90W-80W)
# - Niño 3 (5N-5S, 150W-90W)
# - Niño 3.4 (5N-5S, 170W-120W)
# - Niño 4 (5N-5S, 160E-150W)
# 
# These regions are identified in the map below provided by NOAA Climate portal.
# 
# ![Location of four different nino regions (Credit: NOAA)](https://www.climate.gov/sites/default/files/Fig3_ENSOindices_SST_large.png)
# 
# The Niño 3.4 (5N-5S, 170W-120W) region is the most commonly used region for ENSO monitoring.
# 
# To calculate ENSO index, we will first get the monthly anomaly of the SST data.

# In[ ]:


# Get 30-year climatology from 1982-2011
sst_30yr = ds.sst.sel(time=slice('1982-01-01', '2011-12-01'))
# Calculate monthly climatology
sst_clim = sst_30yr.groupby('time.month').mean()
sst_clim


# In[ ]:


# Calculate monthly anomaly
sst_anom = ds.sst.groupby('time.month') - sst_clim
sst_anom


# Now, we can take a look at the SST anomaly of a given month. We use January of 1998 to show the specific change of SST during that time period.

# In[ ]:


sst = sst_anom.sel(time='1998-01-01')
# Initate plot
fig = plt.figure(figsize=(9,6))
# Focus on the ocean with the central_longitude=180
ax = plt.axes(projection=ccrs.Robinson(central_longitude=180))
ax.coastlines()
ax.gridlines()
sst.plot(ax=ax, transform=ccrs.PlateCarree(),
         vmin = -3, vmax = 3, cmap='RdBu_r',
         cbar_kwargs=dict(shrink=0.5, label='OISST Anomaly (degC)'))


# ## **Section 1.2: Monitoring ENSO with Oceanic Niño Index**
# 
# Oceanic Niño Index (ONI) is a common index used to monitor ENSO. It is calculated using the same region with Niño 3.4 (5N-5S, 170W-120W) with a 3-month rolling mean.

# You may have noticed that the `lon` for the SST data from PSL is organized between 0°–360°E. This is different from how we typically use `longitude` (-180°–180°). How do we covert the value of longitude between two systems (0-360° v.s. -180°–180°).
# 
# The longitude of 0°-360° can be viewed as the equivalent of (0–180°, -180°–0°). So the Niño 3.4 region should be (-5°–5°, 190–240°)

# In[ ]:


## Extract SST data for the Nino 3.4 regions
sst_nino34 = sst_anom.sel(lat=slice(-5,5), lon=slice(190,240))
sst_nino34


# In[ ]:


# Calculate the mean values for the Nino 3.4 region
fig=plt.figure(figsize=(12,6))
nino34 = sst_nino34.mean(dim=['lat', 'lon'])
nino34.plot()
plt.ylabel('Nino3.4 Anomaly (degC)')
plt.axhline(y=0, color='k', linestyle='dashed')


# The Oceanic Nino Index (ONI) is defined as the 3-month rolling mean of the monthly regional average of the SST anomaly for the Nino 3.4 region. We can use `.rolling()` to calculate the ONI value for each month from the OISST monthly anomaly.

# In[ ]:


# Calculate 3-month rolling mean of Nino 3.4 anomaly for the ONI
fig=plt.figure(figsize=(12,6))
oni = nino34.rolling(time=3, center=True).mean()
oni.plot()
plt.ylabel('Ocean Nino Index')
plt.axhline(y=0, color='k', linestyle='dashed')


# Often the different phases of ENSO is defined based on a threshold of 0.5 with ONI index. 
# 
# - El Niño: ONI values higher than 0.5 - which means surface waters in the east-central tropical Pacific are 0.5 degrees Celsius or more warmer than normal.
# - La Niña: ONI values lower than -0.5 - which indicates the region is 0.5 degrees Celsius or more cooler than normal.
# 
# The neutral phase is when ONI values are in between these two thresholds. We can make the ONI plot that is similarly used by NOAA and other organizations to monitor ENSO phases.

# In[ ]:


# Set up the plot size
fig = plt.figure(figsize=(12, 6))
# Create the filled area when ONI values are above 0.5 for El Nino
plt.fill_between(
    oni.time.data,
    oni.where(
        oni >= 0.5
    ).data, 0.5,
    color='red',
    alpha=0.9,
)
# Create the filled area when ONI values are below -0.5 for La Nina
plt.fill_between(
    oni.time.data,
    oni.where(
        oni <= -0.5
    ).data, -0.5,
    color='blue',
    alpha=0.9,
)
# Create the time series of ONI
oni.plot(color='black')
# Add the threshold lines on the plot
plt.axhline(0, color='black', lw=0.5)
plt.axhline(0.5, color='red', linewidth=0.5, linestyle='dotted')
plt.axhline(-0.5, color='blue', linewidth=0.5, linestyle='dotted')
plt.title('Oceanic Niño Index')


# From the plot, we can see the historical ENSO phases swing from El Nino to La Nina events. The major ENSO events like 1997-1998 shows up very clearly on the ONI plot. 
# 
# We will use the ONI data to perform analysis to understand the impact of ENSO on precipitation. So we export the ONI time series here into a netCDF file for future use via `.to_netcdf()`.

# In[ ]:


oni.to_netcdf('t6_oceanic-nino-index.nc')


# ### **Exercise: What is the difference when using different climatology period?**
# 
# As we learned here, ENSO is monitored using the anomaly of SST data for a specific region (e.g., Nino 3.4). Will the change of climatology period affect the ENSO phases significantly? You can explore it in this exercise.
# 
# Please compare the ONI time series calculated using two different climatology period (1982-2011 v.s. 1991-2020). 
# 
# 

# In[ ]:


################################################################################
# Exercise: Compare ONI time series using two different climatology period.    #
################################################################################

# Step 1: Calculate climatology of 1982-2010.

# Step 2: Calculate climatology of 1991-2020.

# Step 3: Calculate anomaly against two different climatology period.

# Step 4: Calculate ONI values using rolling mean for Nino 3.4 region.

# Step 5: Compare the two ONI time series and visualize the difference as a
#         time series plot



'''

Please describe the difference between two ONI time series using different
climatology time period:

'''


# #**Summary**
# 
# In this tutorial, we learned the basic concepts of ENSO and how satellite data can be used to monitor it.
# 
# * ENSO is one of the most influencial climate phenomena on Earth due to its ability to change the global atmospheric circulation. 
# * The three phases of ENSO can be monitored using SST data from satellite through SST anomaly for select regions.
# * The Oceanic Nino Index is used to produce the historical image for past El Nino and La Nina events.
# 
# In the next tutorial, we will use the ONI calculated here to assess the impact of ENSO on precipitation for select regions.
# 
