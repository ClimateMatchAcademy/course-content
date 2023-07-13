#!/usr/bin/env python
# coding: utf-8

# # Tutorial 9:  Exploring other applications
# 
# 
# ---
# 
# 
# **Week 2, Day 5: Climate Response: adaptation and impact**
# 
# **By Climatematch Academy**
# 
# __Content creators:__ Deepak Mewada, Grace Lindsay
# 
# __Content reviewers:__ Ohad Zivan, Name Surname
# 
# __Content editors:__ Name Surname, Name Surname
# 
# __Production editors:__ Name Surname, Name Surname

# 
# ---
# # Tutorial Objective
# 
# 
# The objective of this tutorial is to help participants of the ClimateMatch Academy to explore and think critically about different climate-related datasets, frame problems in data science terms, and consider the potential impact of machine learning solutions in the real world. By the end of this tutorial, participants should have a better understanding of how to identify and evaluate relevant datasets, select appropriate methods and data for solving problems, and consider the ethical and practical implications of their solutions.
# 
# ---
# 
# 

# ##  Tutorial slides
# 

#  These are the slides for the videos in all tutorials today
# 

# In[ ]:


# @title Tutorial slides

# @markdown These are the slides for the videos in all tutorials today
from IPython.display import IFrame
IFrame(src=f"https://mfr.ca-1.osf.io/render?url=https://osf.io/kaq2x/?direct%26mode=render%26action=download%26mode=render", width=854, height=480)


# ---
# 
# # Section 1: Finding Other Datsets, Identifying Applications and Considering Impact
# 
# 
# ---
# 
# 

# ##  Video 1: Video 1 Name
# 

# In[ ]:


# @title Video 1: Video 1 Name
from ipywidgets import widgets
from IPython.display import display, IFrame, YouTubeVideo

out2 = widgets.Output()
with out2:
  class BiliVideo(IFrame):
    def __init__(self, id, page=1, width=400, height=300, **kwargs):
      self.id=id
      src = 'https://player.bilibili.com/player.html?bvid={0}&page={1}'.format(id, page)
      super(BiliVideo, self).__init__(src, width, height, **kwargs)

  video = BiliVideo(id="", width=730, height=410, fs=1)
  print(f'Video available at https://www.bilibili.com/video/{video.id}')
  display(video)

out1 = widgets.Output()
with out1:
  video = YouTubeVideo(id="", width=730, height=410, fs=1, rel=0)
  print(f'Video available at https://youtube.com/watch?v={video.id}')
  display(video)

out = widgets.Tab([out1, out2])
out.set_title(0, 'Youtube')
out.set_title(1, 'Bilibili')

display(out)


# 
# 
# ---
# 
# 
# ## Section 1.1:  Finding Other Datasets
# 
# ---

# Now that you know the basics of how machine learning tools can be applied to climate-related data, In this tutorial, you will explore more climate-related datasets and think about how you would approach them using machine learning tools. Specifically, you will look at the [Climate Change AI wiki](https://wiki.climatechange.ai/wiki/Buildings_and_Cities) and identify 2-3 problems that are of interest to you and your pod.
# 
# Take some time to review the papers or dataset and  Identify 2-3 papers/datasets you'd like to discuss further

# 
# 
# ---
# 
# 
# ## Section 1.2: Framing Problems in Data Science Terms
# 
# ---
# 
# 

# Now that you have identified the datasets and papers that interest you, it's time to frame the problems in data science terms.
# 
# For each problem, consider the following questions:
# 
# - What kind of problem is it? Regression, classification, or something else?
# - What methods could you use to address it? What data is most important?
# - What kind of challenges might you face in trying to build a machine learning system for this problem?
# 
# Write down your answers to these questions for each problem you have selected. Share your findings with your pod and discuss potential solutions.

# 
# 
# ---
# ## Section 1.3: Considering Impact
# 
# 
# ---
# 
# 

# Machine learning and data science can help solve several technical challenges that will be important for addressing and adapting to climate change. However, the full potential of these approaches won't be realized if they aren't appropriately and fairly integrated with companies, communities, governments, and decision makers.
# 
# Discuss what needs to happen to make these models impactful in the real world. Consider the following questions:
# 
# - What are the potential hazards that need to be addressed before implementing machine learning systems for climate-related problems?
# - How can we ensure that these models are appropriately and fairly integrated into decision-making processes at different levels of government and industry?
# - How can we ensure that the models are accessible to stakeholders and the public?
# 
# Work with your pod to brainstorm potential solutions to these challenges and discuss how you can work towards implementing them in your own work.

# 
# 
# ---
# 
# 
# #Summary
# In this tutorial, we explored the importance of exploring more datasets, framing problems in data science terms, and considering impact. We encourage you to continue exploring datasets and framing problems in data science terms. Remember to consider the ethical implications of using datasets and ensure that the models are appropriately and fairly integrated with stakeholders.
# 
# 
# ---
# 
# 
