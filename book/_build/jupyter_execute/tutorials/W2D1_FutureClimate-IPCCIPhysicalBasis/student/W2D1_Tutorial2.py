#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/W2D1_Tutorial_2.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/W2D1_Tutorial_2.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 2: Time Series, Global Averages, and Scenario Comparison**
# 
# **Week 2, Day 1, Future Climate: The Physical Basis**
# 
# **Content creators:** Brodie Pearson, Julius Busecke, Tom Nicholas
# 
# **Content reviewers:** Younkap Nina Duplex, Zahra Khodakaramimaghsoud, Sloane Garelick, Peter Ohue, Jenna Pearson, Derick Temfack, Peizhen Yang, Cheng Zhang, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Jenna Pearson, Ohad Zivan, Chi Zhang
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS

# # **Tutorial Objectives**
# In this tutorial, we will expand to look at data from **three** CMIP6/ScenarioMIP experiments (*historical*, *SSP1-2.6* and *SSP5-8.5*). Our aim will be to calculate the global mean SST for these 3 experiments, taking into account the spatially-varying size of the model's grid cells (i.e., calculating a *weighted* mean).
# 
# By the end of this tutorial, you'll be able to:
# 
# - Load and analyze CMIP6 SST data from different experiments.
# - Understand the difference between historical and future emission scenarios.
# - Calculate the global mean SST from gridded model data.
# - Apply the concept of weighted mean to account for varying grid cell sizes in Earth System Models.

# # **Setup**
# 
#     
# 
# 

# In[ ]:


# !pip install condacolab &> /dev/null
# import condacolab
# condacolab.install()

# # Install all packages in one call (+ use mamba instead of conda), this must in one line or code will fail
# !mamba install xarray-datatree intake-esm gcsfs xmip aiohttp nc-time-axis cf_xarray xmip xarrayutils &> /dev/null


# In[ ]:


# imports
import time

tic = time.time()

import intake
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

from xmip.preprocessing import combined_preprocessing
from xarrayutils.plotting import shaded_line_plot

from datatree import DataTree
from xmip.postprocessing import _parse_metric


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
get_ipython().run_line_magic('matplotlib', 'inline')


# ##  Video 2: Future Climate Scenarios
# 

# ###  Video 2: Future Climate Scenarios
# 

# ####  Video 2: Future Climate Scenarios
# 

# In[ ]:


# @title Video 2: Future Climate Scenarios
# Tech team will add code to format and display the video


# # **Section 1: Load CMIP6 SST Data from Several Experiments Using `xarray`**
# 
# In the last tutorial we loaded data from the *SSP5-8.5* (high-emissions projection) experiment of one CMIP6 model called *TaiESM1*. 
# 
# Let's expand on this by using data from **three** experiments 
# * *historical*: a simulation of 1850-2015 using observed forcing, 
# * *SSP1-2.6*: a future, low-emissions scenario, and 
# * *SSP5-8.5*: a future, high-emissions scenario.
# 
# 
# 
# 
# 

# In[ ]:


# open an intake catalog containing the Pangeo CMIP cloud data
col = intake.open_esm_datastore(
    "https://storage.googleapis.com/cmip6/pangeo-cmip6.json"
)

# pick the experiments you require
experiment_ids = ["historical", "ssp126", "ssp585"]

# from the full `col` object, create a subset using facet search
cat = col.search(
    source_id="TaiESM1",
    variable_id="tos",
    member_id="r1i1p1f1",
    table_id="Omon",
    grid_label="gn",
    experiment_id=experiment_ids,
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


# ## **Coding Exercise 1.1**
# 
# In this tutorial and the following tutorials we will be looking at the global mean sea surface temperature. To calculate this global mean, we need to know the horizontal area of every ocean grid cell in all the models we are using. 
# 
# Write code to load this ocean-grid area data using the previously shown method for SST data, noting that:
# * We now need a variable called *areacello* (area of cells in the ocean) 
# * This variable is stored in table_id *Ofx* (it is from the ocean model and is fixed/constant in time) 
# * A model's grid does not change between experiments so you only need to get grid data from the *historical* experiment for each model
# 

# In[ ]:


cat_area = col.search(
    source_id="TaiESM1",
    # Add the appropriate variable_id
    variable_id="areacello",
    member_id="r1i1p1f1",
    # Add the appropriate table_id
    table_id="Ofx",
    grid_label="gn",
    # Add the appropriate experiment_id
    experiment_id=["historical"],
    require_all_on=["source_id"],
)
# hopefully we can implement https://github.com/intake/intake-esm/issues/562 before the
# actual tutorial, so this would be a lot cleaner
cat_area.esmcat.aggregation_control.groupby_attrs = ["source_id", "experiment_id"]
dt_area = cat_area.to_datatree(**kwargs)

dt_with_area = DataTree()

for model, subtree in dt.items():
    metric = dt_area[model]["historical"].ds["areacello"]
    dt_with_area[model] = subtree.map_over_subtree(_parse_metric, metric)


# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_2_Solution_c1386992.py)
# 
# 

# # **Section 2: Global Mean Sea Surface Temperature (GMSST)**
# 
# The data files above contain spatial maps of the sea surface temperature for every month of each experiment's time period. For the rest of today's tutorials, we're going to focus on the global mean sea surface temperature, rather than maps, as a way to visualize the ocean's changing temperature at a global scale$^*$.
# 
# The global mean of a property can be calculated by integrating that variable over the surface area of Earth covered by the system (ocean, atmosphere etc.) and dividing by the total surface area of that system. For Sea Surface Temperature, $SST(x,y)$, the global mean ($GMSST$) can be written as an integral over the surface of the ocean ($S_{ocean}$):
# 
# \begin{equation}
# GMSST = \frac{\iint_{S_{ocean}}SST(x,y) dxdy}{\iint_{S_{ocean}} dxdy}
# \end{equation}
# 
# where $x$ and $y$ are horizontal coordinates (i.e. longitude and latitude). This formulation works if $SST(x,y)$ is a [spatially-continuous function](https://en.wikipedia.org/wiki/Continuous_or_discrete_variable), but in a global model we only know the SST of *discrete* grid cells rather than a *continuous* SST field. Integrals are only defined for continuous variables, we must instead use a summation over the grid cells (summation is the discrete equivalent of integration):
# 
# \begin{equation}
# GMSST = \frac{ \sum_{i,j} SST(i,j) A(i,j)}{\sum_{i,j} A(i,j)}
# \end{equation}
# 
# where $(i,j)$ represent the indices of the 2D spatial SST data from a CMIP6 model, and $A$ denotes the area of each ocean grid cell, which can vary between cells/locations, as you saw in the last tutorial where *TaiESM1* had irregularly-gridded output. This calculation is essentially a *weighted mean* of the SST across the model cells, where the weighting accounts for the varying area of cells - that is, larger cells should contribute more the global mean than smaller cells.
# 
# $^*$*Note: we could alternatively look at ocean heat content, which depends on temperature at all depths, but it is a more intensive computation that would take too long to calculate in these tutorials.*

# ### **Coding Exercise 2.1**
# 
# Complete the following code so that it calculates and plots a timeseries of global mean sea surface temperature from the *TaiESM1* model for both the *historical* experiment and the two future projection experiments, *SSP1-2.6* (low emissions) and *SSP5-8.5* (high emissions). 
# 
# As you complete this exercise this, consider the following questions:
# * In the first function, what `xarray` operation is the following line doing, and why is it neccessary?
# ```
# return ds.weighted(ds.areacello.fillna(0)).mean(['x', 'y'], keep_attrs=True)
# ```
# * How would your time series plot might change if you instead used took a simple mean of all the sea surface temperatures across all grid cells? (Perhaps your previous maps could provide some help here) 
# 

# In[ ]:


def global_mean(ds: xr.Dataset) -> xr.Dataset:
    """Global average, weighted by the cell area"""
    return ds.weighted(ds.areacello.fillna(0)).mean(["x", "y"], keep_attrs=True)


# average every dataset in the tree globally
dt_gm = ...

for experiment in ["historical", "ssp126", "ssp585"]:
    da = ...
    _ = ...
plt.title("Global Mean SST from TaiESM1")
plt.ylabel("Global Mean SST [$^\circ$C]")
plt.xlabel("Year")
plt.legend()


# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_2_Solution_58e712bd.py)
# 
# *Example output:*
# 
# <img alt='Solution hint' align='left' width=775.0 height=575.0 src=https://raw.githubusercontent.com/NeuromatchAcademy/course-content/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/static/W2D1_Tutorial_2_Solution_58e712bd_1.png>
# 
# 

# ### **Question 1.1: Climate Connection**
# 
# 1.  Is this plot what you expected? If so, explain what you expected, and why, from the historical experiment, and the SSP1-2.6 and SSP5-8.5 scenarios (see below for a potentially useful figure).
# 
# For context, here is [Figure TS.4](https://www.ipcc.ch/report/ar6/wg1/downloads/figures/IPCC_AR6_WGI_TS_Figure_4.png) from the Technical Summary of the [IPCC Sixth Assessment Report](https://www.ipcc.ch/assessment-report/ar6/), which shows how several elements of forcing differ between experiments (including *historical* and *SSP* experiments). In the video above we saw the $CO_2$ panel of this figure:
# 
# <img src="https://www.ipcc.ch/report/ar6/wg1/downloads/figures/IPCC_AR6_WGI_TS_Figure_4.png" alt= "Experiment_Forcing" width="1000" height="1000">
# 
# Figure TS.4 | The climate change cause–effect chain: The intent of this figure is to illustrate the process chain starting from anthropogenic emissions, to changes in atmospheric concentration, to changes in Earth’s energy balance (‘forcing’), to changes in global climate and ultimately regional climate and climatic impact-drivers. Shown is the core set of five Shared Socio-economic Pathway (SSP) scenarios as well as emissions and concentration ranges for the previous Representative Concentration Pathway (RCP) scenarios in year 2100; carbon dioxide (CO2) emissions (GtCO2yr–1), panel top left; methane (CH4) emissions (middle) and sulphur dioxide (SO2), nitrogen oxide (NOx) emissions (all in Mt yr–1), top right; concentrations of atmospheric CO2(ppm) and CH4 (ppb), second row left and right; effective radiative forcing for both anthropogenic and natural forcings (W m–2), third row; changes in global surface air temperature (°C) relative to 1850–1900, fourth row; maps of projected temperature change (°C) (left) and changes in annual-mean precipitation (%) (right) at a global warming level (GWL) of 2°C relative to 1850–1900 (see also Figure TS.5), bottom row. Carbon cycle and non-CO2 biogeochemical feedbacks will also influence the ultimate response to anthropogenic emissions (arrows on the left). {1.6.1, Cross-Chapter Box 1.4, 4.2.2, 4.3.1, 4.6.1, 4.6.2}
# 
# Credit: [IPCC](https://www.ipcc.ch/report/ar6/wg1/downloads/figures/IPCC_AR6_WGI_TS_Figure_4.png)

# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_2_Solution_b0a7a57f.py)
# 
# 

# # **Summary**
# 
# In tutorial 2, you diagnosed changes at a global scale by calculating global mean timeseries with CMIP6 model mapped data. You then synthesized and compared global mean SST evolution in various CMIP6 experiments, spanning Earth's recent past and several future scenarios. 
# 
# We started by loading CMIP6 SST data from three different scenarios: *historical*, *SSP1-2.6* (low-emissions future), and *SSP5-8.5* (high-emissions future). This process expanded our understanding of model outputs. We then focused on calculating global mean SST, by taking into account the spatially-discrete and irregularly-gridded nature of this model's grid cells through a weighted mean. This weighted mean approach yielded the global mean SST, providing a holistic view of the Earth's changing sea surface temperatures under multiple future climate scenarios.
# 

# # **Resources**
# 
# Data for this tutorial can be accessed [here](https://gallery.pangeo.io/repos/pangeo-gallery/cmip6/index.html).
