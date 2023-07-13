#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W1D1_ClimateSystemOverview/instructor/W1D1_Tutorial7.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W1D1_ClimateSystemOverview/instructor/W1D1_Tutorial7.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 7: Other Computational Tools in Xarray**
# 
# **Week 1, Day 1, Climate System Overview**
# 
# **Content creators:** Sloane Garelick, Julia Kent
# 
# **Content reviewers:** Katrina Dobson, Younkap Nina Duplex, Danika Gupta, Maria Gonzalez, Will Gregory, Nahid Hasan, Sherry Mi, Beatriz Cosenza Muralles, Jenna Pearson, Agustina Pesce, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS and Google Deepmind

# ![project pythia](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAc0AAABtCAMAAAD08Mp1AAAAflBMVEX///8aZY8AW4kAXYoAWIcAX4sVY46ju8sAVoasv84caJKFpbwPYY2An7e+z9sAYo5ymLLu8vXh6e7F1N+yxtSOrME8eJzZ4+rn7vJaiahhi6j1+PoAU4Qrb5actcdRg6Ruk67O2+Q3dJnC0t2JqsAATYBIfZ+Ur8PZ5OtRhaVzChr+AAAVl0lEQVR4nO1d2ZryLAy2QBFr7biOS63r/Orc/w3+hW6EpaVadb555j3wQBEobwkkJKHX+8MfmjHbjcbOOMgYz9/d9z9ATBLi++F98JEXv6HLy2i3GI2+dvPjG1qPp8doPo9m08nr224GDb0HgK9yXSOCNfjBabOIVkqrejmO4PNwjeoZWu0uiKC0Wt/HCKFkeHR6yulWaoZ8ZV8eDN0tgU6Gas6jBBGCOAjxNgP1sXrDuirLqjdOfb4DY/wImR69yJWNfKohLRNiRJIdYEkvJ8qKohe7/I4+CaagfZ8EfYfHnDKpGbzIn93Q3Qqfah3LMUK+3HqIySWCZb5qq8zhHxx6fA9m7CEyPS+Qaxv5dtoxWkglqbVgWhQFZj6jgJj+h/Gg8TmnRPqDX7BZJ5ZUNqcb4uutU5QAPr9cJkd4aCbmLtSNqhOIPOVq2OR8JjfHdin51uXtZG/kkgN9aiJPwcNsXpmlMOzrW9l8UM6mIPJmoJZN/uDnomTTW+QHKj9nVDP2IWrYXT/IZnxBNY371dr9TjbPj8rZdmx6Hiueu1EmUAr3jP2GrrJd7ZM+xuYkqd8qkvJdeiObk4dnZhtJy0H9nKNmCR+C/dWu8b1j8rKs4SE2V2FDdykr6Hwjm5eHlJMM7dj0cL45d1ivkTTbBg5ChNXtbR9hM06aJUkhdN7H5rCDqelRucZmNj22FCVddl+orPfotCKwmf1ZH2Hzu/mp0tc0e6vfxuacNLfbCLjzc2AzfxIXNnEx2WLqtvX27YaHB9js12yApDozofMuNpcP7ICqwfVHcp2QTUQIt5soTBBREn7pC6irUzmepp23id8ardyBTQLBkqxQbNWLlOcSkmG0rWqAvcbVD9vObUGTauyEiawFCPGDIECCOagZADbR+ZhiNtjDd5uIFQaMUDASGJ+UgcvXZE3OUkxQSJFiFvKkLfMdbKLlDWKaF1LlDcUofUe1tqmwBMaTCgOZTjyQfuncxHsqnsT/GM2jGsxTiI8C0XHCR3ky5CwhINwAm6z4CYp0LDY38lhU0noJ9xsoI2evCERy6i9jbv7unxQhCO2MMprZJGYxPVFfJZRco+Nydk1UAUzUZTuSS6DIWH03uBTjjg5317EJvRDKDMhm+QYe5FHzx/wrM5u9CSA+m/hLuL5TXxIH0QecItbJeTebCzg1KS1ZiRRDX6jKz5exuS76iA/3VzJHxQ61gIVN8FjZQ1vYhAOc2V/hYkw9YCSaBGDi4rGlr3ezCQjzaCKVUjUXptTwKjYPhUT399pv0+N80O/3U4E6bajlikPl7xY2l/JjUfEfG5t9uNbwr+DkYEqvVnCt9S19vZdNRTDAXXMMu6YS9iI2x0UzYQJ/OC4ufIFH4hAu3dZdhrOa08YPShRjqgubYQs2uUw9GlZdGQOwfiGLqL2XzR3YmKpL45n5EpAiGF7DZkkmBZ4DyyFWd4nUR2xt68bGJ+pJlIVNsLnLlC0nSYv44MHxxHo/Arkune0MDnva2xQgf0i5iH7kOQRQbIsvYbMi80PaKc9PxKz6hwgPTTvqBUIj9TsLm2B98Yf8KwubMZhowqIPxjP7M8RVbjRcmx/aQd9EJm0zACXauUG9gs1NSSau5OTAU5V8ebR9NtbODwfMsBs2aiiTPbQpiCExs3kDvFOPfwe+Qmetzd4RrMom/49ee1tQUQ/QT0g7PfEFbH4Xgoui8ux47jUZr0I2gsvKbLs1nFkANsPMye+kHPMy8WIA1oLMZ/CQwB1N5nMEusYM4xmD5cFi3buTzSncBLUb6uez+amTeTupBlsahtoZkE/kI4oJM/YOKhOZX5/ZXAede0JjUUGdIntNz5SAP3XKJty/WaS4Dc9mszp1pbjQFI9bxXGJefv1Zr0PGIGn/eRQVTTfGAfNweqeH+w62D6xWCMnzbPjJFdmmr29jti0KbMWPJnNW2k5obRU2yT7dYjIul/5qN6iMZWd1LY3c7UVmtmk+e6imU2a+Y+twKqYmFq9yJWpSlOOO9kE6pGv7frq8Vw2o3JZCoPqDS7Z9FNlpNi4rIrfj2NUagiK4ceAZjYL01vz+W++R5sASfthahXMTctO5dfNzcoZw5ftU/3sOX1S7lt3/HDIH+dl4t1Hxqd5YgA0skkKZ+omNkvPKbhuMlOrQIvodt28yX+juuGsFs9ks1QzPQx7xd3RQjLm77TgM/faQNV5xA6n20baPDUb2SSlutjAJjmVUwzsWInB2ghnr8W0dyebK7Bqh40DAPA8NuNyM+sR1dY/Zmx9E67cwqO/UPAEe0c0nqX/XgTbUzOZDWxSya+u3jv6QzIyfQJ906C/nzvSN+EZbi6IgL6Jmrx2IZ7G5tIrO27wbYu5dNqwUHj0l+pbbiUNieDRKX6njk2KAsmGWsMm/QSUgSHXTp20Agdzz5rZxIM5OMXNikDbRbNPvYxnsTkv9z+Vr6CCJJ27gs1ScIm+c0MLtR/pK7CyqYWLKEeDwJgA1+c5sNMybXpAFYYfuxx3MrLX0MHqbnwiUIQG6s9rgNdY3cfVZvbDIi9HvGULm4ansACyWUREIYJOI+X0AdB3uUFGQNwZNMeoZ3CKHVccmPWZFI/131SvpcUZinJCo0zOAZHjH5FiRH4Km5NT+XbjT5ulUdAA2cQlm0bzqAmATdwfcMyj2U0fKMVOC7wTKAK9BAoI8LLlgB51YtkEszlzQ1LYzF8XBzZXYOGkcBc2hZZIdZSeweYRl/YfYlWYbqxkMy7GIls3RY9MRxcmmP2CTFDYhHtH6HsHj8Q8AujsQ1OR4Homj2J+RBYZvnPyPYDvEvUlOm/QlYSqsvoJbC5Y1Zp9Ec8GwMqmqwOo5UTMAPUMBXpqg4U6Vo530L5cLZZreFxAhdPZTZ5P+SoB5DHO9w4ubPbhu0Qr2XBVPAw140LnbE6q2CY/qFExzg1sOtqb72cTUgb1jKGytwpJMurP5/1hQhSFMZchgOLwcsv9C6uRzRdxFzZ7is8exeiwm0f9A1adfDV9vGs2z5KUNdvJi4ISm+UuSGLz2629+9nsXaHLhixGYs05mnIXYKwHx+bhAxcoARFTDuKLnkHfg+NtKeOWW6UXaus0THd2WDtkCjXvz47ZHElStj6c3CRp0Svnpuoc9yG/ewPHGAuUP+S1IXygiJ2psR4gVHgf9JrPhQR0U1mnbK4q32F8avC/M7LJ238dm1AXgPuutdOIltrLtD4oo6zbLQ4lcnqXfH2H2SWbfcli8NVU+AewCc0u0CIbB3WWwKKayu3guzaUkRSzyDFGbIxqihWlDSp5d2zG+/KNqt3+5ABsUqn9F7IJ5wBcqlc1bksFJP5rI6YkmhyjcS/NokG3UXXIZlS6DVDmcsZ6lNj0DWw6BjU9xKayeSFAF182RWrBI566fA7bsqBzpHzSeNJnsn12xeamfM1x4GRj/RFswlgwRXbdcK30DDHcGdgTFUj2N/csFpfafRVFRunXDZvnj2JQHVbMDJnHxJvZ7K1hTAm04cWfNcsXUk2WsWdhSj7cbZFh5lAju1FiPinrgs34UE5M9Fm9sJPVdGUf3pxNzv0b2YR7UYoUDXln8d/2QnbVGrCQj2StsE2+oEizFpSN28yeHbAZ+cUj+4X6desfEh5WQhD2Djuj5G1i8+DW+INsKpGvWqj0ZMS0IFjuu30wtrTYamQpI98ql1f8ZWjc89m31fftYTYn5YpJ2UG82pNrQHBYJg4IMQkWuvKZr5tCLj/Cpvz+1rMpDUxY2vEmcK+jK+Rx9jQSlQiNbB4B0wOTFluaPvoaVqiFTcsItaCTyS5hcuMhRnhU48cI2Wyf/HVQ9h6dxBycjA3SCbODOgDLam72Ph5g8yOogOrYlMoFXjVuiw/LD1JXd2vEkMhDSdhpVPvKTwZrynLTDtoM1A6NaWCHZ4rTvvU3iUjmgBjzvhf1O8zIl6rz287NW7lU+Hk6j2vFZZGQMnuryBiuSR2x+SqslsdzdG4MMBWY8LLHZTuXnvrWp8tll/UZMSw0bMoyrlZJLugpRij53F9OuEy+gH0gdP4xNn89zkG+ZlFyyWX5JvvGJ5+7woF92d+z7NsQHDr9sfmTsNqwYtIFpYAWexKfZAt1PF/shGRaLXy+z4HpO5rYbOnl/YdHsCgMeVhWuSc86XXuwT7h4e/bbNWOvxDyt2AF/2PzxyAK8tUwJDDKcvV1nfYmc76VExnDhBFgHk3SvbaSDh2wKe+p/9h8LaaXXEmjZG3Y5A0Y4SukMJoJB40LYQet1O2PzZ+AVKHMhCxFnybt57ylIrBKnE8Iv+M9lcJBCvyx+RNwRblCiQKzdvodlhxWbOqhNxmb/h+bb8Q810oo9m1uPwk1samFrP6x+W4ci5SRPjIklMghcyixqRpAO2Lz3DdgHi2h4em4A7/vlKOSlfJzZKpUbyX951T+5055xgEonn03q+uH6Ynqk8ffj+k651JLFwLwYWRTO101sYnbszk23tSD0DaRbxxb/Qd+Vo+z4A1C6LJjuBmEH1tG8oVEW8XMfUJyrdl34G6l/0x2ZR82819jsoB7sDrkeVtCtqm1GL6WTXuMWIjQMLYUg6u4kkKULXcN/pRZA9yNqPbQAsSB5hH3wO/aFGN/VPz1sGMIRxvEo5JL++lahoLN7/ZsSpLW4F5oRG38Ji7HN4aEwcgrmEs73KtxKJban8OmdgJqy8p4N+IFyzoRsnWjN57O5vc9bDpm42iIlGfFSwFjEWDAJpwNbPlWNjXfMlRzE8A9KJQSnx2mKbXn62F92Ryukfk08dG5OeuSTQ/nnpxKrnT5XH4Hg0jWWoyYGc9hc655o3R7/nDNz7T8LTfAzjYM4TCkYYgRO5m0lJ/Fplck/YSxBbLTxgcov52+lU2Dl3VtHGM7nKngkiL/mlY6Owk7UHEMnS5M+gaad5e7MrqxKdb4Z7LpsXwaKjGZpRkLzgZhWH4fm1pOd0O19+MqaqfkJGpc8EOwEBH/tL8ERHgZEM0nnR9+QTbr1k3IJh/4rtkssrRAiipfehi+IDzI38emqeW2SYOsyO7KxJf8RUbUw2gzzxSU+DjkSUm3qhwo2RSz2InN0rXoKWwWG1goUYv83jMYYy3k8vvYPKl7INHVjq6/EC5m1cAO/gu5vO3Fe5xFmsyT7UH9j86mu6R9lE1qyGtZbmBhvoJCBYLBC9nAXUmVbBuuY1TKwi2sB92yaY5msWWnbgsxVn5lxZtw/8q4tyMiP3v/KL5RULC5BmzaLHudskm/edaVvXqfbWEjhmFf2VDC8ctbjUZVrm2YmHtd/TDiY9wxm2pMd95qc4I6J2RxGnIekz77LxaNbtPZtzUFQN/Dpux78ACbxe5veQIzqhhluN/JDuMgWYZNJsgTjdUNScdsmrjk5Tqy7o0YV0W2pWFmxWg6ZHwIUZzyRQwy4I1sVqMD8+gXoTFww8ODL2E6F98QQwPTjahZObplc6ZY9cp+dWXdm4/HV+lOi7T3OZuEs2mKFvkRbIK8HqX+rUzOnZY8yqDZvZLNgy2ugfaegjlk07R5trCpCovnsgls15U2AreMgZKXBOuRQi9lU8mSItfcsXUvx3PYLONQeDjsI+tm3V1FHGd4aVgEVRFjuv0XsglERyL/+0nexU9hM+6KzWp0QM5RaT0AA0w/QbZ9syLQgk3cn6wkTE4t2dzL/I3kC3q0UMRukLJJ/gU2QSwWruqC+wyoyJgXpxZsyteXcoDqm9kEueLQDGTa7M66J8OBTa483ssmXzfPj2soCmlYOhyAxgIZyOzo1IbNOjSzCcQ+hnKkM+sewM9mkxz5dVy3aAx3+nLCB+vt4rYcqq9jM1EWSsCuKQPJw/jZbOYXcyFlow9O79Vrb8u/WmTZy9gENzXyNQdI3q6sewCds8lJg/mCoq6t7rAqS2Ifq/XsZWzKT0KFTxgQtR1Z99TeP2Fuglxej8xNIxQhtTFOTus242Vsykc8mUYCTCCa+aUDuLFJDWyqAStgbhZDKs3Ne7ING6E6vU23hkL2V/9VbAKdKnN0AWbHzqx7ElRJazC7F54kLdgEGU07ZlO9jNdsPyPWxOOvYlMWGTR3vr0YFNYuoVoPumUTd88m9bVjkZU+OfUraEu8iM0YmCIP2ZdQ1Dpmum8BBzapG5tTg6Ttnk1MDTt7Pc2LMWldhhexCa5mLjwKgZeQaz6sFsjYHLuwuXk/m5R9myximisVNaV2ydHKFsQA2tiCgMmxvCpbtvU9wbrnMDe91nMT3qDRGZsUeZaNqvqnurt02thp77e6wytYgu+9wPdJ/lZr/GE4zE1P29NeXNlE3bBJKeXevnurbVOJY6jNIf+aMxRwr3n6APntNfCxaiTIfchOq3msRB2b3p1sPjw3syRWyWl/2M3q5BKMPKm9SvA1bHouMF03+BAUNk0ZnoPWbFa3wj3Ipu1KCg3gysV6i/ZL2FQDw8wwnqY/gsx6UErax9kUHkeFF4+YJI+w6ep4Ci5Mrd8svoTN2mSKJZwvV3OFI5v86u4GNpdVtuFen19LTmmWyTX74a687v8sm01Jx4vyrjcfOkKx7NnY5F2HbCKVzcySxTKHl8ElXe0uuSARXkKu7+GvYNNVa217KXkTWrB5qPIFUUMWi+M23bnpUSw9ftTspz85nhn8Cjbrr9+Q23d8Pkc4sEnyGbngDyqSMRv1zd4wSTZmDWo6OiXGVEQG/AY2J6ZzACM6vli8mc14m+9t4oQghPlBGL8XyybyV+fd6PszCWgqX1PNYnydt/Pr/g1s9l2CmBy62hqZ9YBfdsh6Fn3zlJKYidVllK2KnNf/TFezzw8BQdgvsoZnWj/62PfdFavfwCbw7aOeklEaRj11at3L2Iy2eJtqEAdfv2UuHako0po8DnQFfbbWXD6KB8Lk09WK9QvYvMFb5NUOPHIreQOmvggxOu74rDt+MLOf22r+tf4M+KULyDvthwYqe8uLepMlJBR5bv3+BWx+GaMsSgBnr5qju3uxErdF2qTh6itgyC+jKCn1EcEHZdncsUYNCzlpnL+ATWt6jQzQIN+t795seEHZFQCEJAftTgEeVWa4w8ML2UUuOnaxZPmJwyLx77MJGqCaoFVEbZfWvVnAdcGy6RATNUbOev1V+FFN5r6TWVJJBG/Gv88mSPdk6gvIptKhdY+nnlWAYPN9u1VDurvF5tOqovZwI8M/zyZwITEqlDcoajuz7q2RrwFm/vtiPsZ6IZEnoNr/Dpm5CEQYGrMKQjRnITRhIic7NBqkSpxBXkSNzbqsiYkpa6KckJH3dyDXgI0aSCDXwzpL9XpbDDUoL1N/95VCLzYcLqSh3o1MJRSMNw5Ri7OBhL6rNhb35b/VGlimoKgqLKbyjwPF8DEHP1r6G4FCxgP2IyjSuQfCH/5B/A+OXrqx0W8zLwAAAABJRU5ErkJggg==) | 
# -
# Pythia credit: Rose, B. E. J., Kent, J., Tyle, K., Clyne, J., Banihirwe, A., Camron, D., May, R., Grover, M., Ford, R. R., Paul, K., Morley, J., Eroglu, O., Kailyn, L., & Zacharias, A. (2023). Pythia Foundations (Version v2023.05.01) https://zenodo.org/record/8065851
# 
# 

# # **Tutorial Objectives**
# Thus far, we've learned about various climate processes in the videos, and we've explored tools in Xarray that are useful for analyzing and interpreting climate data. 
# 
# In this tutorial you'll continue using the SST data from CESM2 and practice using some additional computational tools in Xarray to resample your data, which can help with data comparison and analysis. The functions you will use are:
# 
# - `resample`: Groupby-like functionality specifically for time dimensions. Can be used for temporal upsampling and downsampling. Additional information about resampling in Xarray can be found [here](https://xarray.pydata.org/en/stable/user-guide/time-series.html#resampling-and-grouped-operations).
# - `rolling`: Useful for computing aggregations on moving windows of your dataset e.g. computing moving averages. Additional information about resampling in Xarray can be found [here](https://xarray.pydata.org/en/stable/user-guide/computation.html#rolling-window-operations).
# - `coarsen`: Generic functionality for downsampling data. Additional information about resampling in Xarray can be found [here](https://xarray.pydata.org/en/stable/user-guide/computation.html#coarsen-large-arrays).

# # **Setup**
# 

# In[ ]:


# imports
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from pythia_datasets import DATASETS
import pandas as pd
import matplotlib.pyplot as plt


# ##  Figure Settings
# 

# ###  Figure Settings
# 

# In[ ]:


# @title Figure Settings
import ipywidgets as widgets       # interactive display
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
plt.style.use("https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/cma.mplstyle")


# ##  Video 1: Video Title
# 

# ###  Video 1: Video Title
# 

# In[ ]:


# @title Video 1: Video Title
#Tech team will add code to format and display the video


# # **Section 1: High-level Computation Functionality**
# 
# In this tutorial you will learn about several methods for dealing with the resolution of data. Here are some links for quick reference, and we will go into detail in each of them in the sections below.
# 
# - `resample`: [Groupby-like functionality specifialized for time dimensions. Can be used for temporal upsampling and downsampling](https://xarray.pydata.org/en/stable/user-guide/time-series.html#resampling-and-grouped-operations)
# - `rolling`: [Useful for computing aggregations on moving windows of your dataset e.g. computing moving averages](https://xarray.pydata.org/en/stable/user-guide/computation.html#rolling-window-operations)
# - `coarsen`: [Generic functionality for downsampling data](https://xarray.pydata.org/en/stable/user-guide/computation.html#coarsen-large-arrays)
# 
# First, let's load the same data that we used in the previous tutorial (monthly SST data from CESM2):

# In[ ]:


filepath = DATASETS.fetch('CESM2_sst_data.nc')
ds = xr.open_dataset(filepath)
ds


# ## **Section 1.1: Resampling Data**
# 
# For upsampling or downsampling temporal resolutions, we can use the `resample()` method in Xarray.  For example, you can use this function to downsample a dataset from hourly to 6-hourly resolution.
# 
# Our original SST data is monthly resolution. Let's use `resample()` to downsample to annual frequency:

# In[ ]:


# resample from a monthly to an annual frequency
tos_yearly = ds.tos.resample(time='AS')
tos_yearly


# In[ ]:


# calculate the global mean of the resampled data
annual_mean = tos_yearly.mean()
annual_mean_global = annual_mean.mean(dim=['lat', 'lon'])
annual_mean_global.plot()


# 
# ## **Section 1.2: Moving Average**
# 
# The `rolling()` method allows for a rolling window aggregation and is applied along one dimension using the name of the dimension as a key (e.g. time) and the window size as the value (e.g. 6). We will use these values in the demonstration below.
# 
# Let's use the `rolling()` function to compute a 6-month moving average of our SST data:

# In[ ]:


# calculate the running mean
tos_m_avg = ds.tos.rolling(time=6, center=True).mean()
tos_m_avg


# In[ ]:


# calculate the global average of the running mean
tos_m_avg_global = tos_m_avg.mean(dim=['lat','lon'])
tos_m_avg_global.plot()


# 
# ## **Section 1.3: Coarsening the Data**
# 
# The `coarsen()` function allows for block aggregation along multiple dimensions. 
# 
# Let's use the `coarsen()` function to take a block mean for every 4 months and globally (i.e., 180 points along the latitude dimension and 360 points along the longitude dimension). Although we know the dimensions of our data quite well, we will include code that finds the length of the latitude and longitude variables so that it could work for other datasets that had a different format.

# In[ ]:


# coarsen the data
coarse_data = ds.coarsen(time=4,lat=len(ds.lat),lon=len(ds.lon)).mean()
coarse_data


# In[ ]:


coarse_data.tos.plot()


# ## **Section 1.4: Compare the Resampling Methods**
# 
# Now that we've tried multiple resampling methods on different temporal resolutions, we can compare the resampled datasets to the original.

# In[ ]:


original_global = ds.mean(dim=['lat', 'lon'])


# In[ ]:


original_global.tos.plot(size=6)
coarse_data.tos.plot()
tos_m_avg_global.plot()
annual_mean_global.plot()


plt.legend(['original data (monthly)','coarsened (4 months)','moving average (6 months)', 'annually resampled (12 months)']);


# ### **Questions 1.4: Climate Connection**
# 
# 1. What type of information can you obtain from each time series?
# 2. In what scenarios would you use different temporal resolutions?
# 

# In[ ]:


# to_remove explanation

"""
1. In general, by examining the data at these different time scales, you can get a more comprehensive understanding of the SST variations and their potential causes.
2. The original monthly data gives you the most granular view of the data, allowing you to see monthly variations in SST. Coarsening the data over 4-month periods reduces the temporal resolution but provides a slightly smoothed series that could help identify patterns or trends over this larger time period. A 6-month moving average could be useful for identifying semi-annual trends and reducing the impact of short-term noise in the data. The annually resampled (12 months) data provides a high-level view of the SST data, emphasizing the annual pattern. This can be useful for identifying long-term trends or changes in the data over the span of years.
""";


# # **Summary**
# 
# In this tutorial, we've explored Xarray tools to simplify and understand climate data better. Given the complexity and variability of climate data, tools like `resample`, `rolling`, and `coarsen` come in handy to make the data easier to compare and find long-term trends. You've also looked at valuable techniques like calculating moving averages. 
# 
# 
# 
# 

# # **Resources**

# Code and data for this tutorial is based on existing content from [Project Pythia](https://foundations.projectpythia.org/core/xarray/computation-masking.html).
