#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W2D2_GoodResearchPractices/instructor/W2D2_Tutorial8.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W2D2_GoodResearchPractices/instructor/W2D2_Tutorial8.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 8: Communicating Your Conclusions**
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

# ##  Video 1: Communicating the Conclusion
# 

# In[ ]:


# @title Video 1: Communicating the Conclusion

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


video_ids = [("Youtube", "XZfqyancNpk"), ("Bilibili", "BV1ho4y1C7Eo")]
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

link_id = "9s6ub"


# # Activity: Communicating Your Conclusions
# 
# For the next 20 minutes, break out into groups of 2 or 3 and pick one presentation format and discuss:
# 
# *   Who is the target audience of this format?
# *   What information is important to include?
# 
# After this, come back together as a whole pod and discuss everyone's suggestions.
# 

# ## Equity in the Science Publishing
# <details>
# <summary>Click here for some information about equity and publishing</summary>
# 
# There are aspects of our current research culture that perpetuate inequity in the publishing process. Academic institutions and funding agencies often place importance on publishing in peer-reviewed journals. However, they have some drawbacks, including
# 
# *    Accessibility
# <ul><li>Papers in these journals are often kept behind a paywall, making them less accessible to people without the backing of either a university or a company.</li>
# <li>More and more journals offer the option of publishing open access, but at expense to the submitting authors: fees can often exceed 1000 USD.</li>
# <li>
# If you want to ensure accessibility, consider also releasing your results in other formats as well. For instance,
# <ul><li>Blog posts</li>
# <li>Podcasts</li>
# <li>Social media posts</li>
# <li>Conferences</li> </ul>
# <li>If you know that your research contains results that are relevant to specific populations, it is valuable to find ways to communicate your results to them.</li></ul>
# *    Peer Review as Gatekeeping
# <ul><li>At its best, the peer review process enforces scientific rigor.</li>
# <li>At its worst, it can become a tool for enforcing pre-existing norms, including the biases of its reviewers.</li>
# <li>REMEMBER: Bad experiences with reviewers and rejections does not mean that your research is bad. There are papers which went on to win Nobel prizes that experienced resistance and rejection during the peer review process BECAUSE they were introducing important new ideas.</li>
# <li>Further Reading:</li>
# <ul><li>Campanario, J. M. (2009). Rejecting and resisting Nobel class discoveries: Accounts by Nobel Laureates. Scientometrics, 81(2), 549–565.</li>
# <li>Bancroft, S. F., Ryoo, K., & Miles, M. (2022). Promoting equity in the peer review process of journal publication. Science Education, 106, 1232– 1248.  https://doi.org/10.1002/sce.21733</li></ul> </ul>

# # Tutorials 5-8 Summary
# 
# In this tutorial, we worked through how to analyze and present research.
# 
# *   We learned how to draft an analysis (Step 5)
# *   We implemented the analysis that we drafted (Step 6)
# *   We learned how to interpret the results of the analysis (Step 7)
# *   We learned about how to communicate the conclusions of our research (Step 8)
# 
