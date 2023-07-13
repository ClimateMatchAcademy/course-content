#!/usr/bin/env python
# coding: utf-8

# # **Change in Earth's albedo and its dependence on land cover changes in the past 20 years**
# 
# **Content creators:** Oz Kira, Julius Bamah
# 
# **Content reviewers:** Yuhan Douglas Rao, Abigail Bodner
# 
# **Content editors:** Zane Mitrevica, Natalie Steinemann, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Production editors:**  Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS and Google DeepMind

# In[1]:


# @title #**Project background** 
#This will be a short video introducing the content creator(s) and motivating the research direction of the template.
#The Tech team will add code to format and display the video


# The global radiative budget is affected by land cover. Regarding vegetation land cover (e.g., forests, grasslands, agricultural fields, etc.), vegetation sequesters carbon, which reduces the greenhouse effect but absorbs more radiation and reduces earth albedo, which counteracts carbon sequestration. 
# 
# In this project, we will evaluate the albedo change vs. carbon sequestration over the past years. In addition, we will track significant land use changes, specifically the creation and abandonment of agricultural land. 
# 
# **In this project**, you will have the opportunity to explore terrestrial remote sensing (recall our W1D3 tutorial on **remote sensing**) and meteorological data from GLASS and ERA5. The datasets will provide information on reflectance, albedo, meteorological variables, and land cover changes in your region of interest. We encourage you to investigate the relationships between these variables and their impact on the global radiative budget. Moreover, you can track agricultural land abandonment and analyze its potential connection to climate change. This project aligns well with the topics covered in W2D3, which you are encouraged to explore further.

# # **Project template**
# ![template](https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/projects/template-images/albedo_template_map.svg)

# # **Data exploration notebook**
# ## Project setup
# 
# Please run the following cells to install the necessary libarries into your Jupyter notebook!
#     

# In[2]:


# google colab installs
# !pip install cartopy
# !pip install DateTime 
# !pip install matplotlib
# !pip install pyhdf
# !pip install numpy
# !pip install pandas
# !pip install modis-tools


# In[3]:


# the further information on the MODIS data can be found here : 
#Import the libraries
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pooch
import xarray as xr
import os


# # **Global Land Surface Satellite (GLASS) Dataset**
# 
# The Global Land Surface Satellite (GLASS) datasets primarily based on NASA’s Advanced Very High Resolution Radiometer (AVHRR) long-term data record [(LTDR)](https://ltdr.modaps.eosdis.nasa.gov) and Moderate Resolution Imaging Spectroradiometer (MODIS) data, in conjunction with other satellite data and ancillary information. 
# 
# Currently, there are more than dozens of GLASS products are officially released, including leaf area index, fraction of green vegetation coverage, gross primary production, broadband albedo, land surface temperature, evapotranspiration, and so on. 
# 
# Here we provide you the datasets of GLASS from 1982 to 2015, a 34-year long annual dynamics of global land cover (GLASS-GLC) at 5 km resolution. In this datasets, there are 7 classes, including cropland, forest, grassland, shrubland, tundra, barren land, and snow/ice. 
# The annual global land cover map (5 km) is presented in a GeoTIFF file format named in the form of ‘GLASS-GLC_7classes_year’ with a WGS 84 projection. The relationship between the labels in the files and the 7 land cover classes is shown in the following table
# 
# You can refer to this [paper](https://doi.pangaea.de/10.1594/PANGAEA.913496) for detailed description of this.ts
# 

# In[2]:


# Table 1 Classification system, with 7 land cover classes. From paper https://www.earth-syst-sci-data-discuss.net/essd-2019-23
import pandas as pd
from IPython.display import display, HTML, Markdown
# Data as list of dictionaries
classification_system = [
    {"Label": 10, "Class": "Cropland", "Subclass": "Rice paddy", "Description": ""},
    {"Label": 10, "Class": "Cropland", "Subclass": "Greenhouse", "Description": ""},
    {"Label": 10, "Class": "Cropland", "Subclass": "Other farmland", "Description": ""},
    {"Label": 10, "Class": "Cropland", "Subclass": "Orchard", "Description": ""},
    {"Label": 10, "Class": "Cropland", "Subclass": "Bare farmland", "Description": ""},
    {"Label": 20, "Class": "Forest", "Subclass": "Broadleaf, leaf-on", "Description": "Tree cover≥10%; Height>5m; For mixed leaf, neither coniferous nor broadleaf types exceed 60%"},
    {"Label": 20, "Class": "Forest", "Subclass": "Broadleaf, leaf-off", "Description": ""},
    {"Label": 20, "Class": "Forest", "Subclass": "Needle-leaf, leaf-on", "Description": ""},
    {"Label": 20, "Class": "Forest", "Subclass": "Needle-leaf, leaf-off", "Description": ""},
    {"Label": 20, "Class": "Forest", "Subclass": "Mixed leaf type, leaf-on", "Description": ""},
    {"Label": 20, "Class": "Forest", "Subclass": "Mixed leaf type, leaf-off", "Description": ""},
    {"Label": 30, "Class": "Grassland", "Subclass": "Pasture, leaf-on", "Description": "Canopy cover≥20%"},
    {"Label": 30, "Class": "Grassland", "Subclass": "Natural grassland, leaf-on", "Description": ""},
    {"Label": 30, "Class": "Grassland", "Subclass": "Grassland, leaf-off", "Description": ""},
    {"Label": 40, "Class": "Shrubland", "Subclass": "Shrub cover, leaf-on", "Description": "Canopy cover≥20%; Height<5m"},
    {"Label": 40, "Class": "Shrubland", "Subclass": "Shrub cover, leaf-off", "Description": ""},
    {"Label": 70, "Class": "Tundra", "Subclass": "Shrub and brush tundra", "Description": ""},
    {"Label": 70, "Class": "Tundra", "Subclass": "Herbaceous tundra", "Description": ""},
    {"Label": 90, "Class": "Barren land", "Subclass": "Barren land", "Description": "Vegetation cover<10%"},
    {"Label": 100, "Class": "Snow/Ice", "Subclass": "Snow", "Description": ""},
    {"Label": 100, "Class": "Snow/Ice", "Subclass": "Ice", "Description": ""},
    {"Label": 0, "Class": "No data", "Subclass": "", "Description": ""}
]

df = pd.DataFrame(classification_system)
pd.set_option('display.max_colwidth', None)
html = df.to_html(index=False)
title_md = "### Table 1 GLASS classification system with 7 land cover classes. From [this paper](https://www.earth-syst-sci-data-discuss.net/essd-2019-23)."
display(Markdown(title_md))
display(HTML(html))


# ## **Alternative Approach to Obtain Land Cover Data and Net Primary Production (NPP) Data from MODIS**
# 
# MODIS (Moderate Resolution Imaging Spectroradiometer) is a key instrument aboard the Terra (originally known as EOS AM-1) and Aqua (originally known as EOS PM-1) satellites. Terra's orbit around the Earth is timed so that it passes from north to south across the equator in the morning, while Aqua passes south to north over the equator in the afternoon. Terra MODIS and Aqua MODIS are viewing the entire Earth's surface every 1 to 2 days, acquiring data in 36 spectral bands, or groups of wavelengths (see MODIS Technical Specifications). These data will improve our understanding of global dynamics and processes occurring on the land, in the oceans, and in the lower atmosphere. MODIS is playing a vital role in the development of validated, global, interactive Earth system models able to predict global change accurately enough to assist policy makers in making sound decisions concerning the protection of our environment (https://modis.gsfc.nasa.gov/data/).
# 
# The following procedures must be ensured:
# 1. Register an account on register at NASA earth data portal: https://urs.earthdata.nasa.gov/users/new 
# 2. pip install the following libraries into your Jupyter notebook
# 
# The following links could help you in preprocessing the MODIS dataset  
# - https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/modis-data-in-python/
# - http://www.hdfeos.org/zoo/LAADS/MYD08_D3.A2009001.006.2015088160849.hdf.py
# - https://www.moonbooks.org/Articles/How-to-read-a-MODIS-HDF-file-using-python-/
# 
# Before running the code please read [this](https://amanbagrecha.github.io/post/rs_gis/download-modis-data-using-cmr-api-in-python/). 
# 
# The following papers could assist in processing of MODIS dataset: 
# - https://www.mdpi.com/2072-4292/8/7/554 
# - https://www.tandfonline.com/doi/full/10.1080/01431161.2018.1430913
# - https://www.mdpi.com/2072-4292/6/6/5368

# In[ ]:


## Alternative Approach to Obtain Land Cover Data and Net Primary Production (NPP) Data from MODIS
# #Import the libraries

# from modis_tools.auth import ModisSession
# from modis_tools.resources import CollectionApi, GranuleApi
# from modis_tools.granule_handler import GranuleHandler
# from typing_extensions import Literal


# In[ ]:


## Alternative Approach to Obtain Land Cover Data and Net Primary Production (NPP) Data from MODIS
# #download_modis.py
# username = ""  # Update this line with your username 
# password = ""  # Update this line with your password
# # 1) connect to earthdata
# session = ModisSession(username=username, password=password)

# # 2) Query the MODIS catalog for collections
# collection_client = CollectionApi(session=session)
# collections = collection_client.query(short_name="", version="") # Collection short name + version
# # Query the selected collection for granules
# granule_client = GranuleApi.from_collection(collections[0], session=session)

# # 3) Filter the selected granules via spatial and temporal parameters
# Israel_bbox = [] # format [x_min, y_min, x_max, y_max] # add min lon,min lat, max lon and max_lat input your preferred location
# Israel_granules = granule_client.query(start_date="", end_date="", bounding_box=Israel_bbox)   #choose the start and end dates for the year-month-day you prefer

# # 4) Download the granules
# GranuleHandler.download_from_granules(Israel_granules, session, threads=-1) 
# #NB the file format will be downloaded in hdf 


# # **Gross Primary Production (GPP) Datasets**
# 
# In the tutorial, you learned about Net primary production (NPP). Another similar key ecosystem process is Gross Primary Production (GPP), which is the total amount of carbon compounds produced by photosynthesis of plants in an ecosystem in a given period of time. NPP is equal to GPP minus energy used by primary producers for respiration. GPP is the amount of energy from light converted to chemical energy per unit of time, while NPP is a measure of the net CO2 sequestered by vegetation.
# 
# Here we provide you the GPP datasets **VODCA2GPP** via [here](https://researchdata.tuwien.ac.at/records/1k7aj-bdz35) and this [paper](https://essd.copernicus.org/articles/14/1063/2022/#section6). This dataset estimates GPP based on VOD (Microwave Vegetation Optical Depth (VOD), a measure of the attenuation of microwave radiation caused by vegetation and thus relates to the total vegetation water content) using Generalized Additive Models. This VODCA2GPP is based on the period from 2007 to 2015 and uses VOD data from C-, X- and Ku-band and various GPP data sets. The data sets have different temporal coverage, which is summarized for VOD and GPP data in Table 2.

# In[6]:


import pandas as pd
from IPython.display import display, HTML, Markdown

# Data as list of dictionaries
data = [
    {"Sensor": "AMSR-E", "Time period used": "Jun 2002–Oct 2011", "AECT": "13:30", "C-band [GHz]": "6.93", "X-band [GHz]": "10.65", "Ku-band [GHz]": "18.7", "Reference": "Van der Schalie et al. (2017)"},
    {"Sensor": "AMSR2", "Time period used": "Jul 2012–Dec 2020", "AECT": "13:30", "C-band [GHz]": "6.93, 7.30", "X-band [GHz]": "10.65", "Ku-band [GHz]": "18.7", "Reference": "Van der Schalie et al. (2017)"},
    {"Sensor": "AMSR2", "Time period used": "Jul 2012–Aug 2017 (Ku-band)", "AECT": "", "C-band [GHz]": "", "X-band [GHz]": "", "Ku-band [GHz]": "", "Reference": ""},
    {"Sensor": "SSM/I F08", "Time period used": "Jul 1987–Dec 1991", "AECT": "18:15", "C-band [GHz]": "", "X-band [GHz]": "", "Ku-band [GHz]": "19.35", "Reference": "Owe et al. (2008)"},
    {"Sensor": "SSM/I F11", "Time period used": "Dec 1991–May 1995", "AECT": "17:00–18:15", "C-band [GHz]": "", "X-band [GHz]": "", "Ku-band [GHz]": "19.35", "Reference": "Owe et al. (2008)"},
    {"Sensor": "SSM/I F13", "Time period used": "May 1995–Apr 2009", "AECT": "17:45–18:40", "C-band [GHz]": "", "X-band [GHz]": "", "Ku-band [GHz]": "19.35", "Reference": "Owe et al. (2008)"},
    {"Sensor": "TMI", "Time period used": "Dec 1997–Apr 2015", "AECT": "Asynchronous", "C-band [GHz]": "", "X-band [GHz]": "10.65", "Ku-band [GHz]": "19.35", "Reference": "Owe et al. (2008), Van der Schalie et al. (2017)"},
    {"Sensor": "WindSat", "Time period used": "Feb 2003–Jul 2012", "AECT": "18:00", "C-band [GHz]": "6.8", "X-band [GHz]": "10.7", "Ku-band [GHz]": "18.7", "Reference": "Owe et al. (2008), Van der Schalie et al. (2017)"}
]

# Convert list of dictionaries into a DataFrame
df = pd.DataFrame(data)

# Set max_colwidth to None so that the full content of Description column is displayed
pd.set_option('display.max_colwidth', None)

# Convert the DataFrame to HTML and hide the index
html = df.to_html(index=False)

# Table title and link to paper in Markdown
title_md = "### Table 2: Variable names, data sets, and additional information of VODCA2GPP datasets. [Reference](https://essd.copernicus.org/articles/14/1063/2022/#section6)"

# Display the title
display(Markdown(title_md))

# Display the table
display(HTML(html))


# ## **Net Primary Production (NPP) Datasets**
# 
# Alternatively, you can access the NPP data by downloading the MCD12Q1.061 MODIS Land Cover Type Yearly Global 500m using the instruction provided earlier. The description of this dataset can be viewed [here](https://lpdaac.usgs.gov/products/mcd12q1v061/).

# In[4]:


# gpp data is acquired from this work: https://essd.copernicus.org/articles/14/1063/2022/
url_GPP='https://researchdata.tuwien.ac.at/records/1k7aj-bdz35/files/VODCA2GPP_v1.nc?download=1'
ds_GPP=xr.open_dataset(pooch.retrieve(url_GPP,known_hash=None))
ds_GPP


# # **ERA5-Land monthly averaged data from 1950 to present**
# 
# **[ERA5-Land](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land-monthly-means?tab=overview)** is a reanalysis dataset that offers an enhanced resolution compared to [ERA5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5), providing a consistent view of land variables over several decades. It is created by replaying the land component of the ECMWF ERA5 climate reanalysis, which combines model data and global observations to generate a complete and reliable dataset using the laws of physics. 
# 
# ERA5-Land focuses on the water and energy cycles at the surface level, offering a detailed record starting from 1950. The data used here is a post-processed subset of the complete ERA5-Land dataset. Monthly-mean averages have been pre-calculated to facilitate quick and convenient access to the data, particularly for applications that do not require sub-monthly fields. The native spatial resolution of the ERA5-Land reanalysis dataset is 9km on a reduced Gaussian grid (TCo1279). The data in the CDS has been regridded to a regular lat-lon grid of 0.1x0.1 degrees.
# 
# ## **To calculate albedo using ERA5-Land**
# ERA5 parameter [`Forecast albedo`](https://codes.ecmwf.int/grib/param-db/?id=243) provides is the measure of the reflectivity of the Earth's surface. It is the fraction of solar (shortwave) radiation reflected by Earth's surface, across the solar spectrum, for both direct and diffuse radiation. Values are between 0 and 1. Typically, snow and ice have high reflectivity with albedo values of 0.8 and above, land has intermediate values between about 0.1 and 0.4 and the ocean has low values of 0.1 or less. Radiation from the Sun (solar, or shortwave, radiation) is partly reflected back to space by clouds and particles in the atmosphere (aerosols) and some of it is absorbed. The rest is incident on the Earth's surface, where some of it is reflected. The portion that is reflected by the Earth's surface depends on the albedo. In the ECMWF Integrated Forecasting System (IFS), a climatological background albedo (observed values averaged over a period of several years) is used, modified by the model over water, ice and snow. Albedo is often shown as a percentage (%).
# 

# ## **Alternative Approach to Obtain Albedo Data from MERRA-2**
# 
# MERRA-2 is a NASA satellite dataset that incorporates advances that facilitate the assimilation of modern hyperspectral radiance, microwave observations, and GPS-Radio Occultation datasets. It also includes NASA's ozone profile observations starting from late 2004, and improvements in the GEOS model and the GSI assimilation system. MERRA-2 maintains a similar spatial resolution to its predecessor, approximately 50 km in the latitudinal direction. It provides different kinds of information at different spatial resolutions than MODIS. MERRA-2 has a coarser spatial resolution than MODIS. While MODIS provides land cover data at a resolution of 500 meters, MERRA-2 offers meteorological data at a much coarser resolution of approximately 50 kilometers. 
# 
# Further background on the dataset could be found [here](https://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/).
# 
# Extra help on downloading MERRA-2 datasets:
# - https://daac.gsfc.nasa.gov/information/howto?title=How%20to%20Access%20MERRA-2%20Data%20using%20OPeNDAP%20with%20Python3%20and%20Calculate%20Daily%2FWeekly%2FMonthly%20Statistics%20from%20Hourly%20Data%20
# 
# - https://github.com/emilylaiken/merradownload
# 
# - https://github.com/Open-Power-System-Data/weather_data/blob/master/download_merra2.ipynb
# 
# - https://daac.gsfc.nasa.gov/information/howto?title=How%20to%20remotely%20access%20MERRA-2%20with%20Python3%20and%20calculate%20monthly%20average%20surface%20PM2.5%20for%20world%20countries

# In[5]:


# source of landuse data: https://doi.pangaea.de/10.1594/PANGAEA.913496
# the folder "land-use" has the data for years 1982 to 2015. choose the years you need and change the path accordingly 
path_LandUse=os.path.expanduser('~/shared/Data/Projects/Albedo/land-use/GLASS-GLC_7classes_1982.tif')
ds_landuse=xr.open_dataset(path_LandUse).rename({'x':'longitude', 'y':'latitude'})
# ds_landuse.band_data[0,:,:].plot() # how to plot the global data
ds_landuse


# In[6]:


# link for albedo data:

albedo_path='~/shared/Data/Projects/Albedo/ERA/albedo-001.nc'
ds_albedo=xr.open_dataset(albedo_path)
ds_albedo # note the official variable name is fal (forecast albedo)


# for your convience, included below are preciptation and temprature ERA5 dataset for the same times as the Albedo dataset

# In[7]:


precp_path='~/shared/Data/Projects/Albedo/ERA/precipitation-002.nc'
ds_precp=xr.open_dataset(precp_path)
ds_precp # the variable name is tp (total preciptation)


# In[8]:


tempr_path='~/shared/Data/Projects/Albedo/ERA/Temperature-003.nc'
ds_tempr=xr.open_dataset(tempr_path)
ds_tempr # the variable name is t2m (temprature at 2m)


# # **Further Reading**
# - Zhao, X., Wu, T., Wang, S., Liu, K., Yang,  J. Cropland abandonment mapping at sub-pixel scales using crop phenological information and MODIS time-series images, Computers and Electronics in Agriculture, Volume 208,
# 2023,107763, ISSN 0168-1699,https://doi.org/10.1016/j.compag.2023.107763
# 
# - Shani Rohatyn et al.,  Limited climate change mitigation potential through forestation of the vast dryland regions.Science377,1436-1439(2022).DOI:10.1126/science.abm9684
# 
# - Hu, Y., Hou, M., Zhao, C., Zhen, X., Yao, L., Xu, Y. Human-induced changes of surface albedo in Northern China from 1992-2012, International Journal of Applied Earth Observation and Geoinformation, Volume 79, 2019, Pages 184-191, ISSN 1569-8432, https://doi.org/10.1016/j.jag.2019.03.018
# 
# - Duveiller, G., Hooker, J. & Cescatti, A. The mark of vegetation change on Earth’s surface energy balance. Nat Commun 9, 679 (2018). https://doi.org/10.1038/s41467-017-02810-8
# 
# - Yin, H., Brandão, A., Buchner, J., Helmers, D., Iuliano, B.G., Kimambo, N.E.,  Lewińska, K.E., Razenkova, E., Rizayeva, A., Rogova, N., Spawn, S.A., Xie, Y., Radeloff, V.C. Monitoring cropland abandonment with Landsat time series, Remote Sensing of Environment, Volume 246, 2020, 111873, ISSN 0034-4257,https://doi.org/10.1016/j.rse.2020.111873
# 
# - Gupta, P., Verma, S., Bhatla, R.,Chandel, A. S., Singh, J., & Payra, S.(2020). Validation of surfacetemperature derived from MERRA‐2Reanalysis against IMD gridded data setover India.Earth and Space Science,7,e2019EA000910. https://doi.org/10.1029/2019EA000910
# 
# - Cao, Y., S. Liang, X. Chen, and T. He (2015) Assessment of Sea Ice Albedo Radiative Forcing and Feedback over the Northern Hemisphere from 1982 to 2009 Using Satellite and Reanalysis Data. J. Climate, 28, 1248–1259, https://doi.org/10.1175/JCLI-D-14-00389.1.
# 
# - Westberg, D. J., P. Stackhouse, D. B. Crawley, J. M. Hoell, W. S. Chandler, and T. Zhang (2013), An Analysis of NASA's MERRA Meteorological Data to Supplement Observational Data for Calculation of Climatic Design Conditions, ASHRAE Transactions, 119, 210-221. 
# https://www.researchgate.net/profile/Drury-Crawley/publication/262069995_An_Analysis_of_NASA's_MERRA_Meteorological_Data_to_Supplement_Observational_Data_for_Calculation_of_Climatic_Design_Conditions/links/5465225f0cf2052b509f2cc0/An-Analysis-of-NASAs-MERRA-Meteorological-Data-to-Supplement-Observational-Data-for-Calculation-of-Climatic-Design-Conditions.pdf
