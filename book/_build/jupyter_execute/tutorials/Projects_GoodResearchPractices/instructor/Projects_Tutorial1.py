#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W2D2_GoodResearchPractices/instructor/W2D2_Tutorial1.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W2D2_GoodResearchPractices/instructor/W2D2_Tutorial1.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 1: Finding a Phenomenon and Asking a Question About It** 
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
# 
# # Demos
# 
# In order to illustrate the process, we will use a sample research question about how the surface temperature of the earth depends on the CO$_2$ content of the atmosphere.

# ##  Video 1: Finding a Phenomenon & Asking a Question about it
# 

# In[ ]:


# @title Video 1: Finding a Phenomenon & Asking a Question about it

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


video_ids = [("Youtube", "jI5FSM_v95s"), ("Bilibili", "BV1ho4y1C7Eo")]
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

link_id = "y9fd4"


# # Activity: Asking Your Own Question
# 
# Write down a phenomenon you would like to gain understanding about. Take 5 minutes to construct a question about the phenomenon. Discuss amongst your group to improve the question. For some inspiration:
# 
# *   Are there other aspects of the planet that may influence the average surface temperature?
# *   Are there other features of the planet that may be impacted by changes in the average surface temperature?

# ## Make Sure to Avoid the Pitfalls!
# <details>
# <summary>Click here for a recap on pitfalls</summary>
# 
# Question is too broad
# <ul>
#   <li>Science advances one small step at a time. Narrowing the scope will help clarify your next steps</li>
#   </ul>
# 
# Question does not identify a precise aspect of the phenomenon
#   <ul>
#   <li>Clarity will help identify next steps in your research</li>
#   <li>If you are struggling to identify a precise aspect, you might need to learn more about the phenomenon. Look to the literature (Step 2)!</li>
#   </ul>
# 
# Question is about an analysis method
#   <ul>
#   <li>An analysis method is a tool, not the big picture</li>
#   </ul>
# 
# </details>
