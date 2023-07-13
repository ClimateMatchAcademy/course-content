#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/W2D1_Tutorial_6.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/W2D1_Tutorial_6.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 6: Synthesising & Interpreting Diverse Data Sources**
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
# In this tutorial, we will synthesize scientific knowledge from various sources and use this diverse information to validate and contextualize CMIP6 simulations. By the end of this tutorial, you will be able to 
# - Create a time series of global mean sea surface temperature from observations, models, and proxy data;
# - Use this data to validate & contextualize climate models, and to provide a holistic picture of Earth's past and future climate evolution.

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

# If any helper functions you want to hide for clarity (that has been seen before
# or is simple/uniformative), add here
# If helper code depends on libraries that aren't used elsewhere,
# import those libaries here, rather than in the main import cell


def global_mean(ds: xr.Dataset) -> xr.Dataset:
    """Global average, weighted by the cell area"""
    return ds.weighted(ds.areacello.fillna(0)).mean(["x", "y"], keep_attrs=True)


# calculate anomaly to reference period
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


# ##  Video 6: Historical Context for Future Projections
# 

# ###  Video 6: Historical Context for Future Projections
# 

# ####  Video 6: Historical Context for Future Projections
# 

# In[ ]:


# @title Video 6: Historical Context for Future Projections
# Tech team will add code to format and display the video


# # **Section 1: Reproduce Global SST for Historical and Future Scenario Experiments**
# 
# We are now going to reproduce the plot you created in Tutorial 4, which showed the likely range of CMIP6 simulated global mean sea surface temperature for historical and future scenario (*SSP1-2.6* and *SSP5-8.5*) experiments from a *multi-model ensemble*. However, now we will add some an additional  dataset called *HadISST* which is an observational dataset spanning back to the 1870. Later in the tutorial, we will also include the paleo data you saw in the previous mini-lecture.
# 

# ## **Section 1.1: Load CMIP6 SST Data from Several Models using `xarray`**
# 
# Let's load the five different CMIP6 models again for the three CMIP6 experiments.
# 
# 

# In[ ]:


col = intake.open_esm_datastore(
    "https://storage.googleapis.com/cmip6/pangeo-cmip6.json"
)  # open an intake catalog containing the Pangeo CMIP cloud data

# pick our five example models
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

dt_gm_anomaly = datatree_anomaly(dt_gm)


# 
# ### **Coding Exercise 1.1**
# 
# Complete the following code to:
# 
# 
# 1.  Calculate a time series of the global mean sea surface temperature (GMSST) from the HadISST dataset
# 2.  Subtract a base period from the HadISST GMSST time series. Use the same base period as the CMIP6 timeseries you are comparing against. 

# In[ ]:


for experiment, color in zip(["historical", "ssp126", "ssp585"], ["C0", "C1", "C2"]):
    datasets = []
    for model in dt_gm_anomaly.keys():
        annual_sst = (
            dt_gm_anomaly[model][experiment]
            .ds.tos.coarsen(time=12)
            .mean()
            .assign_coords(source_id=model)
            .load()
        )
        datasets.append(
            annual_sst.sel(time=slice(None, "2100")).load()
        )  # the french model has a long running member for ssp 126 (we could change the model to keep this clean)
    da = xr.concat(datasets, dim="source_id", join="override").squeeze()
    x = da.time.data
    da_lower = da.squeeze().quantile(0.17, dim="source_id")
    da_upper = da.squeeze().quantile(0.83, dim="source_id")
    plt.fill_between(range(len(x)), da_lower, da_upper, alpha=0.5, color=color)
    da.mean("source_id").plot(
        color=color,
        label=experiment,
    )

# but now add observations (https://pangeo-forge.org/dashboard/feedstock/43)
store = "https://ncsa.osn.xsede.org/Pangeo/pangeo-forge/HadISST-feedstock/hadisst.zarr"
ds_obs = xr.open_dataset(store, engine="zarr", chunks={}).convert_calendar(
    "standard", use_cftime=True
)
# mask missing values
ds_obs = ds_obs.where(ds_obs > -1000)
weights = np.cos(
    np.deg2rad(ds_obs.latitude)
)  # In a regular lon/lat grid, area is ~cos(latitude)
# calculate weighted global mean for observations
sst_obs_gm = ...
# calculate anomaly for observations
sst_obs_gm_anomaly = ...

# coarsen, trim and calculate mean then plot observations
_ = ...
plt.ylabel("Global Mean SST with respect to 1950-1980")
plt.xlabel("Year")
plt.legend()

plt.show()


# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_6_Solution_df5c4f05.py)
# 
# *Example output:*
# 
# <img alt='Solution hint' align='left' width=775.0 height=575.0 src=https://raw.githubusercontent.com/NeuromatchAcademy/course-content/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/static/W2D1_Tutorial_6_Solution_df5c4f05_0.png>
# 
# 

# ### **Questions 1.1 Climate Connection**
# 
# Now that you have a modern and projected time series containing models and observations,
# 1. What context and/or validation of the simulations does this information provide?
# 2. What additional context/validation can you glean by also considering the paleo proxy information in the figure below? (This figure was shown in the last video)
# 
# Note the paleo periods on this figure represent the Mid-Pleiocene Warm Period (MPWP), the Last Inter-glacial (LIG) ad the Last Glacial Maximum (LGM)
# 
# ![](./img/W2D1_Tutorial_6_Insert_Figure.png)
# 
# This image shows part of panel a) from Figure 9.3 from the IPCC AR6 WG1 report. This figure has the following caption: **Figure 9.3** | Sea surface temperature (SST) and its changes with time. (a) Time series of global mean SST anomaly relative to 1950–1980 climatology. Shown are paleoclimate reconstructions and PMIP models, observational reanalyses (HadISST) and multi-model means from the Coupled Model Intercomparison Project (CMIP) historical simulations, CMIP projections, and HighResMIP experiment. (b) Map of observed SST (1995–2014 climatology HadISST). (c) Historical SST changes from observations. (d) CMIP 2005–2100 SST change rate. (e) Bias of CMIP. (f) CMIP change rate. (g) 2005–2050 change rate for SSP5-8.5 for the CMIP ensemble. (h) Bias of HighResMIP (bottom left) over 1995–2014. (i) HighResMIP change rate for 1950–2014. (j) 2005–2050 change rate for SSP5-8.5 for the HighResMIP ensemble. No overlay indicates regions with high model agreement, where ≥80% of models agree on sign of change. Diagonal lines indicate regions with low model agreement, where <80% of models agree on sign of change (see Cross-Chapter Box Atlas.1 for more information). Further details on data sources and processing are available in the chapter data table (Table 9.SM.9).

# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main/tutorials/W2D1_FutureClimate-IPCCIPhysicalBasis/solutions/W2D1_Tutorial_6_Solution_7818edff.py)
# 
# 

# ## **Summary**
# 
# In the final tutorial of the day, we learned about the importance of synthesizing CMIP6 model data (future projections and historical simulations), alongside modern climate and palroclimate observations. This synthesis provides validation of CMIP6 simulation data, and it provides historical context for recent and projected rapid changes in Earth's climate, as many of these changes are unprecedented in human-recored history.
# 
# In the upcoming tutorials, we will shift our focus towards the socio-economic aspects of future climate change. This exploration will take various forms, including the design of the Shared Socioeconomic Pathways (SSPs) we began using today. We'll contemplate the realism of different socio-economic future scenarios and examine their potential impacts on future climate forcings. Moreover, we'll delve into how a changing climate might affect society. As we proceed with the next tutorials, keep in mind the intricate connection between physical and socio-economic changes.

# # **Resources**
# 
# Data for this tutorial can be accessed [here](https://gallery.pangeo.io/repos/pangeo-gallery/cmip6/index.html).
