#!/usr/bin/env python
# coding: utf-8

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ClimateMatchAcademy/course-content/blob/main/tutorials/W2D3_FutureClimate-IPCCII&amp;IIISocio-EconomicBasis/W2D3_Tutorial2.ipynb)   <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/tutorials/W2D3_FutureClimate-IPCCII&amp;IIISocio-EconomicBasis/W2D3_Tutorial2.ipynb" target="_blank"><img alt="Open in Kaggle" src="https://kaggle.com/static/images/open-in-kaggle.svg"/></a>

# # **Tutorial 2: Transition Goals and Integrated Assessment Models**
# 
# **Week 2, Day 3: IPCC Socio-economic Basis**
# 
# **Content creators:** Maximilian Puelma Touzel
# 
# **Content reviewers:** Peter Ohue, Derick Temfack, Zahra Khodakaramimaghsoud, Peizhen Yang, Younkap Nina DuplexLaura Paccini, Sloane Garelick, Abigail Bodner, Manisha Sinha, Agustina Pesce, Dionessa Biton, Cheng Zhang, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS

# # **Tutorial Objectives**
# 
# In this tutorial, you will learn about the Dynamic Integrated Climate-Economy (DICE) model, a cornerstone in the history of climate economics. This is one the first Integrated Assessment Models (IAMs), a class of models that combine climatology, economics, and social science, reflecting the intertwined nature of these domains in addressing climate change.
# 
# You will explore the inner workings of the DICE model, starting with the foundational principles of economics: *utility* and *welfare* functions. You will also learn how these functions aggregate and weight the satisfaction derived from consumption across different societal groups. You will also learn how the these functions incorporate uncertain future utility into decision-making through *discount rates*. Valuing future states of the world allows the DICE model to place a value on its projections of future scenarios.
# 
# Later in the tutorial you will learn about damage functions, which combine climatological and economic knowledge to estimate how climate changes will affect economic productivity and the resultant well-being of society.
# 
# Finally, you will diagnose optimal planning within the DICE model, determining the best strategies for savings and emissions reduction rates (where _best_ is with respect to a chosen utility and welfare function). 
# 
# The overall objective of this tutorial is to provide a technical understanding of how parameters related to the distribution of value in society impact the optimal climate policy within a relatively simple IAM.

# # **Setup**

# In[ ]:


# imports
from IPython.display import display, HTML
import seaborn as sns
import matplotlib.pyplot as pl
import pandas as pd
import numpy as np
import dicelib #https://github.com/mptouzel/PyDICE


# ##  Figure settings
# 

# ###  Figure settings
# 

# In[ ]:


# @title Figure settings
import ipywidgets as widgets       # interactive display
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
plt.style.use("https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/cma.mplstyle")

get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style("ticks", {'axes.grid': False})
params = {'lines.linewidth': '3'}
pl.rcParams.update(params)
display(HTML("<style>.container { width:100% !important; }</style>"))


# ##  Helper functions
# 

# ###  Helper functions
# 

# In[ ]:


# @title Helper functions

def plot_future_returns(gamma, random_seed):
    fig,ax=pl.subplots(1,2,figsize=(8,4))
    np.random.seed(random_seed)
    undiscounted_utility_time_series = np.random.rand(time_steps)
    ax[0].plot(undiscounted_utility_time_series)

    discounted_utility_time_series=undiscounted_utility_time_series*np.power(gamma,np.arange(time_steps))
    ax[0].plot(discounted_utility_time_series)

    cumulsum_discounted_utility_time_series=np.cumsum(discounted_utility_time_series)
    ax[1].plot(cumulsum_discounted_utility_time_series*(1-gamma),color='C1',label=r'discounted on $1/(1-\gamma)=$'+'\n'+r'$'+str(round(1/(1-gamma)))+'$-step horizon',)
    cumulsum_undiscounted_utility_time_series=np.cumsum(undiscounted_utility_time_series)
    ax[1].plot(cumulsum_undiscounted_utility_time_series/cumulsum_undiscounted_utility_time_series[-1],label='undiscounted',color='C0')
    ax[1].axvline(1/(1-gamma),ls='--',color='k')


    ax[0].set_ylabel('utility at step t')
    ax[0].set_xlim(0,time_steps)
    ax[0].set_xlabel('time steps into the future')
    ax[1].legend(frameon=False)
    ax[1].set_ylabel('future return (normalized)')
    ax[1].set_xlabel('time steps into the future')
    ax[1].set_xlim(0,time_steps)
    fig.tight_layout()


# ##  Video 1: Title
# 

# ###  Video 1: Title
# 

# In[ ]:


# @title Video 1: Title
#Tech team will add code to format and display the video


# # **Section 1: Background on IAM Economics and the DICE Model**

# The [Dynamic Integrated Climate-Economy (DICE)](https://www3.nd.edu/~nmark/Climate/DICE-simplified_2019.pdf) was the first prominent Integrated Assessment Model (IAM), a class of models economists use to inform policy decisions. Recall that IAMs couple a climate model to an economic model, allowing us to evaluate the two-way coupling between economic productivity and climate change severity. DICE is too idealized to be predictive, like `world3`, but DICE is still useful as a sandbox for exploring climate policy ideas, which is how we will use it here.
# 
# Let's begin with a brief description of IAMs and the DICE model:
# 
# - DICE is a fully aggregated (i.e., non-spatial) model, but otherwise contains the essence of many key components of more complex IAMs. 
# - Unlike `world3`, which we encountered in Tutorial 1, the world models used in IAMs usually have *exogeneous* (externally set) times series for variables, in addition to fixed world system parameters. These exogeneous variables are assumed to be under our society's control (e.g. mitigation). 
# - IAMs come equipped with an objective function (a formula that calculates the quantity to be optimized). This function returns the value of a projected future obtained from running the world model under a given climate policy. This value is defined by time series of these exogeneous variables. In this sense, the objective function is what defines "good" in "good climate policy". 
# - The computation in an IAM is then an optimization of this objective as a function of the time series of these exogeneous variables over some fixed time window. In DICE, there are two exogeneous parameters:
#     - **$\mu(t)$**: time-dependent mitigation rate (i.e. emissions reduction), which limits warming-caused damages
#     - **$S(t)$**: savings rate, which drives capital investment 
# - The choices for the standard values of the parameters used in the DICE models have been critisized, and updated versions have been analyzed and proposed ([Hansel et al. 2020](https://www.nature.com/articles/s41558-020-0833-x);[Barrage & Nordhaus 2023](https://www.nber.org/papers/w31112)). Here, we look at the standard DICE2016 version of the model.
# 
# All DICE models (and most IAMs) are based on *Neo-classical economics* (also referred to as "establishment economics"). This is an approach to economics that makes particular assumptions. For example, it is assumed that production, consumption, and valuation of goods and services are driven solely by the supply and demand model. To understand this approach and how it is used in the DICE model, it is important to begin with a brief overview of some fundamental concepts. One such concept is **utility** (i.e. economic value), which is not only central to economics but also to decision theory as a whole, which is a research field that mathematically formalizes the activity of *planning* (planning here means selecting strategies based on how they are expected to play out given a model that takes those strategies and projects forward into the future).

# ## **Section 1.1: Utility**

# **Utility**, or economic value, is the total degree of satisfaction someone gets from using a product or service. In the context of socioeconomic climate impacts, utility of a state of the world for an individual is quantified by the consumption conferred (i.e. capital consumed; you can think of money as a placeholder for capital). 
# 
# Reducing value to consumption may seem restrictive, and it is, but it's how most economists see the world (not all! c.f. [Hüttel, Balderjahn, & Hoffmann,*Welfare Beyond Consumption: The Benefits of Having Less* Ecological Economics (2020)](https://www.sciencedirect.com/science/article/abs/pii/S0921800919318683)). That said, economists don't think utility is identical to consumption. Let's work through the assumptions in a standard presentation of the economics that links the two.

# ### **Section 1.1.1: Utilities at Different Levels of Consumption**
# It's natural that the utility of consumption is relative to the level of consumption. A crude illustration here is that the value of a meal is higher to those who haven't eaten recently than for those who have. Thus, we assume units of consumption at low values confer more utility than those at high values. In other words:
# 
# - **A unit of consumption has less value to an individual, the more that individual tends to consume overall**
# 
# The one parameter for the utility function is **elasticity** ($\alpha$), which is the measure of a variable's sensitivity to change in another variable, in this case, how utility changes with consumption. 
# 
# We can plot the utility function for different values of elasticity to assess how the sensitivity of utility to changes in comsumption varies with different elasticity values.

# In[ ]:


fig,ax=pl.subplots()
c = np.linspace(0,10,1000)
for alpha in [0, 0.1,0.5,1.0, 1.45]:
    if alpha==1:
        ax.plot(c,np.log(1+c),label=r'$\alpha='+str(alpha)+'$')
    elif alpha==1.45:
        ax.plot(c,((c+1)**(1-alpha)-1)/(1-alpha),label=r'$\alpha='+str(alpha)+'$(DICE)')
    else:
        ax.plot(c,((c+1)**(1-alpha)-1)/(1-alpha),label=r'$\alpha='+str(alpha)+'$')

ax.plot([0,10],[0,10],'k--')
ax.legend(frameon=False)
ax.set_xlabel('consumption, c')
ax.set_ylabel('utility, u(c)')


# The plot you just made shows the relationship between consumption and utility for four different values of elasticity. For all values of elasticity, as consumption increases, the utility also increases, as we discussed above. However, let's make some observations about how changes in elasticity affect this relationship. For lower elasticity values (i.e. $\alpha$ = 1 shown in blue) an increase in consumption results in a stronger increase in utility. In constrast, for high elasticity values (i.e. $\alpha$ = 1.45 shown in red), such as what is used in the DICE model, an increase in consumption results in only a smaller increase in utility.

# #### **Questions 1.1.1**
# 1. What do you think the function looks like for $\alpha=0$?

# In[ ]:


# to_remove explanation
"""
1. Plug alpha=0 into (c+1)**(1-alpha)-1)/(1-alpha). Since alpha is zero, the expression becomes c. Therefore, the plot for alpha = 0 would fall on the 1:1 line shown in the dashed black line in the plot above.
""";


# ### **Section 1.1.2: Utilities Over a Population**
# In the case that individuals are of the same type, i.e. a population of such individuals, we assume that 
# * **Utilities of individuals of the same type sum**

# ### **Section 1.1.3: Utilities Over Time**
# Since our actions now affect those in the future (the socalled *intertemporal choice problem*), we can't decide what is best to do at each time point by looking only at how it affects the world at that time. We need to incorporate utilities from the future into our value definition to know what is best to do now. How should we combine these? 
# 
# Economists and decision theorists generally operate under the assumption that the value of a unit of utility decreases as it is received further into the future. This assumption is based on the recognition of the inherent uncertainty surrounding future events and the finite probability that they may not materialize. In other words:
# * **Utilities in the near future are valued more than those in the far future**
# 
# This devaluation of the future is called *temporal discounting*. You can imagine that there is a lot of debate about how and even whether to do this in climate policy design! 
# 
# The standard approach to incorporate temporal discounting into the model is to multiply the utilities of future benefits and costs by a **discount factor** ($\gamma$ ('gamma'), which is a number just less than 1, e.g. 0.95). The discount factor is raised to the power of time (in years) into the future to give the discount rate at that future time: 
# - after 1 year $(0.95)^1=0.95$
# - after 2 years $(0.95)^2=0.90$
# - after 10 years $(0.95)$<sup>10</sup>$=0.60$
# 
# The _return_ is the sum of future utilities, which is taken as the value of that future projection. If these utilies are discounted, their sum is called the _discounted return_. The following code will show an illustration of the effect of temporal discounting on future utilities and the return up to a given number of time steps into the future for a discount factor of $\gamma$ = 0.95.

# In[ ]:


time_steps=300
gamma=0.95
random_seed=1
plot_future_returns(gamma,random_seed)


# In both plots, the blue lines are undiscounted case (i.e. without the effect of temporal discounting) and the orange lines are the discounted case (i.e. including the effect of temporal discounting). 
# 
# The figure on the left shows utility at each time step. In both the undiscounted scenario (blue) and the discounted scenario (orange), projected utilities are variable and uncertain. Notice that in the unsidcounted case, the average size of these utilities stays the same. In contrast, in the discounted case the typical size of utility rapidly decreases to zero, reflecting the effect of temporal discounting (i.e. the devaluation of utilities in the far future). 
# 
# The figure on the right shows changes in return (i.e. the cumulative sum of future utilities) over time. The black dashed line shows the effective time horizon beyond which rewards are ignored in the discounted case for this chosen value of the discount factor, $\gamma$ (this time is set by the natural convention of when the return gets to a fraction ($1-1/e\approx0.64$) of the final value). Beyond the time horizon, the future discounted return (orange) reaches saturation, and no additional utility from further time steps contributes to the overall value. In contrast, in the undiscounted case (blue), all future times are equally important, and the return grows linearly with the maximum time considered for computing utilities. 

# # **Section 2: Damage Functions**

# Now that we have familiarized ourselves with some of the main components of IAMs and the DICE model, we can begin to explore another important component: the **damage function**. The damage function is a central model component that connects climate and socio-economic processes in integrated assessment models.
# 
# Damage functions are the objects in IAMs that dictate how changes in temperature affect production (e.g. through direct weather-related damages). They play a crucial role in determining the model's projections.
# 
# The standard form is a deterministic continuous function that maps changes in temperature, $\Delta T$, to the fraction of productivity that is destroyed by climate change every year, $\Omega$. The standard parametrization is a quadratic dependence 
# $$\Omega=a \times (\Delta T)^2$$
# where $a$ is some small constant (e.g. 0.001) whose value is set by regression of GDP and temperature over geographic and historical variation. Let's plot this function. 

# In[ ]:


fig,ax=pl.subplots()
T = np.linspace(0,4,1000)
a1DICE = 0.00236
a2 = 2.00
for a1 in [a1DICE,1e-2,1e-1]:
    ax.plot(T,a1*(T**a2),label=r'$a_1='+str(a1)+'$' +('(DICE2023)' if a1==a1DICE else ''))
ax.legend(frameon=False)
ax.set_xlabel('temperature change, $\Delta T$')
ax.set_ylabel('fraction productivity destroyed')
ax.set_ylim(0,0.5)


# Observe how larger temperature changes lead to a larger fraction of productivity destroyed due to the damages caused by that temperature. The damage at a given temperature scales linearly with the parameter $a_1$, and exponentially with the parameters $a_2$.

# There are at least two fundamental problems with damage functions (for more see [*The appallingly bad neoclassical economics of climate change* by S. Keen in *Globalizations* (2020)](https://www.tandfonline.com/doi/full/10.1080/14747731.2020.1807856)):
# 1. As mathematical model objects, they are likely too simple to be useful predictors in characterizing climate damages in sufficient complexity. 
# 2. They arise from a poorly validated model-fitting procedure. In particular, it relies on ad hoc functional forms and the relevance of historical and geographical variability to future variability.

# ## **Questions 2**
# 1. Pick an assumption that is made about the relationship between temperature and economic damage in arriving at a conventional damage function (e.g. that it is: _deterministic_, _continuous_, _constant in time_, _functional_ (instead of dynamical), ...) and explain why you think that assumption might be unrealistic for a specific sector of the economy or a specific region of the planet.
# 2. Can you think of a specific way that temperature variation might cause variation in GDP that could have been significant in structuring the historical and/or geographical covariation of the two variables? How about a causal relationship that will not have been significant in historical or geographic variation up to now, but is likely to be significant as temperatures continue to rise and we experience more extreme climates? 

# In[ ]:


# to_remove explanation

"""
1. You can consider a few reasons such as nonlinearity, regional differences, socioeconomic factors, and non-monetary damages. In particular, one could imagine subway systems being minimally affected until the sea level rises to the level of entrances to the subway at which point the subway is completely flooded.
2. Significant in past and future: reduced worker productivity; Significant only in future: Heat-induced crop failures
""";


# Despite these problems highlighting a pressing need to improve how we formulate climate damages, damage functions allow economists within the neoclassical paradigm to start seriously considering the damaging effects of climate change. After a few decades of economists using overly optimistic damage functions that downplayed the damaging effects of climate change, current research on damage functions is striving to incorporate more realism and better estimation.
# 
# For more contemporary damage functions see [van der Wijst et al. *Nat. Clim. Change* (2023)](https://www.nature.com/articles/s41558-023-01636-1). Note that even this modern publication is hindered by the [McNamara Fallacy](https://en.wikipedia.org/wiki/McNamara_fallacy) of leaving out things that are hard to measure. The authors state: "The climate change impacts did not include potential losses originated in ecosystems or in the health sector. This is motivated by the difficulty in addressing the non-market dimension of those impacts with a ‘market-transaction-based’ model such as CGE. Also, catastrophic events were not considered, even though some ‘extremes’ (riverine floods) were included."

# ## **Section 2.1: IAM Model Summary** 
# 
# We've now explored both the utility function and damage function components of IAMs.  Before we move on to actually running the DICE model, let's summarize what we've learned so far about IAMs, specifically regarding the economy and climate models:
# 
# The economy model in most IAMs is a capital accumulation model. 
# - Capital ($K$) combines with a laboring population and technology to generate productivity ($Y$) that is hindered by climate damage. 
# - A savings rate, $S$, drives capital accumulation, while the rest is consumed. Welfare is determined by consumption.
# - Climate action is formulated by a mitigation rate, $\mu$, which along with the savings rate, $S$, are the two exogeneous control parameters in the model and are used to maximize welfare.
# 
# The climate model in DICE interacts with the economy model via the following equation: 
# $$E_\mathrm{ind}=(1-\mu)\sigma Y,$$ 
# - Productivity ($Y$) generates industrial emissions ($E_\mathrm{ind}$), where the $1-\mu$ factor accounts for a reduction of the carbon intensity of production, $\sigma$, via supply-side mitigation measures (e.g. increased efficiency). 
# - The productivity $Y$ rather than output production ($Q$) is used here because damages aren't included. 
# - Damages aren't included because the emissions produced in the process of capital production occur before climate change has a chance to inflict damage on the produced output. 
# - These industrial emissions combine with natural emissions to drive the temperature changes appearing in the damage function, closing the economy-climate loop. 

# ## **Section 2.2: Optimal Planning**
# The goal of the model is to maximize the overall value of a projected future, $V$, within the bounds of mitigation rate, $\mu$, and savings rate, $S$, time courses (while considering constraints on $\mu$ and $S$). This approach is known as **optimal planning**. But why does this "sweet spot" in which overall value is maximized exist? Increasing savings boosts investment and productivity, but higher production leads to higher emissions, resulting in increased temperature and damages that reduce production. Mitigation costs counterbalance this effect, creating a trade-off. As a result, there typically exists a meaningful joint time series of $\mu_t$ and $S_t$ that maximizes $V$. Due to the discount factor $\gamma$, $V$ depends on the future consumption sequence (non-invested production) within a few multiples of the time horizon, approximately $1/(1-\gamma)$ time steps into the future.

# We gone over many variables so far in this tutorial. Here is a list of variables used fore easier reference:
# - $K$ capital
# - $Y$ productivity
# - $S$ savings rate
# - $\mu$ mitigation rate
# - $E$ emissions
# - $\sigma$ carbon intensity of production
# - $Q$ production
# - $\gamma$ discount factor
# - $V$ value
# 
# If you'd like to explore the mathematical equations behind these models in more detail, please refer to the information in the "Further Reading" section for this day.

# # **Section 3: DICE Simulations**
# 

# Now, let's move to the DICE model that gives us some control over our emissions and consumption to see the effect of varying the parameters arising from the above design choices.
# 
# I've forked an existing `Python` implementation of the [DICE2016 model](https://github.com/hazem2410/PyDICE) and refactored it into a class (defined in [`dicelib.py`](https://github.com/mptouzel/PyDICE/blob/master/dicelib.py)) and made a few other changes to make it easier to vary parameters. We'll use that [forked version](https://github.com/mptouzel/PyDICE/) in this tutorial.
# Note that the DICE model was recently updated ([DICE2023](https://www.nber.org/papers/w31112)).
# 
# The model equations are described in a [document](https://github.com/hazem2410/PyDICE/blob/master/PyDICE2016.pdf) associated with the exising `Python` implementation.

# ## **Section 3.1: Case 1 Standard Run**

# Let's run the standard run of the DICE model:

# In[ ]:


dice_std = dicelib.DICE()  #create an instance of the model
dice_std.init_parameters()
dice_std.init_variables()
controls_start_std,controls_bounds_std=dice_std.get_control_bounds_and_startvalue()
dice_std.optimize_controls(controls_start_std,controls_bounds_std);


# Before assessing the results, let's first check that the optimal control solution is within the bounds we set. To do so, let's assess the mitigation rate and savings rate:

# In[ ]:


fig,ax=pl.subplots(1,2)
max_year=2100
TT=dice_std.TT
NT=dice_std.NT
upp,low=zip(*controls_bounds_std[:NT])
ax[0].plot(TT,dice_std.optimal_controls[:NT],label='optimal')
ax[0].plot(TT, upp,'k--',label='bounds')
ax[0].plot(TT,low,'k--')
ax[0].set_ylabel('mitigation rate')
ax[0].set_xlim(2000,max_year)
ax[0].legend(frameon=False)
upp,low=zip(*controls_bounds_std[NT:])
ax[1].plot(TT,dice_std.optimal_controls[NT:])
ax[1].plot(TT,upp,'k--')
ax[1].plot(TT,low,'k--')
ax[1].set_ylabel('savings rate')
ax[1].set_xlabel('year')
ax[1].set_xlim(2000,max_year)

fig.tight_layout()


# ### **Coding Exercise 3.1**
# 1. Please change `max_year` to 2500 in the cell above to see what happens after 2100. What does the mitigation rate do?

# ```python
# fig,ax=pl.subplots(1,2)
# max_year=2500
# TT=dice_std.TT
# NT=dice_std.NT
# upp,low=zip(*controls_bounds_std[:NT])
# ax[0].plot(TT,dice_std.optimal_controls[:NT],label='optimal')
# ax[0].plot(TT, upp,'k--',label='bounds')
# ax[0].plot(TT,low,'k--')
# ax[0].set_ylabel('mitigation rate')
# ax[0].set_xlim(2000,max_year)
# ax[0].legend(frameon=False)
# upp,low=zip(*controls_bounds_std[NT:])
# ax[1].plot(TT,dice_std.optimal_controls[NT:])
# ax[1].plot(TT,upp,'k--')
# ax[1].plot(TT,low,'k--')
# ax[1].set_ylabel('savings rate')
# ax[1].set_xlabel('year')
# ax[1].set_xlim(2000,max_year)
# 
# fig.tight_layout()
# 
# ```

# In[ ]:


# to_remove solution
fig,ax=pl.subplots(1,2)
max_year=2500
TT=dice_std.TT
NT=dice_std.NT
upp,low=zip(*controls_bounds_std[:NT])
ax[0].plot(TT,dice_std.optimal_controls[:NT],label='optimal')
ax[0].plot(TT, upp,'k--',label='bounds')
ax[0].plot(TT,low,'k--')
ax[0].set_ylabel('mitigation rate')
ax[0].set_xlim(2000,max_year)
ax[0].legend(frameon=False)
upp,low=zip(*controls_bounds_std[NT:])
ax[1].plot(TT,dice_std.optimal_controls[NT:])
ax[1].plot(TT,upp,'k--')
ax[1].plot(TT,low,'k--')
ax[1].set_ylabel('savings rate')
ax[1].set_xlabel('year')
ax[1].set_xlim(2000,max_year)

fig.tight_layout()


# In[ ]:


# to_remove explanation

"""
After 2100, the mitigation rate stops increasing and remains constant at a value of 1 until ~2140 at which point there is a rapid increase in mitigation rate followed by an immediate plateau at a value that exceeds 1. This occurs because the model incorporates the effects of negative emission technologies.

""";


# 
# The model incorporates the effects of negative emission technologies by allowing the mitigation rate (via the bounds) to exceed 1 around the year 2140. It is worth noting that the solution explicitly utilizes this feature and would do so even before 2100 if permitted. The decision to include this behavior was made by the modellers who realized that it enabled feasible solutions for the higher forcing SSP scenarios that were previously unattainable.
# 
# At the time, there was a lively debate surrounding this decision, although it was largely in favor of allowing mitigation rates greater than 1. As a result, such rates have become a standard feature in many models for high forcing regimes. However, it is important to acknowledge that there have been arguments against this practice, as discussed in [Anderson & Peters, 2006](https://DOI:10.1126/science.aah45).
# 
# In the final two tutorials, we will explore sociological aspects such as these.
# 
# Now, let's examine the remaining variables of the DICE model:

# In[ ]:


dice_std.roll_out(dice_std.optimal_controls)
dice_std.plot_run('standard run')


# In this plot, the mitigation rate we looked at earlier is now referred to as the "Em rate" (orange line), which closely follows the patter of the carbon price (green line). Similarly, the rate of CO2 emissions (gray line) aligns with the industrial emissions (red line). Cumulative emissions (pink line) reach their peak around 2090, considering that negative emission technologies (NETs) are not employed until 2140.

# ## **Section 3.2: Case 2 Damage Functions**

# The rate at which we increase our mitigation efforts in the standard scenario depends on the projected damage caused by climate change (brown line in the plot above), which is determined by the parameters of the damage function. The question is, how responsive is our response to these parameters?

# ### **Coding Exercise 3.2**
# Change the strength of the nonlinearity in the damage function by changing the exponent from 2 to 3.

# ```python
# for a3 in [2,3]:
#     dice = dicelib.DICE()
#     dice.init_parameters(a3=a3)
#     dice.init_variables()
#     controls_start,controls_bounds=dice.get_control_bounds_and_startvalue()
#     dice.optimize_controls(controls_start,controls_bounds)
#     dice.roll_out(dice.optimal_controls)
#     dice.plot_run('damage function exponent, a3='+str(a3))
# 
# ```

# In[ ]:


# to_remove solution
for a3 in [2,3]:
    dice = dicelib.DICE()
    dice.init_parameters(a3=a3)
    dice.init_variables()
    controls_start,controls_bounds=dice.get_control_bounds_and_startvalue()
    dice.optimize_controls(controls_start,controls_bounds)
    dice.roll_out(dice.optimal_controls)
    dice.plot_run('damage function exponent, a3='+str(a3))


# ### **Questions 3.2**
# 1. What are the main differences between these two projections?

# In[ ]:


# to_remove explanation

"""
1.The carbon price and the mitigation rate reach their peaks much earlier in the second scenario and the industrial emission and damages also reach the low plateau earlier.
""";


# IAMs model climate damages as affecting productivity only in the year in which they occur. What if the negative effects on productivity persist into the future? A persistence time can be added to damages such that damage incurred in one year can continue affecting productivity into following years (c.f. [Schultes et al. *Environ. Res. Lett.* (2021)](https://iopscience.iop.org/article/10.1088/1748-9326/ac27ce/pdf); [Hansel et al. *Nat. Clim. Change* (2020)](https://eprints.lse.ac.uk/105699/1/Climate_economics_support_for_the_UN_climate_targets_2.pdf)). These effects are not negligible, but are absent from current IAMs used by the IPCC.

# ## **Section 3.3: Case 3 Discount Rate**

# The value definition includes exponential temporal discounting (i.e. devaluation of utilities over time) at a rate of r = 1.5% per year so that utility obtained $t$ years into the future is scaled down by $1/(1+r)^t$. What if we set this rate lower so that we don't down scale as quickly (i.e. utilities have more value for longer) and incorporate more in the value definition of what happens in the future when we make decisions?

# ### **Coding Exercise 3.3**
# Change the discount rate from 1.5% to 0.5% (c.f. [Arrow et al. *Science* (2013)](https://www.science.org/doi/10.1126/science.1235665)).

# ```python
# for prstp in [0.015, 0.005]:
#     dice = dicelib.DICE()
#     dice.init_parameters(prstp=prstp)
#     dice.init_variables()
#     controls_start,controls_bounds=dice.get_control_bounds_and_startvalue()
#     dice.optimize_controls(controls_start,controls_bounds)
#     dice.roll_out(dice.optimal_controls)
#     dice.plot_run('discount rate, r='+str(prstp))
# 
# ```

# In[ ]:


# to_remove solution
for prstp in [0.015, 0.005]:
    dice = dicelib.DICE()
    dice.init_parameters(prstp=prstp)
    dice.init_variables()
    controls_start,controls_bounds=dice.get_control_bounds_and_startvalue()
    dice.optimize_controls(controls_start,controls_bounds)
    dice.roll_out(dice.optimal_controls)
    dice.plot_run('discount rate, r='+str(prstp))


# ### **Questions 3.3**
# 1. How are the differences in these two sets of projections consistent with the change in the discount rate? 

# In[ ]:


# to_remove explanation

"""
1. As the discount rate decreases, carbon price, mitigation rate, industrial emissions, and damages reach their peaks sooner.
""";


# ## **Section 3.4: Case 4 the Utility Function**

# These models use an elasticity of consumption when defining the utility function that serves as the basis for the value definition. Recall that elasticity describes the sensitivity of utility to changes in comsumption. Here, the elasticity parameter is the exponent called `elasmu`.

# Let's vary this elasticity exponent:

# In[ ]:


for elasmu in [1.45, 2.0]:
    dice = dicelib.DICE()
    dice.init_parameters(elasmu=elasmu)
    dice.init_variables()
    controls_start,controls_bounds=dice.get_control_bounds_and_startvalue()
    dice.optimize_controls(controls_start,controls_bounds)
    dice.roll_out(dice.optimal_controls)
    dice.plot_run('elasticity exponent, elasmu='+str(elasmu))


# ### **Questions 3.4**
# 1. How are the differences in these two sets of projections consistent with the change in the elasticity? 

# In[ ]:


# to_remove explanation

"""
As the elasticity exponent increase, we also observe an increased and slightly delayed peak value of damages and industrial emissions, while the emission rate and carbon price decrease.
""";


# # **Summary**
# In this tutorial, you've gained a foundational understanding of the DICE model, a basic Integrated Assessment Model in climate economics. You've learned how utility and welfare functions quantify societal satisfaction and balance the needs of different groups and near and far futures. You now understand the role of damage functions in relating climatic changes to economic impacts, giving you insight into the economic implications of climate change. Lastly, you've explored how the DICE model navigates the challenges of economic growth and climate mitigation through optimal planning. These insights equip you to participate more effectively in dialogues and decisions about our climate future.

# # **Resources**
# 
# The Python implementation of DICE used in this tutorial can be accessed [here](https://github.com/mptouzel/PyDICE/).
# 
