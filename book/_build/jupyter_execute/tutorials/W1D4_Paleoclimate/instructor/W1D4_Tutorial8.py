#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W1D4_Paleoclimate/instructor/W1D4_Tutorial8.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W1D4_Paleoclimate/instructor/W1D4_Tutorial8.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 8: Paleoclimate Models**
# **Week 1, Day 4, Paleoclimate**
# 
# **Content creators:** Sloane Garelick
# 
# **Content reviewers:** Yosmely Bermúdez, Dionessa Biton, Katrina Dobson, Maria Gonzalez, Will Gregory, Nahid Hasan, Sherry Mi, Beatriz Cosenza Muralles, Brodie Pearson, Jenna Pearson, Rieke Schäfer, Chi Zhang, Ohad Zivan 
# 
# **Content editors:** Yosmely Bermúdez, Zahra Khodakaramimaghsoud, Jenna Pearson, Agustina Pesce, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS

# # **Tutorial Objectives**
# 
# So far today, we've been focusing on how proxy-based reconstructions can be used to understand past variations in Earth's climate sytem. However, another useful tool in paleoclimate is the use of climate models.  
# 
# In this tutorial, you'll explore data from the [Paleoclimate Modelling Intercomparison Project 3 (PMIP3)](https://www.nature.com/articles/nclimate1456). More specifically, you'll be analyzing global mean surface temperature (GMST) data from  simulations for the past 1,000 years. 
# 
# You'll also compare the PMIP3 GMST data to a proxy-based reconstruction of temperature from Lake Tanganyika in East Africa [(Tierney et al., 2010)](https://www.nature.com/articles/ngeo865). Through this proxy-model comparison, you'll be able to assess the differences and similarities between the two datasets. 
# 
# 
# By the end of this tutorial you will be able to:
# 
# *   Plot time series of paleoclimate model simulations
# *   Compare and interpret proxy-based reconstructions of climate to paleoclimate model simulations of climate
# 
# 
# 

# # Setup

# In[ ]:


# imports
import pandas as pd
import numpy as np
import xarray as xr
import pooch

import cartopy
import pyleoclim as pyleo


# ##  Video 1: Speaker Introduction
# 

# ###  Video 1: Speaker Introduction
# 

# In[ ]:


# @title Video 1: Speaker Introduction
#Tech team will add code to format and display the video


# 
# # **Section 1: Load Proxy-Based Temperature Reconstructions**
# 
# The proxy record we'll be analyzing in this tutorial is a 1,000 year-long lake surface temperature reconstruction from [Tierney et al., 2010](https://https://doi.org/10.1038/ngeo865). This record is from Lake Taganyika in equatorial East Africa and is based on the [TEX86 ratio](https://en.wikipedia.org/wiki/TEX86), which is a temperature proxy derived from the distribution of the isoprenoid glycerol dialkyl glycerol tetraether (iGDGT) of archaeal membrane lipids. The organisms producing these iGDGT compounds alter the structure of the compound in response to changes in temperature, so by measuring changes in the ratio of the different compounds, we can infer past changes in temperature.   
# 
# Let's start by loading the proxy data, saving it as a `Series` in Pyleoclim, and plotting a time series. 

# In[ ]:


proxy_temp = pd.read_csv(pooch.retrieve("https://osf.io/p8tx3/download", known_hash=None))
proxy_temp.head()


# In[ ]:


proxy_t = pyleo.Series(
    time=proxy_temp['Year'],
    value= proxy_temp['LST'],
    time_name='Time',
    time_unit='yrs',
    value_name='Surface Temperature',
    value_unit='ºC',
    label='Lake Tanganyika Surface Temperature'
)

proxy_t.plot(color='C1')


# ## **Questions 1**

# Let's make some initial observations about the data:
# 
# 
# 1. What is the overall temperature trend over the past 2,000 years? Where are the major increases or decrease in temperature? 
# 2. What could be the cause of these shifts in lake surface temperature? 
# 
# 

# In[ ]:


# to_remove explanation

"""
Write your observations here
1. Until about 1850, the overall temperature is relatively constant with a ~1ºC decrease from 600-1000 and a ~1.5ºC warming from 1000-1300. However, from 1850 to the present, temperature has increased by ~2.5ºC.
2. This recent increase in temperature is likely due to the impacts of anthropogenic activities.

""";


# # **Section 2: Last Millenium PMIP3 GMST Data**
# 
# We can now load GMST anomaly data from the PMIP3 simulations for the past 1,000 years ([Braconnot et al., 2012](https://doi.org/10.1038/nclimate1456) and [PAGES 2k-PMIP3 group, 2015](https://cp.copernicus.org/articles/11/1673/2015/)). The anomalies are computed compared to the mean of the time series over the full length of temporal overlap between simulations.
# 

# In[ ]:


# load the raw data 'PMIP3_GMST.txt'
url_PMIP3="https://osf.io/gw2m5/download"
df = pd.read_table(pooch.retrieve(url_PMIP3,known_hash=None))

# display the raw data
df


# Note that the data file includes several ensemble members for [Community Earth System Model (CESM)](https://www.cesm.ucar.edu/) and [Goddard Institute for Space Studies (GISS)](https://www.giss.nasa.gov/) simulations. Ensembles are essentially groups of climate model simulations used for climate projections, or in this case, reconstructions. You will learn about this in much more detail on W1D5: Climate Modeling.
# 
# For now, we can replace these with their ensemble mean series.
# 

# In[ ]:


# create a new pandas.DataFrame to store the processed data
df_new = df.copy()

# remove the data columns for CESM and GISS ensemble members
for i in range(10):
    df_new = df_new.drop([f'CESM_member_{i+1}'], axis=1)

df_new = df_new.drop(['GISS-E2-R_r1i1p127.1'], axis=1)
df_new = df_new.drop(['GISS-E2-R_r1i1p127'], axis=1)
df_new = df_new.drop(['GISS-E2-R_r1i1p121'], axis=1)

# calculate the ensemble mean for CESM and GISS, and add the results into the table
df_new['CESM'] = df[[
    'CESM_member_1',
    'CESM_member_2',
    'CESM_member_3',
    'CESM_member_4',
    'CESM_member_5',
    'CESM_member_6',
    'CESM_member_7',
    'CESM_member_8',
    'CESM_member_9',
    'CESM_member_10',
]].mean(axis=1)

df_new['GISS'] = df[[
    'GISS-E2-R_r1i1p127.1',
    'GISS-E2-R_r1i1p127',
    'GISS-E2-R_r1i1p121',
]].mean(axis=1)


# In[ ]:


# display the processed data
df_new


# In our new dataframe, you can now see that the ensemble members for CESM and GISS are now replaced with one ensemble mean for each model simulation.
# 
# 
# 
# Now we can create a Pyleoclim `Series` object for each simulated GMST time series, which will allow us to easily plot the time series for each simulation and perform data analysis using various built-in tools.

# In[ ]:


# store each pyleoclim.Series() object into a dictionary
ts_dict = {}
for name in df_new.columns[1:]:
    ts_dict[name] = pyleo.Series(
        time=df_new['Year'].values,  # the time axis
        value=df_new[name].values,   # the value axis
        label=name,                  # optional metadata: the nickname of the series
        time_name='Time',            # optional metadata: the name of the time axis
        time_unit='yrs',             # optional metadata: the unit of the time axis
        value_name='GMST anomaly',     # optional metadata: the name of the value axis
        value_unit='ºC',              # optional metadata: the unit of the value axis
    )


# We can now plot each simulation. For example, let's plot the CCSM4 GMST anomaly:

# In[ ]:


fig, ax = ts_dict['CCSM4'].plot()


# But what if we wanted to plot all of the PMIP3 time series at once? We can do that using the `MultipleSeries` object in Pyleoclim, which takes a list of `Series` objects as input. To do so, we have to convert the dictionary of `Series` into a list and then create a `MultipleSeries` object.

# In[ ]:


ts_list = [v for k, v in ts_dict.items()]  # a pythonic way to convert the pyleo.Series items in the dictionary to a list
ms_pmip = pyleo.MultipleSeries(ts_list)


# We can now plot all PMIP3 simulation time series at once:

# In[ ]:


fig, ax = ms_pmip.plot(
    lgd_kwargs={
        'bbox_to_anchor': (1.25, 1),  # move the legend to the right side
    }
)


# Note that like the paleo proxy data we have looked at, these model simulations are also referred to as reconstructions as they are attempts to recreate past climates.
# 
# The reconstructed GMST anomalies from all of the PMIP3 simulations follow the same overall trend of relatively stable, long-term temperature from 800-1800 AD, followed by an increase in temperature over the past 200 years. What do you think is driving this recent warming trend?
# 
# Despite the long-term similarities, there are also noticeable differences between the GMST time series from each simulation.  
# 
# ## **Questions 2: Climate Connection**
# 
# 1.   How are the GMST anomalies from each simulation different? What could be causing these differences?
# 4.   How do we know which simulation is the most accurate and reliable?

# In[ ]:


# to_remove explanation

"""
1. The reconstructed Global Mean Surface Temperature (GMST) anomalies from the collective time series displays a variation within the range of 1.5 ˚C. The consistency among the reconstructed values tends to increase as we approach the present day, with more substantial variation observed between the years 1200 and 1800. These differences can be attributed to several factors. For instance, each model's unique sensitivity to different forcings and their distinct representations of physical processes or spatial resolutions can lead to variations in outcomes.
2. In order to obtain the "best" simulation, a comparative analysis is conducted against observational or proxy data. The simulation that best mirrors the observed or reconstructed climate trends and variability over the same time period is often deemed the most reliable. However, it's essential to note that all models possess their own strengths and weaknesses, and the "best" model can depend on the specific climate variable or region of interest.

""";


# # **Section 3: Proxy-Model Comparisons**
# 
# Proxy-based reconstructions of climate variables in the past can provide direct measurements of temperature, precipitation, greenhouse gas concentration, etc. Comparing proxy paleoclimate records with paleoclimate model simulations can help to clarify the interpretation of the proxy record and also help to improve the ability of climate models to simulate past variations in climate.
# 
# Here, we'll compare the proxy-based Lake Tanganyika surface temperature reconstruction we downloaded and plotted at the beginning of the tutorial, with the GMST anomaly PMIP3 simulations. But first, we need to standardize the Lake Tanganyika data since we're comparing the data to the GMST anomaly.

# In[ ]:


# standardize the proxy data
proxy_stnd = proxy_t.standardize()


# In[ ]:


fig, ax = ms_pmip.plot(
    lgd_kwargs={
        'bbox_to_anchor': (1.25, 1),  # move the legend to the right side
    }
)

ax.set_ylabel('GMST anomaly (ºC)')
ax1 = ax.twinx()  # create a second axes that shares the same x-axis
ax1.set_ylabel('Tanganyika Surface Temperature Anomaly (ºC)')

proxy_stnd.plot(ax=ax1,color='black')
ax.set_xlim(xmin=850,xmax=2000)
ax.set_ylim(ymin=-4,ymax=2)
ax1.set_ylim(ymin=-4,ymax=2)


# ## **Questions 3: Climate Connection**
# 
# How do the model simulated GMST and proxy-based surface temperature compare?
# 
# 
# 1.  Is there more variability in the proxy or model temperatures? What might be causing this?
# 2.  Are the long-term trends over the last millenium in the simulated GMST anomaly and proxy-based surface temperature record similar or different?

# In[ ]:


# to_remove explanation

"""
1. The model temperatures exhibit greater variability compared to the proxy records due to the significantly lower sampling frequency of the proxies.
2. Despite the differences in variability and temporal resolution, the overall temperature trends seen in the proxy record and GMST anomaly reconstructions from all PMIP3 simulations are similar. Overall, both the model and the proxy show relatively constant temperatures until ~1850 when temperature rapidly increases due to the influence of anthropogenic forcings, particularly the increase in greenhouse gas concentrations due to human activities.

""";


# This is just one simplified example of a proxy-model comparison. Larger-scale proxy-model comparisons can help to identify spatial patterns of temperature change and assess forcing mechanisms of paleoclimate variations. In W2D1, you'll spend more time exploring climate models.

# # **Summary**
# In this tutorial, you explored the role of climate models in paleoclimate research, particularly focusing on data from PMIP3. You learned to analyze and plot time series of paleoclimate model simulations, specifically GMST anomaly data from the past 1,000 years. This data reveals a trend of relatively stable global mean surface temperature anomalies from 800-1800 AD, followed by a noticeable rise in temperature over the last two centuries.
# 
# Furthermore, you have learned to compare this model data with proxy-based reconstructions. Using the example of temperature data from Lake Tanganyika in East Africa, we've assessed the differences and similarities between the model and proxy data. This process not only enhances our interpretation of the proxy record but also improves our understanding of how well climate models simulate past climate variations.
# 
# In the next and final tutorial for today, you'll explore another tool for assessing past climate variability using both proxies and models.

# # **Resources**
# 
# Code for this tutorial is based on existing notebooks from LinkedEarth that explore [paleoclimate model-data comparisons](https://github.com/LinkedEarth/paleoHackathon/blob/main/notebooks/PaleoHack-nb08_Model-DataConfrontationInTimeDomain.ipynb) using [PMIP3 model simulations](https://github.com/LinkedEarth/paleoHackathon/blob/main/notebooks/PaleoHack-nb07_Model-DataConfrontationInFrequencyDomain.ipynb).
# 
# Data from the following sources are used in this tutorial:
# 
# *   Braconnot, P., Harrison, S., Kageyama, M. et al. Evaluation of climate models using palaeoclimatic data. Nature Clim Change 2, 417–424 (2012). https://doi.org/10.1038/nclimate1456
# *   Tierney, J., Mayes, M., Meyer, N. et al. Late-twentieth-century warming in Lake Tanganyika unprecedented since AD 500. Nature Geosci 3, 422–425 (2010). https://doi.org/10.1038/ngeo865
