#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W1D1_ClimateSystemOverview/instructor/W1D1_Tutorial4.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W1D1_ClimateSystemOverview/instructor/W1D1_Tutorial4.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 4: Arithmetic and Aggregation Methods**
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
# 
# As we just learned in the video, alongside the latitudinal temperature gradients set by solar radiation, the large-scale ocean circulation patterns are one of the main controls on global sea surface temperature (SST, or tos). The surface currents distort this meridional gradient and can transport heat globally. In this tutorial, we'll use a series of tools in Xarray to interpret sea surface temperature data. 
# 
# Specifically, we’ll import monthly SST data from the Community Earth System Model  v2 (CESM2), which is a Global Climate Model. A climate model is a mathematical representation of Earth's climate system components and their interactions. Climate models are based on well-documented physical processes to simulate the transfer of energy and materials through the climate system. You'll learn more about climate models later this week and next week, but for now, we're going to be working with SST data produced from a climate model. 
# 
# To assess global variations in this SST dataset, we will practice using multiple attributes of Xarray:
# 
# 
# *   Arithmetic methods to convert temperatures from Celsius to Kelvin
# *   Aggregation methods to calculate mean, median, minimum and maximum values of the data.
# 
# 
# Finally, we'll create a map of global mean annual SST to visualize spatial variations in SST.
# 

# # **Setup**
# 

# In[ ]:


# imports
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from pythia_datasets import DATASETS
import pandas as pd
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


# # Section 1: Arithmetic Operations
# 
# Arithmetic operations with a single `DataArray` automatically apply over all array values (like NumPy). This process is called **vectorization**.  First, let's open the monthly sea surface temperature (SST) data from the Community Earth System Model v2 (CESM2), which is a Global Climate Model.

# In[ ]:


filepath = DATASETS.fetch('CESM2_sst_data.nc')
ds = xr.open_dataset(filepath)
ds


# And look at the temeprature variable `tos`.

# In[ ]:


ds.tos


# Note in the attributes that the units are 'degC'. One arithmetic operation we can do is to the  convert the temperature from degrees Celsius to Kelvin:

# In[ ]:


ds.tos + 273.15


# 
# You may notice that there are a lot of NaN values in the DataArray for `tos`. NaN isn’t a bad thing and it just means there isn’t data for those coordinates. In this case, there's no `tos` data for areas with land since this dataset only contains SST values.
# 
# 
# Just to practice another arithmetic operation, lets's square all values in `tos`:

# In[ ]:


ds.tos**2


# # **Section 2: Aggregation Methods**
# 
# A very common step during data analysis is to summarize the data in question by computing aggregations like `sum()`, `mean()`, `median()`, `min()`, `max()` in which reduced data provide insight into the nature of the large dataset. For example, in the introductory video for this tutorial, we saw maps of the mean annual sea surface temperature and sea surface density. 
# 
# 
# The following table summarizes some other built-in xarray aggregations:
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
# 
# 
# Let's explore some of these aggregation methods.
# 

# Compute the temporal minimum:

# In[ ]:


ds.tos.min(dim='time')


# Compute the spatial sum:

# In[ ]:


ds.tos.sum(dim=['lat', 'lon'])


# Compute the temporal median:

# In[ ]:


ds.tos.median(dim='time')


# Compute the mean SST:

# In[ ]:


ds.tos.mean()


# Because we specified no `dim` argument, the function was applied over all dimensions, computing the mean of every element of `tos` across time and space. It is possible to specify a dimension along which to compute an aggregation. For example, to calculate the mean in time for all locations (i.e. the global mean annual SST), specify the time dimension as the dimension along which the mean should be calculated:

# In[ ]:


ds.tos.mean(dim='time').plot(size=7, vmin = -2, vmax = 32, cmap = 'coolwarm');


# ### **Questions 2: Climate Connection**
# 
# Observe the spatial patterns in SST and consider the following in the context of the components of the ocean climate system we learned about in the video:
# 1. Recall that upwelling commonly occurs off the west coast of continents, for example, in the eastern tropical Pacific off the west coast of South America. Do you see evidence for upwelling in this region? How do you think the mean SST in this region would change if you looked at a specific season rather than the annual mean? Would upwelling be more or less evident?

# In[ ]:


# to_remove explanation

"""
1.  Upwelling is a process in which deep, cold water rises toward the surface. This can be identified in a sea surface temperature (SST) map as areas where the SST is colder than the surrounding waters. We note off the west coast of South America there is a 'tongue' of colder water from about -40 S northward. The strength of upwelling can often vary seasonally, and thus in our annual mean SST map above, the effects of this are likely more subtle.
""";


# # **Summary**
# 
# In this tutorial, we have explored the use of the CESM2 and have imported and analyzed monthly sea surface temperature (SST, or tos) data. We used arithmetic methods to convert SST from Celsius to Kelvin, and aggregation methods such as the mean, median, minimum, and maximum values of the data. To conclude, we visualized the spatial variations in SST by generating a map of the global mean annual SST. This tutorial has provided us with valuable insights into global variations in SST and how to manipulate and analyze such data using Xarray.
# 

# # **Resources**

# Code and data for this tutorial is based on existing content from [Project Pythia](https://foundations.projectpythia.org/core/xarray/computation-masking.html).
