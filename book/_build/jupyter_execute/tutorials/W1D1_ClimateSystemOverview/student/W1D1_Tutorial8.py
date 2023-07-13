#!/usr/bin/env python
# coding: utf-8

# # **Tutorial 8: Masking with One Condition**
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
# **Our 2023 Sponsors:** NASA TOPS and google DeepMind
# 

# ## ![project pythia](https://projectpythia.org/_static/images/logos/pythia_logo-blue-rtext.svg)
# 
# Pythia credit: Rose, B. E. J., Kent, J., Tyle, K., Clyne, J., Banihirwe, A., Camron, D., May, R., Grover, M., Ford, R. R., Paul, K., Morley, J., Eroglu, O., Kailyn, L., & Zacharias, A. (2023). Pythia Foundations (Version v2023.05.01) https://zenodo.org/record/8065851
# 
# ## ![CMIP.png](https://github.com/ClimateMatchAcademy/course-content/blob/main/tutorials/Art/CMIP.png?raw=true)
# 

# # **Tutorial Objectives**
# 
# One useful tool for assessing climate data is masking, which allows you to filter elements of a dataset according to a specific condition and create a "masked array" in which the elements not fulfilling the condition will not be shown. This tool is helpful if you wish to, for example, only look at data greater or less than a certain value, or from a specific temporal or spatial range. For instance, when analyzing a map of global precipitation, we could mask regions that contain a value of mean annual precipitation above or below a specific value or range of values in order to assess wet and dry seasons.
# 
# In this tutorial you will learn how to mask data with one condition, and will apply this to your map of global SST.
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


# # **Section 1: Masking Data**
# 

# Using the `xr.where()` or `.where()` method, elements of an xarray Dataset or xarray DataArray that satisfy a given condition or multiple conditions can be replaced/masked. To demonstrate this, we are going to use the `.where()` method on the `tos` DataArray that we've been using in the past few tutorials.
# 

# Let's load the same data that we used in the previous tutorial (monthly SST data from CESM2):
# 

# In[ ]:


filepath = DATASETS.fetch("CESM2_sst_data.nc")
ds = xr.open_dataset(filepath)
ds


# ## **Section 1.1: Using `where` with One Condition**
# 

# Let's say we want to analyze SST just from the last time in the dataset (2014-09-15). We can isolate this time using `.isel()`:
# 

# In[ ]:


sample = ds.tos.sel(time="2014-09")
sample


# Now that we have our `DataArray` from the desired time period, we can use another function, `.where()` to filter elements according to a condition. The conditional expression in `.where()` can be a `DataArray`, a `Dataset` or a function. Indexing methods on xarray objects generally return a subset of the original data. However, it is sometimes useful to select an object with the same shape as the original data, but with some elements masked. Unlike `.isel()` and `.sel()` that change the shape of the returned results, `.where()` preserves the shape of the original data. It accomplishes this by returning values from the original `DataArray` or `Dataset` if the `condition` is `True`, and fills in values (by default `nan`) wherever the `condition` is `False`. Additional information can be found in the [`.where()` documentation](http://xarray.pydata.org/en/stable/generated/xarray.DataArray.where.html).
# 
# Let's use `.where()` to mask locations with temperature values greater than 0ºC. Note that the condition we supply to `.where()` are the regions we wish to preserve, not those we wish to mask. So if we are interested in masking temperature values that are above 0ºC, we will pass the condition to preserve those that are greater than or equal to 0ºC.
# 

# In[ ]:


# preserve temperatures greater than or equal to 0, mask those that are less than 0
masked_sample = sample.where(sample <= 0.0)
masked_sample


# Let's plot both our original sample, and the masked sample for September 15th, 2014. Note we are using a different colorbar for the right hand figure, where the range of values is much smaller, and the same colors on the left would not correspond to the same colors on the right.
# 

# In[ ]:


fig, axes = plt.subplots(ncols=2, figsize=(19, 6))
sample.plot(ax=axes[0])
masked_sample.plot(ax=axes[1])


# Notice how in the figure on the right, only the SST from the areas where SST is below 0ºC is shown and the other areas are white since these are now NaN values. Now let's assess how polar SST has changed over the time period recorded by the original dataset. To do so, we can run the same code but focus on the time 2000-09-15.
# 

# In[ ]:


sample_2 = ds.tos.sel(time="2000-09")
masked_sample_2 = sample_2.where(sample_2 < 0.0)
fig, axes = plt.subplots(ncols=2, figsize=(19, 6))
masked_sample_2.plot(ax=axes[0])
masked_sample.plot(ax=axes[1])


# ### **Questions 1.1: Climate Connection**
# 
# 1. What is the purpose of masking in the analysis of climate data?
# 2. Within the areas that are not masked, how does the distribution of SST compare between these maps?
# 3. The minimum sea ice extent in the Arctic typically occurs annually in September after spring has brought in more sunlight and warmer temperatures. Considering both plots of September SST above (from 2000 on the left and 2014 on the right), how might changes in the ice-albedo feedback be playing a role in what you observe? Please state any assumptions you would make in your answer.
# 

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D1_ClimateSystemOverview/solutions/W1D1_Tutorial8_Solution_0bc6741a.py)
# 
# 

# # **Summary**
# 
# In this tutorial, we've explored the application of masking tools in the analysis of Sea Surface Temperature (SST) maps. Through masking, we've been able to focus our attention on areas where the SST is below 0°C. These are the regions where changes in the ice-albedo feedback mechanism are most evident in our present day. This has facilitated a more targeted analysis and clearer understanding of the data.
# 

# # **Resources**
# 

# Code and data for this tutorial is based on existing content from [Project Pythia](https://foundations.projectpythia.org/core/xarray/computation-masking.html).
# 
