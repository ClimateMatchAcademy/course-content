#!/usr/bin/env python
# coding: utf-8

# # **Tutorial 2: A Lot of Weather Makes Climate - Exploring the ERA5 Reanalysis**
# 
# **Week 1, Day 2, Ocean-Atmosphere Reanalysis**
# 
# __Content creators:__ Momme Hell
# 
# **Content reviewers:** Katrina Dobson, Danika Gupta, Maria Gonzalez, Will Gregory, Nahid Hasan, Sherry Mi, Beatriz Cosenza Muralles, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS and Google DeepMind

# 
# ![CMIP.png](https://github.com/ClimateMatchAcademy/course-content/blob/main/tutorials/Art/CMIP.png?raw=true)|
# -
# 

# # **Tutorial Objectives**
# 
# In the previous tutorial, we learned about ENSO, which is a specific atmosphere-ocean dynamical phenomena. You will now examine the atmosphere and the ocean systems more generally.
# 
# In this tutorial, you will learn to work with reanalysis data. These data combine observations and models of the Earth system, and are a critical tool for weather and climate science. You will first utilize two methods to access a specific reanalysis dataset (ECMWF's ERA5; through [PO.DAAC](https://podaac.jpl.nasa.gov/) and through the web Copernicus API). You will then select and mask a region of interest, investigating how important climate variables change on medium length timescales (hours to months) within this region.
# 
# By the end of this tutorial, you will be able to:
# - Access and select reanalysis data of cliamtically-important variables
# - Plot maps to explore changes on various time scales.
# - Compute and compare timeseries of different variables from reanalysis data.

# # **Setup**

# In[ ]:


# !pip install pythia_datasets
# !pip install cartopy
# !pip install geoviews


# In[ ]:


# imports
from intake import open_catalog
import matplotlib.pyplot as plt
import matplotlib
import xarray as xr
import fsspec
import numpy as np

import boto3
import botocore
import datetime
import numpy as np
import os
import pooch
import tempfile
import geoviews as gv
import holoviews
from geoviews import Dataset as gvDataset
import geoviews.feature as gf
from geoviews import Image as gvImage

from cartopy import crs as ccrs
from cartopy import feature as cfeature

# import warnings
# #  Suppress warnings issued by Cartopy when downloading data files
# warnings.filterwarnings('ignore')


# ##  Figure settings
# 

# ###  Figure settings
# 

# ####  Figure settings
# 

# In[ ]:


# @title Figure settings
import ipywidgets as widgets  # interactive display

get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
plt.style.use(
    "https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/cma.mplstyle"
)


# ##  Video 1: Video 1 Name
# 

# ###  Video 1: Video 1 Name
# 

# ####  Video 1: Video 1 Name
# 

# In[ ]:


# @title Video 1: Video 1 Name
# Tech team will add code to format and display the video


# In[ ]:


# helper functions


def pooch_load(filelocation=None, filename=None, processor=None):
    shared_location = "/home/jovyan/shared/Data/tutorials/W1D2_StateoftheClimateOceanandAtmosphereReanalysis"  # this is different for each day
    user_temp_cache = tempfile.gettempdir()

    if os.path.exists(os.path.join(shared_location, filename)):
        file = os.path.join(shared_location, filename)
    else:
        file = pooch.retrieve(
            filelocation,
            known_hash=None,
            fname=os.path.join(user_temp_cache, filename),
            processor=processor,
        )

    return file


# # **Section 1: What is Reanalysis Data?**
# 
# **Reanalysis** refers to the process of combining historical observations from a variety of sources, such as weather stations, satellite measurments, and ocean buoys, with numerical models to create a comprehensive and consistent record of past weather and climate conditions. Reanalysis data is a useful tool to examine the Earth's climate system over a wide range of time scales, from seasonal through decadal to century-scale changes. 
# 
# There are multiple Earth system reanalysis products (e.g. MERRA-2, NCEP-NCAR, JRA-55C, [see extensive list here](https://climatedataguide.ucar.edu/climate-data/atmospheric-reanalysis-overview-comparison-tables)), and no single product fits all needs. For the purposes of this tutorial you will be using a product from the European Centre for Medium-Range Weather Forecasts (ECMWF) called **ECMWF Reanalysis v5 (ERA5)**. [This video](https://climate.copernicus.eu/climate-reanalysis) from the ECMWF provides you with a brief introduction to the ERA5 product.

# ## **Section 1.1: Accessing ERA5 Data**
# 
# You will access the data through the an AWS S3 bucket of the data: [ECMWF ERA5 Reanalysis](https://registry.opendata.aws/ecmwf-era5/). To do this you need the name of the bucket "era5-pds", and the file location in the bucket. *Note: you can open the [AWS link](https://registry.opendata.aws/ecmwf-era5/) and find a guided tutorial on how to explore the S3 bucket.*
# 
# Let's select a specific year and month to work with, March of 2018:

# In[ ]:


era5_bucket = "era5-pds"
client = boto3.client(
    "s3", config=botocore.client.Config(signature_version=botocore.UNSIGNED)
)  # initialize aws s3 bucket client
date_sel = datetime.datetime(
    2018, 3, 1, 0
)  # select a desired date and hours (midnight is zero)
prefix = date_sel.strftime("%Y/%m/")  # format the date to match the s3 bucket
metadata_file = "main.nc"  # filename on the s3 bucket
metadata_key = prefix + metadata_file  # file location and name on the s3 bucket
filepath = pooch_load(
    filelocation="http://s3.amazonaws.com/" + era5_bucket + "/" + metadata_key,
    filename=metadata_file,
)  # open the file

ds_meta = xr.open_dataset(filepath)  # open the file
ds_meta


# You just loaded an `xarray` dataset, as introduced at the first day. This dataset contains 19 variables covering the whole globe (-90 to +90 degrees in latitude, 0 to 360 degrees on longitude) along with their respective coordinates. With this dataset you have access to our best estimates of climate parameters with a temporal resolution of 1 hour and a spatial resolution of 1/4 degree (i.e. grid points near the Equator represent a ~25 km x 25 km region). This is a lot of data, but still just a fraction the data available through the [full ERA5 dataset](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=overview). 
# 

# ## **Section 1.2: Selecting Regions of Interest**
# The global ERA5 data over the entire time range is so large that even just one variable would be too large to store on your computer. Here you will apply a method to load a region (i.e., a spatial subset) of the data. In this first example, you will load *air surface temperature at 2 meters* data for a small region in the Northeastern United States. In later tutorials you will have the opportunity to select a region of your choice and to explore other climate variables. 

# In[ ]:


# the order of the lat lon range has to follow the convention of the data set.
# for this dataset, longitude ranges from 0 to 360 degrees and
# latitude ranges from 90 degrees Northto 90 degrees South .

# northeastern United States
lat_range = [55.2, 30.2]  # from north to south
lon_range = [270, 295]  # from west to east


# In[ ]:


# note this can take several minutes to download
selected_vars = [
    "air_temperature_at_2_metres",
    "northward_wind_at_10_metres",
    "eastward_wind_at_10_metres",
    "surface_air_pressure",
    "sea_surface_temperature",
]  # the variables we want
s3_data_ptrn = (
    "{year}/{month}/data/{var}.nc"  # path and filename format for this S3 bucket
)
year_s3 = date_sel.strftime("%Y")  # extract the year
month_s3 = date_sel.strftime("%m")  # extract the month
ERA5_select = []  # initialize the dataset, will save a complicated check later
for var in selected_vars:  # this will download 5 files of 500Mb each.
    s3_data_key = s3_data_ptrn.format(
        year=year_s3, month=month_s3, var=var
    )  # variable specific  key
    print("Downloading %s from S3..." % s3_data_key)
    filepath = pooch_load(
        filelocation="http://s3.amazonaws.com/" + era5_bucket + "/" + s3_data_key,
        filename=s3_data_key,
    )  # open the file
    ds_temp = xr.open_dataset(filepath)  # retrieve the variable from the bucket
    if (
        ERA5_select
    ):  # check if the dataset is empty or not (first iteration of the loop)
        ERA5_select = xr.merge(
            [ERA5_select, ds_temp]
        )  # if not empty, merge the new file
    else:
        ERA5_select = ds_temp  # if empty, just assign the new file

ERA5_allvars = ERA5_select.sel(lon=slice(lon_range[0], lon_range[1])).sel(
    lat=slice(lat_range[0], lat_range[1])
)
ERA5_allvars


# The magnitude of the wind vector represents the wind speed 
# 
# \begin{align}
# ||u|| = \sqrt{u^2 + v^2}
# \end{align}
# 
# which you will use later in the tutorial and discuss in more detail in tutorial 4. We will calculate that here and add it to our dataset.

# In[ ]:


# compute ten meter wind speed
ERA5_allvars["wind_speed"] = np.sqrt(
    ERA5_allvars["northward_wind_at_10_metres"] ** 2
    + ERA5_allvars["eastward_wind_at_10_metres"] ** 2
)  # calculate the wind speed from the vectors
# name and units in the DataArray:
ERA5_allvars["wind_speed"].attrs[
    "long_name"
] = "10-meter wind speed"  # assigning long name to the windspeed
ERA5_allvars["wind_speed"].attrs["units"] = "m/s"  # assigning units
ERA5_allvars


# # **Section 2: Plotting Spatial Maps of Reanalysis Data**
# First, let's plot the region's surface temperature for the first time step of the reanalysis dataset. To do this let's extract the air temperatre data from the dataset containing all the variables.

# In[ ]:


ds_surface_temp_2m = ERA5_allvars.air_temperature_at_2_metres


# We will be plotting this a little bit differently that you have previously plotted a map (and differently to how you will plot in most tutorials) so we can look at a few times steps interactively later. To do this we are using the package [geoviews](https://geoviews.org). 

# In[ ]:


holoviews.extension("bokeh")

dataset_plot = gvDataset(ds_surface_temp_2m.isel(time0=0))  # select the first time step

# create the image
images = dataset_plot.to(
    gvImage, ["longitude", "latitude"], ["air_temperature_at_2_metres"], "hour"
)

# aesthetics, add coastlines etc.
images.opts(
    cmap="coolwarm",
    colorbar=True,
    width=600,
    height=400,
    projection=ccrs.PlateCarree(),
    clabel="2m Air Temperature [K]",
) * gf.coastline


# In the above figure, coastlines are shown as black lines. Most of the selected region is land, with some ocean (lower left) and a lake (top middle).
# 
# Next, we will examine variability at two different frequencies using interactive plots:
# 
# 1. **Hourly variability** 
# 2. **Daily variability** 
# 
# Note that in the previous tutorial you computed the monthly variability, or *climatology*, but here you only have one month of data loaded (March 2018). If you are curious about longer timescales you will visit this in the next tutorial!

# In[ ]:


# interactive plot of hourly frequency of surface temperature
# this cell may take a little longer as it contains several maps in a single plotting function
ds_surface_temp_2m_hour = ds_surface_temp_2m.groupby("time0.hour").mean()
dataset_plot = gvDataset(
    ds_surface_temp_2m_hour.isel(hour=slice(0, 12))
)  # only the first 12 time steps, as it is a time consuming task
images = dataset_plot.to(
    gvImage, ["longitude", "latitude"], ["air_temperature_at_2_metres"], "hour"
)
images.opts(
    cmap="coolwarm",
    colorbar=True,
    width=600,
    height=400,
    projection=ccrs.PlateCarree(),
    clabel="2m Air Temperature [K]",
) * gf.coastline


# In[ ]:


# interactive plot of hourly frequency of surface temperature
# this cell may take a little longer as it contains several maps in a single plotting function holoviews.extension('bokeh')
ds_surface_temp_2m_day = ds_surface_temp_2m.groupby("time0.day").mean()
dataset_plot = gvDataset(
    ds_surface_temp_2m_day.isel(day=slice(0, 10))
)  # only the first 10 time steps, as it is a time consuming task
images = dataset_plot.to(
    gvImage, ["longitude", "latitude"], ["air_temperature_at_2_metres"], "day"
)
images.opts(
    cmap="coolwarm",
    colorbar=True,
    width=600,
    height=400,
    projection=ccrs.PlateCarree(),
    clabel="Air Temperature [K]",
) * gf.coastline


# ### **Question 2**
# 1. What differences do you notice between the hourly and daily interactive plots, and are there any interesting spatial patterns of these temperature changes?

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D2_StateoftheClimateOceanandAtmosphereReanalysis/solutions/W1D2_Tutorial2_Solution_64cd961b.py)
# 
# 

# # **Section 3: Plotting Timeseries of Reanalysis Data**
# 
# ## **Section 3.1: Surface Air Temperature Timeseries**
# 
# You have demonstrated that there are a lot of changes in surface temperature within a day and between days. It is crucial to understand this *temporal variability* in the data when performing climate analysis.
# 
# Rather than plotting interactive spatial maps for different timescales, in this last section you will create a timeseries of surface air temperature from the data you have already examined to look at variability on longer than daily timescales. Instead of taking the mean in ***time*** to create *maps*, you will now take the mean in ***space*** to create *timeseries*.
# 
# *Note that the spatially-averaged data will now only have a time coordinate coordinate, making it a timeseries (ts).*

# In[ ]:


# find weights (this is a regular grid so we can use cos(lat))
weights = np.cos(np.deg2rad(ds_surface_temp_2m.lat))
weights.name = "weights"

# take the weighted spatial mean since the latitude range of the region of interest is large
ds_surface_temp_2m_ts = ds_surface_temp_2m.weighted(weights).mean(["lon", "lat"])
ds_surface_temp_2m_ts


# In[ ]:


# plot the timeseries of surface temperature

fig, ax = plt.subplots(1, 1, figsize=(10, 3))

ax.plot(ds_surface_temp_2m_ts.time0, ds_surface_temp_2m_ts)
ax.set_ylabel("2m Air \nTemperature (K)")
ax.xaxis.set_tick_params(rotation=45)


# ### **Questions 3.1**
# 1. What is the dominant source of the high frequency (short timescale) variability? 
# 2. What drives the lower frequency variability? 
# 3. Would the ENSO variablity that you computed in the previous tutorial show up here? Why or why not?

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D2_StateoftheClimateOceanandAtmosphereReanalysis/solutions/W1D2_Tutorial2_Solution_edb98043.py)
# 
# 

# ## **Section 3.2: Comparing Timeseries of Multiple Variables**
# 
# Below you will calculate the timeseries of the surface air temperature which we just plotted, alongside timeseries of several other ERA5 variables for the same period and region: 10-meter wind speed, atmospheric surface pressure, and sea surface temperature. 

# In[ ]:


ERA5_allvars_ts = ERA5_allvars.weighted(weights).mean(["lon", "lat"])


# In[ ]:


plot_vars = [
    "air_temperature_at_2_metres",
    "wind_speed",
    "surface_air_pressure",
    "sea_surface_temperature",
]

fig, ax_list = plt.subplots(len(plot_vars), 1, figsize=(10, 13), sharex=True)

for var, ax in zip(plot_vars, ax_list):

    ax.plot(ERA5_allvars_ts.time0, ERA5_allvars_ts[var])
    ax.set_ylabel(
        ERA5_allvars[var].attrs["long_name"] + ": " + ERA5_allvars[var].attrs["units"],
        fontsize=12,
    )
    ax.xaxis.set_tick_params(rotation=45)


# ### **Questions 3.2**
# 
# Which variable shows variability that is dominated by:
# 1. The diurnal cycle?
# 2. The synoptic [~5 day] scale?
# 3. A mix of these two timescales?
# 4. Longer timescales?

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D2_StateoftheClimateOceanandAtmosphereReanalysis/solutions/W1D2_Tutorial2_Solution_86cbd94f.py)
# 
# 

# # **Summary**
# 
# In this tutorial, you learned how to access and process ERA5 reanalysis data. You are able to select specific regions within the reanalysis dataset and perform operations such as taking spatial and temporal averages.
# 
# You also looked at different climate variables to distinguish idenitfy the variability present at different timescales.
# 

# ## **Bonus Section 1: Selecting a Different Spatial Region**
# 
# Define another spatial region, such as where you live, by selecting a longitude and latitude range of of your choosing. To find the longitude and latitude coordinates of your region, you can use [Google Earth view](https://earth.google.com/), and read the position of your cursor in the lower right corner.
# 
# ### **Bonus Section 1.1: Note About the Geographic Coordinate System and the Coordinates Used in This Dataset**
# A point on Earth is described by latitude-longitude coordinates relative to the zero-meridian line going through Greenwich in London, UK (longitude = 0 degree) and the xero-latitude line along the equator (latitude = 0 degrees). Points east of Greenwich up to the *dateline* on the opposite side of the globe are referenced as 0 to +180 and points to the west of Greenwich are 0 to -180. -180 and +180 refer to the same longitude, the so-called *dateline* in the central pacific. 
# 
# However, our data is referenced in a slightly different way where longitude runs from 0 to 360 rather than -180 to +180. Longitude increases as you move east of Greenwich, until you reach Greenwich again (0 or 360 degrees), rather than stopping at the *dateline*. 

# # **Resources**
# 
# Data for this tutorial can be accessed [here](https://registry.opendata.aws/ecmwf-era5/).
