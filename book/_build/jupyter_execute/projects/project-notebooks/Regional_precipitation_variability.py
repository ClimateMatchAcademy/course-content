#!/usr/bin/env python
# coding: utf-8

# # Regional Precipitation Variability and Extreme Events
# 
# **Content creators:** Laura Paccini, Raphael Rocha
# 
# **Content reviewers:** Marguerite Brown, Ohad Zivan, Jenna Pearson, Chi Zhang
# 
# **Content editors:** Zane Mitrevica, Natalie Steinemann, Douglas Rao, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS and Google DeepMind

# In[ ]:


# @title Project Background
# This will be a short video introducing the content creator(s) and motivating the research direction of the template.

# @markdown
from ipywidgets import widgets
from IPython.display import YouTubeVideo
from IPython.display import IFrame
from IPython.display import display


class PlayVideo(IFrame):
    def __init__(self, id, source, page=1, width=400, height=300, **kwargs):
        self.id = id
        if source == "Bilibili":
            src = f"https://player.bilibili.com/player.html?bvid={id}&page={page}"
        elif source == "Osf":
            src = f"https://mfr.ca-1.osf.io/render?url=https://osf.io/download/{id}/?direct%26mode=render"
        super(PlayVideo, self).__init__(src, width, height, **kwargs)


def display_videos(video_ids, W=400, H=300, fs=1):
    tab_contents = []
    for i, video_id in enumerate(video_ids):
        out = widgets.Output()
        with out:
            if video_ids[i][0] == "Youtube":
                video = YouTubeVideo(
                    id=video_ids[i][1], width=W, height=H, fs=fs, rel=0
                )
                print(f"Video available at https://youtube.com/watch?v={video.id}")
            else:
                video = PlayVideo(
                    id=video_ids[i][1],
                    source=video_ids[i][0],
                    width=W,
                    height=H,
                    fs=fs,
                    autoplay=False,
                )
                if video_ids[i][0] == "Bilibili":
                    print(
                        f"Video available at https://www.bilibili.com/video/{video.id}"
                    )
                elif video_ids[i][0] == "Osf":
                    print(f"Video available at https://osf.io/{video.id}")
            display(video)
        tab_contents.append(out)
    return tab_contents


video_ids = [("Youtube", "W5o_HTsef0I"), ("Bilibili", "BV1ho4y1C7Eo")]
tab_contents = display_videos(video_ids, W=730, H=410)
tabs = widgets.Tab()
tabs.children = tab_contents
for i in range(len(tab_contents)):
    tabs.set_title(i, video_ids[i][0])
display(tabs)


# **In this project**, you will explore rain gauge and satellite data from CHIRPS and NOAA Terrestrial Climate Data Records NDVI datasets to extract rain estimates and land surface reflectance, respectively. This data will enable identification of extreme events in your region of interest. Besides investigating the relationships between these variables, you are encouraged to study the impact of extreme events on changes in vegetation.

# # Project Template
# ![Project Template](https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/projects/template-images/precipitation_template_map.svg)
# 
# *Note: The dashed boxes are socio-economic questions.*

# # Data Exploration Notebook
# ## Project Setup

# In[ ]:


# imports

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pooch
import pandas as pd
import s3fs
import boto3
import botocore
import datetime


# ## CHIRPS Version 2.0 Global Daily 0.25°
# 
# The Climate Hazards Group InfraRed Precipitation with Station data (CHIRPS) is a high-resolution precipitation dataset developed by the Climate Hazards Group at the University of California, Santa Barbara. It combines satellite-derived precipitation estimates with ground-based station data to provide gridded precipitation data at a quasi-global scale between 50°S-50°N. 
# 
# Read more about CHIRPS here:
# 
# * [The climate hazards infrared precipitation with stations—a new environmental record for monitoring extremes](https://www.nature.com/articles/sdata201566)
# 
# * [Climate Hazard Group CHG Wiki](https://wiki.chc.ucsb.edu/CHIRPS_FAQ)
# 
# * [Data storage location](https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p25/)

# ### Indices for Extreme Events
# The Expert Team on Climate Change Detection and Indices ([ETCCDI]( http://etccdi.pacificclimate.org/list_27_indices.shtml)) has defined various indices that focus on different aspects such as duration or intensity of extreme events. The following functions provide examples of how to compute indices for each category. You can modify these functions to suit your specific needs or create your own custom functions. Here are some tips you can use:
# 
# - Most of the indices require daily data, so in order to select a specific season you can just use xarray to subset the data. Example:
# 
# `daily_precip_DJF = data_chirps.sel(time=data_chirps['time.season']=='DJF')`
# 
# - A common threshold for a wet event is precipitation greater than or equal to 1mm/day, while a dry (or non-precipitating) event is defined as precipitation less than 1mm/day.
# - Some of the indices are based on percentiles. You can define a base period climatology to calculate percentile thresholds, such as the 5th, 10th, 90th, and 95th percentiles, to determine extreme events.

# In[ ]:


def calculate_sdii_index(data):
    """
    This function calculates the Simple Daily Intensity Index (SDII), which
    represents the average amount of precipitation on wet days (days with
    precipitation greater than or equal to 1mm) for each year in the input data.
    The input data should be a Dataset with time coordinates, and the function
    returns a Dataset with the SDII index values for each year in the data.
    ----------
    - data (xarray.Dataset): Input dataset containing daily precipitation data.
    - period (str, optional): Period for which to calculate the SDII index.

    Returns:
    -------
        - xarray.Dataset: Dataset containing the SDII index for the given period.
    """
    # calculate daily precipitation amount on wet days (PR >= 1mm)
    wet_days = data.where(data >= 1)

    # group by year and calculate the sum precipitation on wet days
    sum_wet_days_grouped = wet_days.groupby("time.year").sum(dim="time")

    # count number of wet days for each time step
    w = wet_days.groupby("time.year").count(dim="time")

    # divide by the number of wet days to get SDII index
    sdii = sum_wet_days_grouped / w

    return sdii


# In[ ]:


def calculate_cdd_index(data):
    """
    This function takes a daily precipitation dataset as input and calculates
    the Consecutive Dry Days (CDD) index, which represents the longest sequence
    of consecutive days with precipitation less than 1mm. The input data should
    be a DataArray with time coordinates, and the function returns a DataArray
    with the CDD values for each unique year in the input data.
    Parameters:
    ----------
      - data (xarray.DataArray): The input daily precipitation data should be
      a dataset (eg. for chirps_data the SataArray would be chirps_data.precip)
    Returns:
    -------
      - cdd (xarray.DataArray): The calculated CDD index

    """
    # create a boolean array for dry days (PR < 1mm)
    dry_days = data < 1
    # initialize CDD array
    cdd = np.zeros(len(data.groupby("time.year")))
    # get unique years as a list
    unique_years = list(data.groupby("time.year").groups.keys())
    # iterate for each day
    for i, year in enumerate(unique_years):
        consecutive_trues = []
        current_count = 0
        for day in dry_days.sel(time=data["time.year"] == year).values:
            if day:
                current_count += 1
            else:
                if current_count > 0:
                    consecutive_trues.append(current_count)
                    current_count = 0
        if current_count > 0:
            consecutive_trues.append(current_count)
        # print(consecutive_trues)
        # CDD is the largest number of consecutive days
        cdd[i] = np.max(consecutive_trues)
    # transform to dataset
    cdd_da = xr.DataArray(cdd, coords={"year": unique_years}, dims="year")
    return cdd_da


# In[ ]:


# code to retrieve and load the data

years = range(1981, 2024)  # the years you want. we want 1981 till 2023
files = [
    "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p25/chirps-v2.0."
    + str(year)
    + ".days_p25.nc"
    for year in years
]  # the format of the files
downloaded_files = [
    pooch.retrieve(file, known_hash=None) for file in files
]  # download all of the files
#### open data as xarray
chirps_data = xr.open_mfdataset(
    downloaded_files, combine="by_coords"
)  # open the files as one dataset


# We can now visualize the content of the dataset.
# 
# 

# In[ ]:


# code to print the shape, array names, etc of the dataset
chirps_data


# ## NOAA Fundamental Climate Data Records (FCDR) AVHRR Land Bundle - Surface Reflectance and Normalized Difference Vegetation Index
# 
# As we learned in the W1D3 tutorials, all the National Atmospheric and Oceanic Administration Climate Data Record (NOAA-CDR) datasets are available both at NOAA National Centers for Environmental Information (NCEI) and commercial cloud platforms. See the link [here](https://registry.opendata.aws/noaa-cdr-terrestrial/). We are accessing the data directly via the [Amazon Web Service (AWS) cloud storage space](https://noaa-cdr-ndvi-pds.s3.amazonaws.com/index.html).
# 
# For this project we recommend using the Normalized Difference Vegetation Index (NDVI). It is one of the most commonly used remotely sensed indices. It measures the "greeness" of vegetation, and is useful in understanding vegetation density and assessing changes in plant health. For example, NDVI can be used to study the impacts of droughts, heatwaves, and insect infestations on plants covering Earth's surface. A good overview of this index from this particular sensor can be accessed [here](https://digitalcommons.unl.edu/nasapub/217/).
# 
# Recall what we learned in W1D3 Tutorial 3, the data files on AWS are named systematically:
# 
# > Sensor name: `AVHRR`  
# > Product category: `Land`  
# > Product version: `v005`  
# > Product code: `AVH13C1`  
# > Satellite platform: `NOAA-07`  
# > Date of the data: `19810624`  
# > Processing time: `c20170610041337` (*This will change for each file based on when the file was processed*)  
# > File format: `.nc` (*netCDR-4 format*)
# 
# In other words, if we are looking for the data of a specific day, we can easily locate where the file might be. 
# 
# For example, if we want to find the AVHRR data for the day of *2002-03-12 (or March 12, 2002)*, you can use:
# 
# `s3://noaa-cdr-ndvi-pds/data/2002/AVHRR-Land_v005_AVH13C1_*_20020312_c*.nc`
# 
# The reasaon that we put `*` in the above directory is because we are not sure about what satellite platform this data is from and when the data was processed. The `*` is called a **wildcard**, and is used because we want *all* the files that contain our specific criteria, but do not want to have to specify all the other pieces of the filename we are not sure about yet. It should return all the data satisfying that initial criteria and you can refine further once you see what is available. Essentially, this first step helps to narrow down the data search. You can then use this to create datasets from the timeframe of your choosing.
# 

# In[ ]:


# we can use the data from W1D3 tutorial 3
# to access the NDVI data from AWS S3 bucket, we first need to connect to s3 bucket

fs = s3fs.S3FileSystem(anon=True)
client = boto3.client(
    "s3", config=botocore.client.Config(signature_version=botocore.UNSIGNED)
)  # initialize aws s3 bucket client


date_sel = datetime.datetime(2002, 1, 1, 0)  # select a desired year
file_location = fs.glob(
    "s3://noaa-cdr-ndvi-pds/data/"
    + date_sel.strftime("%Y")
    + "/AVHRR-Land_v005_AVH13C1_*_c*.nc"
)  # the files we want for a whole year
files_for_pooch = [
    pooch.retrieve("http://s3.amazonaws.com/" + file, known_hash=None)
    for file in file_location
]

ds = xr.open_mfdataset(files_for_pooch, combine="by_coords")  # open the file
ds


# <a name="dataset2-1"></a>
# ## Worldbank Data: Cereal Production
# 
# Cereal production is a crucial component of global agriculture and food security. The [World Bank](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/AG.PRD.CREL.MT) collects and provides data on cereal production, which includes crops such as wheat, rice, maize, barley, oats, rye, sorghum, millet, and mixed grains. The data covers various indicators such as production quantity, area harvested, yield, and production value.
# 
# The World Bank also collects data on land under cereals production, which refers to the area of land that is being used to grow cereal crops. This information can be valuable for assessing the productivity and efficiency of cereal production systems in different regions, as well as identifying potential areas for improvement. Overall, the World Bank's data on cereal production and land under cereals production is an important resource for policymakers, researchers, and other stakeholders who are interested in understanding global trends in agriculture and food security.

# In[ ]:


# code to retrieve and load the data
url_cereal = "https://raw.githubusercontent.com/Sshamekh/Heatwave/f85f43997e3d6ae61e5d729bf77cfcc188fbf2fd/data_cereal_land.csv"
ds_cereal_land = pd.read_csv(pooch.retrieve(url_cereal, known_hash=None))
ds_cereal_land.head()


# In[ ]:


# example
ds_cereal_land[(ds_cereal_land["Country Name"] == "Brazil")].reset_index(
    drop=True
).iloc[0].transpose()


# 
# Now you are all set to address the questions you are interested in! Just be mindful of the specific coordinate names to avoid any issues. 
# 
# You can use the provided functions as examples to compute various indices for extreme events based on duration or intensity. Don't hesitate to modify them according to your specific needs or create your own custom functions.
# 
# 
# Happy exploring and analyzing precipitation variability and extreme events in your project!
# 

# # Further Reading
# 
# - Anyamba, A. and Tucker, C.J., 2012. Historical perspective of AVHRR NDVI and vegetation drought monitoring. Remote sensing of drought: innovative monitoring approaches, 23, pp.20.[https://digitalcommons.unl.edu/nasapub/217/](https://digitalcommons.unl.edu/nasapub/217/)
# - Zhang, X., Alexander, L., Hegerl, G.C., Jones, P., Tank, A.K., Peterson, T.C., Trewin, B. and Zwiers, F.W., 2011. Indices for monitoring changes in extremes based on daily temperature and precipitation data. Wiley Interdisciplinary Reviews: Climate Change, 2(6), pp.851-870.
# - Schultz, P. A., and M. S. Halpert. "Global correlation of temperature, NDVI and precipitation." Advances in Space Research 13.5 (1993): 277-280. 
# - Seneviratne, S.I. et al., 2021: Weather and Climate Extreme Events in a Changing Climate. In Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change [Masson-Delmotte, V. et al. (eds.)]. Cambridge University Press, Cambridge, United Kingdom and New York, NY, USA, pp. 1513–1766, https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-11/
# - IPCC, 2021: Annex VI: Climatic Impact-driver and Extreme Indices [Gutiérrez J.M. et al.(eds.)]. In Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change [Masson-Delmotte, V. et al. (eds.)]. Cambridge University Press, Cambridge, United Kingdom and New York, NY, USA, pp. 2205–2214, https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_AnnexVI.pdf
