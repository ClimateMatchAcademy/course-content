#!/usr/bin/env python
# coding: utf-8

# # **Tutorial 3: Opening and Plotting netCDF Data**
# 
# **Week 1, Day 1, Climate System Overview**
# 
# **Content creators:** Sloane Garelick, Julia Kent
# 
# **Content reviewers:** Katrina Dobson, Younkap Nina Duplex, Danika Gupta, Maria Gonzalez, Will Gregory, Nahid Hasan, Sherry Mi, Beatriz Cosenza Muralles, Jenna Pearson, Agustina Pesce, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS and Google DeepMind
# 

# ## ![project pythia](https://projectpythia.org/_static/images/logos/pythia_logo-blue-rtext.svg)
# 
# Pythia credit: Rose, B. E. J., Kent, J., Tyle, K., Clyne, J., Banihirwe, A., Camron, D., May, R., Grover, M., Ford, R. R., Paul, K., Morley, J., Eroglu, O., Kailyn, L., & Zacharias, A. (2023). Pythia Foundations (Version v2023.05.01) https://zenodo.org/record/8065851
# 
# ## ![CMIP.png](https://github.com/ClimateMatchAcademy/course-content/blob/main/tutorials/Art/CMIP.png?raw=true)
# 

# # **Tutorial Objectives**
# 
# Many global climate datasets are stored as [NetCDF](https://pro.arcgis.com/en/pro-app/latest/help/data/multidimensional/what-is-netcdf-data.htm) (network Common Data Form) files. NetCDF is a file format for storing multidimensional variables such as temperature, humidity, pressure, wind speed, and direction. These types of files also include metadata that gives you information about the variables and dataset itself.
# 
# In this tutorial, we will import atmospheric pressure and temperature data stored in a NetCDF file. We will learn how to use various attributes of Xarray to import, analyze, interpret, and plot the data.
# 

# # **Setup**
# 

# In[ ]:


# imports
import numpy as np
import pandas as pd
import xarray as xr
from pythia_datasets import DATASETS
import matplotlib.pyplot as plt


# ##  Figure Settings
# 

# In[ ]:


# @title Figure Settings
import ipywidgets as widgets  # interactive display

get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
plt.style.use(
    "https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/cma.mplstyle"
)


# ##  Video 1: Video Title
# 

# In[ ]:


# @title Video 1: Video Title
# Tech team will add code to format and display the video


# # **Section 1: Opening netCDF Data**
# 
# Xarray is closely linked with the netCDF data model, and it even treats netCDF as a 'first-class' file format. This means that Xarray can easily open netCDF datasets. However, these datasets need to follow some of Xarray's rules. One such rule is that coordinates must be 1-dimensional.
# 
# Here we're getting the data from Project Pythia's custom library of example data, which we already imported above with <code>from pythia_datasets import DATASETS</code>. The <code>DATASETS.fetch()</code> method will automatically download and cache (store) our example data file <code>NARR_19930313_0000.nc</code> locally.
# 

# In[ ]:


filepath = DATASETS.fetch("NARR_19930313_0000.nc")


# Once we have a valid path to a data file that Xarray knows how to read, we can open it like this:
# 

# In[ ]:


ds = xr.open_dataset(filepath)
ds


# ### **Questions 1**
# 

# 1. What are the dimensions of this dataset?
# 1. How many climate variables are in this dataset?
# 

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D1_ClimateSystemOverview/solutions/W1D1_Tutorial3_Solution_f9b80099.py)
# 
# 

# ## **Section 1.1: Subsetting the `Dataset`**
# 
# Our call to `xr.open_dataset()` above returned a `Dataset` object that we've decided to call `ds`. We can then pull out individual fields. First, let's assess the `isobaric1` values. **Isobaric** means characterized by constant or equal pressure. Let's look at the `isobaric1` values:
# 

# In[ ]:


ds.isobaric1
# Recall that we can also use dictionary syntax like `ds['isobaric1']` to do the same thing


# The `isobaric1` coordinate contains 29 pressure values (in hPa) corresponding to different pressures of the atmosphere. Recall from the video that pressure decreases with height in the atmosphere. Therefore, in our dataset lower atmospheric pressure values will correspond to higher altitudes. For each isobaric pressure value, there is data for all other variables in the dataset at that same pressure level of the atmosphere:
# 
# - **Wind**: the u and v components of the wind describe the direction of wind movement along a pressure level of the atmosphere. The U wind component is parallel to the x-axis (i.e. longitude) and the V wind component is parallel to the y- axis (i.e. latitude).
# - **Temperature**: temperatures on a specific atmospheric pressure level
# - **Geopotential Height**: the height of a given point in the atmosphere in units proportional to the potential energy of unit mass (geopotential) at this height relative to sea level
# 
# Let's explore this `Dataset` a bit further.
# 

# `Datasets` also support much of the same subsetting operations as `DataArray`, but will perform the operation on all data. Let's subset all data from an atmospheric pressure of 1000 hPa (the typical pressure at sea level):
# 

# In[ ]:


ds_1000 = ds.sel(isobaric1=1000.0)
ds_1000


# We can further subset to a single `DataArray` to isolate a specific climate measurement. Let's subset temperature from the atmospheric level at which the isobaric pressure is 1000 hPa:
# 

# In[ ]:


ds_1000.Temperature_isobaric


# ## **Section 1.2: Aggregation Operations**
# 
# Not only can you use the named dimensions for manual slicing and indexing of data (as we saw in the last tutorial), but you can also use it to control aggregation operations (e.g., average, sum, standard deviation). Aggregation methods for Xarray objects operate over the named coordinate dimensions specified by keyword argument <code>dim</code>.
# 
# First, let's try calculating the `std` (standard deviation) of the u component of the isobaric wind from our `Dataset`. The following code will calculate the standard deviation of all the `u-component_of_wind_isobaric` values at each isobaric level. In other words, we'll end up with one standard deviation value for each of the 29 isobaric levels. Note: because of the '-' present in the name, we cannot use dot notation to select this variable and must use a dictionary key style selection instead.
# 

# In[ ]:


# get wind data
u_winds = ds["u-component_of_wind_isobaric"]

# take the standard deviation
u_winds.std(dim=["x", "y"])


# Side note: Recall that the U wind component is parallel to the x-axis (i.e. longitude) and the V wind component is parallel to the y- axis (i.e. latitude). A positive U wind comes from the west, and a negative U wind comes from the east. A positive V wind comes from the south, and a negative V wind comes from the north.
# 

# Next, let's try calculating the mean of the temperature profile (temperature as a function of pressure) over a specific region. For this exercise, we will calculate the temperature profile over Colorado, USA. The bounds of Colorado are:
# 
# - x: -182km to 424km
# - y: -1450km to -990km
# 
# If you look back at the values for `x` and `y` in our dataset, the units for these values are kilometers (km). Remember that they are also the coordinates for the `lat` and `lon` variables in our dataset. The bounds for Colorado correspond to the coordinates 37°N to 41°N and 102°W to 109°W.
# 

# In[ ]:


# get the temperature data
temps = ds.Temperature_isobaric

# take just the spatial data we are interested in for Colorado
co_temps = temps.sel(x=slice(-182, 424), y=slice(-1450, -990))

# take the average
prof = co_temps.mean(dim=["x", "y"])
prof


# # **Section 2: Plotting with Xarray**
# 
# Another major benefit of using labeled data structures is that they enable automated plotting with axis labels.
# 
# ## **Section 2.1: Simple Visualization with `.plot()`**
# 
# Much like [Pandas](https://foundations.projectpythia.org/core/pandas.html), Xarray includes an interface to [Matplotlib](https://foundations.projectpythia.org/core/matplotlib.html) that we can access through the `.plot()` method of every `DataArray`.
# 
# For quick and easy data exploration, we can just call `.plot()` without any modifiers:
# 

# In[ ]:


prof.plot()


# Here Xarray has generated a line plot of the temperature data against the coordinate variable `isobaric`. Also, the metadata are used to auto-generate axis labels and units.
# 
# Consider the following questions:
# 
# - What isobaric pressure corresponds to Earth's surface?
# - How does temperature change with increasing altitude in the atmosphere?
# 
# It might be a bit difficult to answer these questions with our current plot, so let's try customizing our figure to present the data clearer.
# 

# ## **Section 2.2: Customizing the Plot**
# 
# As in Pandas, the `.plot()` method is mostly just a wrapper to Matplotlib, so we can customize our plot in familiar ways.
# 
# In this air temperature profile example, we would like to make two changes:
# 
# - swap the axes so that we have isobaric levels on the y (vertical) axis of the figure (since isobaric levels correspond to altitude)
# - make pressure decrease upward in the figure, so that up is up (since pressure decreases with altitude)
# 
# We can do this by adding a few keyword arguments to our `.plot()`:
# 

# In[ ]:


prof.plot(y="isobaric1", yincrease=False)


# ### **Questions 2.2**
# 

# 1. What isobaric pressure corresponds to Earth's surface?
# 2. Why do you think temperature generally decreases with height?
# 

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D1_ClimateSystemOverview/solutions/W1D1_Tutorial3_Solution_6605983a.py)
# 
# 

# ## **Section 2.3: Plotting 2D Data**
# 
# In the example above, the `.plot()` method produced a line plot.
# 
# What if we call `.plot()` on a 2D array? Let's try plotting the temperature data from the 1000 hPa isobaric level (surface temperature) for all x and y values:
# 

# In[ ]:


temps.sel(isobaric1=1000).plot()


# Xarray has recognized that the `DataArray` object calling the plot method has two coordinate variables, and generates a 2D plot using the `pcolormesh` method from Matplotlib.
# 
# In this case, we are looking at air temperatures on the 1000 hPa isobaric surface over North America. Note you could improve this figure further by using [Cartopy](https://foundations.projectpythia.org/core/cartopy.html) to handle the map projection and geographic features.
# 

# ### **Questions 2.2: Climate Connection**
# 
# 1. The map you made is showing temperature across the United States at the 1000 hPa level of the atmosphere. How do you think temperatures at the 500 hPa level would compare? What might be causing the spatial differences in temperature seen in the map?
# 

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D1_ClimateSystemOverview/solutions/W1D1_Tutorial3_Solution_1c4e9001.py)
# 
# 

# # **Summary**
# 
# Xarray brings the joy of Pandas-style labeled data operations to N-dimensional data. As such, it has become a central workhorse in the geoscience community for analyzing gridded datasets. Xarray allows us to open self-describing NetCDF files and make full use of the coordinate axes, labels, units, and other metadata. By utilizing labeled coordinates, our code becomes simpler to write, easier to read, and more robust.
# 

# # **Resources**
# 

# Code and data for this tutorial is based on existing content from [Project Pythia](https://foundations.projectpythia.org/core/xarray/xarray-intro.html).
# 
