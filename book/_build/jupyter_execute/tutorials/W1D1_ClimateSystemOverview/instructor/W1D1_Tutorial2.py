#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W1D1_ClimateSystemOverview/instructor/W1D1_Tutorial2.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W1D1_ClimateSystemOverview/instructor/W1D1_Tutorial2.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 2: Selection, Interpolation and Slicing**
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
# **Our 2023 Sponsors:** NASA TOPS and Google deepmind

# ![project pythia](data:image/png;base64,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) | 
# -
# Pythia credit: Rose, B. E. J., Kent, J., Tyle, K., Clyne, J., Banihirwe, A., Camron, D., May, R., Grover, M., Ford, R. R., Paul, K., Morley, J., Eroglu, O., Kailyn, L., & Zacharias, A. (2023). Pythia Foundations (Version v2023.05.01) https://zenodo.org/record/8065851
# 
# 

# # **Tutorial Objectives**
# In the previous tutorial, we learned how to use `Xarray` to create `DataArray` and `Dataset` objects. Global climate datasets can be very large with multiple variables, and DataArrays and Datasets are very useful tools for organizing, comparing and interpreting such data. However, sometimes we are not interested in examining a *global* dataset but wish to examine a specific time or location. For example, we might want to look at climate variables in a particular region of Earth, and potentially compare that to another region. In order to carry-out such analyses, it’s useful to be able to extract and compare subsets of data from a global dataset. 
# 
# In this tutorial, you will explore multiple computational tools in `Xarray` that allow you to select data from a specific spatial and temporal range. In particular, you will practice using:
# 
# 
# *   **`.sel()`:** select data based on coordinate values or date
# *   **`.interp()`:** interpolate to any latitude/longitude location to extract data
# *   **`slice()`:** to select a range (or slice) along one or more coordinates, we can pass a Python slice object to `.sel()`
# 

# # **Setup**

# In[ ]:


# imports
from datetime import timedelta
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt


# ##  Figure Settings
# 

# ###  Figure Settings
# 

# In[ ]:


# @title Figure Settings
import ipywidgets as widgets       # interactive display
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
plt.style.use("https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/cma.mplstyle")


# ##  Video 1: Video Title
# 

# ###  Video 1: Video Title
# 

# In[ ]:


# @title Video 1: Video Title
#Tech team will add code to format and display the video


# To explore these Xarray tools, first recreate the synthetic temperature and pressure DataArrays you generated in the previous tutorial, and combine these two DataArrays into a Dataset.

# # **Section 1: Subsetting and Selection by Coordinate Values**
# 
# Since Xarray allows us to label coordinates, you can select data based on coordinate names and values, rather than array indices. We'll explore this briefly here. First, we will recreate the temperature and pressure data from Tutorial 1.

# In[ ]:


# temperature data
rand_data = 283 + 5 * np.random.randn(5, 3, 4)
times_index = pd.date_range('2018-01-01', periods=5)
lons = np.linspace(-120, -60, 4)
lats = np.linspace(25, 55, 3)
temperature = xr.DataArray(rand_data, coords=[times_index, lats, lons], dims=['time', 'lat', 'lon'])
temperature.attrs['units'] = 'kelvin'
temperature.attrs['standard_name'] = 'air_temperature'

# pressure data
pressure_data = 1000.0 + 5 * np.random.randn(5, 3, 4)
pressure = xr.DataArray(
    pressure_data, coords=[times_index, lats, lons], dims=['time', 'lat', 'lon']
)
pressure.attrs['units'] = 'hPa'
pressure.attrs['standard_name'] = 'air_pressure'

# combinate temperature and pressure DataArrays into a Dataset called 'ds'
ds = xr.Dataset(data_vars={'Temperature': temperature, 'Pressure': pressure})
ds


# To refresh your memory from the previous tutorial, take a look at the DataArrays you created for temperature and pressure by clicking on those variables in the dataset above.

# 
# ## **Section 1.1: NumPy-like Selection**
# 
# Suppose you want to extract all the spatial data for one single date: January 2, 2018. It's possible to achieve that with NumPy-like index selection:

# In[ ]:


indexed_selection = temperature[1, :, :]  # index 1 along axis 0 is the time slice we want...
indexed_selection


# However, notice that this requires us (the user) to have detailed knowledge of the order of the axes and the meaning of the indices along those axes. By having named coordinates in Xarray, we can avoid this issue.

# ## **Section 1.2: `.sel()`**
# 
# Rather than using a NumPy-like index selection, in Xarray, we can instead select data based on coordinate values using the `.sel()` method, which takes one or more named coordinate(s) as a keyword argument:

# In[ ]:


named_selection = temperature.sel(time='2018-01-02')
named_selection


# We got the same result as when we used the NumPy-like index selection, but 
# - we didn't have to know anything about how the array was created or stored
# - our code is agnostic about how many dimensions we are dealing with
# - the intended meaning of our code is much clearer!
# 
# By using the .sel() method in Xarray, we can easily isolate data from a specific time. You can also isolate data from a specific coordinate. 

# ### **Coding Exercises 1.2**

# 1. Write a line of code to select the temperature data from the coordinates 25,-120.

# ```python
# coordinate_selection = ...
# coordinate_selection
# 
# ```

# In[ ]:


# to_remove solution

coordinate_selection =  temperature.sel(lat='25.0', lon='-120.0')
coordinate_selection


# ## **Section 1.3: Approximate Selection and Interpolation**
# 
# The spatial and temporal resolution of climate data often differs between datasets or a dataset may be incomplete. Therefore, with time and space data, we frequently want to sample "near" the coordinate points in our dataset. For example, we may want to analyze data from a specific coordinate or a specific time, but may not have a value from that specific location or date. In that case, we would want to use the data from the closest coordinate or time-step. Here are a few simple ways to achieve that.
# 
# ### **Section 1.3.1: Nearest-neighbor Sampling**
# 
# Suppose we want to know the temperature from `2018-01-07`. However, the last day on our `time` axis is `2018-01-05`. We can therefore sample within two days of our desired date of `2018-01-07`. We can do this using the `.sel` method we used earlier, but with the added flexibility of performing [nearest neighbor sampling](https://docs.xarray.dev/en/stable/user-guide/indexing.html#nearest-neighbor-lookups) and specifying an optional tolerance. This is called an **inexact lookup** because we are not searching for a perfect match, although there may be one. Here the **tolerance** is the maximum distance away from our desired point Xarray will search for a nearest neighbor.

# In[ ]:


temperature.sel(time='2018-01-07', method='nearest', tolerance=timedelta(days=2))


# Notice that the resulting data is from the date `2018-01-05`.

# ### **Section 1.3.2:  Interpolation**
# 
# The latitude values of our dataset are 25ºN, 40ºN, 55ºN, and the longitude values are 120ºW, 100ºW, 80ºW, 60ºW. But suppose we want to extract a timeseries for Boulder, Colorado, USA (40°N, 105°W). Since `lon=-105` is _not_ a point on our longitude axis, this requires interpolation between data points.
# 
# We can do this using the `.interp()` method (see the docs [here](http://xarray.pydata.org/en/stable/interpolation.html)), which works similarly to `.sel()`. Using `.interp()`, we can interpolate to any latitude/longitude location using an interpolation method of our choice. In the example below, you will linearly interpolate between known points.

# In[ ]:


temperature.interp(lon=-105, lat=40, method='linear')


# In this case, we specified a linear interpolation method, yet one can choose other methods as well (e.g., nearest, cubic, quadratic). Note that the temperature values we extracted in the code cell above are not actual values in the dataset, but are instead calculated based on linear interpolations between values that are in the dataset.

# ## **Section 1.4: Slicing Along Coordinates**
# 
# Frequently we want to select a range (or _slice_) along one or more coordinate(s). For example, you may wish to only assess average annual temperatures in equatorial regions. We can achieve this by passing a Python [slice](https://docs.python.org/3/library/functions.html#slice) object to `.sel()`. The calling sequence for <code>slice</code> always looks like <code>slice(start, stop[, step])</code>, where <code>step</code> is optional. In this case, let's only look at values between 110ºW-70ºW and 25ºN-40ºN:

# In[ ]:


temperature.sel(
    time=slice('2018-01-01', '2018-01-03'), lon=slice(-110, -70), lat=slice(25, 45)
)


# ## **Section 1.5: One More Selection Method: `.loc`**
# 
# All of these operations can also be done within square brackets on the `.loc` attribute of the `DataArray`:
# 

# In[ ]:


temperature.loc['2018-01-02']


# This is sort of in between the NumPy-style selection
# ```
# temp[1,:,:]
# ```
# and the fully label-based selection using `.sel()`
# 
# With `.loc`, we make use of the coordinate *values*, but lose the ability to specify the *names* of the various dimensions. Instead, the slicing must be done in the correct order:

# In[ ]:


temperature.loc['2018-01-01':'2018-01-03', 25:45, -110:-70]


# One advantage of using `.loc` is that we can use NumPy-style slice notation like `25:45`, rather than the more verbose `slice(25,45)`. But of course that also works:

# In[ ]:


temperature.loc['2018-01-01':'2018-01-03', slice(25, 45), -110:-70]


# What *doesn't* work is passing the slices in a different order to the dimensions of the dataset:

# In[ ]:


# This will generate an error
# temperature.loc[-110:-70, 25:45,'2018-01-01':'2018-01-03']


# # **Summary**
# 
# In this tutorial, we have explored the practical use of **`.sel()`** **`.interp()`** **`.loc()`:** and **slicing** techniques to extract data from specific spatial and temporal ranges. These methods are valuable when we are intereseted in only certain pieces of large datasets.

# # **Resources**

# Code and data for this tutorial is based on existing content from [Project Pythia](https://foundations.projectpythia.org/core/xarray/xarray-intro.html).
