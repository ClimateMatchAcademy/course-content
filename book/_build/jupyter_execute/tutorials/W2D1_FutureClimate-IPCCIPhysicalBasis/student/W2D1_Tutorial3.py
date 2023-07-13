#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/W2D1_Tutorial_3.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/W2D1_Tutorial_3.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 3: Multi-model Ensembles**
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
# In this tutorial, we will analyze datafrom five different CMIP6 models developed by various institutions around the world, focusing on their *historical* simulations and low-emission projections (*SSP1-2.6*). By the end of this tutorial, you will be able to 
# - Load CMIP6 Sea Surface Temperature (SST) data from multiple models;
# - Calculate the SST anomalies, and recall the concept of temperature anomaly in relation to a base period

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
# model_colors = {k:f"C{ki}" for ki, k in enumerate(source_ids)}
get_ipython().run_line_magic('matplotlib', 'inline')


# ##  Helper functions
# 

# ###  Helper functions
# 

# ####  Helper functions
# 

# In[ ]:


# @title Helper functions


def global_mean(ds: xr.Dataset) -> xr.Dataset:
    """Global average, weighted by the cell area"""
    return ds.weighted(ds.areacello.fillna(0)).mean(["x", "y"], keep_attrs=True)


# ##  Video 3: Why so many Earth System Models?
# 

# ###  Video 3: Why so many Earth System Models?
# 

# ####  Video 3: Why so many Earth System Models?
# 

# In[ ]:


# @title Video 3: Why so many Earth System Models?
# Tech team will add code to format and display the video


# # **Section 1: Load CMIP6 SST Data from Five Models and Three Experiments**
# In the previous section, you compared how a single CMIP6 model (*TaiESM1*) simulated past temperature, and how it projected temperature would change under a low-emissions scenario and a high-emissions scenario (*historical*, *SSP1-2.6* and *SSP5-8.5* experiments respectively). 
# 
# Now we will start to analyze a **multi-model ensemble** that consists of data from multiple CMIP6 models. For now, we will focus on just the historical simulation and the low-emissions projection.
# 
# Your multi-model ensemble will consist of:
# 
# *  **Five** different CMIP6 models developed by institutions from a variety of countries: 
#   * *TaiESM1* (Research Center for Environmental Changes, Taiwan),
#   * *IPSL-CM6A-LR* (Institut Pierre Simon Laplace, France),
#   * *GFDL-ESM4* (NOAA Geophysical Fluid Dynamics Laboratory, USA), 
#   * *ACCESS-CM2* (CSIRO and ARCCSS, Australia), and 
#   * *MPI-ESM1-2-LR* (Max Planck Institute, Germany). 
# 
# Note that these are only a subset of the dozens of models, institutes, countries, and experiments that contribute to CMIP6, as discussed in the previous W2D1 Tutorial 2 video. Some of the abbreviations in the model names refer to institutes (*MPI/GFDL*), while some refer to the complexity and version of the model (e.g., Earth System or Climate Model [*ESM/CM*] and low- or high-resolution [*LR/HR*]). There are often several models from a single institute with each having a distinct level of complexity.

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


# In[ ]:


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


# Let's first reproduce the previous tutorial's timeseries of Global Mean SST from *TaiESM1* through the historical experiment and two future emissions scenarios

# In[ ]:


# average every dataset in the tree globally
dt_gm = dt_with_area.map_over_subtree(global_mean)

for experiment in ["historical", "ssp126", "ssp585"]:
    da = dt_gm["TaiESM1"][experiment].ds.tos
    da.plot(label=experiment)
plt.title("Global Mean SST from TaiESM1")
plt.ylabel("Global Mean SST [$^\circ$C]")
plt.xlabel("Year")
plt.legend()


# ### **Coding Exercise 1.1: Combine Past Data and Future Data, and Remove Seasonal Oscillations, and plot all 5 of the CMIP6 models we just loaded**
# 
# * The historical and projected data are separate time series. Complete the `xr.concat` function to combine the historical and projected data into a single continuous time series for each model.
# * The previous timeseries oscillated very rapidly due to Earth's seasonal cycles. Finish the `xarray` `resample` function so that it smooths the monthly data with a one-year running mean. This will make it easier to distinguish the long-term changes in sea surface temperature.
# * Note: this code is already set up to use all 5 of the CMIP6 models you just loaded, as it loops through and plots each model in the DataTree [`dt.keys()`]

# In[ ]:


def plot_historical_ssp126_combined(dt):
    for model in dt.keys():
        datasets = []
        for experiment in ["historical", "ssp126"]:
            datasets.append(dt[model][experiment].tos)

        # for each of the models, concatenate its historical and future data
        da_combined = ...
        # plot annual averages
        ...


_ = ...

plt.title("Global Mean SST from five CMIP6 models (annually smoothed)")
plt.ylabel("Global Mean SST [$^\circ$C]")
plt.xlabel("Year")
plt.legend()


# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_3_Solution_a8a2e784.py)
# 
# *Example output:*
# 
# <img alt='Solution hint' align='left' width=826.0 height=575.0 src=https://raw.githubusercontent.com/NeuromatchAcademy/course-content/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/static/W2D1_Tutorial_3_Solution_a8a2e784_1.png>
# 
# 

# ### **Question 1.1**
# 
# 1.   Why do you think the global mean temperature varies so much between models?* 
# 
# **If you get stuck here, reflect on the videos from earlier today and the tutorials/videos from the Climate Modelling day for inspiration.*

# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_3_Solution_23243afa.py)
# 
# 

# ### **Coding Exercise 1.2**
# 
# As you just saw, the global mean SST varies between climate models. This is not surprising given the slight differences in physics, numerics, and discretization between each model.
# 
# When we are looking at future projections, we care about how the model's *change* relative to their equilibrium/previous state. To do this, we typically subtract a historical reference period from the timeseries, which creates a new timeseries which we call the temperature *anomaly* relative to that period. **Recall that you already calculated and used *anomalies* earlier in the course (e.g., on W1D1).**
# 
# **Modify the following code to recreate the previous multi-model figure, but now instead plot the global mean sea surface temperature (GMSST) *anomaly* relative the 1950-1980 base period (i.e., subtract the 1950-1980 mean GMSST of each model from that model's timeseries)**
# 
# *Hint: you will need to use `ds.sel` to select data during the base period ([see here](https://docs.xarray.dev/en/stable/user-guide/indexing.html#indexing-with-dimension-names) under "Indexing with dimension names" for a helpful example) along with the averaging operator, `mean()`.*

# In[ ]:


# calculate anomaly to reference period
def datatree_anomaly(dt):
    dt_out = DataTree()
    for model, subtree in dt.items():
        # find the temporal average over the desired reference period
        ref = ...
        dt_out[model] = ...
    return dt_out


dt_gm_anomaly = datatree_anomaly(dt_gm)

_ = ...

plt.title("Global Mean SST Anomaly from five CMIP6 models (base period: 1950 to 1980)")
plt.ylabel("Global Mean SST Anomaly [$^\circ$C]")
plt.xlabel("Year")
plt.legend()


# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_3_Solution_cccfcaec.py)
# 
# *Example output:*
# 
# <img alt='Solution hint' align='left' width=1012.0 height=575.0 src=https://raw.githubusercontent.com/NeuromatchAcademy/course-content/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/static/W2D1_Tutorial_3_Solution_cccfcaec_1.png>
# 
# 

# ### **Questions 1.2: Climate Connection**
# 
# 1.  How does this figure compare to the previous one where the reference period was not subtracted?
# 2.  This figure uses the reference period of 1950-1980 for its anomaly calculation. How does the variability across models 100 years before the base period (1850) compare to the variability 100 years after the base period (2080)? Why do you think this is?
# 

# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_3_Solution_a59e8ac4.py)
# 
# 

# # **Summary**
# 
# In this tutorial, we expanded on the previous examination of a single CMIP6 model (*TaiESM1*), to instead work with multi-model ensemble comprising five different CMIP6 models (*TaiESM1*, *IPSL-CM6A-LR*, *GFDL-ESM4*, *ACCESS-CM2*, and *MPI-ESM1-2-LR*) developed by institutions around the world. We demonstrated the importance of anomalizing each of these models relative to a base period when calculating changes in the simulated Earth system. If variables are not anomalized, these absolute values can differ significantly between models due to the diversity of models (i.e., their distinct physics, numerics and discretization).

# # **Resources**
# 
# Data for this tutorial can be accessed [here](https://gallery.pangeo.io/repos/pangeo-gallery/cmip6/index.html).
