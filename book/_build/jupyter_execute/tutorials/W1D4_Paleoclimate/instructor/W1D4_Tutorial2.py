#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W1D4_Paleoclimate/instructor/W1D4_Tutorial2.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W1D4_Paleoclimate/instructor/W1D4_Tutorial2.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 2: Reconstructing Past Changes in Ocean Climate**
# **Week 1, Day 4, Paleoclimate**
# 
# **Content creators:** Sloane Garelick
# 
# **Content reviewers:** Yosmely Bermúdez, Dionessa Biton, Katrina Dobson, Maria Gonzalez, Will Gregory, Nahid Hasan, Sherry Mi, Beatriz Cosenza Muralles, Brodie Pearson, Jenna Pearson, Chi Zhang, Ohad Zivan 
# 
# **Content editors:** Yosmely Bermúdez, Zahra Khodakaramimaghsoud, Jenna Pearson, Agustina Pesce, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS

# # **Tutorial Objectives**
# 
# In the previous days, you learned about the El Niño–Southern Oscillation (ENSO), and have explored how satellite data can be employed to track this phenomenon during the instrumental period. In this tutorial, you will explore how oxygen isotopes of corals can record changes in temperature associated with the phase of ENSO even further back in time.
# 
# By the end of this tutorial you will be able to:
# 
# *   Understand the types of marine proxies that are used to reconstruct past climate
# *   Create a stacked plot and warming stripe to visualize ENSO temperature reconstructions
# 
# 
# 
# ### **An Overview of Isotopes in Paleoclimate**
# 
# In this tutorial, and many of the remaining tutorials in this day, you will be looking at data of hydrogen and oxygen isotopes (δD and δ<sup>18</sup>O). As you learned in the video, isotopes are forms of the same element that contain the same numbers of protons but different numbers of neutrons. The two oxygen isotopes that are most commonly used in paleoclimate are oxygen 16 (<sup>16</sup>O), which is the which is the **"lighter"** oxygen isotope, and oxygen 18 (<sup>16</sup>O), which is the **"heavier"** oxygen isotope. The two hydrogen isotopes that are most commonly used in paleoclimate are hydrogen (H), which is the **"lighter"** oxygen isotope, and deuterium (D), which is the **"heavier"** oxygen isotope. 
# 
# ![image-3.png](attachment:image-3.png)
# 
# Credit: [NASA Climate Science Investigations](https://www.ces.fau.edu/nasa/module-3/how-is-temperature-measured/isotopes.php)
# 
# ![image-2.png](attachment:image-2.png)
# 
# Credit: [NASA Climate Science Investigations](https://www.ces.fau.edu/nasa/module-3/how-is-temperature-measured/isotopes.php)
# 
# Changes in the ratio of the heavy to light isotope can reflect changes in different climate variables, depending on geographic location and the material being measured. The ratio represented in delta notation (δ) and in units of per mille (‰), and is calculated using the equation below (the same applies to the ratio of the heavy and light hydrogen isotopes):
# 
# 
# ![image.png](attachment:image.png)
# 
# The terminology for discussing δ<sup>18</sup>O and δD can be a bit confusing and there are multiple ways to reference the same trends in the data. The most common terms used to describe isotopic compositions are **"depleted"** and **"enriched"**. These terms refer to the relative amout of the heavy isotopes. Therefore, a "more depleted" isotopic value is more depleted in the heavy isotope (i.e., there is less of the heavy isotope), whereas a "more enriched" isotopic value is more enriched in the heavy isotope (i.e., there is more of the heavy isotope). Other terms that are sometimes used to describe whether isotopes are depleted or enriched are **"more negative"** or **"more positive"**. Isotopic values can be both positive and negative, so using "more negative" and "more positive" can be a bit confusing. For example, if we have isotopic values are of -15‰ and -9‰, the value of -9‰ is "more enriched" (i.e., has more of the heavy isotope) or "more positive" (i.e., is closer to zero and positive values) than -15‰. Finally, the terms **"smaller"** or **"larger"** isotopic values can also be used to reference isotopes.
# 
# Additional information about the use of isotopes in paleoclimate can be found [here](https://earthobservatory.nasa.gov/features/Paleoclimatology_OxygenBalance).
# 
# 

# # **Setup**
# 

# In[ ]:


# imports
import pandas as pd
import numpy as np
import pooch
import cartopy
import pyleoclim as pyleo
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib import patches


# ##  Video 1: Speaker Introduction
# 

# ###  Video 1: Speaker Introduction
# 

# In[ ]:


# @title Video 1: Speaker Introduction
#Tech team will add code to format and display the video


# # Section 1: Assessing Variability Related to El Niño Using Pyleoclim Series
# 
# ENSO is a recurring climate pattern involving changes in SST in the central and eastern tropical Pacific Ocean.  As we learned in the introductory video, oxygen isotopes ([&delta;<sup>18</sup>O](https://en.wikipedia.org/wiki/Δ18O)) of corals are a commonly used proxy for reconstructing changes in tropical Pacific SST and ENSO.  Long-lived corals are well-suited for studying paleo-ENSO variability because they store decades to centuries of sub-annually resolved proxy information in the tropical Pacific. The oxygen isotopes of corals are useful for studying ENSO because they record changes in sea-surface temperature (SST), with more positive values of &delta;<sup>18</sup>O corresponding to colder SSTs, and vice-versa.
# 
# One approach for detecting ENSO from coral isotope data is applying a 2- to 7-year bandpass filter to the &delta;<sup>18</sup>O records to highlight ENSO-related variability and compare (quantitatively) the bandpassed coral records to the Oceanic Niño Index (ONI) you learned about in Day 2 and Day 3. While we won't be going into this amount of detail, you may utilize the methods sections of these papers as a guide: [Cobb et al.(2003)](https://www.nature.com/articles/nature01779), [Cobb et al.(2013)](https://www.science.org/doi/10.1126/science.1228246). In this tutorial we will be looking at the &delta;<sup>18</sup>O records and comparing to a plot of the ONI without this band-pass filtering, in part to highlight why the filtering is needed.

# ## Section 1.1: Load coral oxygen isotope proxy reconstructions
# 
# The two coral records we'll look at are from [Palmyra Atoll](https://en.wikipedia.org/wiki/Palmyra_Atoll) and [Line Islands](https://en.wikipedia.org/wiki/Line_Islands), both of which are in the tropical central Pacific Ocean.
# 
# Let's plot these approximate locations as well as the Niño 3.4 region you are familiar with from the first three days.

# In[ ]:


# select data for the month of interest
# data = precip.sel(time='1979-01-01', method='nearest')

# initate plot with the specific figure size
fig = plt.figure(figsize=(9,6))

# set base map projection
ax = plt.axes(projection=ccrs.Robinson(central_longitude=180))

# add background image to show land and sea
ax.stock_img()

# add coastlines
ax.add_feature(cfeature.COASTLINE)

# add in rectangle showing Nino 3.4 region
rectangle = patches.Rectangle((170, -5),50, 10, transform=ccrs.Geodetic(),edgecolor='k',
facecolor="none", linewidth=3)
ax.add_patch(rectangle)

rx, ry = rectangle.get_xy()
cx = rx + rectangle.get_width()/2.0
cy = ry + rectangle.get_height()/2.0

# add labels
ax.annotate("Nino 3.4", (cx-10,cy), color='w', transform=ccrs.PlateCarree(), weight='bold', fontsize=10, ha='center', va='center')

# add the proxy locations
ax.scatter([-162.078333],[5.883611],transform=ccrs.Geodetic(),
          s= 50, marker = 'v',color = 'w')
ax.scatter([-157.2],[1.7],transform=ccrs.Geodetic(),
          s= 50, marker = 'v',color = 'w')

# add labels
ax.annotate("Palmyra Atoll", (-170,10), color='w', transform=ccrs.Geodetic(), weight='bold', fontsize=10, ha='center', va='center')

ax.annotate("Line Islands", (-144,-1), color='w', transform=ccrs.Geodetic(), weight='bold', fontsize=10, ha='center', va='center')

# change the map view to zoom in on central Pacific
ax.set_extent((120, 300, -25, 25), crs =ccrs.PlateCarree())


# To analyze and visualize paleoclimate proxy time series, we will be using [Pyleoclim](https://pyleoclim-util.readthedocs.io/en/latest/). Pycleoclim is specifically designed for the analysis of paleoclimate data. The package is designed around object-oriented `Series`, which can be directly manipulated for plotting and time series-appropriate analysis and operation. 
# 
# The `Series` object describes the fundamentals of a time series. To create a Pyleoclim `Series`, we first need to load the data set, and then specify values for its various properties:
# 
# *   `time`: Time values for the time series
# *   `value`: Paleo values for the time series
# *   `time_name` (optional): Name of the time vector, (e.g., 'Time', 'Age'). This is used to label the x-axis on plots
# *   `time_unit` (optional): The units of the time axis (e.g., 'years')
# *   `value_name` (optional): The name of the paleo variable (e.g., 'Temperature')
# *   `value_unit` (optional): The units of the paleo variable (e.g., 'deg C')
# *   `label` (optional): Name of the time series (e.g., 'Nino 3.4')
# *   `clean_ts` (optional): If True (default), remove NaNs and set an increasing time axis
# 
# A common data format for datasets downloaded from the NOAA Paleoclimate Database is a templated text file, which contains helpful data and metadata. 
# 
# Take a look at our two datasets [here](https://www.ncei.noaa.gov/pub/data/paleo/coral/east_pacific/palmyra_2003.txt) and [here](https://www.ncei.noaa.gov/pub/data/paleo/coral/east_pacific/cobb2013-fan-modsplice-noaa.txt).
# 
# The functionality in python allows us to ignore all of the information at the beginning of the text files, and we can load the data directly into a `pandas.DataFrame` using `.read_csv()`.
# 
# ### Section 1.1.1: Load Palmyra coral data

# In[ ]:


# download the data using the url
data_path = pooch.retrieve(
    url='https://www.ncei.noaa.gov/pub/data/paleo/coral/east_pacific/palmyra_2003.txt',
    known_hash=None
)

# from the data set, we only want the data related to Modern Living Coral.
# this data is between row 6190 and 7539 of the dataset
rows = [int(row) for row in np.linspace(6190, 7539, 7539 - 6190 + 1)]

# use pandas to read in the csv file
palmyra = pd.read_csv(
    data_path,
    skiprows=lambda x: x not in rows, # number of rows to skip based on definition of rows above
    sep='\s+',                        # how the data values are seperated (delimited) : '\s+' = space
    encoding = 'ISO-8859-1',
    names=['CalendarDate', 'd180'],
    header=None,
)

palmyra.head()


# Now that we have the data in a dataframe, we can pull the relevant columns of this datframe into a `Series` object in Pyleoclim, which will allow us to organize the relevant metadata so that we can get a well-labeled, publication-quality plot:

# In[ ]:


ts_palmyra = pyleo.Series(
    time=palmyra['CalendarDate'],
    value=palmyra['d180'],
    time_name='Calendar date',
    time_unit='Years',
    value_name = r'$d18O$',
    value_unit='per mille',
    label='Palmyra Coral'
)


# Since we want to compare datasets based on different measurements (coral &delta;<sup>18</sup>O and the ONI, i.e., a temperature anomaly), it's helpful to standardize the data by removing it's estimated mean and dividing by its estimated standard deviation. Thankfully Pyleoclim has a [function](https://pyleoclim-util.readthedocs.io/en/v0.7.4/core/ui.html#pyleoclim.core.ui.Series.standardize) to do that for us.

# In[ ]:


palmyra_stnd = ts_palmyra.standardize()
palmyra_stnd


# ### Section 1.1.2: Load Line Island coral data
# 
# We will repeat these steps for the other dataset.

# In[ ]:


# Download the data using the url
data_path2 = pooch.retrieve(
    url='https://www.ncei.noaa.gov/pub/data/paleo/coral/east_pacific/cobb2013-fan-modsplice-noaa.txt',
    known_hash=None
)
# From the data set, we only want the data related to Modern Living Coral.
# So this data is between row 6190 and 7539 of the dataset
rows = [int(row) for row in np.linspace(127, 800, 800 - 127 + 1)]
line = pd.read_csv(
    data_path2,
    skiprows=lambda x: x not in rows,
    sep='\s+',
    encoding = 'ISO-8859-1',
    names=['age', 'd18O'],
    header=None,
)

line.head()


# In[ ]:


ts_line = pyleo.Series(
    time=line['age'],
    value=line['d18O'],
    time_name='Calendar date',
    time_unit='Years',
    value_name = r'$d18O$',
    value_unit='per mille',
    label='Line Island Coral'
)


# In[ ]:


line_stnd = ts_line.standardize()
line_stnd


# # Section 2: Plot the Data Using Multiseries
# 
# We will utilize the built in features of a [multiseries](https://pyleoclim-util.readthedocs.io/en/latest/core/api.html#multipleseries-pyleoclim-multipleseries) object to plot our coral proxy data side by side. To create a `pyleo.MultipleSeries`, we first create a list with our `pyleo.Series` objects and then pass this into a `pyleo.MultipleSeries`.

# In[ ]:


# combine into a list
nino_comparison = [palmyra_stnd, line_stnd]


# In[ ]:


# create multiseries
nino = pyleo.MultipleSeries(nino_comparison, name='El Nino Comparison')


# In[ ]:


# plot the time series of both datasets
fig, ax = nino.stackplot(time_unit="year",xlim=[1960,2000], colors = ['b','g'])


# ## Questions 2: Climate Connection
# 
# Recall that as SST becomes colder, &delta;<sup>18</sup>O becomes more positive, and vice versa. Compare the figure below of the ONI to the time series of coral &delta;<sup>18</sup>O you plotted above and answer the questions below.
# 
# ![](https://climatedataguide.ucar.edu/sites/default/files/styles/extra_large/public/2022-03/indices_oni_2_2_lg.png?itok=Zew3VK_4)
# 
# Credit: [UCAR](https://climatedataguide.ucar.edu/sites/default/files/styles/extra_large/public/2022-03/indices_oni_2_2_lg.png?itok=Zew3VK_4)
# 
# 1. Do the ENSO events recorded by the ONI agree with the coral data?
# 2. What are some considerations you can think of when comparing proxies such as this to the ONI?
# 

# In[ ]:


# to_remove explanation

"""
1. In general when there is a recorded ENSO event in the ONI, there is an agreement with the coral records.  During El Nino Phases captured by the ONI (where SSTs are anomolously warm) we typically see a more negative d18O and vice versa for La Nina events.
2. ENSO is an interannual occurence, happening every 2-7 years. Within the d18O records there are high frequency signals. One thing (among many) we could do is remove these by filtering. This would help resolve our dataset into something more comparable to what the ONI is tracking.
""";


# # **Section 1.3: Make Warming Stripes Plot**

# We can also make a warming stripe for this data `Series` using the [`.stripes()`](https://pyleoclim-util.readthedocs.io/en/latest/core/api.html#pyleoclim.core.multipleseries.MultipleSeries.stripes) method, where darker red stripes indicate a warmer eastern Pacific and possibly an El Niño phase, and darker blue stripes indicate a cooler eastern Pacific and possibly La Niña phase. Can you see the trend present in the data?

# In[ ]:


fig, ax = nino.stripes(ref_period=(1960,1990), time_unit="year", show_xaxis = True, cmap = 'RdBu')


# # **Summary**
# In this tutorial, we discovered how oxygen isotopes within corals serve as a valuable archive, recording changes in temperature associated with ENSO phases.
# 
# During our explorations, 
# - We ventured into the study of proxy-based coral &delta;<sup>18</sup>O records, gaining insights into the rich historical climate data encapsulated within these marine structures.
# - We compared these records to noted ENSO events over a few decades, offering us a glimpse into the dynamic nature of this influential climate phenomenon.

# # **Resources**
# 
# Code for this tutorial is based on existing notebooks from LinkedEarth that uses the `Pyleoclim` package to [assess variability in the El Nino](https://github.com/LinkedEarth/PyleoTutorials/blob/main/notebooks/L0_a_quickstart.ipynb). 
# 
# Data from the following sources are used in this tutorial:
# 
# 
# * Cobb,K., et al., Highly Variable El Niño–Southern Oscillation Throughout the Holocene.Science 339, 67-70(2013). https://doi.org/10.1126/science.1228246 accessible [here]( https://www.ncei.noaa.gov/pub/data/paleo/coral/east_pacific/palmyra_2003.txt)
# 
# * Cobb, K., Charles, C., Cheng, H. et al. El Niño/Southern Oscillation and tropical Pacific climate during the last millennium. Nature 424, 271–276 (2003). https://doi.org/10.1038/nature01779 accessible [here]( https://www.ncei.noaa.gov/pub/data/paleo/coral/east_pacific/cobb2013-fan-modsplice-noaa.txt)
