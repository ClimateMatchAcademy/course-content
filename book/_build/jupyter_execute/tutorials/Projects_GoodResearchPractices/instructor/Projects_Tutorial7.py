#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W2D2_GoodResearchPractices/instructor/W2D2_Tutorial7.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W2D2_GoodResearchPractices/instructor/W2D2_Tutorial7.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 7: Interpreting the Results**
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

# # Tutorials Objectives
# 
# In Tutorials 5-8, you will learn about the research process. This includes how to
# 
# 5.   Draft analyses of data to test a hypothesis
# 6.   Implement analysis of data
# 7.   Interpret results in the context of existing knowledge
# 8.   Communicate your results and conclusions
# 
# By the end of these tutorials you will be able to:
# 
# *   Understand the principles of good research practices
# *   Learn to view a scientific data set or question through the lens of equity: Who is represented by this data and who is not? Who has access to this information? Who is in a position to use it?

# ##  Video 1: Interpreting the Results
# 

# In[ ]:


# @title Video 1: Interpreting the Results

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


video_ids = [("Youtube", "yswUuHU3Y_Y"), ("Bilibili", "BV1ho4y1C7Eo")]
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

link_id = "yje9x"


# In Step 6, we created plots displaying the global CO<sub>2</sub> levels and sea surface temperature data spanning the past 800 thousand years. Additionally, we attempted to fit both variables using a linear regression model. Nevertheless, it is crucial to bear in mind that correlation does not imply causation. The fact that global CO<sub>2</sub> and sea surface temperature appear to co-vary does not automatically imply that one variable directly causes changes in the other. To establish causation, it is imperative to gather multiple lines of evidence. This underscores the importance of literature review in Step 2, as it aids in identifying corroborating evidence in climate research.

# # Quantifying the Uncertainty
# <details>
# <summary>Click here for some information</summary>
# Look up "linear regression model R squared" and how it measures the uncertainty of a linear regression model. What does it say about how confident you can be about a linear relationship between CO<sub>2</sub> and temperature?

# # Activity: Interpreting the Results Through the Lens of Equity
# For the next 10 minutes, discuss what the results capture well in terms of the relationship between CO<sub>2</sub> and temperature. Who is represented by this data, specifically the compiled temperature record, and who is not? Who generated these data? Who has access to this information? Who is in a position to use it?

# # Further readings
# <details>
# <summary>Click here for more readings on Interpreting the Results through the lens of equity</summary>
# 
# Donovan, R. (2023), Climate journalism needs voices from the Global South, Eos, 104, https://doi.org/10.1029/2023EO230085
# 
# Tandon, A. (2021), Analysis: The lack of diversity in climate-science research, Carbon Brief, [https://www.carbonbrief.org/analysis-the-lack-of-diversity-in-climate-science-research/](https://www.carbonbrief.org/analysis-the-lack-of-diversity-in-climate-science-research/)
