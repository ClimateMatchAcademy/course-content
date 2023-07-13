#!/usr/bin/env python
# coding: utf-8

# # **Heatwaves: Assessing the Dynamic Interactions of the Atmosphere and Land**
# 
# **Content creators:** Sara Shamekh, Ibukun Joyce Ogwu
# 
# **Content reviewers:** Sloane Garelick, Grace Lindsay, Douglas Rao, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Sloane Garelick, Zane Mitrevica, Natalie Steinemann, Ohad Zivan, Chi Zhang
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS, Google DeepMind, and CMIP

# The atmosphere and land are entwined components of the Earth's system, constantly exchanging energy, mass, and momentum. Their interaction contributes to a variety of physical and biological processes. Understanding of the dynamic interactions between atmosphere and land is crucial for predicting and mitigating the impacts of climate change, such as land-use changes and hazards ranging from droughts, floods, and even fluctuation in agricultural production and products ([Jach et. al., 2022](https://esd.copernicus.org/articles/13/109/2022/); [Ogwu et. al. 2018](https://www.researchgate.net/publication/325142745_Economics_of_Soil_Fertility_Management_Practices_in_Nigeria); [Dirmeyer et. al. 2016](https://journals.ametsoc.org/view/journals/bams/99/6/bams-d-17-0001.1.xml)). 
# 
# Climate change is also expected to have a significant impact on cereal production around the world. Changes in temperature, precipitation patterns, and extreme weather events can all affect crop yields, as well as the timing and quality of harvests. For example, higher temperatures can lead to reduced yields for crops like wheat and maize, while changes in rainfall patterns can result in droughts or floods that can damage crops or delay planting.  
# 
# In order to better understand the relationship between climate change and cereal production, researchers have begun to explore the use of environmental monitoring data, including air temperature and soil moisture, to help identify trends and patterns in crop production. By collecting and analyzing this data over time, it may be possible to develop more accurate models and predictions of how climate change will affect cereal production in different regions of the world.
# 
# However, it is important to note that while environmental monitoring data can provide valuable insights, there are many other factors that can affect cereal production, including soil quality, pests and diseases, and agricultural practices. Therefore, any efforts to correlate cereal production with climate change must take into account a wide range of factors and be based on robust statistical analyses in order to ensure accurate and reliable results.
# 
# **In this project**, you will look into how specific climate variables represent and influence our changing climate. In particular,you will explore various climate variables from model data to develop a more comprehensive understanding of different drivers of heatwaves (periods during which the temperature exceeds the climatological average for a certain number of consecutive days over a region larger than a specified value). You will further use this data to understand land-atmosphere interactions, and there will also be an opportunity to relate the aforementioned climate variables to trends in cereal production.

# # Project Template
# 
# ![Project Template](https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/projects/template-images/heatwaves_template_map.svg)
# 
# *Note: The dashed boxes are socio-economic questions.*

# # Data Exploration Notebook
# ## Project Setup

# In[ ]:


# google colab installs
# !pip install condacolab
# import condacolab
# condacolab.install()


# In[ ]:


# !mamba install xarray-datatree intake intake-esm gcsfs xmip aiohttp cartopy nc-time-axis cf_xarray xarrayutils "esmf<=8.3.1" xesmf


# In[ ]:


# imports
import time

tic = time.time()

import pandas as pd
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
import random
import pooch


# In[ ]:


# @title Figure settings
import ipywidgets as widgets  # interactive display

get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
plt.style.use(
    "https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/cma.mplstyle"
)
# model_colors = {k:f"C{ki}" for ki, k in enumerate(source_ids)}
get_ipython().run_line_magic('matplotlib', 'inline')


# ## CMIP6: Near Surface Temperature
# 
# The CMIP6 dataset will be utilized to examine temperature trends and heatwaves. Specifically, we will be focusing on near-surface temperature, which refers to the air temperature at the Earth's surface. In this study, we will be analyzing data from one model and examining its historical temperature records. However, we encourage students to explore other models and investigate intermodel variability, as they have learned to do during their exploration of the CMIP dataset in W2D1 tutorials.
# 
# After selecting our model, we will plot the near-surface air temperature for the entire globe.

# In[ ]:


# loading CMIP data

col = intake.open_esm_datastore(
    "https://storage.googleapis.com/cmip6/pangeo-cmip6.json"
)  # open an intake catalog containing the Pangeo CMIP cloud data

# pick our five example models
# There are many more to test out! Try executing `col.df['source_id'].unique()` to get a list of all available models
source_ids = ["MPI-ESM1-2-LR"]


# In[ ]:


# from the full `col` object, create a subset using facet search
cat = col.search(
    source_id=source_ids,
    variable_id="tas",
    member_id="r1i1p1f1",
    table_id="3hr",
    grid_label="gn",
    experiment_id=["historical"],  # add scenarios if interested in projection
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
dt


# In[ ]:


# select just a single model and experiment
tas_historical = dt["MPI-ESM1-2-LR"]["historical"].ds.tas
print("The time range is:")
print(
    tas_historical.time[0].data.astype("M8[h]"),
    "to",
    tas_historical.time[-1].data.astype("M8[h]"),
)


# Now it's time to plot the data. For this initial analysis, we will focus on a specific date and time. As you may have noticed, we are using 3-hourly data, which allows us to also examine the diurnal and seasonal cycles. It would be fascinating to explore how the amplitude of the diurnal and seasonal cycles varies by region and latitude. You can explore this later!

# In[ ]:


fig, ax_present = plt.subplots(
    figsize=[12, 6], subplot_kw={"projection": ccrs.Robinson()}
)

# plot a timestep for July 1, 2013
tas_present = tas_historical.sel(time="2013-07-01T00").squeeze()
tas_present.plot(ax=ax_present, transform=ccrs.PlateCarree(), cmap="magma", robust=True)
ax_present.coastlines()
ax_present.set_title("July, 1st 2013")


# ### CMIP6: Precipitation and Soil Moisture (Optional)

# In addition to examining temperature trends, you can also load precipitation data or variables related to soil moisture. This is an optional exploration, but if you choose to do so, you can load regional precipitation data at the same time and explore how these two variables are related when analyzing regional temperature trends. This can provide insights into how changes in temperature and precipitation may be affecting the local environment.

# The relationship between soil moisture, vegetation, and temperature is an active field of research. To learn more about covariability of temperature and moisture, you can have a look at [Dong et al. (2022)](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2021GL097697) or [Humphrey et al. (2021)](https://www.nature.com/articles/s41586-021-03325-5). 

# ## World Bank Data: Cereal Production and Land Under Cereal Production
# 
# Cereal production is a crucial component of global agriculture and food security. The World Bank collects and provides data on cereal production, which includes crops such as wheat, rice, maize, barley, oats, rye, sorghum, millet, and mixed grains. The data covers various indicators such as production quantity, area harvested, yield, and production value.
# 
# The World Bank also collects data on land under cereals production, which refers to the area of land that is being used to grow cereal crops. This information can be valuable for assessing the productivity and efficiency of cereal production systems in different regions, as well as identifying potential areas for improvement. Overall, the World Bank's data on cereal production and land under cereals production is an important resource for policymakers, researchers, and other stakeholders who are interested in understanding global trends in agriculture and food security.

# In[ ]:


# code to retrieve and load the data
rrl_cereal = "https://raw.githubusercontent.com/Sshamekh/Heatwave/f85f43997e3d6ae61e5d729bf77cfcc188fbf2fd/data_cereal_land.csv"
ds_cereal_land = pd.read_csv(pooch.retrieve(rrl_cereal, known_hash=None))
ds_cereal_land.head()


# ### Hint for Q7: Heatwave Detection
# 
# Question 7 asks you to detect heatwave. Below you can see a flowchart for detecting heatwaves. The flowchart includes three parameters that you need to set in adavance. These three parameters are:
# 1. **w-day:** the window (number of days) over which you detect the extreme (95 percentile) of temperature.
# 2. **E (km<sup>2</sup>):** the spatial extent of the heatwave.
# 3. **X (days):** the duration of heatwave. 
# 
# 
# ![picture](https://raw.githubusercontent.com/Sshamekh/Heatwave/e7ae59ac394b0a9a040bcc4f58009ab478a3daa8/Heat_wave_detection_flewchart.jpg)
# 

# ### Hint for Q9: Correlation
# For Question 9 you need to compute the correlation between two variables. You can use Pearson's correlation coefficient to evaluate the correlation between two variables. You can read about Pearsons correlation coefficient [on Wikipedia](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient) and from [Scipy python library](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html). You are also encouraged to plot the scatter plot between two variables to visually see their correlation. 

# ### Hint for Q12: Linear Regressions for Heatwave Detection
# For Question 12, read the following article: [Rousi et al. (2022)](https://www.nature.com/articles/s41467-022-31432-y.pdf)
# 
# For Question 12 you need to build the regession model. You can read abut regression models [on Wikipedia](https://en.wikipedia.org/wiki/Simple_linear_regression) and from [Scipy python library](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html).

# ### Hint for Q13: Data-Driven Approaches for Heatwave Detection
# For Question 13, read the following articles: [Li et al. (2023)](https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2023GL103405) and [Jacques-Dumas et al. (2022)](https://www.frontiersin.org/articles/10.3389/fclim.2022.789641/full)

# # Further Reading
# 
# - Dirmeyer, P. A., Gochis, D. J., & Schultz, D. M. (2016). Land-atmosphere interactions: the LoCo perspective. Bulletin of the American Meteorological Society, 97(5), 753-771.
# 
# - Ogwu I. J., Omotesho, O. A. and Muhammad-Lawal, A., (2018) Chapter 11: Economics of Soil Fertility Management Practices in Nigeria in the book by Obayelu, A. E. ‘Food Systems Sustainability and Environmental Policies in Modern Economies’ (pp. 1-371).Hershey, PA: IGI Global. doi:10.4018/978-1-5225-3631-4 
# 
# - Jach, L., Schwitalla, T., Branch, O., Warrach-Sagi, K., and Wulfmeyer, V. (2022) Sensitivity of land–atmosphere coupling strength to changing atmospheric temperature and moisture over Europe, Earth Syst. Dynam., 13, 109–132, https://doi.org/10.5194/esd-13-109-2022
# 

# # **Resources**
# 
# This tutorial uses data from the simulations conducted as part of the [CMIP6](https://wcrp-cmip.org/) multi-model ensemble. 
# 
# For examples on how to access and analyze data, please visit the [Pangeo Cloud CMIP6 Gallery](https://gallery.pangeo.io/repos/pangeo-gallery/cmip6/index.html) 
# 
# For more information on what CMIP is and how to access the data, please see this [page](https://github.com/ClimateMatchAcademy/course-content/blob/main/tutorials/CMIP/CMIP_resource_bank.md).
