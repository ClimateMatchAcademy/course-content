#!/usr/bin/env python
# coding: utf-8

# # Intro

# ## Overview

# Welcome to the third day of Computational Tools for Climate Science course! Today’s focus is on satellite remote sensing for climate applications. Various international agencies and organizations have been using environmental satellite to monitor our earth system since the late 1970s. With more than 40 years of long-term satellite data records, we can understand the change of different components of the earth system, including land, ocean, atmosphere. More importantly, the long-term remote sensing data can help us study the impact of climate change on natural and human systems, such as ecosystem’s response to climate and climate impact on agriculture systems. 
# 
# During today’s curriculum, you will learn the fundamental concepts of satellite remote sensing, different sources of satellite remote sensing data for climate applications, how to access remote sensing datasets using python, and how to apply selected remote sensing datasets for climate applications. After today’s content, you should be familiar with basic concept of satellite remote sensing and basic computational tools to access and analyze satellite remote sensing data for climate applications.
# 

# ## Video 1: Introduction to Remote Sensing

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


video_ids = [("Youtube", "jtY4_WU6vgE"), ("Bilibili", "BV1Du411j7Az")]
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
    display(IFrame(src=f"py52", width=730, height=410))
display(out)

