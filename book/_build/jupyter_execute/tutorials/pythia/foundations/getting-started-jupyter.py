#!/usr/bin/env python
# coding: utf-8

# <img src="https://jupyter.org/assets/homepage/main-logo.svg" width="200px"></img>

# # Getting Started with Jupyter

# ---

# ## Overview
# Project Jupyter is a project and community whose goal is to "develop open-source software, open-standards, and services for interactive computing across dozens of programming languages". Jupyter consists of four main components: Jupyter Notebooks, Jupyter Kernels, Jupyter Lab, and Jupyter Hub. Jupyter can be executed locally and remotely.
# 
# 1. Jupyter Notebooks
# 2. Jupyter Kernels
# 3. Jupyter Lab
# 4. Jupyter Hub
# 5. Executing Jupyter

# ## Prerequisites
# 
# | Concepts | Importance | Notes |
# | --- | --- | --- |
# | [Installing and Running Python: Python in Jupyter](jupyter) | Helpful | |
# 
# - **Time to learn**: 10 minutes

# ---

# ## Jupyter Notebooks
# 
# The Jupyter Notebook software is an open-source web application that allows you to create and share Jupyter Notebooks (*.ipynb files). Jupyter Notebooks contain executable code, LaTeX equations, visualizations (e.g., plots, pictures), and narrative text. The code does not have to just be Python, other languages such as Julia or R are supported as well. 
# 
# Jupyter Notebooks are celebrated for their interactive output that allows movement between code, code output, explanations, and more code - similar to how scientists think and solve problems. Jupyter Notebooks can be thought of as a living, runnable publication and make for a great presentation platform.

# ## Jupyter Kernels
# Software engines and their environments (e.g., conda environments) that execute the code contained in Jupyter Notebooks.

# ## Jupyter Lab
# 
# A popular web application on which users can create and write their Jupyter Notebooks, as well as explore data, install software, etc.
# 
# You can find more information on running Jupyter Lab [here](jupyterlab).

# ## Jupyter Hub
# A web-based platform that authenticates users and launches Jupyter Lab applications for users on remote systems.

# ## Executing Jupyter

# ### Local Execution Model
# 
# You can launch JupyterLab from a terminal; it will open up in a web browser. The application will then be running in that web browser. When you open a notebook, Jupyter opens a kernel which can be tied to a specific coding language.
# 
# To launch the JupyterLab interface in your browser, follow the instructions in [Installing and Running Python: Python in Jupyter](https://foundations.projectpythia.org/foundations/jupyter.html).
# 
# ![Local Execution Model](../images/local-execution-model.gif)

# ### Remote Execution Model
# 
# In the remote execution model, you start out in the browser, then navigate to a specific URL that points to a JupyterHub. On JupyterHub, you authenticate on the remote system, and then JupyterLab is launched and redirected back to your browser. The interface appears the same as if you were running Jupyter locally.
# 
# ![Remote Execution Model](../images/remote-execution-model.gif)

# ---

# ## Summary
# 
# Jupyter consists of four main components:
# - Jupyter Notebooks (the "*.ipynb" files),
# - Jupyter Kernels (the work environment),
# - Jupyter Lab (a popular web application and interface for local execution),
# - and Jupyter Hub (an application and launcher for remote execution).
# 
# ### What's next?
# 
# - [JupyterLab](jupyterlab)

# ## Resources and references
# 
# - [Jupyter Documentation](https://jupyter.org/)
# - [Xdev Python Tutorial Seminar Series - Jupyter Notebooks](https://youtu.be/xSzXvwzFsDU)

# 
# ```{toctree}
# :hidden:
# :titlesonly:
# 
# 
# jupyterlab
# markdown
# ```
# 
