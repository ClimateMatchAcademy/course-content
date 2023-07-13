#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W1D5_ClimateModeling/instructor/W1D5_Tutorial2.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W1D5_ClimateModeling/instructor/W1D5_Tutorial2.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 2 : Energy Balance**
# 
# 
# **Week 1, Day 5, Climate Modeling**
# 
# **Content creators:** Jenna Pearson
# 
# **Content reviewers:** Dionessa Biton, Younkap Nina Duplex, Zahra Khodakaramimaghsoud, Will Gregory, Peter Ohue, Derick Temfack,  Yunlong Xu, Peizhen Yang, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Brodie Pearson, Abigail Bodner, Ohad Zivan, Chi Zhang
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS

# # **Tutorial Objectives**
# 
# In this tutorial students will learn about the components that define energy balance, including insolation and albedo.
# 
# By the end of this tutorial students will be able to:
# * Calculate the albedo of Earth based on observations.
# * Define and find the equilibrium temperature under the assumption of energy balance.
# * Understand the relationship between transmissivity and equilibrium temperature.

# # **Setup**

# In[ ]:


# imports
import xarray as xr                     # used to manipulate data and open datasets
import numpy as np                      # used for algebra and array operations
import matplotlib.pyplot as plt         # used for plotting


# ##  Figure settings
# 

# ###  Figure settings
# 

# In[ ]:


# @title Figure settings
import ipywidgets as widgets       # interactive display
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
plt.style.use("https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/cma.mplstyle")


# ##  Video 1: Energy Balance
# 

# ###  Video 1: Energy Balance
# 

# In[ ]:


# @title Video 1: Energy Balance
#Tech team will add code to format and display the video


# # **Section 1 : A Radiating Sun**

# ## **Section 1.1: Incoming Solar Radiation (Insolation) and Albedo ($\alpha$)**

# Just as Earth emits radiation, so does the sun. The incoming solar radiation, called **[insolation](https://glossary.ametsoc.org/wiki/Insolation)**. From the 'All Sky' Energy budget shown below, this is observed to be $Q = 340 W m^{-2}$. 
# 
# Some of this radiation is reflected back to space (for example off of ice and snow or clouds). 
# 
# From the 'All Sky' energy budget below, the amount reflected back is $F_{ref} = 100 W m^{-2}$. 
# 
# 
# ![Global Mean Energy Budget](https://www.ipcc.ch/report/ar6/wg1/downloads/figures/IPCC_AR6_WGI_Figure_7_2.png)
# Figure 7.2 | Schematic representation of the global mean energy budget of the Earth (upper panel), and its equivalent without considerations of cloud effects (lower panel). Numbers indicate best estimates for the magnitudes of the globally averaged energy balance components in W m–2 together with their uncertainty ranges in parentheses (5–95% confidence range), representing climate conditions at the beginning of the 21st century. Note that the cloud-free energy budget shown in the lower panel is not the one that Earth would achieve in equilibrium when no clouds could form. It rather represents the global mean fluxes as determined solely by removing the clouds but otherwise retaining the entire atmospheric structure. This enables the quantification of the effects of clouds on the Earth energy budget and corresponds to the way clear-sky fluxes are calculated in climate models. Thus, the cloud-free energy budget is not closed and therefore the sensible and latent heat fluxes are not quantified in the lower panel. Figure adapted from Wild et al. (2015, 2019). (Credit: [IPCC AR6 Report](https://www.ipcc.ch/report/ar6/wg1/downloads/figures/IPCC_AR6_WGI_Figure_7_2.png))

# The *fraction* of reflected radiation is captured by the **albedo (**$\mathbf{\alpha}$**)**
# 
# \begin{align}
# \alpha = \frac{F_{ref}}{Q}
# \end{align}
# 
# Albedo is a unitless number between 0 and 1. We can use this formula to find the albedo of Earth.

# In[ ]:


# define the observed insolation based on observations from the IPCC AR6 Figure 7.2
Q = 340 # W m^-2

# define the observed reflected radiation based on observations from the IPCC AR6 Figure 7.2
F_ref = 100 # W m^-2

# plug into equation
alpha = (F_ref/Q) # unitless number between 0 and 1

# display answer
print('Albedo: ',alpha)


# ### **Questions 1.1: Climate Connection**

# 1. Keeping insolation ($Q$) constant, what does a low albedo imply? What about a high albedo?
# 2. There are two components to albedo, the reflected radiation in the numerator and the insolation in the denomenator. Do you think one or both of these have changed over Earth's history?

# In[ ]:


# to_remove explanation

"""
1. If the insolation does not vary, a low albedo implies that Earth is less reflective (e.g less cloud, snow or ice cover) and vice versa for high albedo.
2. Both. The reflected radiation is a function of land surface changes (e.g. glaciations and vegetation changes) and clouds (water vapor changes).  The radiation from the sun has also varied over time, which you will go into more detail in tutorial 4.
""";


# ## **Section 1.2 : Absorbed Shortwave Radiation (ASR)**

# The **absorbed shortwave radiation (ASR)** is the amount of this isolation that is *not* reflected, and actually makes it to Earth's surface. Thus,
# 
# \begin{align}
# ASR = Q-F_{ref} = (1-\alpha)Q
# \end{align}
# 
# From observations, we can esimate the absorbed shortwave radiation.

# In[ ]:


# plug into equation
ASR = (1-alpha)*Q

# display answer
print('Absorbed Shortwave Radiation: ',ASR,' W m^-2')


# ### **Questions 1.2: Climate Connection**
# 
# 1. Compare the value of ASR to the observed OLR of $239 W m^{-2}$. Is it more or less? What do you think this means?
# 2. Does this model take into account any effects of gases in that atmosphere on the incoming shortwave radiation that makes it to Earth's surface? Are there any greenhouse gases you think are important and should be included in more complex models?

# In[ ]:


# to_remove explanation

"""
1. It is slightly more. This means that Earth is absorbing more energy than it is losing. This is just to get you thinking about energy balance that will be discussed in the remainder of the tutorial.
2. It does not take these into account. For example, ozone is a notable greenhouse gas that absorbs in the UV range.
""";


# # **Section 2 : Energy Balance**

# ## **Section 2.1: Equilibrium Temperature**

# Energy Balance is achieved when radiation absorbed by Earth's surface (ASR) is equal to longwave radiation going out to space (OLR). That is 
# 
# \begin{align}
# ASR = OLR
# \end{align}
# 
# By substituting into the equations from previous sections, we can find the surface temperature of Earth needed to maintain this balance. This is called the **equilibrium temperature (** $\mathbf{T_{eq}}$ **)**.
# 
# Recall $OLR = \tau\sigma T^4$ and $ASR = (1-\alpha)Q$. The **equilibrium temperature** is the temperature the system would have if energy balance was perfectly reached. Assuming energy balance, we will call the emission temperature denoted previously the equilibrium temperature ($T_{eq}$) instead. Thus,
# 
# \begin{align}
# (1-\alpha)Q = ASR = OLR = \tau\sigma T_{eq}^4
# \end{align}
# 
# Solving for $T_{eq}$ we find
# 
# \begin{align}
# T_{eq} = \sqrt[4]{\frac{(1-\alpha)Q}{\tau\sigma}}
# \end{align}
# 
# Let's calculate what this should be for Earth using observations:

# In[ ]:


# define the Stefan-Boltzmann Constant, noting we are using 'e' for scientific notation
sigma = 5.67e-8 # W m^-2 K^-4

# define transmissivity (calculated previously from observations in tutorial 1)
tau = 0.6127 # unitless number between 0 and 1

# plug into equation
T_eq = (((1-alpha)*Q)/(tau * sigma))**(1/4)

# display answer
print('Equilibrium Temperature: ',T_eq,'K or',T_eq - 273, 'C')


# # **Section 3 : Climate Change Scenario**

# ## **Section 3.1: Increasing Greenhouse Gas Concentrations**

# Assume due to the increasing presence of greenhouse gases in the the atmosphere, that $\tau$ decreases to $0.57$.
# 
# We can then use our climate model and python to find the new equilibrium temperature.

# In[ ]:


# define transmissivity (assupmtion in this case)
tau_2 = 0.57 # unitless number between 0 and 1

# plug into equation
T_eq_2 = (((1-alpha)*Q)/(tau_2 * sigma))**(1/4)

# display answer
print('New Equilibrium Temperature: ',T_eq_2,'K or',T_eq_2 - 273, 'C')


# ### **Questions 3.1: Climate Connection**

# 1.  Does a reduction in the transmissivity, $\tau$, imply a decrease or increase in OLR?
# 2.  How does the new equilibrium temperature compare to that calculated previously? Why do you think this is?

# In[ ]:


# to_remove explanation

"""
1. A decrease. A lower transmissivity means the atmosphere is less transparent, and therefore less radiation escapes to space.
2. It is much higher because the greenhouse effect is stronger and trapping more heat.
""";


# ### **Coding Exercises 3.1**

# 1. Plot the equilibrium temperature as a function of $\tau$, for $\tau$ ranging from zero to one.

# ```python
# # define the observed insolation based on observations from the IPCC AR6 Figure 7.2
# Q = ...
# 
# # define the observed reflected radiation based on observations from the IPCC AR6 Figure 7.2
# F_ref = ...
# 
# # define albedo
# alpha = ...
# 
# # define the Stefan-Boltzmann Constant, noting we are using 'e' for scientific notation
# sigma = ...
# 
# # define a function that returns the equilibrium temperature and takes argument tau
# def get_eqT(tau):
#   return ...
# 
# # define tau as an array extending from 0 to 1 with spacing interval 0.01
# tau = ...
# 
# # use list comprehension to obtain the equilibrium temperature as a function of tau
# eqT = ...
# 
# 
# _ = ...
# plt.xlabel(...)
# plt.ylabel(...)
# 
# ```

# In[ ]:


# to_remove solution

# define the observed insolation based on observations from the IPCC AR6 Figure 7.2
Q = 340 # W m^-2

# define the observed reflected radiation based on observations from the IPCC AR6 Figure 7.2
F_ref = 100 # W m^-2

# define albedo
alpha = (F_ref/Q) # unitless number between 0 and 1

# define the Stefan-Boltzmann Constant, noting we are using 'e' for scientific notation
sigma = 5.67e-8 # W m^-2 K^-4

# define a function that returns the equilibrium temperature and takes argument tau
def get_eqT(tau):
  return (((1-alpha)*Q)/(tau * sigma))**(1/4)

# define tau as an array extending from 0 to 1 with spacing interval 0.01
tau = np.arange(0,1.01,.01)

# use list comprehension to obtain the equilibrium temperature as a function of tau
eqT = [get_eqT(t) for t in tau]

_ = plt.plot(tau,eqT, lw = 3)
plt.xlabel('Transmissivity')
plt.ylabel('Equilibrium Temperature');


# # **Summary**
# In this tutorial, you explored the fundamentals of Earth's energy balance.  You learned how to calculate Earth's albedo $\mathbf{\alpha}$ and how absorbed shortwave radiation contributes to energy balance. You also discovered the concept of equilibrium temperature and it's relationship to energy balance. The tutorial also highlighted the impact of increasing greenhouse gases on the equilibrium temperature.
