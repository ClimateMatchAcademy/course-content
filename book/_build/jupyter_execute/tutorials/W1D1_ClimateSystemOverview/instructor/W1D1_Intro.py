#!/usr/bin/env python
# coding: utf-8

# # Intro

# ## Overview

# Welcome to the first day of the Computational Tools for Climate Science course! During this first day, the videos will provide an overview of Earth’s climate system. You’ll learn about various aspects of Earth’s climate including different parts of the climate system, forcings and mechanisms that drive changes in the climate system and the importance of understanding past, present and future climate variability. You’ll begin by learning about the effect of incoming solar radiation and Earth’s energy budget on the climate. You’ll then explore various processes within the atmospheric, oceanic and terrestrial components of Earth’s climate system. Finally, you’ll investigate long-term, natural forcings and feedbacks that influence Earth’s climate, and will begin to think about these processes in the contest of past, present and future climate variability.  
# 
# Additionally, the notebooks in today’s tutorials will elaborate on the climate concepts introduced in the videos, but will primarily focus on introducing the Xarray Python package, which is commonly used to analyze large climate datasets and makes working with multi-dimensional arrays simple and efficient. Xarray introduces labels in the form of dimensions, coordinates and attributes on top of raw data array, and includes a large number of functions for advanced analytics and visualization with these data structures. Throughout the tutorials today, you’ll learn the basics of Xarray and apply some of these tools to climate datasets to further explore the climate system concepts introduced in the videos.

# ## Video 1: Climate Solutions for a Warming World

# 
# 

# In[ ]:


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


video_ids = [("Youtube", "RhEQhWTAOJ0"), ("Bilibili", "BV1Eh4y1j7FB")]
tab_contents = display_videos(video_ids, W=730, H=410)
tabs = widgets.Tab()
tabs.children = tab_contents
for i in range(len(tab_contents)):
    tabs.set_title(i, video_ids[i][0])
display(tabs)


# ## Slides

# 
# 

# In[ ]:


# @markdown
from IPython.display import IFrame
from ipywidgets import widgets
out = widgets.Output()
with out:
    display(IFrame(src=f"ghmn", width=730, height=410))
display(out)

