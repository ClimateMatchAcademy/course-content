#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W1D5_ClimateModeling/student/W1D5_Tutorial5.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/{ORG}/course-content/main/tutorials/W1D5_ClimateModeling/student/W1D5_Tutorial5.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 5: Radiative Equilibrium**
# 
# 
# **Week 1, Day 5, Climate Modeling**
# 
# **Content creators:** Jenna Pearson
# 
# **Content reviewers:** Yunlong Xu, Will Gregory, Peter Ohue, Derick Temfack, Zahra Khodakaramimaghsoud, Peizhen Yang, Younkap Nina Duplex, Ohad Zivan, Chi Zhang
# 
# **Content editors:** Brodie Pearson, Abigail Bodner, Ohad Zivan, Chi Zhang
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS and Google DeepMind

# # **Tutorial Objectives**
# 
# In this tutorial students will run a one-dimensional radiative equilibrium model that predicts the global mean atmospheric temperature as a function of height. Much of the code shown here was taken from [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook/home.html) by Brian Rose. Students are encouraged to visit this website for more tutorials and background on these models.
# 
# By the end of this tutorial students will be able to:
# * Implement a 1-D model that predicts atmospheric temperature as a function of height using the python package `climlab`.
# * Understand how this model builds off of the energy balance models developed in the previous tutorials.

# # **Setup**

# In[ ]:


# note the conda install takes quite a while, but conda is REQUIRED to properly download the dependencies (that are not just python packages)
# !pip install condacolab &> /dev/null           # need to use conda installation of climlab, pip won't work. condacolab is a workaround
# import condacolab
# condacolab.install()
# !mamba install -c anaconda cftime xarray numpy &> /dev/null    # for decoding time variables when opening datasets
# !mamba install -c conda-forge metpy climlab &> /dev/null


# In[ ]:


# imports
import xarray as xr  # used to manipulate data and open datasets
import numpy as np  # used for algebra/arrays
import urllib.request  # used to download data from the internet
import climlab  # one of the models we are using
import matplotlib.pyplot as plt  # used for plotting
import metpy  # used to make Skew T Plots of temperature and pressure
from metpy.plots import SkewT  # plotting function used widely in climate science
import pooch
import os
import tempfile


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


# ##  Video 1: Radiative Equilibrium
# 

# ###  Video 1: Radiative Equilibrium
# 

# ####  Video 1: Radiative Equilibrium
# 

# In[ ]:


# @title Video 1: Radiative Equilibrium
# Tech team will add code to format and display the video


# In[ ]:


# helper functions


def pooch_load(filelocation=None, filename=None, processor=None):
    shared_location = "/home/jovyan/shared/Data/tutorials/W1D4_Paleoclimate"  # this is different for each day
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


# # **Section 1: Setting up the Radiative Equilibrium Model Using Climlab**

# 
# The energy balance model we used earlier today was *zero-dimensional*, yielding only the global mean surface temperature. We might ask, is it possible to construct a similar, *one-dimensional*, model for an *atmospheric column* to estimate the global mean temperature *profile* (i.e., including the height/$z$ dimension). Additionally, can we explicitly include the effects of different gases in this model, rather than just parametrizing their collective effects through a single parameter $\tau$? **The answer is yes, we can!**
# 
# This model is too complex to construct from scratch, as we did in the previous tutorials. Instead, we will use a model already available within the python package [climlab](https://climlab.readthedocs.io/en/latest/intro.html). 
#  
# The model we will first use is a radiative equilbrium model.  **Radiative equilibrium models** consider different layers of the atmosphere. Each of these layers absorbs and emits radiation depending on its constituent gases, allowing the model to calculate the radiation budget for each layer as radiative energy is transferred between atmospheric layers, the Earth's surface, and space. **Radiative equilibrium** is reached when each layer gains energy at the same rate as it loses energy. In this tutorial you will analyze the temperature profile of this new model once it has reached equilibrium.
# 
# To set up this model, we will need information about some of the mean properties of the atmosphere. We are going to download water vapor data from the Community Earth System Model, a global climate model that we will go into detail on in the next tutorial, to use a variable called [specific humidity](https://glossary.ametsoc.org/wiki/Specific_humidity). **Specific humidity** is the mass of water vapor per mass of a unit block of air. This is useful because water vapor is an important greenhouse gas.

# In[ ]:


filename_sq = "cpl_1850_f19-Q-gw-only.cam.h0.nc"
url_sq = "https://osf.io/c6q4j/download/"

ds = xr.open_dataset(
    pooch_load(filelocation=url_sq, filename=filename_sq)
)  # ds = dataset
ds


# In[ ]:


# the specific humidity is stored in a variable called Q
ds.Q


# In[ ]:


ds.time


# however, we want an annual average profile:

# In[ ]:


# take global, annual average using a weighting (ds.gw) that is calculated based on the model grid - and is similar, but not identical, to a cosine(latitude) weighting

weight_factor = ds.gw / ds.gw.mean(dim="lat")
Qglobal = (ds.Q * weight_factor).mean(dim=("lat", "lon", "time"))
# print specific humidity profile
Qglobal


# Now that we have a global mean water vapor profile, we can define a model that has the same vertical levels as this water vapor data.

# In[ ]:


# use 'lev=Qglobal.lev' to create an identical vertical grid to water vapor data
mystate = climlab.column_state(lev=Qglobal.lev, water_depth=2.5)
mystate


# To model the absorption and emission of different gases within each atmospheric layer, we use the **[Rapid Radiative Transfer Model](https://climlab.readthedocs.io/en/latest/api/climlab.radiation.RRTMG.html)**, which is contained within the `RRTMG` module. We must first initialize our model using the water vapor .

# In[ ]:


radmodel = climlab.radiation.RRTMG(
    name="Radiation (all gases)",  # give our model a name!
    state=mystate,  # give our model an initial condition!
    specific_humidity=Qglobal.values,  # tell the model how much water vapor there is
    albedo=0.25,  # this the SURFACE shortwave albedo
    timestep=climlab.constants.seconds_per_day,  # set the timestep to one day (measured in seconds)
)
radmodel


# Let's explore this initial state. Here `Ts` is the initial global mean surface temperature, and `Tatm` is the initial global mean air temperature profile.

# In[ ]:


radmodel.state


# One of the perks of using this model is it's ability to incorporate the radiative effects of individual greenhouse gases in different parts of the radiation spectrum, rather than using a bulk reduction in transmission of outgoing longwave radiation (as in our previous models).
# 
# Let's display 'absorber_vmr', which contains the **volume mixing ratio**'s of each gas used in the radiative transfer model (these are pre-defined; and do not include the water vapor we used as a model input above). The volume mixing ratio describes the fraction of molecules in the air that are a given gas. For example, $21\%$ of air is oxygen and so it's volumn mixing ratio is 0.21.

# In[ ]:


radmodel.absorber_vmr


# To look at carbon dioxide (`CO2`) in a more familiar unit, parts per million (by volume), we can convert and print the new value.

# In[ ]:


radmodel.absorber_vmr["CO2"] * 1e6


# We can also look at all the available diagnostics of our model:

# In[ ]:


diag_ds = climlab.to_xarray(radmodel.diagnostics)
diag_ds


# For example to look at OLR,

# In[ ]:


radmodel.OLR


# Note. the OLR is currently 0 as we have not ran the model forward in time, so it has not calculated any radiation components.

# ## **Questions 1: Climate Connection**

# 1.  Why do you think all gases, except ozone and water vapor, are represented by single values in the model?

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D5_ClimateModeling/solutions/W1D5_Tutorial5_Solution_57426c01.py)
# 
# 

# ## **Coding Exercises 1**

# 1.  On the same graph, plot the annual mean specific humidity profile and ozone profiles.

# In[ ]:


fig, ax = plt.subplots()
# multiply Qglobal by 1000 to put in units of grams water vapor per kg of air
_ = ...
# multiply by 1E6 to get units of ppmv = parts per million by volume
_ = ...

# pressure decreases logarithmically with height in the atmosphere
# invert the axis so the largest value of pressure is lowest
ax.invert_yaxis()
# set y axis to a log scale
_ = ...

ax.set_ylabel("Pressure (hPa)")
ax.set_xlabel("Specific humidity (g/kg)")

# turn on the grid lines
_ = ...

# turn on legend
_ = ...


# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D5_ClimateModeling/solutions/W1D5_Tutorial5_Solution_8eaf5c15.py)
# 
# *Example output:*
# 
# <img alt='Solution hint' align='left' width=774.0 height=575.0 src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W1D5_ClimateModeling/static/W1D5_Tutorial5_Solution_8eaf5c15_0.png>
# 
# 

# # **Section 2: Getting Data to Compare to the Model**

# Before we run our model forward, we will download a reanalysis product from NCEP to get a sense of what the real global mean atmospheric temperature profile looks like. We will compare this profile to our model runs later.

# In[ ]:


filename_ncep_air = "air.mon.1981-2010.ltm.nc"
url_ncep_air = "https://osf.io/w6cd5/download/"
ncep_air = xr.open_dataset(
    pooch_load(filelocation=url_ncep_air, filename=filename_ncep_air)
)  # ds = dataset

# this is the long term monthly means (note only 12 time steps)
ncep_air.air


# In[ ]:


# need to take the average over space and time
# the grid cells are not the same size moving towards the poles, so we weight by the cosine of latitude to compensate for this
coslat = np.cos(np.deg2rad(ncep_air.lat))
weight = coslat / coslat.mean(dim="lat")

Tglobal = (ncep_air.air * weight).mean(dim=("lat", "lon", "time"))
Tglobal


# Below we will define two helper funcitons to visualize the profiles output from our model with a *SkewT* plot. This is common way to plot atmospheric temperature in climate science, and the `metpy` package has a built in function to make this easier.
# 
# 

# In[ ]:


# to setup the skewT and plot observations
def make_skewT():
    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig, rotation=30)
    skew.plot(
        Tglobal.level,
        Tglobal,
        color="black",
        linestyle="-",
        linewidth=2,
        label="Observations",
    )
    skew.ax.set_ylim(1050, 10)
    skew.ax.set_xlim(-90, 45)
    # Add the relevant special lines
    # skew.plot_dry_adiabats(linewidth=1.5, label = 'dry adiabats')
    # skew.plot_moist_adiabats(linewidth=1.5, label = 'moist adiabats')
    # skew.plot_mixing_lines()
    skew.ax.legend()
    skew.ax.set_xlabel("Temperature (degC)", fontsize=14)
    skew.ax.set_ylabel("Pressure (hPa)", fontsize=14)
    return skew


# In[ ]:


# to add a model derived profile to the skewT figure
def add_profile(skew, model, linestyle="-", color=None):
    line = skew.plot(
        model.lev,
        model.Tatm - climlab.constants.tempCtoK,
        label=model.name,
        linewidth=2,
    )[0]
    skew.plot(
        1000,
        model.Ts - climlab.constants.tempCtoK,
        "o",
        markersize=8,
        color=line.get_color(),
    )
    skew.ax.legend()


# In[ ]:


skew = make_skewT()


# SkewT (also known as SkewT-logP) plots are generally used for much [more complex reasons](https://www.weather.gov/source/zhu/ZHU_Training_Page/convective_parameters/skewt/skewtinfo.html) than we will use here. However, one of the benefits of this plot that we will utilize is the fact that pressure decreases approximately logarithmically with height. Thus, with a *logP* axis, we are showing information that is roughly linear in height, making the plots more intuitive. 

# # **Section 3: Running the Radiative Equilibrium Model Forward in Time**

# We can run this model over many time steps, just like the simple greenhouse model, but now we can examine the behavior of the temperature profile rather than just the surface temperature. 
# 
# There is no need to write out a function to step our model forward - `climlab` already has this feature. We will use this function to run our model to equilibrium (i.e., until OLR is balanced by ASR).

# In[ ]:


# take a single step forward to the diagnostics are updated and there is some energy imbalance
radmodel.step_forward()

# run the model to equilibrium (the difference between ASR and OLR is a very small number)
while np.abs(radmodel.ASR - radmodel.OLR) > 0.001:
    radmodel.step_forward()


# In[ ]:


#  check the energy budget to make sure we are really at equilibrium
radmodel.ASR - radmodel.OLR


# Now let's can compare this to observations.

# In[ ]:


skew = make_skewT()
add_profile(skew, radmodel)
skew.ax.set_title("Pure Radiative Equilibrium", fontsize=18);


# ## **Questions 3: Climate Connection**

# 1. The profile from our model does not match observations well. Can you think of one component we might be missing?
# 2. What effect do you think the individual gases play in determining this profile and why?

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D5_ClimateModeling/solutions/W1D5_Tutorial5_Solution_4724967d.py)
# 
# 

# ## **Coding Exercises 3**

# 1. Create a second model called 'Radiation (no H20)' that lacks water vapor. Then re-create the plot above, but add on this extra profile without water vapor.

# In[ ]:


# make an exact clone of our existing model
radmodel_noH2O = climlab.process_like(radmodel)
# change the name of our new model
radmodel_noH2O.name = ...

# set the water vapor profile to all zeros
radmodel_noH2O.specific_humidity *= 0.0

# run the model to equilibrium
radmodel_noH2O.step_forward()
while np.abs(radmodel_noH2O.ASR - radmodel_noH2O.OLR) > 0.01:
    radmodel_noH2O.step_forward()

# create skewT plot
skew = make_skewT()

# add profiles for both models to plot
for model in [...]:
    ...


# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D5_ClimateModeling/solutions/W1D5_Tutorial5_Solution_5eb5cfa0.py)
# 
# *Example output:*
# 
# <img alt='Solution hint' align='left' width=765.0 height=875.0 src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W1D5_ClimateModeling/static/W1D5_Tutorial5_Solution_5eb5cfa0_0.png>
# 
# 

# # **Summary**
# In this tutorial, you've learned how to use the python package `climlab` to construct a one-dimensional radiative equilibrium model, and run it forward in time to predict the global mean atmospheric temperature profile. You've also visualized these results through SkewT plots.

# # **Resources**
# 
# Data from this tutorial can be accessed for specific humidity [here](http://thredds.atmos.albany.edu:8080/thredds/fileServer/CESMA/cpl_1850_f19/concatenated/cpl_1850_f19.cam.h0.nc) and reanalysis temperature [here](https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/Monthlies/pressure/air.mon.1981-2010.ltm.nc).
