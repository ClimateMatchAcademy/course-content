#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W2D4_ClimateResponse-Extremes&amp;Variability/W2D4_Tutorial8.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/{ORG}/course-content/main/tutorials/W2D4_ClimateResponse-Extremes&amp;Variability/W2D4_Tutorial8.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 8: Thresholds**
# 
# **Week 2, Day 4, Extremes & Vulnerability**
# 
# **Content creators:** Matthias Aengenheyster, Joeri Reinders
# 
# **Content reviewers:** Younkap Nina Duplex, Sloane Garelick, Zahra Khodakaramimaghsoud, Peter Ohue, Laura Paccini, Jenna Pearson, Derick Temfack, Peizhen Yang, Cheng Zhang, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS and Google DeepMind

# # **Tutorial Objectives**

# The human body has physiological limits within which it can function. In hot conditions, the body cools itself through the process of sweating, where water evaporates from the skin, resulting in the loss of heat. The effectiveness of this cooling mechanism depends on the air's capacity to hold moisture. This is why sweating is more effective in dry heat, while humid heat feels "hotter" because it hampers the body's ability to cool down.
# 
# As a result, the combination of temperature and humidity sets limits on the body's ability to regulate its temperature. One measure that captures this combined effect is the "wet-bulb globe temperature," which combines information about ambient temperature, relative humidity, wind, and solar radiation to monitor heat stress risks while in direct sunlight. You can learn more about wet-bulb temperature on the following Wikipedia page: [Wet-bulb globe temperature](https://en.wikipedia.org/wiki/Wet-bulb_globe_temperature).
# 
# In this tutorial we will look at extreme levels of wet-bulb temperature spatially, and consider the importance of thresholds. 
# 
# By the end of the tutorial you will be able to:
# 1. Assess the risk of increasing wet-bulb globe temperatures.
# 2. Analyse how the probability of crossing threshold changes over time and between scenarios.
# 3. Assess the results of a spatial GEV analysis

# # **Setup**

# In[ ]:


# !pip install -q condacolab
# import condacolab
# condacolab.install()


# In[ ]:


# imports
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import seaborn as sns
import cmocean.cm as cmo
import os
import numpy as np
import cartopy.crs as ccrs
from scipy import stats
from scipy.stats import genextreme as gev
import gev_functions as gf
import pooch
import os
import tempfile
import extremes_functions as ef
from mystatsfunctions import OLSE, LMoments
import SDFC as sd
import cftime
import nc_time_axis

import warnings

warnings.filterwarnings("ignore")


# Note that `import gev_functions as gf` imports the functions introduced in previous tutorials.

# ##  Figure Settings
# 

# ###  Figure Settings
# 

# In[ ]:


# @title Figure Settings
import ipywidgets as widgets  # interactive display

get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
plt.style.use(
    "https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/cma.mplstyle"
)


# ##  Video 1: Speaker Introduction
# 

# ###  Video 1: Speaker Introduction
# 

# In[ ]:


# @title Video 1: Speaker Introduction
# Tech team will add code to format and display the video


# In[ ]:


# helper functions


def pooch_load(filelocation=None, filename=None, processor=None):
    shared_location = "/home/jovyan/shared/Data/tutorials/W2D4_ClimateResponse-Extremes&Variability"  # this is different for each day
    user_temp_cache = tempfile.gettempdir()

    if os.path.exists(os.path.join(shared_location, filename)):
        file = os.path.join(shared_location, filename)
    else:
        file = pooch.retrieve(
            filelocation,
            known_hash=None,
            fname=os.path.join(user_temp_cache, filename),
            processor=processor,
        )

    return file


# # **Section 1: Downloading the Data**
# 
# In this tutorial, we will utilize wet-bulb globe temperature data derived from the MPI-ESM1-2-HR climate model, developed by the Max Planck Institute for Meteorology in Hamburg, Germany. The data covers the historical period (hist) as well as three future climate scenarios (SSP1-2.6, SSP2-4.5, and SSP5-8.5). These scenarios were introduced in previous tutorials.
# 
# During the pre-processing phase, the data was subjected to a 7-day averaging process, followed by the computation of the annual maximum. As a result, the data for each grid point represents the wet bulb temperature during the most extreme 7-day period within each year.

# In[ ]:


# download file: 'WBGT_day_MPI-ESM1-2-HR_historical_r1i1p1f1_raw_runmean7_yearmax.nc'

filename_WBGT_day = "WBGT_day_MPI-ESM1-2-HR_historical_r1i1p1f1_raw_runmean7_yearmax.nc"
url_WBGT_day = "https://osf.io/69ms8/download"

wetbulb_hist = xr.open_dataset(pooch_load(url_WBGT_day, filename_WBGT_day)).WBGT
wetbulb_hist.attrs["units"] = "degC"


# The dataset consists of one entry per year. However, due to the inclusion of leap years, the data processing step resulted in different days assigned to each year. This discrepancy is deemed undesirable for analysis purposes. To address this, we resampled the data by grouping all the data points belonging to each year and taking their average. Since there is only one data point per year, this resampling process does not alter the data itself, but rather adjusts the time coordinate. This serves as a reminder to thoroughly inspect datasets before analysis, as overlooking such issues can lead to workflow failures.

# In[ ]:


wetbulb_hist = wetbulb_hist.resample(time="1Y").mean()


# Let's load the data for the remaining scenarios:

# In[ ]:


# SSP1-2.6 - 'WBGT_day_MPI-ESM1-2-HR_ssp126_r1i1p1f1_raw_runmean7_yearmax.nc'
filename_SSP126 = "WBGT_day_MPI-ESM1-2-HR_ssp126_r1i1p1f1_raw_runmean7_yearmax.nc"
url_SSP126 = "https://osf.io/67b8m/download"
wetbulb_126 = xr.open_dataset(pooch_load(url_SSP126, filename_SSP126)).WBGT
wetbulb_126.attrs["units"] = "degC"
wetbulb_126 = wetbulb_126.resample(time="1Y").mean()

# SSP2-4.5 - WBGT_day_MPI-ESM1-2-HR_ssp245_r1i1p1f1_raw_runmean7_yearmax.nc
filename_SSP245 = "WBGT_day_MPI-ESM1-2-HR_ssp245_r1i1p1f1_raw_runmean7_yearmax.nc"
url_SSP245 = "https://osf.io/fsx5y/download"
wetbulb_245 = xr.open_dataset(pooch_load(url_SSP245, filename_SSP245)).WBGT
wetbulb_245.attrs["units"] = "degC"
wetbulb_245 = wetbulb_245.resample(time="1Y").mean()

# SSP5-8.5 - WBGT_day_MPI-ESM1-2-HR_ssp585_r1i1p1f1_raw_runmean7_yearmax.nc
filename_SSP585 = "WBGT_day_MPI-ESM1-2-HR_ssp585_r1i1p1f1_raw_runmean7_yearmax.nc"
url_SSP585 = "https://osf.io/pr456/download"
wetbulb_585 = xr.open_dataset(pooch_load(url_SSP585, filename_SSP585)).WBGT
wetbulb_585.attrs["units"] = "degC"
wetbulb_585 = wetbulb_585.resample(time="1Y").mean()


# Let's look at how the data is structured:

# In[ ]:


wetbulb_hist


# There is one data point per year on a latitude-longitude grid. Let's compute the grid spacing in the longitude and latitude directions:

# In[ ]:


wetbulb_hist.lon.diff("lon").values.mean()


# In[ ]:


wetbulb_hist.lat.diff("lat").values.mean()


# Each grid box in the dataset has an approximate size of 1 degree by 1 degree, which translates to about 100 km by 100 km at the equator. However, this size decreases as we move towards the poles due to the convergence of the meridians. It is important to consider the limitations imposed by this grid resolution.
# 
# As a result, at the equator, the grid boxes cover an area of approximately 100 km by 100 km, while their size decreases in the mid-latitudes.
# 
# Considering these grid box limitations, can you identify any potential limitations or challenges they may introduce in the analysis?

# ## **Section 1.1: Focus on New Delhi, India**

# In[ ]:


# find the nearest model point to the latitude and longitude of New Delhi
wetbulb_hist_delhi = wetbulb_hist.sel(lon=77.21, lat=28.61, method="nearest")
wetbulb_126_delhi = wetbulb_126.sel(lon=77.21, lat=28.61, method="nearest")
wetbulb_245_delhi = wetbulb_245.sel(lon=77.21, lat=28.61, method="nearest")
wetbulb_585_delhi = wetbulb_585.sel(lon=77.21, lat=28.61, method="nearest")


# In[ ]:


# plot the results
fig, ax = plt.subplots()
wetbulb_hist_delhi.plot(linestyle="-", marker=".", label="hist", ax=ax)
wetbulb_126_delhi.plot(linestyle="-", marker=".", label="ssp126", ax=ax)
wetbulb_245_delhi.plot(linestyle="-", marker=".", label="ssp245", ax=ax)
wetbulb_585_delhi.plot(linestyle="-", marker=".", label="ssp585", ax=ax)

ax.legend()
ax.set_title("")
ax.set_ylabel("Maximum 7-day Mean Wet-Bulb Globe Temperature")
ax.grid(True)


# Note:
# 1. Trends are visible in the historical period
# 2. Distinct differences between climate scenarios are apparent
# 3. Strong variability - each year is not necessarily warmer than the previous one
# 
# Let't fit the data to a GEV distribution and get the associated return levels.

# In[ ]:


shape_hist, loc_hist, scale_hist = gev.fit(wetbulb_hist_delhi.values, 0)
return_levels_hist = gf.fit_return_levels(
    wetbulb_hist_delhi.values, years=np.arange(1.1, 1000), N_boot=100
)


# Now we can plot the probability density functions, the return levels, and assess the fit using the QQ plot from previous tutorials.

# In[ ]:


fig, axs = plt.subplots(2, 2, constrained_layout=True)
ax = axs.flatten()

x = np.linspace(0, 1, 100)
ax[0].plot(
    gev.ppf(x, shape_hist, loc=loc_hist, scale=scale_hist),
    np.quantile(wetbulb_hist_delhi, x),
    "o",
)
xlim = ax[0].get_xlim()
ylim = ax[0].get_ylim()
ax[0].plot(
    [min(xlim[0], ylim[0]), max(xlim[1], ylim[1])],
    [min(xlim[0], ylim[0]), max(xlim[1], ylim[1])],
    "k",
)

ax[0].set_xlim(xlim)
ax[0].set_ylim(ylim)


x = np.linspace(wetbulb_hist_delhi.min() - 1, wetbulb_hist_delhi.max() + 1, 1000)
wetbulb_hist_delhi.plot.hist(
    bins=np.arange(29, 33, 0.25),
    histtype="step",
    density=True,
    lw=1,
    color="k",
    ax=ax[2],
    label="histogram",
)
ax[2].plot(x, gev.pdf(x, shape_hist, loc=loc_hist, scale=scale_hist), label="Modeled")
sns.kdeplot(wetbulb_hist_delhi, ax=ax[2], label="Empirical")
ax[2].legend()

gf.plot_return_levels(return_levels_hist, ax=ax[3])
ax[3].set_xlim(1.5, 1000)
# ax[3].set_ylim(0,None)

ax[0].set_title("QQ-plot")
ax[2].set_title("PDF")
ax[3].set_title("Return levels")

ax[1].remove()


# Let's calculate the 100-year return level.

# In[ ]:


print(
    "100-year return level: %.2f"
    % gf.estimate_return_level_period(100, loc_hist, scale_hist, shape_hist)
)


# Now let's compare with the last 30 years of the SSP-245 scenario, the middle scenario we looked at before. 2050-2100 are approximately stationary here, so we can leave out that utility.

# In[ ]:


shape_245, loc_245, scale_245 = gev.fit(
    wetbulb_245_delhi.sel(time=slice("2070", "2100")).values, 0
)
return_levels_245 = gf.fit_return_levels(
    wetbulb_245_delhi.sel(time=slice("2070", "2100")).values,
    years=np.arange(1.1, 1000),
    N_boot=100,
)


# In[ ]:


fig, axs = plt.subplots(2, 2, constrained_layout=True)
ax = axs.flatten()

x = np.linspace(0, 1, 100)
ax[0].plot(
    gev.ppf(x, shape_245, loc=loc_245, scale=scale_245),
    np.quantile(wetbulb_245_delhi.sel(time=slice("2051", "2100")), x),
    "o",
)
xlim = ax[0].get_xlim()
ylim = ax[0].get_ylim()
ax[0].plot(
    [min(xlim[0], ylim[0]), max(xlim[1], ylim[1])],
    [min(xlim[0], ylim[0]), max(xlim[1], ylim[1])],
    "k",
)

ax[0].set_xlim(xlim)
ax[0].set_ylim(ylim)


x = np.linspace(
    wetbulb_245_delhi.sel(time=slice("2051", "2100")).min() - 1,
    wetbulb_245_delhi.sel(time=slice("2051", "2100")).max() + 1,
    1000,
)
wetbulb_245_delhi.sel(time=slice("2051", "2100")).plot.hist(
    bins=np.arange(29, 33, 0.25),
    histtype="step",
    density=True,
    lw=1,
    color="k",
    ax=ax[2],
    label="histogram",
)
ax[2].plot(x, gev.pdf(x, shape_245, loc=loc_245, scale=scale_245), label="Modeled")
sns.kdeplot(
    wetbulb_245_delhi.sel(time=slice("2051", "2100")), ax=ax[2], label="Empirical"
)
ax[2].legend()

gf.plot_return_levels(return_levels_245, ax=ax[3])
ax[3].set_xlim(1.5, 1000)
# ax[3].set_ylim(0,None)

ax[0].set_title("QQ-plot")
ax[2].set_title("PDF")
ax[3].set_title("Return levels")

ax[1].remove()


# In[ ]:


print(
    "100-year return level: %.2f"
    % gf.estimate_return_level_period(100, loc_245, scale_245, shape_245)
)


# Compute as well the fit and return levels for the remaining two scenarios (SSP-126 and SSP-585). Save the QQ plot etc for your own testing later on.
# 
# You can then plot all return level curves together to compare.

# In[ ]:


return_levels_126 = gf.fit_return_levels(
    wetbulb_126_delhi.sel(time=slice("2070", "2100")).values,
    years=np.arange(1.1, 1000),
    N_boot=100,
)
return_levels_585 = gf.fit_return_levels(
    wetbulb_585_delhi.sel(time=slice("2070", "2100")).values,
    years=np.arange(1.1, 1000),
    N_boot=100,
)


# In[ ]:


fig, ax = plt.subplots()
gf.plot_return_levels(return_levels_hist, c="k", label="historical", ax=ax)
gf.plot_return_levels(return_levels_126, c="C0", label="ssp126", ax=ax)
gf.plot_return_levels(return_levels_245, c="C1", label="ssp245", ax=ax)
gf.plot_return_levels(return_levels_585, c="C2", label="ssp585", ax=ax)

ax.set_xlim(1, 100)
ax.set_ylim(29.5, 37)
ax.legend()
ax.grid(True, which="both")
ax.set_xlabel("Return Period (years)")
ax.set_ylabel("Return Level (degrees C)")


# ## **Questions 1.2**
# 
# Compare the common event (return period << 10 years) to the very rare event (return period ~ 100 years) events under the different scenarios.
# 
# 1. What is the return level of a 3-year event under the SSP5-8.5 scenario? Note down the level. What would be the return period of such an event in the other scenarios?
# 
# 2. What is the return level of a 100-year event in the historical scenario. How often would such an event occur under the other scenarios?

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W2D4_ClimateResponse-Extremes&Variability/solutions/W2D4_Tutorial8_Solution_cd448da3.py)
# 
# 

# ## **Section 1.2: Return Levels Over Different Intervals**

# Besides the late period (2070-2011), compute the return levels over the near future (2015-2050). Then let's plot the timeseries, and overlay the 100-year return level, as computed over 2015-2050, 2070-2100, and the historical period:

# In[ ]:


return_levels_126_2015_2050 = gf.fit_return_levels(
    wetbulb_126_delhi.sel(time=slice("2015", "2050")).values,
    years=np.arange(1.1, 1000),
    N_boot=100,
)
return_levels_245_2015_2050 = gf.fit_return_levels(
    wetbulb_245_delhi.sel(time=slice("2015", "2050")).values,
    years=np.arange(1.1, 1000),
    N_boot=100,
)
return_levels_585_2015_2050 = gf.fit_return_levels(
    wetbulb_585_delhi.sel(time=slice("2015", "2050")).values,
    years=np.arange(1.1, 1000),
    N_boot=100,
)


# In[ ]:


fig, ax = plt.subplots()
wetbulb_hist_delhi.groupby("time.year").mean().plot.line(
    alpha=0.5, c="k", label="hist", ax=ax
)
wetbulb_126_delhi.groupby("time.year").mean().plot.line(
    alpha=0.5, c="C0", label="ssp126", ax=ax
)
wetbulb_245_delhi.groupby("time.year").mean().plot.line(
    alpha=0.5, c="C1", label="ssp245", ax=ax
)
wetbulb_585_delhi.groupby("time.year").mean().plot.line(
    alpha=0.5, c="C2", label="ssp585", ax=ax
)
ax.set_title("")
ax.legend()
ax.hlines(
    return_levels_hist.GEV.sel(period=100, method="nearest").values,
    1950,
    2014,
    "k",
    linestyle="--",
    lw=2,
)

ax.hlines(
    return_levels_126_2015_2050.GEV.sel(period=100, method="nearest").values,
    2015,
    2050,
    "C0",
    linestyle="--",
    lw=2,
)
ax.hlines(
    return_levels_245_2015_2050.GEV.sel(period=100, method="nearest").values,
    2015,
    2050,
    "C1",
    linestyle="--",
    lw=2,
)
ax.hlines(
    return_levels_585_2015_2050.GEV.sel(period=100, method="nearest").values,
    2015,
    2050,
    "C2",
    linestyle="--",
    lw=2,
)

ax.hlines(
    return_levels_126.GEV.sel(period=100, method="nearest").values,
    2070,
    2100,
    "C0",
    linestyle=":",
    lw=2,
)
ax.hlines(
    return_levels_245.GEV.sel(period=100, method="nearest").values,
    2070,
    2100,
    "C1",
    linestyle=":",
    lw=2,
)
ax.hlines(
    return_levels_585.GEV.sel(period=100, method="nearest").values,
    2070,
    2100,
    "C2",
    linestyle=":",
    lw=2,
)
plt.title("")
plt.ylabel("Maximum 7-day Mean Wet-Bulb Globe Temperature")


# ## **Section 1.2: Time-Dependent Return Levels**

# Looking at the previous plot we see trends present in our datasets, with the 100-year event return levels varying across the time periods we have choosen. This suggests that our location parameter is changing with time.
# 
# Now, similar to the previous tutorial, we assume that the location parameter is a function of time and proceed to estimate the GEV distribution for the four scenarios:

# In[ ]:


def estimate_return_level_model(quantile, model):
    loc, scale, shape = model.loc, model.scale, model.shape
    level = loc - scale / shape * (1 - (-np.log(quantile)) ** (-shape))
    return level


# In[ ]:


law_ns_hist = sd.GEV()
law_ns_hist.fit(
    wetbulb_hist_delhi.values, c_loc=np.arange(wetbulb_hist_delhi.time.size)
)

law_ns_126 = sd.GEV()
law_ns_126.fit(wetbulb_126_delhi.values, c_loc=np.arange(wetbulb_126_delhi.time.size))

law_ns_126 = sd.GEV()
law_ns_126.fit(wetbulb_126_delhi.values, c_loc=np.arange(wetbulb_126_delhi.time.size))

law_ns_245 = sd.GEV()
law_ns_245.fit(wetbulb_245_delhi.values, c_loc=np.arange(wetbulb_245_delhi.time.size))

law_ns_585 = sd.GEV()
law_ns_585.fit(wetbulb_585_delhi.values, c_loc=np.arange(wetbulb_585_delhi.time.size))


# In[ ]:


fig, ax = plt.subplots()
wetbulb_hist_delhi.plot.line(c="k", ax=ax)
wetbulb_126_delhi.plot.line(c="C0", ax=ax)
wetbulb_245_delhi.plot.line(c="C1", ax=ax)
wetbulb_585_delhi.plot.line(c="C2", ax=ax)

ax.plot(
    wetbulb_hist_delhi.time,
    estimate_return_level_model(1 - 1 / 100, law_ns_hist),
    "k--",
    label="100-year return level: hist",
)
ax.plot(
    wetbulb_126_delhi.time,
    estimate_return_level_model(1 - 1 / 100, law_ns_126),
    "C0--",
    label="100-year return level: ssp126",
)
ax.plot(
    wetbulb_245_delhi.time,
    estimate_return_level_model(1 - 1 / 100, law_ns_245),
    "C1--",
    label="100-year return level: ssp245",
)
ax.plot(
    wetbulb_585_delhi.time,
    estimate_return_level_model(1 - 1 / 100, law_ns_585),
    "C2--",
    label="100-year return level: ssp585",
)

ax.legend()
ax.set_title("")
ax.set_ylabel("Maximum 7-day Mean Wet-Bulb Globe Temperature")


# Now we again compute the AIC for the constant and time-dependent models, and compare their performance:

# In[ ]:


def compute_aic(model):
    return 2 * len(model.coef_) + 2 * model.info_.mle_optim_result.fun


# In[ ]:


# compute stationary models:
law_ss_hist = sd.GEV()
law_ss_hist.fit(wetbulb_hist_delhi.values)

law_ss_126 = sd.GEV()
law_ss_126.fit(wetbulb_126_delhi.values)

law_ss_126 = sd.GEV()
law_ss_126.fit(wetbulb_126_delhi.values)

law_ss_245 = sd.GEV()
law_ss_245.fit(wetbulb_245_delhi.values)

law_ss_585 = sd.GEV()
law_ss_585.fit(wetbulb_585_delhi.values)


# In[ ]:


aics = pd.DataFrame(
    columns=["hist", "ssp126", "ssp245", "ssp585"], index=["constant", "covariate"]
)

aics["hist"] = compute_aic(law_ss_hist), compute_aic(law_ns_hist)
aics["ssp126"] = compute_aic(law_ss_126), compute_aic(law_ns_126)
aics["ssp245"] = compute_aic(law_ss_245), compute_aic(law_ns_245)
aics["ssp585"] = compute_aic(law_ss_585), compute_aic(law_ns_585)


# In[ ]:


aics.round(2)


# The AIC is lower when using a covariate, suggesting that including the time-dependence into the location parameter improves the quality of the model. The exception is the SSP1-2.6 scenario, which does not perform as well. This is because, unlike the other scenarios and historical period, the wet-bulb globe temperatures stabilize, and this the location parameter is less dependent on time. In this instance, making other parameters depend on time could potentially improve the performance.

# # **Section 2: Spatial Analysis**

# After looking at New Delhi, India, now we can make use of the spatial information:

# 
# The code provided below is commented and is used to fit the GEV distribution for each grid point. For the historical scenario, the entire time range is used, while for the selected scenarios, the period from 2071 to 2100 (the last 30 years of the data) is used.
# 
# Please note that the computation for this code takes some time (approximately 9 minutes per dataset). To save time, we have already precomputed the data, so there is no need to run the commented code. However, you are free to uncomment and run the code, make modifications, or include time-dependent parameters (as shown above) at your convenience. If desired, you can also focus on specific regions.

# Expensive code that fits a GEV distribution to each grid point:

# In[ ]:


# this code requires the authors' extremes_functions.py file and SDFC library from github: https://github.com/yrobink/SDFC
# The code takes roughly 30 minutes to execute, in the next cell we load in the precomputed data. Uncomment the following lines if you want to rerun.
# fit_sp_hist = ef.fit_return_levels_sdfc_2d(wetbulb_hist.rename({'lon':'longitude','lat':'latitude'}),times=np.arange(1.1,1000),periods_per_year=1,kind='GEV',N_boot=0,full=True)
# fit_sp_126 = ef.fit_return_levels_sdfc_2d(wetbulb_126.sel(time=slice('2071','2100')).rename({'lon':'longitude','lat':'latitude'}),times=np.arange(1.1,1000),periods_per_year=1,kind='GEV',N_boot=0,full=True)
# fit_sp_245 = ef.fit_return_levels_sdfc_2d(wetbulb_245.sel(time=slice('2071','2100')).rename({'lon':'longitude','lat':'latitude'}),times=np.arange(1.1,1000),periods_per_year=1,kind='GEV',N_boot=0,full=True)
# fit_sp_585 = ef.fit_return_levels_sdfc_2d(wetbulb_585.sel(time=slice('2071','2100')).rename({'lon':'longitude','lat':'latitude'}),times=np.arange(1.1,1000),periods_per_year=1,kind='GEV',N_boot=0,full=True)


# ## **Section 2.1: Load Pre-Computed Data**

# In[ ]:


# historical - wbgt_hist_raw_runmean7_gev.nc
fname_wbgt_hist = "wbgt_hist_raw_runmean7_gev.nc"
url_wbgt_hist = "https://osf.io/dakv3/download"
fit_sp_hist = xr.open_dataset(pooch_load(url_wbgt_hist, fname_wbgt_hist))

# SSP-126 - wbgt_126_raw_runmean7_gev_2071-2100.nc
fname_wbgt_126 = "wbgt_126_raw_runmean7_gev_2071-2100.nc"
url_wbgt_126 = "https://osf.io/ef9pv/download"
fit_sp_126 = xr.open_dataset(pooch_load(url_wbgt_126, fname_wbgt_126))

# SSP-245 - wbgt_245_raw_runmean7_gev_2071-2100.nc
fname_wbgt_245 = "wbgt_245_raw_runmean7_gev_2071-2100.nc"
url_wbgt_245 = "https://osf.io/j4hfc/download"
fit_sp_245 = xr.open_dataset(pooch_load(url_wbgt_245, fname_wbgt_245))

# SSP-585 - wbgt_585_raw_runmean7_gev_2071-2100.nc
fname_bgt_58 = "wbgt_585_raw_runmean7_gev_2071-2100.nc"
url_bgt_585 = "https://osf.io/y6edw/download"
fit_sp_585 = xr.open_dataset(pooch_load(url_bgt_585, fname_bgt_58))


# Also load the area for each grid box - we will use this later to compute global averages:

# In[ ]:


# filename - area_mpi.nc
filename_area_mpi = "area_mpi.nc"
url_area_mpi = "https://osf.io/zqd86/download"
area = xr.open_dataarray(pooch_load(url_area_mpi, filename_area_mpi))

# filename - area_land_mpi.nc
filename_area_mpi = "area_land_mpi.nc"
url_area_land_mpi = "https://osf.io/dxq98/download"
area_land = xr.open_dataarray(pooch_load(url_area_land_mpi, filename_area_mpi)).fillna(
    0.0
)


# Now, let's examine the 100-year return level in the historical run and compare it to the period from 2071-2100 in the three scenarios. The colorbar has been set to start at 28 degrees, which is approximately the temperature reached during the severe heatwaves in Europe in 2003 and Russia in 2010.

# In[ ]:


fig, axs = plt.subplots(
    2,
    2,
    constrained_layout=True,
    figsize=(12, 8),
    subplot_kw=dict(projection=ccrs.Robinson()),
)
ax = axs.flatten()

kwargs = dict(
    vmin=28, vmax=38, cmap=cmo.amp, transform=ccrs.PlateCarree(), add_colorbar=False
)

p = (
    fit_sp_hist["return level"]
    .sel({"return period": 100}, method="nearest")
    .plot(ax=ax[0], **kwargs)
)
fit_sp_126["return level"].sel({"return period": 100}, method="nearest").plot(
    ax=ax[1], **kwargs
)
fit_sp_245["return level"].sel({"return period": 100}, method="nearest").plot(
    ax=ax[2], **kwargs
)
fit_sp_585["return level"].sel({"return period": 100}, method="nearest").plot(
    ax=ax[3], **kwargs
)

cbar = fig.colorbar(
    p,
    ax=ax,
    pad=0.025,
    orientation="horizontal",
    shrink=0.75,
    label="100-year return level (degree)",
    extend="max",
)

ax[0].set_title("Historical")
ax[1].set_title("SSP1-2.6, 2091-2100")
ax[2].set_title("SSP2-4.5, 2091-2100")
ax[3].set_title("SSP5-8.5, 2091-2100")

[axi.set_facecolor("grey") for axi in ax]
[axi.coastlines(lw=0.5) for axi in ax]


# In the following regions where the hottest heatwave is above 31 degrees wet-bulb globe temperature are given by the red shading, which is considered a "critical temperature" above which a human will die within a few hours without non-evaporative cooling like air conditioning:

# In[ ]:


fig, axs = plt.subplots(
    2,
    2,
    constrained_layout=True,
    figsize=(12, 8),
    subplot_kw=dict(projection=ccrs.Robinson()),
)
ax = axs.flatten()

kwargs = dict(vmin=0, cmap=cmo.amp, transform=ccrs.PlateCarree(), add_colorbar=False)

p = (wetbulb_hist.sel(time=slice("2005", "2014")).max("time") > 31).plot(
    ax=ax[0], **kwargs
)
(wetbulb_126.sel(time=slice("2091", "2100")).max("time") > 31).plot(ax=ax[1], **kwargs)
(wetbulb_245.sel(time=slice("2091", "2100")).max("time") > 31).plot(ax=ax[2], **kwargs)
(wetbulb_585.sel(time=slice("2091", "2100")).max("time") > 31).plot(ax=ax[3], **kwargs)

# cbar = fig.colorbar(p,ax=ax,pad=0.025,orientation='horizontal',shrink=0.75,label='Most extreme 7-day mean WBGT')

ax[0].set_title("Historical, 2005-2014")
ax[1].set_title("SSP1-2.6, 2091-2100")
ax[2].set_title("SSP2-4.5, 2091-2100")
ax[3].set_title("SSP5-8.5, 2091-2100")

[axi.set_facecolor("grey") for axi in ax]
[axi.coastlines(lw=0.5) for axi in ax]

fig.suptitle("Shaded regions for most extreme heatwave is > 31 WBGT")


# Now we will examine the changes over time in the portion of the Earth's land surface affected by extreme heatwaves. To accomplish this, we utilize the previously loaded grid box area data.
# 
# Next, we assign a value of "1" to the temporal-spatial data if it surpasses the defined threshold, and a value of "0" if it does not. By conducting an area-weighted average across the entire land area of the world, we determine the fraction of land area experiencing a heatwave above the threshold for each year.

# In[ ]:


fig, ax = plt.subplots()
((wetbulb_hist > 31) * 1).weighted(area_land).mean(["lon", "lat"]).plot.line(
    "k.-", label="historical", ax=ax
)
((wetbulb_126 > 31) * 1).weighted(area_land).mean(["lon", "lat"]).plot.line(
    ".-", label="ssp126", ax=ax
)
((wetbulb_245 > 31) * 1).weighted(area_land).mean(["lon", "lat"]).plot.line(
    ".-", label="ssp245", ax=ax
)
((wetbulb_585 > 31) * 1).weighted(area_land).mean(["lon", "lat"]).plot.line(
    ".-", label="ssp585", ax=ax
)

ax.grid(True)

ax.legend()
ax.set_ylabel("Land Area Fraction")
ax.set_title("Fraction of land area with 7 days of wet bulb temperature > 31 degrees")


# In[ ]:


print(
    "Fraction of the land area of the world that experiences a heatwave above wet bulb temperature of 31 in the last 10 years of each run:"
)
(
    pd.Series(
        index=["historical", "SSP-126", "SSP-245", "SSP-585"],
        data=[
            ((wetbulb_hist > 31) * 1)
            .weighted(area_land)
            .mean(["lon", "lat"])
            .isel(time=slice(-10, None))
            .mean()
            .values,
            ((wetbulb_126 > 31) * 1)
            .weighted(area_land)
            .mean(["lon", "lat"])
            .isel(time=slice(-10, None))
            .mean()
            .values,
            ((wetbulb_245 > 31) * 1)
            .weighted(area_land)
            .mean(["lon", "lat"])
            .isel(time=slice(-10, None))
            .mean()
            .values,
            ((wetbulb_585 > 31) * 1)
            .weighted(area_land)
            .mean(["lon", "lat"])
            .isel(time=slice(-10, None))
            .mean()
            .values,
        ],
    ).astype(float)
    * 100
).round(2)


# ###  **Questions 2.1** 
# 1. What observations can you make when examining the time evolution and comparing the different scenarios?
# 2. Do you think these results would change if you used a different threshold such as 28 aor 33 degrees? Why would it be important to look at this?

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W2D4_ClimateResponse-Extremes&Variability/solutions/W2D4_Tutorial8_Solution_43e64815.py)
# 
# 

# # **Summary**
# In this tutorial, you learned what the "wet-bulb glob temperature" is and its implications for human health. You analyzed the likelihood of crossing critical thresholds under historical and future climate scenarios, using data from a specific climate model. You learned how to conduct a spatial GEV analysis and evaluated the potential human impact under extreme heatwaves.

# # **Resources**
# 
# The data for this tutorial was accessed through the [Pangeo Cloud platform](https://pangeo.io/cloud.html). 
#  
# This tutorial uses data from the simulations conducted as part of the [CMIP6](https://pcmdi.llnl.gov/CMIP6/) multi-model ensemble, in particular the models MPI-ESM1-2-HR. 
# 
# MPI-ESM1-2-HR was developed and the runs conducted by the [Max Planck Institute for Meteorology](https://mpimet.mpg.de/en/homepage) in Hamburg, Germany. 
# 
# For references on particular model experiments see this [database](https://www.wdc-climate.de/ords/f?p=127:2).
