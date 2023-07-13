#!/usr/bin/env python
# coding: utf-8

# # Intro

# ## Overview

# Welcome to the second day of the Computational Tools for Climate Science course! Today we dive into scientific exploration of the modern ocean and atmosphere systems using reanalysis datasets, building on yesterday’s climate system overview. 
# 
# In the course of today's study, you will leverage computational tools and datasets such as Xarray, climate models (CESM2), and reanalysis dataset (ERA5), to explore the large-scale properties of the ocean and atmosphere, and their interactions. You will start by diagnosing anomalies of sea surface temperature (SST), their relation to El Niño and La Niña events, and their influence on global atmospheric circulation patterns and ocean dynamics. You will then examine how large-scale ocean currents are driven by both atmospheric flow (wind-driven circulation) and ocean density variations (thermohaline circulation). Finally, you will investigate how the heat stored within different layers of the ocean has changed over recent decades, and the consequent impacts on Earth's climate system. 
# 
# Throughout Day 2, you will learn about large-scale ocean and atmospheric circulation, and develop familiarity with computational tools for the analysis and interpretation of complex climate data. 
# 

# ## Video 1: Oceans in Climate

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


video_ids = [("Youtube", "6lqkFuLI0ms"), ("Bilibili", "BV1Bh4y1Z7DK")]
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
    display(IFrame(src=f"2pxs", width=730, height=410))
display(out)

