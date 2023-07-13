#!/usr/bin/env python
# coding: utf-8

# # **Ocean Acidification**
# 
# 
# **Content creators:** C. Gabriela Mayorga Adame, Lidia Krinova
# 
# **Content reviewers:** Jenna Pearson, Abigail Bodner, Ohad Zivan, Chi Zhang
# 
# **Content editors:** Zane Mitrevica, Natalie Steinemann, Ohad Zivan, Chi Zhang, Jenna Pearson
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS, Google DeepMind

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


# **In this project**, you will analyse ocean model and observational data from global databases to extract variables like pH, CO<sub>2</sub>, and temperature, and to investigate ocean acidification process in your region of interest. This project will also be an opportunity to investigate the relationships between these variables as well as their impact on the marine ecosystems.

# # Project Template
# 
# ![Project Template](https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/projects/template-images/ocean_acidification_template_map.svg)
# 
# *Note: The dashed boxes are socio-economic questions.*

# # Data Exploration Notebook
# ## Project Setup
# 

# In[ ]:


# google colab installs

# !mamaba install netCDF4


# In[ ]:


# imports

import random
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pooch
import pandas as pd


# ## NOAA Ocean pH and Acidity

# ### Global surface ocean acidification indicators from 1750 to 2100 (NCEI Accession 0259391)
# 
# This data package contains a hybrid surface OA data product that is produced based on three recent observational data products: (a) the Surface Ocean CO2 Atlas (SOCAT, version 2022), (b) the Global Ocean Data Analysis Product version 2 (GLODAPv2, version 2022), and (c) the Coastal Ocean Data Analysis Product in North America (CODAP-NA, version 2021), and 14 Earth System Models from the sixth phase of the Coupled Model Intercomparison Project (CMIP6). The trajectories of ten OA indicators, including fugacity of carbon dioxide, pH on Total Scale, total hydrogen ion content, free hydrogen ion content, carbonate ion content, aragonite saturation state, calcite saturation state, Revelle Factor, total dissolved inorganic carbon content, and total alkalinity content are provided under preindustrial conditions, historical conditions, and future Shared Socioeconomic Pathways: SSP1-19, SSP1-26, SSP2-45, SSP3-70, and SSP5-85 from 1750 to 2100 on a global surface ocean grid. These OA trajectories are improved relative to previous OA data products with respect to data quantity, spatial and temporal coverage, diversity of the underlying data and model simulations, and the provided SSPs over the 21st century.
# 
# **Citation:** 
# Jiang, L.-Q., Dunne, J., Carter, B. R., Tjiputra, J. F., Terhaar, J., Sharp, J. D., et al. (2023). Global surface ocean acidification indicators from 1750 to 2100. Journal of Advances in Modeling Earth Systems, 15, e2022MS003563. https://doi.org/10.1029/2022MS003563
# 
# **Dataset**: https://www.ncei.noaa.gov/data/oceans/ncei/ocads/metadata/0259391.html
# 

# We can load and visualize the **surface pH** as follows:

# In[ ]:


# code to retrieve and load the data
# url_SurfacepH= 'https://www.ncei.noaa.gov/data/oceans/ncei/ocads/data/0206289/Surface_pH_1770_2100/Surface_pH_1770_2000.nc' $ old CMIP5 dataset
url_SurfacepH = "https://www.ncei.noaa.gov/data/oceans/ncei/ocads/data/0259391/nc/median/pHT_median_historical.nc"
ds_pH = xr.open_dataset(pooch.retrieve(url_SurfacepH, known_hash=None))
ds_pH


# These are the files of the climate change projections under various scenarios (SSP1-19, SSP1-26, SSP2-45, SSP3-70, and SSP5-85, recall W2D1 tutorials) for those feeling adventurous: 
# *   pHT_median_ssp119.nc 
# *   pHT_median_ssp126.nc	 
# *   pHT_median_ssp245.nc 
# *   pHT_median_ssp370.nc
# *   pHT_median_ssp585.nc
# 
# To load them, replace the filename in the path/filename line above

# ## Copernicus
# 
# Copernicus is the Earth observation component of the European Union’s Space programme, looking at our planet and its environment to benefit all European citizens. It offers information services that draw from satellite Earth Observation and in-situ (non-space) data.
# 
# The European Commission manages the Programme. It is implemented in partnership with the Member States, the European Space Agency (ESA), the European Organisation for the Exploitation of Meteorological Satellites (EUMETSAT), the European Centre for Medium-Range Weather Forecasts (ECMWF), EU Agencies and Mercator Océan.
# 
# Vast amounts of global data from satellites and ground-based, airborne, and seaborne measurement systems provide information to help service providers, public authorities, and other international organisations improve European citizens' quality of life and beyond. The information services provided are free and openly accessible to users.
# 
# **Source**: https://www.copernicus.eu/en/about-copernicus

# ### ECMWF Atmospheric Composition Reanalysis: Carbon Dioxide (CO<sub>2</sub>)
# 
# From this dataset we will use **CO<sub>2</sub> column-mean molar fraction** from the Single-level chemical vertical integrals variables & **Sea Surface Temperature** from the Single-level meteorological variables (in case you need to download them direclty from the catalog). 
# 
# This dataset is part of the [ECMWF Atmospheric Composition Reanalysis focusing on long-lived greenhouse gases: carbon dioxide (CO<sub>2</sub>) and methane (CH<sub>4</sub>)](https://www.copernicus.eu/en/access-data/copernicus-services-catalogue/cams-global-ghg-reanalysis-egg4-monthly). The emissions and natural fluxes at the surface are crucial for the evolution of the long-lived greenhouse gases in the atmosphere. In this dataset the CO<sub>2</sub> fluxes from terrestrial vegetation are modelled in order to simulate the variability across a wide range of scales from diurnal to inter-annual. The CH<sub>4</sub> chemical loss is represented by a climatological loss rate and the emissions at the surface are taken from a range of datasets.
# 
# Reanalysis combines model data with observations from across the world into a globally complete and consistent dataset using a model of the atmosphere based on the laws of physics and chemistry. This principle, called data assimilation, is based on the method used by numerical weather prediction centres and air quality forecasting centres, where every so many hours (12 hours at ECMWF) a previous forecast is combined with newly available observations in an optimal way to produce a new best estimate of the state of the atmosphere, called analysis, from which an updated, improved forecast is issued. Reanalysis works in the same way to allow for the provision of a dataset spanning back more than a decade. Reanalysis does not have the constraint of issuing timely forecasts, so there is more time to collect observations, and when going further back in time, to allow for the ingestion of improved versions of the original observations, which all benefit the quality of the reanalysis product.
# 
# **Source & further information:** https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-ghg-reanalysis-egg4-monthly?tab=overview
# 

# We can load and visualize the **sea surface temperature** and **CO<sub>2</sub> concentration** (from [NOAA Global Monitoring Laboratory](https://gml.noaa.gov/ccgg/trends/gl_data.html)):

# In[ ]:


url_CO2 = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.csv"
ds_CO2 = pd.read_csv(pooch.retrieve(url_CO2, known_hash=None), header=55)

ds_CO2


# In[ ]:


# from W1D3 tutorial 6 we have Sea Surface Temprature from 1981 to the present:
# download the monthly sea surface temperature data from NOAA Physical System
# Laboratory. The data is processed using the OISST SST Climate Data Records
# from the NOAA CDR program.
# the data downloading may take 2-3 minutes to complete.

url_sst = "https://osf.io/6pgc2/download/"
ds_SST = xr.open_dataset(pooch.retrieve(url_sst, known_hash=None))
ds_SST


# **Hint for question 4:**
# 
# Use the attached image (figure 5 in this [website](https://coastadapt.com.au/ocean-acidification-and-its-effects)) and this [mapping tool](https://mapper.obis.org/). Search for each species on the mapping tool to see the spatial global distribution.

# ![effects of ocean acidifaction](https://coastadapt.com.au/sites/default/files/coastadapt_image/T2I3_Figure%205.jpg)

# # Further Reading
# 
