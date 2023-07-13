#!/usr/bin/env python
# coding: utf-8

# # Intro

# ## Overview

# Over the past two days, we’ve been analyzing climate reanalysis and remote sensing data to better understand variations in modern climate dynamics in land, ocean and atmosphere systems on timescales from days to months to years. Today, we’re going to explore even longer timescales of climate variability, on the order of tens to hundreds of thousands of years or more, prior to the widespread availability of instrumental records. The term for this study of past climate is “paleoclimate”. It’s important to study paleoclimate because past climate states can serve as analogs for future warming on Earth. Understanding the response of Earth’s climate systems in the past, can help to assess future changes in the climate system, evaluate the environmental response to these climate changes and validate/improve climate models and their projections of future climate.
# 
# During the first few tutorials today, you will explore different types of oceanic, terrestrial and atmospheric paleoclimate archives and proxies. Paleoclimate archives are geologic and biologic materials that preserve evidence of past changes in climate (e.g. speleothems, tree rings, ice cores, marine and lake sediment cores) and paleoclimate proxies are substances or features within archives (e.g. isotopes, foraminifera, leaf waxes, organic molecules) that record a climate variable and can be sampled and analyzed using a variety of physical and chemical methods. 
# 
# Throughout the tutorials today, you will explore paleoclimate reconstructions created using various proxies and will use these records to interpret past variations in Earth’s climate. You will also explore computational tools that are frequently used to interpret paleoclimate data and assess climate forcings. Finally, you will investigate paleoclimate data from climate models that simulate past variations in Earth’s climate.
# 

# ## Video 1: Past Climates Inform Our Future

# 
# 

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


video_ids = [("Youtube", "sng-2W6sKqY"), ("Bilibili", "BV12j411Z7jm/")]
tab_contents = display_videos(video_ids, W=730, H=410)
tabs = widgets.Tab()
tabs.children = tab_contents
for i in range(len(tab_contents)):
    tabs.set_title(i, video_ids[i][0])
display(tabs)


# ## Slides

# 
# 

# 
# 

# In[ ]:


# @markdown
from IPython.display import IFrame
from ipywidgets import widgets
out = widgets.Output()
with out:
    display(IFrame(src=f"2pv", width=730, height=410))
display(out)

