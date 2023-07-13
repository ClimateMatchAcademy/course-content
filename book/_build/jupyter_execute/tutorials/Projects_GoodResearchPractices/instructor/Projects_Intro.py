#!/usr/bin/env python
# coding: utf-8

# # Intro

# ## Overview

# This tutorial is all about the research process from concept to conclusion. We will walk you through the thinking process behind scientific research and some tools that will help you as you think through your own projects. The first half will focus on the process of planning a research project. In Step 1, we will walk you through how to ask a good research question. Step 2 will explain the goals of the literature review process. Step 3 will introduce you to the wide range of datasets used in climate science and give an introduction to when you might use some of them. Step 4 will explain how to develop a robust hypothesis based on the resources available.
# 
# The second half will focus on data analysis and communicating your results. Step 5 will guide you through drafting the analysis, and at Step 6 we will implement a sample analysis. Step 7 will explain what to take into consideration when interpreting your results. Finally, Step 8 will talk you through how to communicate your conclusions to different audiences. We hope that after this tutorial, you will have a better understanding of how to complete research that is clearly motivated and rigorously supported.
# 

# ## Video 1: Futures from the frontiers of climate science

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


video_ids = [("Youtube", "zHNCB0lnA6M"), ("Bilibili", "BV1ho4y1C7Eo")]
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
    display(IFrame(src=f"3tc2", width=730, height=410))
display(out)

