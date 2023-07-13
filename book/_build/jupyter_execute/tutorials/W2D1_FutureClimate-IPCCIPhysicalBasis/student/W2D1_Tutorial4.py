#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/W2D1_Tutorial_4.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/W2D1_Tutorial_4.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 4: Quantifying Uncertainty in Projections**
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
# 
# In the previous tutorial, we constructed a *multi-model ensemble* using data from a diverse set of five CMIP6 models. We showed that the projections differ between models due to their distinct physics, numerics and discretizations. In this tutorial, we will calculate the uncertainty associated with future climate projections by utilizing this variability across CMIP6 models. We will establish a *likely* range of projections as defined by the IPCC. 
# 
# By the end of this tutorial, you will be able to 
# - apply IPCC confidence levels to climate model data
# - quantify the uncertainty associated with CMIP6/ScenarioMIP projections.
# 

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
# !mamba install xarray-datatree intake-esm gcsfs xmip aiohttp nc-time-axis cf_xarray xarrayutils &> /dev/null


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
# %matplotlib inline


# ##  Helper functions
# 

# ###  Helper functions
# 

# ####  Helper functions
# 

# In[ ]:


# @title Helper functions

# If any helper functions you want to hide for clarity (that has been seen before
# or is simple/uniformative), add here
# If helper code depends on libraries that aren't used elsewhere,
# import those libaries here, rather than in the main import cell


def global_mean(ds: xr.Dataset) -> xr.Dataset:
    """Global average, weighted by the cell area"""
    return ds.weighted(ds.areacello.fillna(0)).mean(["x", "y"], keep_attrs=True)


# Calculate anomaly to reference period
def datatree_anomaly(dt):
    dt_out = DataTree()
    for model, subtree in dt.items():
        # for the coding exercise, ellipses will go after sel on the following line
        ref = dt[model]["historical"].ds.sel(time=slice("1950", "1980")).mean()
        dt_out[model] = subtree - ref
    return dt_out


def plot_historical_ssp126_combined(dt):
    for model in dt.keys():
        datasets = []
        for experiment in ["historical", "ssp126"]:
            datasets.append(dt[model][experiment].ds.tos)

        da_combined = xr.concat(datasets, dim="time")


# ##  Video 4: Quantifying Uncertainty in Projections
# 

# ###  Video 4: Quantifying Uncertainty in Projections
# 

# ####  Video 4: Quantifying Uncertainty in Projections
# 

# In[ ]:


# @title Video 4: Quantifying Uncertainty in Projections
# Tech team will add code to format and display the video


# # **Section 1: Loading CMIP6 Data from Various Models & Experiments**

# First, lets load the datasets that we used in the previous tutorial, which spanned 5 models. We will use three CMIP6 experiments, adding the high-emissions (*SSP5-8.5*) future scenario to the *historical* and *SSP1-2.6* experiments used in the last tutorial.
# 
# 

# In[ ]:


col = intake.open_esm_datastore(
    "https://storage.googleapis.com/cmip6/pangeo-cmip6.json"
)  # open an intake catalog containing the Pangeo CMIP cloud data

# pick our five models and three experiments
# there are many more to test out! Try executing `col.df['source_id'].unique()` to get a list of all available models
source_ids = ["IPSL-CM6A-LR", "GFDL-ESM4", "ACCESS-CM2", "MPI-ESM1-2-LR", "TaiESM1"]
experiment_ids = ["historical", "ssp126", "ssp585"]


# In[ ]:


# from the full `col` object, create a subset using facet search
cat = col.search(
    source_id=source_ids,
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

cat_area = col.search(
    source_id=source_ids,
    variable_id="areacello",  # for the coding exercise, ellipses will go after the equals on this line
    member_id="r1i1p1f1",
    table_id="Ofx",  # for the coding exercise, ellipses will go after the equals on this line
    grid_label="gn",
    experiment_id=[
        "historical"
    ],  # for the coding exercise, ellipses will go after the equals on this line
    require_all_on=["source_id"],
)

cat_area.esmcat.aggregation_control.groupby_attrs = ["source_id", "experiment_id"]
dt_area = cat_area.to_datatree(**kwargs)

dt_with_area = DataTree()

for model, subtree in dt.items():
    metric = dt_area[model]["historical"].ds["areacello"]
    dt_with_area[model] = subtree.map_over_subtree(_parse_metric, metric)

# average every dataset in the tree globally
dt_gm = dt_with_area.map_over_subtree(global_mean)

for experiment in ["historical", "ssp126", "ssp585"]:
    da = dt_gm["TaiESM1"][experiment].ds.tos
#     da.plot(label=experiment)
# plt.title('Global Mean SST from TaiESM1')
# plt.ylabel('Global Mean SST [$^\circ$C]')
# plt.xlabel('Year')
# plt.legend()

# plot_historical_ssp126_combined(dt_gm)

dt_gm_anomaly = datatree_anomaly(dt_gm)

# plot_historical_ssp126_combined(dt_gm_anomaly)


# # **Section 2: Quantifying Uncertainty in a CMIP6 Multi-model Ensemble**
# 
# Let's create a multi-model ensemble containing data from multiple CMIP6 models, which we can use to quantify our confidence in future projected sea surface temperature change under low- and high-emissions scenarios. 
# 
# **Your goal in this tutorial is to create a *likely* range of future projected conditions. The IPCC uncertainty language defines the *likely* range as the middle 66% of model results (ignoring the upper 17% and lower 17% of results)**

# ### **Coding Exercise 2.1**
# 
# Complete the following code to display multi-model ensemble data with IPCC uncertainty bands:
# 
# 
# 1. The multi-model mean temperature
# 2. Shading to display the *likely* range of temperatures for the CMIP6 historical and projected data (include both *SSP1-2.6* and *SSP5-8.5*). *da_upper* and *da_lower* are the boundaries of this shaded region
# 
# 

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

for experiment, color in zip(["historical", "ssp126", "ssp585"], ["C0", "C1", "C2"]):
    datasets = []
    for model in dt_gm_anomaly.keys():
        annual_sst = (
            dt_gm_anomaly[model][experiment]
            .ds.tos.coarsen(time=12)
            .mean()
            .assign_coords(source_id=model)
        )
        datasets.append(
            annual_sst.sel(time=slice(None, "2100")).load()
        )  # the french model has a long running member for ssp126
    da = xr.concat(datasets, dim="source_id", join="override").squeeze()
    x = da.time.data
    # Calculate the lower bound of the likely range
    da_lower = ...
    # Calculate the upper bound of the likely range
    da_upper = ...
    # plt.fill_between(range(x), da_lower, da_upper,  alpha=0.5, color=color)
    # Calculate the multi-model mean at each time within each experiment
    _ = ...
plt.title(
    "Global Mean SST Anomaly from five-member CMIP6 ensemble (base period: 1950 to 1980)"
)
plt.ylabel("Global Mean SST Anomaly [$^\circ$C]")
plt.xlabel("Year")
plt.legend()

plt.show()


# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_4_Solution_5a678182.py)
# 
# *Example output:*
# 
# <img alt='Solution hint' align='left' width=1158.0 height=575.0 src=https://raw.githubusercontent.com/NeuromatchAcademy/course-content/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/static/W2D1_Tutorial_4_Solution_5a678182_0.png>
# 
# 

# ### **Questions 2.1: Climate Connection**
# 
# 1.   What does this figure tell you about how the multi-model uncertainty compares to projected physical changes in the global mean SST? 
# 2.   Is this the same for both scenarios?
# 3.   For a 5-model ensemble like this, how do the *likely* ranges specifically relate to the 5 individual model temperatures at a given time?

# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_4_Solution_0effd963.py)
# 
# 

# # **Summary**
# In this tutorial, we have quantified the uncertainty of future climate projections by analyzing variability across a multi-model CMIP6 ensemble. We learned to apply the IPCC's confidence levels to establish a *likely* range of projections, which refers to the middle 66% of model results. 

# # **Resources**
# 
# Data for this tutorial can be accessed [here](https://gallery.pangeo.io/repos/pangeo-gallery/cmip6/index.html).
