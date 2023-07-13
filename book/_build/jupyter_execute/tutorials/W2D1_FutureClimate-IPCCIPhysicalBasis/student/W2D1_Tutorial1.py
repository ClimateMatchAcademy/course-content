#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/W2D1_Tutorial_1.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/W2D1_Tutorial_1.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 1: Creating Maps of CMIP6 Earth System Model (ESM) Projections**
# 
# **Week 2, Day 1, Future Climate: The Physical Basis**
# 
# **Content creators:** Brodie Pearson, Julius Busecke, Tom Nicholas
# 
# **Content reviewers:** Younkap Nina Duplex, Zahra Khodakaramimaghsoud, Sloane Garelick, Peter Ohue, Jenna Pearson, Agustina Pesce, Derick Temfack, Peizhen Yang, Cheng Zhang, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Jenna Pearson, Ohad Zivan, Chi Zhang
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS

# # **Tutorial Objectives**
# Earth System Models (ESMs) provide physically-based projections of how Earth's climate could change in the coming years, decades, and centuries at both global and local scales. In the following tutorial you will:
# 
# - Revisit how to load ESM data from the CMIP6 experiments, and 
# - Create maps showing projected future changes in sea surface temperature (SST).

# # **Setup**
# 

# In[ ]:


# !pip install condacolab &> /dev/null
# import condacolab
# condacolab.install()

# # Install all packages in one call (+ use mamba instead of conda), this must in one line or code will fail
# !mamba install xarray-datatree intake-esm gcsfs xmip aiohttp cartopy nc-time-axis cf_xarray xarrayutils "esmf<=8.3.1" xesmf &> /dev/null
# # For xesmf install we need to pin "esmf<=8.3.1". More context here: https://github.com/pangeo-data/xESMF/issues/246


# In[ ]:


# imports
import time

tic = time.time()

import intake
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import xesmf as xe

from xmip.preprocessing import combined_preprocessing
from xarrayutils.plotting import shaded_line_plot

from datatree import DataTree
from xmip.postprocessing import _parse_metric

import cartopy.crs as ccrs


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


# ##  Video 1: Recap of Earth System Models
# 

# ###  Video 1: Recap of Earth System Models
# 

# ####  Video 1: Recap of Earth System Models
# 

# In[ ]:


# @title Video 1: Recap of Earth System Models
# Tech team will add code to format and display the video


# ## **Section 1.1: Loading CMIP6 SST Data with `xarray`**
# 
# As a reminder, these ESMs simulate several systems (ocean, atmosphere, cryosphere, land) that are coupled to each other, and each system has its own variables, physics, and discretizations (grid & timestep).
# 
# <img src="https://upload.wikimedia.org/wikipedia/commons/7/73/AtmosphericModelSchematic.png" alt= “EarthSystemModel” width="420" height="400">
# 
# Atmospheric Model Schematic (Credit: [Wikipedia](https://upload.wikimedia.org/wikipedia/commons/7/73/AtmosphericModelSchematic.png))
# 
# Let's repeat the CMIP6 loading method that we learned in Tutorial 6 on last week's Climate Modelling day (Day 5).
# 
#  **Although we will only work with monthly SST (ocean) data today, the methods introduced can easily be applied/extended to load and analyze other CMIP6 variables, including from other components of the Earth system.**
# 
# As a reminder, the *facets* that have to be specified for CMIP6, along with the facet choice(s) we make in this tutorial, are:
# 1. **variable_id**: *tos* = sea surface temperature
# 2. **source_id**: The CMIP6 model(s) that we want data from 
# 3. **table_id**: *Omon* (ocean monthly output)
# 4. **grid_id**: *gn* = data on the model's *native* grid
# 5. **experiment_id**: *ssp585* (we'll discuss experiments later today)
# 6. **member_id**: *r1i1p1f1* for now
# 
# Now, let's repeat our CMIP6 loading method from the previous tutorial.
# 
# *Note: today we will start by using only use one model, **TaiESM1**, which stands for **Taiwan Earth System Model version 1**, and a single experiment, **ssp585** which is a high-emissions future scenario. In later tutorials you will work with 5 distinct CMIP6 models (**source_id**), and two additional experiments (**experiment_id**). **TaiESM1** was developed by modifying the Community Earth System Model (**CESM**) version 1.2.2 to include different parameterizations (i.e., physics). As a result, the **TaiESM1** model output is distinct from the **CESM** output you used in previous tutorials/days.*
# 

# In[ ]:


# open an intake catalog containing the Pangeo CMIP cloud data
col = intake.open_esm_datastore(
    "https://storage.googleapis.com/cmip6/pangeo-cmip6.json"
)

# from the full `col` object, create a subset using facet search
cat = col.search(
    source_id="TaiESM1",
    variable_id="tos",
    member_id="r1i1p1f1",
    table_id="Omon",
    grid_label="gn",
    experiment_id="ssp585",
    require_all_on=[
        "source_id"
    ],  # make sure that we only get models which have all of the above experiments
)

# convert the sub-catalog into a datatree object, by opening each dataset into an xarray.Dataset (without loading the data)
kwargs = dict(
    preprocess=combined_preprocessing,  # apply xMIP fixes to each dataset
    xarray_open_kwargs=dict(
        use_cftime=True
    ),  # ensure all datasets use the same time index
    storage_options={
        "token": "anon"
    },  # anonymous/public authentication to google cloud storage
)

cat.esmcat.aggregation_control.groupby_attrs = ["source_id", "experiment_id"]
dt = cat.to_datatree(**kwargs)


# We now have a "datatree" containing the data we searched for. A datatree is a high-level container of xarray data, useful for organizing many related datasets together. You can think of a single `DataTree` object as being like a (nested) dictionary of `xarray.Dataset` objects. Each dataset in the tree is known as a "node" or "group", and we can also have empty nodes. *This `DataTree` object may seem complicated when we load only one dataset, but it will prove to be very useful in later tutorials where you will work with multiple models, experiments, and ensemble members* 
# 
# You can explore the nodes of the tree and its contents interactively in a similar way to how you can explore the contents of an `xarray.Dataset`:

# In[ ]:


dt


# Now that we have the model datasets organized within thie datatree (`dt`) we can plot the datasets. Let's start by plotting a map of SST from the `TaiESM1` CMIP6 model in July 2023. 
# 
# *Note that CMIP6 experiments were run several years ago, so the cut-off between **past** (observed forcing) and **future** (scenario-based/projected forcing) was at the start of 2015. This means that July 2023 is about 8 years into the CMIP6 **future** and so it is unlikely to look exactly like Earth's current SST state.*

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

# select just a single model (TaiESM1) and experiment (ssp585) to plot
sst_ssp585 = dt["TaiESM1"]["ssp585"].ds.tos

fig, (ax_present) = plt.subplots(
    ncols=1, nrows=1, figsize=[8, 4], subplot_kw={"projection": ccrs.Robinson()}
)

# select the model data for July 2023
sst_present = sst_ssp585.sel(time="2023-07").squeeze()

# plot the model data
sst_present.plot(
    ax=ax_present,
    x="lon",
    y="lat",
    transform=ccrs.PlateCarree(),
    vmin=-10,
    vmax=30,
    cmap="magma",
    robust=True,
)
ax_present.coastlines()
ax_present.set_title("July 2023")


# ### **Coding Exercise 1.1**
# 
# Now that we can plot maps of CMIP6 data, let's look at some projected future changes using this data!
# 
# In this coding exercise your goals are to: 
# 1. Create a map of the projected sea surface temperature in July 2100 under the SSP5-8.5 high-emissions scenario (we'll discuss scenarios in the next mini-lecture) using data from the *TaiESM1* CMIP6 model.
# 2. Create a map showing how this sea surface temperature projection is different from the current (July 2023) sea surface temperature in this model
# 3. Plot a similar map for this model that shows how *January* 2100 is different from *January* 2023
# 
# To get you started, we have provided code to load the required data set into a variable called *sst_ssp585*, and we have plotted the current (July 2023) sea surface temperature from this data set.
# 
# *Note: differences between two snapshots of SST are not the same as the **anomalies** that you encountered earlier in the course, which were the difference relative to the average during a reference period.*

# In[ ]:


# %matplotlib inline

# select just a single model and experiment
sst_ssp585 = dt["TaiESM1"]["ssp585"].ds.tos

fig, ([ax_present, ax_future], [ax_diff_july, ax_diff_jan]) = plt.subplots(
    ncols=2, nrows=2, figsize=[12, 6], subplot_kw={"projection": ccrs.Robinson()}
)

# plot a timestep for 2023
sst_present = sst_ssp585.sel(time="2023-07").squeeze()
sst_present.plot(
    ax=ax_present,
    x="lon",
    y="lat",
    transform=ccrs.PlateCarree(),
    vmin=-10,
    vmax=30,
    cmap="magma",
    robust=True,
)
ax_present.coastlines()
ax_present.set_title("July 2023")

# repeat for 2100
# complete the following line to extract data for July 2100
sst_future = ...
_ = ...
ax_future.coastlines()
ax_future.set_title("July 2100")

# now find the difference between July 2100 and July 2023
# complete the following line to extract the July difference
sst_difference_july = ...
_ = ...
ax_diff_july.coastlines()
ax_diff_july.set_title("2100 vs. 2023 Difference (July)")

# finally, find the difference between January of the two years used above
# complete the following line to extract the January difference
sst_difference_jan = ...
_ = ...
ax_diff_jan.coastlines()
ax_diff_jan.set_title("2100 vs. 2023 Difference (January)")

plt.show()


# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_1_Solution_55810c8f.py)
# 
# *Example output:*
# 
# <img alt='Solution hint' align='left' width=1164.0 height=586.0 src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/static/W2D1_Tutorial_1_Solution_55810c8f_0.png>
# 
# 

# ## **Questions 1.1: Climate Connection**
# 
# 1.   *Comparing only the top two panels*, how is the July SST projected to change in this particular model simulation? Do these changes agree with the map of July change that you plotted in the bottom left, and are these changes easier to see in this bottom map?
# 2.   In what ways are the July and January maps similar or dissimilar, and can you think of any physical explanations for these (dis)similarities?
# 3. Why do you think the color bar axes vary? (i.e., the top panels say "*Sea Surface Temperature [$^oC$]*" while the bottom panels say "*tos*")
# 
# Many of the changes seen in the maps are a result of a changing climate under this high-emissions scenarios. However, keep in mind that these are differences between two months that are almost 80 years apart, so some of the changes are due to weather/synoptic differences between these particular months.
# 

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_1_Solution_edfd8cc7.py)
# 
# 

# ## **Section 1.2: Horizontal Regridding**
# 
# Many CMIP6 models use distinct spatial grids, we call this the model's *native grid*. 
# 
# You are likely familiar with the *regular latitude-longitude* grid where we separate the planet into boxes that have a fixed latitude and longitude span like this image we saw in the tutorial:
# 
# <img src="https://upload.wikimedia.org/wikipedia/commons/4/4c/Azimutalprojektion-schief_kl-cropped.png" alt= "Lat_Lon_Grid" width="250" height="250">
# 
# Let's look at the grid used for the ocean component of the *TaiESM1* CMIP6 model:
# 

# In[ ]:


# create a scatter plot with a symbol at the center of each ocean grid cell in TaiESM1
plt.scatter(x=sst_ssp585.lon, y=sst_ssp585.lat, s=0.1)
plt.ylabel("Latitude")
plt.xlabel("Longitude")
plt.title("Grid cell locations in TaiESM1")


# ## **Questions 1.2**
# 
# 1. How would this plot look for a *regular latitude-longitude* grid like the globe image shown above and in the slides? In what ways is the TaiESM1 grid different from this regular grid?
# 2. Can you think of a reason the Northern and Southern hemisphere ocean grids differ?*
# 
# **Hint: from an oceanographic context, how are the North and South poles different from each other?*

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_1_Solution_319c2307.py)
# 
# 

# If you want to compare spatial maps from different models/observations, e.g. plot a map averaged over several models or the bias of this map relative to observations, you must first ensure the data from all the models (and observations) is on the same spatial grid. This is where regridding becomes essential!
# 
# > Regridding is applied lazily, but it is still taking time to compute *when* it is applied. So if you want to compare for example the mean over time of several models it is often much quicker to compute the mean in time over the native grid and then regrid the result of that, instead of regridding each timestep and then calculating the mean!

# In[ ]:


# define a 'target' grid. This is simply a regular lon/lat grid that we will interpolate our data on
ds_target = xr.Dataset(
    {
        "lat": (["lat"], np.arange(-90, 90, 1.0), {"units": "degrees_north"}),
        "lon": (["lon"], np.arange(0, 360, 1.0), {"units": "degrees_east"}),
    }
)  # you can try to modify the parameters above to e.g. just regrid onto a region or make the resolution coarser etc
ds_target


# In[ ]:


# define the regridder object (from our source dataarray to the target)
regridder = xe.Regridder(
    sst_ssp585, ds_target, "bilinear", periodic=True
)  # this takes some time to calculate a weight matrix for the regridding
regridder


# In[ ]:


# now we can apply the regridder to our data
sst_ssp585_regridded = regridder(sst_ssp585)  # this is a lazy operation!
# so it does not slow us down significantly to apply it to the full data!
# we can work with this array just like before and the regridding will only be
# applied to the parts that we later load into memory or plot.
sst_ssp585_regridded


# In[ ]:


# compare the shape to the original array
sst_ssp585


# ## **Section 1.3: Visually Comparing Data with Different Map Projections**
# 
# Let's use the code from above to plot a map of the model data on its original (*native*) grid, and a map of the model data after it is regridded.

# In[ ]:


fig, ([ax_regridded, ax_native]) = plt.subplots(
    ncols=2, figsize=[12, 3], subplot_kw={"projection": ccrs.Robinson()}
)

# Native grid data
sst_future = sst_ssp585.sel(time="2100-07").squeeze()
sst_future.plot(
    ax=ax_native,
    x="lon",
    y="lat",
    transform=ccrs.PlateCarree(),
    vmin=-10,
    vmax=30,
    cmap="magma",
    robust=True,
)
ax_native.coastlines()
ax_native.set_title("July 2100 Native Grid")

# Regridded data
sst_future_regridded = sst_ssp585_regridded.sel(time="2100-07").squeeze()
sst_future_regridded.plot(
    ax=ax_regridded,
    x="lon",
    y="lat",
    transform=ccrs.PlateCarree(),
    vmin=-10,
    vmax=30,
    cmap="magma",
    robust=True,
)
ax_regridded.coastlines()
ax_regridded.set_title("July 2100 Regridded")


# ## **Questions 1.3**
# 
# 1. Is this what you expected to see after regridding the data?

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_1_Solution_f9a48a4e.py)
# 
# 

# # **Summary**
# 
# In Tutorial 1 you have: 
# 
# *   Loaded and manipulated data from a CMIP6 model under a high-emissions future scenario experiment
# *   Created maps of future projected changes in the Earth system using CMIP6 data
# *   Converted/regridded CMIP6 model data onto a desired grid. This is a critical processing step that allows us to directly compare data from different models and/or observations 
# 

# # **Resources**
# 
# Data for this tutorial can be accessed [here](https://gallery.pangeo.io/repos/pangeo-gallery/cmip6/index.html).
