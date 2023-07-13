#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W1D1_ClimateSystemOverview/instructor/W1D1_Tutorial5.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W1D1_ClimateSystemOverview/instructor/W1D1_Tutorial5.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 5: Xarray Data Analysis and Climatology**
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
# **Our 2023 Sponsors:** NASA TOPS and Google deepmind

# ![project pythia](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAc0AAABtCAMAAAD08Mp1AAAAflBMVEX///8aZY8AW4kAXYoAWIcAX4sVY46ju8sAVoasv84caJKFpbwPYY2An7e+z9sAYo5ymLLu8vXh6e7F1N+yxtSOrME8eJzZ4+rn7vJaiahhi6j1+PoAU4Qrb5actcdRg6Ruk67O2+Q3dJnC0t2JqsAATYBIfZ+Ur8PZ5OtRhaVzChr+AAAVl0lEQVR4nO1d2ZryLAy2QBFr7biOS63r/Orc/w3+hW6EpaVadb555j3wQBEobwkkJKHX+8MfmjHbjcbOOMgYz9/d9z9ATBLi++F98JEXv6HLy2i3GI2+dvPjG1qPp8doPo9m08nr224GDb0HgK9yXSOCNfjBabOIVkqrejmO4PNwjeoZWu0uiKC0Wt/HCKFkeHR6yulWaoZ8ZV8eDN0tgU6Gas6jBBGCOAjxNgP1sXrDuirLqjdOfb4DY/wImR69yJWNfKohLRNiRJIdYEkvJ8qKohe7/I4+CaagfZ8EfYfHnDKpGbzIn93Q3Qqfah3LMUK+3HqIySWCZb5qq8zhHxx6fA9m7CEyPS+Qaxv5dtoxWkglqbVgWhQFZj6jgJj+h/Gg8TmnRPqDX7BZJ5ZUNqcb4uutU5QAPr9cJkd4aCbmLtSNqhOIPOVq2OR8JjfHdin51uXtZG/kkgN9aiJPwcNsXpmlMOzrW9l8UM6mIPJmoJZN/uDnomTTW+QHKj9nVDP2IWrYXT/IZnxBNY371dr9TjbPj8rZdmx6Hiueu1EmUAr3jP2GrrJd7ZM+xuYkqd8qkvJdeiObk4dnZhtJy0H9nKNmCR+C/dWu8b1j8rKs4SE2V2FDdykr6Hwjm5eHlJMM7dj0cL45d1ivkTTbBg5ChNXtbR9hM06aJUkhdN7H5rCDqelRucZmNj22FCVddl+orPfotCKwmf1ZH2Hzu/mp0tc0e6vfxuacNLfbCLjzc2AzfxIXNnEx2WLqtvX27YaHB9js12yApDozofMuNpcP7ICqwfVHcp2QTUQIt5soTBBREn7pC6irUzmepp23id8ardyBTQLBkqxQbNWLlOcSkmG0rWqAvcbVD9vObUGTauyEiawFCPGDIECCOagZADbR+ZhiNtjDd5uIFQaMUDASGJ+UgcvXZE3OUkxQSJFiFvKkLfMdbKLlDWKaF1LlDcUofUe1tqmwBMaTCgOZTjyQfuncxHsqnsT/GM2jGsxTiI8C0XHCR3ky5CwhINwAm6z4CYp0LDY38lhU0noJ9xsoI2evCERy6i9jbv7unxQhCO2MMprZJGYxPVFfJZRco+Nydk1UAUzUZTuSS6DIWH03uBTjjg5317EJvRDKDMhm+QYe5FHzx/wrM5u9CSA+m/hLuL5TXxIH0QecItbJeTebCzg1KS1ZiRRDX6jKz5exuS76iA/3VzJHxQ61gIVN8FjZQ1vYhAOc2V/hYkw9YCSaBGDi4rGlr3ezCQjzaCKVUjUXptTwKjYPhUT399pv0+N80O/3U4E6bajlikPl7xY2l/JjUfEfG5t9uNbwr+DkYEqvVnCt9S19vZdNRTDAXXMMu6YS9iI2x0UzYQJ/OC4ufIFH4hAu3dZdhrOa08YPShRjqgubYQs2uUw9GlZdGQOwfiGLqL2XzR3YmKpL45n5EpAiGF7DZkkmBZ4DyyFWd4nUR2xt68bGJ+pJlIVNsLnLlC0nSYv44MHxxHo/Arkune0MDnva2xQgf0i5iH7kOQRQbIsvYbMi80PaKc9PxKz6hwgPTTvqBUIj9TsLm2B98Yf8KwubMZhowqIPxjP7M8RVbjRcmx/aQd9EJm0zACXauUG9gs1NSSau5OTAU5V8ebR9NtbODwfMsBs2aiiTPbQpiCExs3kDvFOPfwe+Qmetzd4RrMom/49ee1tQUQ/QT0g7PfEFbH4Xgoui8ux47jUZr0I2gsvKbLs1nFkANsPMye+kHPMy8WIA1oLMZ/CQwB1N5nMEusYM4xmD5cFi3buTzSncBLUb6uez+amTeTupBlsahtoZkE/kI4oJM/YOKhOZX5/ZXAede0JjUUGdIntNz5SAP3XKJty/WaS4Dc9mszp1pbjQFI9bxXGJefv1Zr0PGIGn/eRQVTTfGAfNweqeH+w62D6xWCMnzbPjJFdmmr29jti0KbMWPJnNW2k5obRU2yT7dYjIul/5qN6iMZWd1LY3c7UVmtmk+e6imU2a+Y+twKqYmFq9yJWpSlOOO9kE6pGv7frq8Vw2o3JZCoPqDS7Z9FNlpNi4rIrfj2NUagiK4ceAZjYL01vz+W++R5sASfthahXMTctO5dfNzcoZw5ftU/3sOX1S7lt3/HDIH+dl4t1Hxqd5YgA0skkKZ+omNkvPKbhuMlOrQIvodt28yX+juuGsFs9ks1QzPQx7xd3RQjLm77TgM/faQNV5xA6n20baPDUb2SSlutjAJjmVUwzsWInB2ghnr8W0dyebK7Bqh40DAPA8NuNyM+sR1dY/Zmx9E67cwqO/UPAEe0c0nqX/XgTbUzOZDWxSya+u3jv6QzIyfQJ906C/nzvSN+EZbi6IgL6Jmrx2IZ7G5tIrO27wbYu5dNqwUHj0l+pbbiUNieDRKX6njk2KAsmGWsMm/QSUgSHXTp20Agdzz5rZxIM5OMXNikDbRbNPvYxnsTkv9z+Vr6CCJJ27gs1ScIm+c0MLtR/pK7CyqYWLKEeDwJgA1+c5sNMybXpAFYYfuxx3MrLX0MHqbnwiUIQG6s9rgNdY3cfVZvbDIi9HvGULm4ansACyWUREIYJOI+X0AdB3uUFGQNwZNMeoZ3CKHVccmPWZFI/131SvpcUZinJCo0zOAZHjH5FiRH4Km5NT+XbjT5ulUdAA2cQlm0bzqAmATdwfcMyj2U0fKMVOC7wTKAK9BAoI8LLlgB51YtkEszlzQ1LYzF8XBzZXYOGkcBc2hZZIdZSeweYRl/YfYlWYbqxkMy7GIls3RY9MRxcmmP2CTFDYhHtH6HsHj8Q8AujsQ1OR4Homj2J+RBYZvnPyPYDvEvUlOm/QlYSqsvoJbC5Y1Zp9Ec8GwMqmqwOo5UTMAPUMBXpqg4U6Vo530L5cLZZreFxAhdPZTZ5P+SoB5DHO9w4ubPbhu0Qr2XBVPAw140LnbE6q2CY/qFExzg1sOtqb72cTUgb1jKGytwpJMurP5/1hQhSFMZchgOLwcsv9C6uRzRdxFzZ7is8exeiwm0f9A1adfDV9vGs2z5KUNdvJi4ISm+UuSGLz2629+9nsXaHLhixGYs05mnIXYKwHx+bhAxcoARFTDuKLnkHfg+NtKeOWW6UXaus0THd2WDtkCjXvz47ZHElStj6c3CRp0Svnpuoc9yG/ewPHGAuUP+S1IXygiJ2psR4gVHgf9JrPhQR0U1mnbK4q32F8avC/M7LJ238dm1AXgPuutdOIltrLtD4oo6zbLQ4lcnqXfH2H2SWbfcli8NVU+AewCc0u0CIbB3WWwKKayu3guzaUkRSzyDFGbIxqihWlDSp5d2zG+/KNqt3+5ABsUqn9F7IJ5wBcqlc1bksFJP5rI6YkmhyjcS/NokG3UXXIZlS6DVDmcsZ6lNj0DWw6BjU9xKayeSFAF182RWrBI566fA7bsqBzpHzSeNJnsn12xeamfM1x4GRj/RFswlgwRXbdcK30DDHcGdgTFUj2N/csFpfafRVFRunXDZvnj2JQHVbMDJnHxJvZ7K1hTAm04cWfNcsXUk2WsWdhSj7cbZFh5lAju1FiPinrgs34UE5M9Fm9sJPVdGUf3pxNzv0b2YR7UYoUDXln8d/2QnbVGrCQj2StsE2+oEizFpSN28yeHbAZ+cUj+4X6desfEh5WQhD2Djuj5G1i8+DW+INsKpGvWqj0ZMS0IFjuu30wtrTYamQpI98ql1f8ZWjc89m31fftYTYn5YpJ2UG82pNrQHBYJg4IMQkWuvKZr5tCLj/Cpvz+1rMpDUxY2vEmcK+jK+Rx9jQSlQiNbB4B0wOTFluaPvoaVqiFTcsItaCTyS5hcuMhRnhU48cI2Wyf/HVQ9h6dxBycjA3SCbODOgDLam72Ph5g8yOogOrYlMoFXjVuiw/LD1JXd2vEkMhDSdhpVPvKTwZrynLTDtoM1A6NaWCHZ4rTvvU3iUjmgBjzvhf1O8zIl6rz287NW7lU+Hk6j2vFZZGQMnuryBiuSR2x+SqslsdzdG4MMBWY8LLHZTuXnvrWp8tll/UZMSw0bMoyrlZJLugpRij53F9OuEy+gH0gdP4xNn89zkG+ZlFyyWX5JvvGJ5+7woF92d+z7NsQHDr9sfmTsNqwYtIFpYAWexKfZAt1PF/shGRaLXy+z4HpO5rYbOnl/YdHsCgMeVhWuSc86XXuwT7h4e/bbNWOvxDyt2AF/2PzxyAK8tUwJDDKcvV1nfYmc76VExnDhBFgHk3SvbaSDh2wKe+p/9h8LaaXXEmjZG3Y5A0Y4SukMJoJB40LYQet1O2PzZ+AVKHMhCxFnybt57ylIrBKnE8Iv+M9lcJBCvyx+RNwRblCiQKzdvodlhxWbOqhNxmb/h+bb8Q810oo9m1uPwk1samFrP6x+W4ci5SRPjIklMghcyixqRpAO2Lz3DdgHi2h4em4A7/vlKOSlfJzZKpUbyX951T+5055xgEonn03q+uH6Ynqk8ffj+k651JLFwLwYWRTO101sYnbszk23tSD0DaRbxxb/Qd+Vo+z4A1C6LJjuBmEH1tG8oVEW8XMfUJyrdl34G6l/0x2ZR82819jsoB7sDrkeVtCtqm1GL6WTXuMWIjQMLYUg6u4kkKULXcN/pRZA9yNqPbQAsSB5hH3wO/aFGN/VPz1sGMIRxvEo5JL++lahoLN7/ZsSpLW4F5oRG38Ji7HN4aEwcgrmEs73KtxKJban8OmdgJqy8p4N+IFyzoRsnWjN57O5vc9bDpm42iIlGfFSwFjEWDAJpwNbPlWNjXfMlRzE8A9KJQSnx2mKbXn62F92Ryukfk08dG5OeuSTQ/nnpxKrnT5XH4Hg0jWWoyYGc9hc655o3R7/nDNz7T8LTfAzjYM4TCkYYgRO5m0lJ/Fplck/YSxBbLTxgcov52+lU2Dl3VtHGM7nKngkiL/mlY6Owk7UHEMnS5M+gaad5e7MrqxKdb4Z7LpsXwaKjGZpRkLzgZhWH4fm1pOd0O19+MqaqfkJGpc8EOwEBH/tL8ERHgZEM0nnR9+QTbr1k3IJh/4rtkssrRAiipfehi+IDzI38emqeW2SYOsyO7KxJf8RUbUw2gzzxSU+DjkSUm3qhwo2RSz2InN0rXoKWwWG1goUYv83jMYYy3k8vvYPKl7INHVjq6/EC5m1cAO/gu5vO3Fe5xFmsyT7UH9j86mu6R9lE1qyGtZbmBhvoJCBYLBC9nAXUmVbBuuY1TKwi2sB92yaY5msWWnbgsxVn5lxZtw/8q4tyMiP3v/KL5RULC5BmzaLHudskm/edaVvXqfbWEjhmFf2VDC8ctbjUZVrm2YmHtd/TDiY9wxm2pMd95qc4I6J2RxGnIekz77LxaNbtPZtzUFQN/Dpux78ACbxe5veQIzqhhluN/JDuMgWYZNJsgTjdUNScdsmrjk5Tqy7o0YV0W2pWFmxWg6ZHwIUZzyRQwy4I1sVqMD8+gXoTFww8ODL2E6F98QQwPTjahZObplc6ZY9cp+dWXdm4/HV+lOi7T3OZuEs2mKFvkRbIK8HqX+rUzOnZY8yqDZvZLNgy2ugfaegjlk07R5trCpCovnsgls15U2AreMgZKXBOuRQi9lU8mSItfcsXUvx3PYLONQeDjsI+tm3V1FHGd4aVgEVRFjuv0XsglERyL/+0nexU9hM+6KzWp0QM5RaT0AA0w/QbZ9syLQgk3cn6wkTE4t2dzL/I3kC3q0UMRukLJJ/gU2QSwWruqC+wyoyJgXpxZsyteXcoDqm9kEueLQDGTa7M66J8OBTa483ssmXzfPj2soCmlYOhyAxgIZyOzo1IbNOjSzCcQ+hnKkM+sewM9mkxz5dVy3aAx3+nLCB+vt4rYcqq9jM1EWSsCuKQPJw/jZbOYXcyFlow9O79Vrb8u/WmTZy9gENzXyNQdI3q6sewCds8lJg/mCoq6t7rAqS2Ifq/XsZWzKT0KFTxgQtR1Z99TeP2Fuglxej8xNIxQhtTFOTus242Vsykc8mUYCTCCa+aUDuLFJDWyqAStgbhZDKs3Ne7ING6E6vU23hkL2V/9VbAKdKnN0AWbHzqx7ElRJazC7F54kLdgEGU07ZlO9jNdsPyPWxOOvYlMWGTR3vr0YFNYuoVoPumUTd88m9bVjkZU+OfUraEu8iM0YmCIP2ZdQ1Dpmum8BBzapG5tTg6Ttnk1MDTt7Pc2LMWldhhexCa5mLjwKgZeQaz6sFsjYHLuwuXk/m5R9myximisVNaV2ydHKFsQA2tiCgMmxvCpbtvU9wbrnMDe91nMT3qDRGZsUeZaNqvqnurt02thp77e6wytYgu+9wPdJ/lZr/GE4zE1P29NeXNlE3bBJKeXevnurbVOJY6jNIf+aMxRwr3n6APntNfCxaiTIfchOq3msRB2b3p1sPjw3syRWyWl/2M3q5BKMPKm9SvA1bHouMF03+BAUNk0ZnoPWbFa3wj3Ipu1KCg3gysV6i/ZL2FQDw8wwnqY/gsx6UErax9kUHkeFF4+YJI+w6ep4Ci5Mrd8svoTN2mSKJZwvV3OFI5v86u4GNpdVtuFen19LTmmWyTX74a687v8sm01Jx4vyrjcfOkKx7NnY5F2HbCKVzcySxTKHl8ElXe0uuSARXkKu7+GvYNNVa217KXkTWrB5qPIFUUMWi+M23bnpUSw9ftTspz85nhn8Cjbrr9+Q23d8Pkc4sEnyGbngDyqSMRv1zd4wSTZmDWo6OiXGVEQG/AY2J6ZzACM6vli8mc14m+9t4oQghPlBGL8XyybyV+fd6PszCWgqX1PNYnydt/Pr/g1s9l2CmBy62hqZ9YBfdsh6Fn3zlJKYidVllK2KnNf/TFezzw8BQdgvsoZnWj/62PfdFavfwCbw7aOeklEaRj11at3L2Iy2eJtqEAdfv2UuHako0po8DnQFfbbWXD6KB8Lk09WK9QvYvMFb5NUOPHIreQOmvggxOu74rDt+MLOf22r+tf4M+KULyDvthwYqe8uLepMlJBR5bv3+BWx+GaMsSgBnr5qju3uxErdF2qTh6itgyC+jKCn1EcEHZdncsUYNCzlpnL+ATWt6jQzQIN+t795seEHZFQCEJAftTgEeVWa4w8ML2UUuOnaxZPmJwyLx77MJGqCaoFVEbZfWvVnAdcGy6RATNUbOev1V+FFN5r6TWVJJBG/Gv88mSPdk6gvIptKhdY+nnlWAYPN9u1VDurvF5tOqovZwI8M/zyZwITEqlDcoajuz7q2RrwFm/vtiPsZ6IZEnoNr/Dpm5CEQYGrMKQjRnITRhIic7NBqkSpxBXkSNzbqsiYkpa6KckJH3dyDXgI0aSCDXwzpL9XpbDDUoL1N/95VCLzYcLqSh3o1MJRSMNw5Ri7OBhL6rNhb35b/VGlimoKgqLKbyjwPF8DEHP1r6G4FCxgP2IyjSuQfCH/5B/A+OXrqx0W8zLwAAAABJRU5ErkJggg==) | 
# -
# Pythia credit: Rose, B. E. J., Kent, J., Tyle, K., Clyne, J., Banihirwe, A., Camron, D., May, R., Grover, M., Ford, R. R., Paul, K., Morley, J., Eroglu, O., Kailyn, L., & Zacharias, A. (2023). Pythia Foundations (Version v2023.05.01) https://zenodo.org/record/8065851
# 
# 

# # **Tutorial Objectives**
# 
# Global climate can vary on long timescales, but it's also important to understand seasonal variations. For example, seasonal variations in precipitation associated with the migration of the [Intertropical Convergence Zone (ITCZ)](https://glossary.ametsoc.org/wiki/Intertropical_convergence_zone#:~:text=(Also%20called%20ITCZ%2C%20equatorial%20convergence,and%20Northern%20Hemispheres%2C%20respectively).) and monsoon systems occur in response to seasonal changes in temperature. In this tutorial, we will use data analysis tools in Xarray to explore the seasonal climatology of global temperature. Specifically, in this tutorial, we'll use the `groupby` operation in Xarray, which involves the following steps:
# 
# - **Split**: group data by value (e.g., month).
# - **Apply**: compute some function (e.g., aggregate) within the individual groups.
# - **Combine**: merge the results of these operations into an output dataset.

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


# # **Section 1: GroupBy: Split, Apply, Combine**
# 
# Simple aggregations (as we learned in the previous tutorial) can give useful summary of our dataset, but often we would prefer to aggregate conditionally on some coordinate labels or groups. Xarray provides the so-called `groupby` operation which enables the **split-apply-combine** workflow on Xarray DataArrays and Datasets. The split-apply-combine operation is illustrated in this figure from [Project Pythia](https://foundations.projectpythia.org/core/xarray/computation-masking.html):
# 
# ![image.png](attachment:image.png)
# 
# 
# 
# - The **split** step involves breaking up and grouping an xarray Dataset or DataArray depending on the value of the specified group key.
# - The **apply** step involves computing some function, usually an aggregate, transformation, or filtering, within the individual groups.
# - The **combine** step merges the results of these operations into an output xarray Dataset or DataArray.
# 
# We are going to use `groupby` to remove the seasonal cycle ("climatology") from our dataset, which will allow us to better observe long-term trends in the data. See the [xarray `groupby` user guide](https://xarray.pydata.org/en/stable/user-guide/groupby.html) for more examples of what `groupby` can take as an input.

# Let's start by loading the same data that we used in the previous tutorial (monthly SST data from CESM2):

# In[ ]:


filepath = DATASETS.fetch('CESM2_sst_data.nc')
ds = xr.open_dataset(filepath)
ds


# Then, let's select a gridpoint closest to a specified lat-lon (in this case let's select 50ºN, 310ºE), and plot a time series of SST at that point (recall that we learned this is Tutorial 2). The annual cycle will be quite pronounced. Note that we are using the `nearest` method (see Tutorial 2 for a refresher) to find the points in our datasets closest to the lat-lon values we specify. What this returns may not match these inputs exactly.

# In[ ]:


ds.tos.sel(lon=310, lat=50, method='nearest').plot(); #time range is 2000-01-15 to 2014-12-15


# This plot is showing changes in monthly SST between 2000-01-15 to 2014-12-15. The annual cycle of SST change is apparent in this figure, but to understand the climatatology of this region, we need to calculate the average SST for each month over this time period. The first step is to split the data into groups based on month.

# ## **Section 1.1: Split**
# 
# Let's group data by month, i.e. all Januaries in one group, all Februaries in one group, etc.
# 

# In[ ]:


ds.tos.groupby(ds.time.dt.month)


# <div class="admonition alert alert-info">
# 
# In the above code, we are using the `.dt` [`DatetimeAccessor`](https://xarray.pydata.org/en/stable/generated/xarray.core.accessor_dt.DatetimeAccessor.html) to extract specific components of dates/times in our time coordinate dimension. For example, we can extract the year with `ds.time.dt.year`. See also the equivalent [Pandas documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.html).
#     
#    </div>

# Xarray also offers a more concise syntax when the variable you’re grouping on is already present in the dataset. This is identical to `ds.tos.groupby(ds.time.dt.month)`:

# In[ ]:


ds.tos.groupby('time.month')


# ## **Section 1.2: Apply & Combine**
# 
# Now that we have groups defined, it’s time to “apply” a calculation to the group. These calculations can either be:
# 
# - aggregation: reduces the size of the group
# - transformation: preserves the group’s full size
# 
# At then end of the apply step, xarray will automatically combine the aggregated/transformed groups back into a single object. 
# 
# 
# 
# ### **Section 1.2.1: Compute the Climatology** 
# 
# 
# Let's calculate the climatology at every point in the dataset. To do so, we will use aggregation and will calculate the mean SST for each month:
# 

# In[ ]:


tos_clim = ds.tos.groupby('time.month').mean()
tos_clim


# For every spatial coordinate, we now have a monthly mean SST for the time period 2000-01-15 to 2014-12-15.
# 
# We can now plot the climatology at a specific point:

# In[ ]:


tos_clim.sel(lon=310, lat=50, method='nearest').plot();


# Based on this plot, the climatology of this location is defined by cooler SST from December to April and warmer SST from June to October, with an annual SST range of ~8ºC. 

# #### **Questions 1.2.1: Climate Connection**
# 
# 1. Considering the latitude and longitude of this data, can you explain why we observe this climatology?
# 2. How do you think seasonal variations in SST would differ at the equator? What about at the poles? What about at 50ºS?

# In[ ]:


# to_remove explanation

"""
1. This location's strong seasonality suggests that it experiences significant seasonal changes in incoming solar radiation received at the surface over the course of a year.
2. Seasonal variations in sea surface temperature (SST) would differ at different latitudes. At the equator, the seasonal variations in SST tend to be relatively small. This is because the equatorial region experiences a relatively constant amount of solar radiation throughout the year, resulting in a relatively stable SST. At the poles, however, the seasonal variations in SST are more pronounced. At 50ºS, the seasonal cycle would be opposite that shown here because the northern and southern hemispheres experience their seasons at different times of year (that is northern hemisphere summer is southern hemisphere winter).
""";


# ### **Section 1.2.2: Spatial Variations**

# We can now add a spatial dimension to this plot and look at the zonal mean climatology (the monthly mean SST at different latitudes):

# In[ ]:


tos_clim.mean(dim='lon').transpose().plot.contourf(levels=12, cmap='turbo');


# This gives us helpful information about the mean SST for each month, but it's difficult to asses the range of monthly temperatures throughout the year using this plot.
# 
# To better represent the range of SST, we can calculate and plot the difference between January and July climatologies:

# In[ ]:


(tos_clim.sel(month=1) - tos_clim.sel(month=7)).plot(size=6, robust=True);


# #### **Questions 1.2.1: Climate Connection**
# 
# 1. What patterns do you observe in this map?
# 2. Why is there such an apparent difference between the Northern and Southern Hemisphere SST changes?
# 3. How does the migration of the ITCZ relate to seasonal changes in Northern vs. Southern Hemisphere temperatures?

# In[ ]:


# to_remove explanation

"""
1. Generally the difference is negative in the northern hemisphere and positive in the southern hemisphere.
2. The hemispheres have opposing signs, which is because of Earth's tilt and how it affects the timing of the seasons in each hemisphere (i.e. northern hemisphere summer is southern hemisphere winter). In the northern hemisphere the difference is negative because northern hemisphere July is warmer than northern hemisphere January. In the southern hemisphere, the opposite is true.
3. The ITCZ shifts with the seasons. During the time when the Sun is directly overhead at the Northern Tropics (June), the ITCZ moves northwards, and when the Sun is directly overhead at the Southern Tropics (December), the ITCZ shifts southwards. This migration can affect the distribution of rain, leading to wet and dry seasons in many tropical regions.
""";


# # **Summary**
# 
# In this tutorial, we focused on exploring seasonal climatology in global temperature data using the split-apply-combine approach in Xarray. By utilizing the split-apply-combine approach, we gained insights into the seasonal climatology of temperature and precipitation data, enabling us to analyze and understand the seasonal variations associated with global climate patterns.
# 
# 
# 

# # **Resources**

# Code and data for this tutorial is based on existing content from [Project Pythia](https://foundations.projectpythia.org/core/xarray/computation-masking.html).
