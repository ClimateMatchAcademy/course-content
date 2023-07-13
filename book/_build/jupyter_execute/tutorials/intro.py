#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/NeuromatchAcademy/course-content/blob/main/tutorials/intro.ipynb" target="_blank"><img alt="Open In Colab" src="https://colab.research.google.com/assets/colab-badge.svg"/></a>   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/NeuromatchAcademy/course-content/main/tutorials/intro.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # Introduction
# 
# ## Welcome to Computational Tools in Climate Science!

# ![Sponsors](./static/cma_sponsors_intro_2.png)

# ## Welcome Video

# 
# 

# 
# 

# In[ ]:


# @markdown
from ipywidgets import widgets

out2 = widgets.Output()
with out2:
    from IPython.display import IFrame

    class BiliVideo(IFrame):
        def __init__(self, id, page=1, width=400, height=300, **kwargs):
            self.id = id
            src = "https://player.bilibili.com/player.html?bvid={0}&page={1}".format(
                id, page
            )
            super(BiliVideo, self).__init__(src, width, height, **kwargs)

    video = BiliVideo(id="BV12a411p7Zj", width=730, height=410, fs=1)
    print("Video available at https://www.bilibili.com/video/{0}".format(video.id))
    display(video)

out1 = widgets.Output()
with out1:
    from IPython.display import YouTubeVideo

    video = YouTubeVideo(id="KRSomVVqYwI", width=730, height=410, fs=1, rel=0)
    print("Video available at https://youtube.com/watch?v=" + video.id)
    display(video)

out = widgets.Tab([out1, out2])
out.set_title(0, "Youtube")
out.set_title(1, "Bilibili")

display(out)


# ## Concepts map
# 
# <img src="Art/CMA_Concept_Map.png" alt="Concept map overview of curriculum" class="bg-primary" width="100%">
# 
# *Image made by Sloane Garelick

# We have curated an integrated program of tutorials, research projects and professional development activities. The curriculum spans most areas of climate science and will cover cutting-edge methods to analyse climate data and models. This section will overview the curriculum.
# 
# ## Prerequisite refreshers
# We curated a number of [refresher resources](https://github.com/NeuromatchAcademy/precourse/blob/main/prereqs/ClimateScience.md) for you that will help you prepare for Climatematch Academy. You are not required to study this material before the course. It is rather meant to help you detect and fill any gaps you may have in your knowledge. 
# The **Introduction to Python** pre-course is an asynchronous course that you can complete on your own time. You will learn how to code in Python from scratch using straightforward examples curated by Project Pythia. If you have questions about the pre-course material, we offer support via Discord chat on July 12-14, 2023
# You will also find other open-source resources to catch up on algebra, statistics, calculus, physics, chemistry, and climate science. The topics covered on these days were carefully chosen based on what you need for the course.
# 
# ## The Academy begins!
# You will start out your two weeks at Climatematch Academy covering the **fundamentals** for understanding climate science data and research. This will include an overview of the climate system and xarray, as well as an introduction to good, equitable research practices.  
# 
# You will then switch your focus on different types of **climate data**. You will use reanalysis products, remote sensing data, and paleoclimate proxy data to understand multi-scale climate interactions, climate monitoring, and variations in past marine, terrestrial, and atmospheric climates. 
# 
# This will be followed by an introduction to the **future of the climate system** as predicted through climate modeling. You will learn about climate models, how to interpret their projections of future climate and the standard framework for assessing socio-economic climate risks. You will also explore pathways to mitigate those risks. During this time, you will also have a full day to work on your research projects, which will give you a chance to incorporate these new insights into your data analyses and interpretation. 
# 
# Finally, the course will cover the **responses to climate change**, including identification of extreme climate events, like heatwaves, droughts, or wildfires, and the use of climate data for tracking the impacts of climate change to inform adaptation measures.
# 
# You can find more details on the daily schedule and topics taught on different days in the [General Schedule](https://comptools.climatematch.io/tutorials/Schedule/daily_schedules.html).

# 
# ```{toctree}
# :hidden:
# :titlesonly:
# 
# 
# Schedule/schedule_intro.md
# ```
# 
# 
# ```{toctree}
# :hidden:
# :titlesonly:
# 
# 
# TechnicalHelp/tech_intro.md
# ```
# 
# 
# ```{toctree}
# :hidden:
# :titlesonly:
# 
# 
# TechnicalHelp/Links_Policy.md
# ```
# 
# 
# ```{toctree}
# :hidden:
# :titlesonly:
# 
# 
# prereqs/ClimateScience.md
# ```
# 
# 
# ```{toctree}
# :hidden:
# :titlesonly:
# :caption: Fundamentals
# 
# Climate System Overview (W1D1) <W1D1_ClimateSystemOverview/chapter_title.md>
# Good Research Practices (Projects) <Projects_GoodResearchPractices/chapter_title.md>
# ```
# 
# 
# ```{toctree}
# :hidden:
# :titlesonly:
# :caption: Climate Data
# 
# State of the Climate Ocean and Atmosphere Reanalysis (W1D2) <W1D2_StateoftheClimateOceanandAtmosphereReanalysis/chapter_title.md>
# Remote Sensing Land Ocean and Atmosphere (W1D3) <W1D3_RemoteSensingLandOceanandAtmosphere/chapter_title.md>
# Paleoclimate (W1D4) <W1D4_Paleoclimate/chapter_title.md>
# ```
# 
# 
# ```{toctree}
# :hidden:
# :titlesonly:
# :caption: Climate Future
# 
# Climate Modeling (W1D5) <W1D5_ClimateModeling/chapter_title.md>
# Future Climate - IPCC I Physical Basis (W2D1) <W2D1_FutureClimate-IPCCIPhysicalBasis/chapter_title.md>
# Future Climate - IPCC II & III Socio-Economic Basis (W2D3) <W2D3_FutureClimate-IPCCII&IIISocio-EconomicBasis/chapter_title.md>
# ```
# 
# 
# ```{toctree}
# :hidden:
# :titlesonly:
# :caption: Climate Response
# 
# Climate Response - Extremes & Variability (W2D4) <W2D4_ClimateResponse-Extremes&Variability/chapter_title.md>
# Climate Response - Adaptation Impact (W2D5) <W2D5_ClimateResponse-AdaptationImpact/chapter_title.md>
# ```
# 
# 
# ```{toctree}
# :hidden:
# :titlesonly:
# :caption: Project Booklet
# 
# Introduction <../projects/README.md>
# Daily guide for projects <../projects/docs/project_guidance.md>
# Project materials <../projects/docs/datasets_overview.md>
# Continuing your project after the course <../projects/docs/continuing_your_project_after_the_course.md>
# ```
# 
# 
# ```{toctree}
# :hidden:
# :titlesonly:
# :caption: Professional Development
# 
# Introduction <../projects/professional_development/README.md>
# Impact Talks <../projects/professional_development/impact_talks.ipynb>
# Mentor Meetings <../projects/professional_development/mentors.md>
# Career Features <../projects/professional_development/career_features.md>
# Career Panels <../projects/professional_development/career_panels.md>
# ```
# 
