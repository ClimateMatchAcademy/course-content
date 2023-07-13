#!/usr/bin/env python
# coding: utf-8

# # Intro

# ## Overview

# Today you will utilize the climate modelling background from the prior day to explore future projections of Earth’s climate by analyzing an ensemble of Earth System Models (ESMs) from the most recent Coupled Model Intercomparison Project (CMIP6). In today’s first two tutorials, you will analyze data from a CMIP6 ESM to develop fundamental model analysis techniques such as diagnosing geographic variations of future climate change, contrasting projections from different different socioeconomic & emission scenarios, calculating global mean properties on arbitrary ESM data grids, and re-gridding CMIP6 datasets to allow comparison with observations and/or other CMIP6 models.
# In the final tutorials, you will synthesize data from five different CMIP6 models to develop ensemble analysis techniques. You will analyze this CMIP6 ensemble to contrast the climate states of distinct Earth System Models, to estimate the uncertainty associated with CMIP6 future projections, and to separate the natural- and human-driven components of this uncertainty. Finally, you will synthesize these CMIP6 projections with data from observations, proxy records and CMIP6 paleo-simulations, to create a long-term past & future record of global mean sea surface temperature. 
# 

# ## Video 1: Future Projections of Climate

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


video_ids = [("Youtube", "bkaGA-xx4zY"), ("Bilibili", "BV1ho4y1C7Eo")]
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
    display(IFrame(src=f"bfm6", width=730, height=410))
display(out)

