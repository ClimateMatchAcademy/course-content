#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W2D2_GoodResearchPractices/instructor/W2D2_Tutorial3.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W2D2_GoodResearchPractices/instructor/W2D2_Tutorial3.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 3: Identifying the Basic Ingredients**
# 
# **Good Research Practices**
# 
# **Content creators:** Marguerite Brown, Yuxin Zhou
# 
# **Content reviewers:** Sherry Mi, Maria Gonzalez, Nahid Hasan, Beatriz Cosenza Muralles, Katrina Dobson, Sloane Garelick, Cheng Zhang
# 
# **Content editors:** Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS and Google DeepMind

# # Tutorial Objectives
# 
# In Tutorials 1-4, you will learn about the process of research design. This includes how to
# 
# 1.   Identify a phenomenon and formulate a research question surrounding it
# 2.   Efficiently review existing literature and knowledge about the phenomenon
# 3.   Identify what is needed to study the phenomenon
# 4.   Formulate a testable hypothesis regarding the phenomenon
# 
# By the end of these tutorials you will be able to:
# 
# *   Understand the principles of good research practices
# *   Learn to view a scientific data set or question through the lens of equity: Who is represented by this data and who is not? Who has access to this information? Who is in a position to use it?

# ##  Video 1: Basic Ingredients
# 

# In[ ]:


# @title Video 1: Basic Ingredients

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


# ##  Tutorial slides
# 

#  These are the slides for the videos in all tutorials today
# 

# In[ ]:


# @title Tutorial slides
# @markdown These are the slides for the videos in all tutorials today
from IPython.display import IFrame

link_id = "zyvwp"


# # Activity: Identifying Basic Ingredients
# 
# Take 10 minutes to discuss the advantages and disadvantages of utilizing the following basic ingredients to explore the research question discussed in Video 1:
# 
# 
# *   Ice core data for CO<sub>2</sub>
# 
# *   Deep sea sediment data for sea surface temperature
# 
# Can you think of alternative approaches that might work well?
# 
# 

# ## Choosing Your Data
# <details>
# <summary>Click here for some pointers on how to choose your data</summary>
# 
# Here are some questions to ask yourself when choosing the data to use:
# 
# What physical processes must be included?
# <ul>
#   <li>You don't want an approach that contains less than the bare minimum. For some phenomena, we know what the bare minimum is. For others, more research is needed...</li>
#   <li>If you are unsure about what physical processes are needed, check the literature!</li></ul>
# 
# What spatial and temporal resolution is necessary to capture the phenomenon?
# <ul>
# <li>GCMs can typically have a spatial resolution around 100km and time resolution of several hours.</li>
# <li> For phenomena that require higher resolution, you can either </li>
# <ul><li>Use a more idealized model that resolves smaller scales</li><li>Implement a parameterization of the sub-gridscale features within the GCM.</li>
#   </ul></ul>
# 
# What restrictions do I have for computational resources?
# <ul>
#   <li>If you do not have access to large computational resources, you can still do research using smaller datasets or idealized models</li>
#   </ul>
# 
# Am I interested in looking at a particular time period or a specific physical location?
# <ul>
#   <li>Reanalysis can be used for time periods after roughly the 1940s</li>
#   <li>Proxy data can be used for a wider historical and prehistorical data</li>
#   <li>Both reanalysis and proxy data can provide specific location information</li>
#   <li>Models can be designed to mimic the conditions of the location or time, for example:</li><ul>
#   <li>GCMs (General Circulation Models or Global Climate Models) can be set according to parameters that resemble the time period</li>
#   <li>Energy balance models can capture some aspects of average temperature in other time periods</li>
#   <li>Radiative-convective equilibrium models can capture some phenomena in the tropics</li>
#   <li>Quasi-geostrophic models can capture some phenomena in the mid-latitudes (between ~30-60 degrees)</li>
#   <li>And many more!</li>
#   </ul>
#   </ul>
# 
# Am I interested in studying a feature of the phenomenon in isolation or interactions between multiple features?
# 
# <ul>
#   <li>If you want to isolate a single aspect of the phenomenon, an idealized model may be more appropriate</li>
#   <li>If you want to study interactions between multiple features, either observational data or a more complex model may be appropriate</li>
#   </ul>
# 
# Am I trying to...
# <ul> 
# <li>explain the theory behind the phenomenon? An idealized model may be appropriate</li>
# <li>provide evidence to support or challenge a pre-existing hypothesis? Observational data or a more complex model may be appropriate</li>
# <li> document the features of the phenomenon? Observational data may be appropriate</li>
# </ul>
# 
# For more information on observational data:  
# * [NCAR's climate data guide](https://climatedataguide.ucar.edu/climate-data)
# * [NCAR's guide on real-time weather data](https://weather.rap.ucar.edu/)
# * [NOAA's guide on hydrological survey data](https://nauticalcharts.noaa.gov/data/hydrographic-survey-data.html)
# * [USGS's guide on paleoclimate proxies](https://www.usgs.gov/programs/climate-research-and-development-program/science/paleoclimate-proxies)
# * [Pangeo](https://pangeo.io/) hosts a few open-access datasets
# 
# For more information on numerical modeling: 
# 
# *    Atmospheric Model Hierarchies: Maher, P., Gerber, E. P., Medeiros, B., Merlis, T. M., Sherwood, S., Sheshadri, A., et al. (2019). Model hierarchies for understanding atmospheric circulation, Reviews of Geophysics, 57, 250– 280. https://doi.org/10.1029/2018RG000607
# *    Ocean Model Hierarchies:  Hsu, T.-Y., Primeau, F., & Magnusdottir, G. (2022). A hierarchy of global ocean models coupled to CESM1. Journal of Advances in Modeling Earth Systems, 14, e2021MS002979. https://doi.org/10.1029/2021MS002979 
