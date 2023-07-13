#!/usr/bin/env python
# coding: utf-8

# <img src=https://github.com/numpy/numpy/raw/main/branding/logo/primary/numpylogo.svg width=250 alt="NumPy Logo"></img>
# # NumPy Basics
# ---

# ## Overview
# NumPy is the fundamental package for scientific computing with Python. It contains among other things:
# 
# - a powerful N-dimensional array object
# - sophisticated (broadcasting) functions
# - useful linear algebra, Fourier transform, and random number capabilities
# 
# The NumPy array object is the common interface for working with typed arrays of data across a wide-variety of scientific Python packages. NumPy also features a C-API, which enables interfacing existing Fortran/C/C++ libraries with Python and NumPy. In this notebook we will cover
# 
# 1. Creating an `array`
# 1. Math and calculations with arrays
# 1. Inspecting an array with slicing and indexing

# ## Prerequisites
# 
# | Concepts | Importance | Notes |
# | --- | --- | --- |
# | [Python Quickstart](../../foundations/quickstart) | Necessary | Lists, indexing, slicing, math |
# 
# * **Time to learn**: 35 minutes
# ---

# ## Imports
# A common convention you might encounter is to rename `numpy` to `np` on import to shorten it for the many times we will be calling on `numpy` for functionality.

# In[ ]:


import numpy as np


# ## Create an array of 'data'
# 
# The NumPy array represents a *contiguous* block of memory, holding entries of a given type (and hence fixed size). The entries are laid out in memory according to the shape, or list of dimension sizes. Let's start by creating an array from a list of integers and taking a look at it,

# In[ ]:


a = np.array([1, 2, 3])
a


# We can inspect the number of dimensions our array is organized along with `ndim`, and how long each of these dimensions are with `shape`

# In[ ]:


a.ndim


# In[ ]:


a.shape


# So our 1-dimensional array has a shape of `3` along that dimension! Finally we can check out the underlying type of our underlying data,

# In[ ]:


a.dtype


# Now, let's expand this with a new data type, and by using a list of lists we can grow the dimensions of our array!

# In[ ]:


a = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
a


# In[ ]:


a.ndim


# In[ ]:


a.shape


# In[ ]:


a.dtype


# And as before we can use `ndim`, `shape`, and `dtype` to discover how many dimensions of what lengths are making up our array of floats.

# ### Generation
# NumPy also provides helper functions for generating arrays of data to save you typing for regularly spaced data. Don't forget your Python indexing rules!
# 
# * `arange(start, stop, step)` creates a range of values in the interval `[start,stop)` with `step` spacing.
# * `linspace(start, stop, num)` creates a range of `num` evenly spaced values over the range `[start,stop]`.

# #### arange

# In[ ]:


a = np.arange(5)
a


# In[ ]:


a = np.arange(3, 11)
a


# In[ ]:


a = np.arange(1, 10, 2)
a


# #### linspace

# In[ ]:


b = np.linspace(0, 4, 5)
b


# In[ ]:


b.shape


# In[ ]:


b = np.linspace(3, 10, 15)
b


# In[ ]:


b = np.linspace(2.5, 10.25, 11)
b


# In[ ]:


b = np.linspace(0, 100, 30)
b


# ## Perform calculations with NumPy
# 
# ### Arithmetic
# 
# In core Python, that is *without* NumPy, creating sequences of values and adding them together requires writing a lot of manual loops, just like one would do in C/C++:

# In[ ]:


a = list(range(5, 10))
b = [3 + i * 1.5 / 4 for i in range(5)]

a, b


# In[ ]:


result = []
for x, y in zip(a, b):
    result.append(x + y)
print(result)


# That is very verbose and not very intuitive. Using NumPy this becomes:

# In[ ]:


a = np.arange(5, 10)
b = np.linspace(3, 4.5, 5)


# In[ ]:


a + b


# Many major mathematical operations operate in the same way. They perform an element-by-element calculation of the two arrays.

# In[ ]:


a - b


# In[ ]:


a / b


# In[ ]:


a**b


# <div class="admonition alert alert-warning">
#     <p class="admonition-title" style="font-weight:bold">Warning</p>
#     These arrays must be the same shape!
# </div>

# In[ ]:


b = np.linspace(3, 4.5, 6)
a.shape, b.shape


# In[ ]:


a * b


# ### Constants
# 
# NumPy provides us access to some useful constants as well - remember you should never be typing these in manually! Other libraries such as SciPy and MetPy have their own set of constants that are more domain specific.

# In[ ]:


np.pi


# In[ ]:


np.e


# You can use these for classic calculations you might be familiar with! Here we can create a range `t = [0, 2 pi]` by `pi/4`,

# In[ ]:


t = np.arange(0, 2 * np.pi + np.pi / 4, np.pi / 4)
t


# In[ ]:


t / np.pi


# ### Array math functions
# 
# NumPy also has math functions that can operate on arrays. Similar to the math operations, these greatly simplify and speed up these operations. Let's start with calculating $\sin(t)$!

# In[ ]:


sin_t = np.sin(t)
sin_t


# and clean it up a bit by `round`ing to three decimal places.

# In[ ]:


np.round(sin_t, 3)


# In[ ]:


cos_t = np.cos(t)
cos_t


# <div class="admonition alert alert-info">
#     <p class="admonition-title" style="font-weight:bold">Info</p>
#     Check out NumPy's list of mathematical functions <a href=https://numpy.org/doc/stable/reference/routines.math.html>here</a>!
# </div>

# We can convert between degrees and radians with only NumPy, by hand

# In[ ]:


t / np.pi * 180


# or with built-in function `rad2deg`,

# In[ ]:


degrees = np.rad2deg(t)
degrees


# We are similarly provided algorithms for operations including integration, bulk summing, and cumulative summing.

# In[ ]:


sine_integral = np.trapz(sin_t, t)
np.round(sine_integral, 3)


# In[ ]:


cos_sum = np.sum(cos_t)
cos_sum


# In[ ]:


cos_csum = np.cumsum(cos_t)
print(cos_csum)


# ## Indexing and subsetting arrays
# 
# ### Indexing
# 
# We can use integer indexing to reach into our arrays and pull out individual elements. Let's make a toy 2-d array to explore. Here we create a 12-value `arange` and `reshape` it into a 3x4 array.

# In[ ]:


a = np.arange(12).reshape(3, 4)
a


# Recall that Python indexing starts at `0`, and we can begin indexing our array with the list-style `list[element]` notation,

# In[ ]:


a[0]


# to pull out just our first _row_ of data within `a`. Similarly we can index in reverse with negative indices,

# In[ ]:


a[-1]


# to pull out just the last row of data within `a`. This notation extends to as many dimensions as make up our array as `array[m, n, p, ...]`. The following diagram shows these indices for an example, 2-dimensional `6x6` array,

# ![](array_index.png)

# For example, let's find the entry in our array corresponding to the 2nd row (`m=1` in Python) and the 3rd column (`n=2` in Python)

# In[ ]:


a[1, 2]


# We can again use these negative indices to index backwards,

# In[ ]:


a[-1, -1]


# and even mix-and-match along dimensions,

# In[ ]:


a[1, -2]


# ### Slices
# 
# Slicing syntax is written as `array[start:stop[:step]]`, where **all numbers are optional**.
# - defaults: 
#   - start = 0
#   - stop = len(dim)
#   - step = 1
# - The second colon is **also optional** if no step is used.
# 
# Let's pull out just the first row, `m=0` of `a` and see how this works!

# In[ ]:


b = a[0]
b


# Laying out our default slice to see the entire array explicitly looks something like this,

# In[ ]:


b[0:4:1]


# where again, these default values are optional,

# In[ ]:


b[::]


# and even the second `:` is optional

# In[ ]:


b[:]


# Now to actually make our own slice, let's select all elements from `m=0` to `m=2`

# In[ ]:


b[0:2]


# <div class="admonition alert alert-warning">
#     <p class="admonition-title" style="font-weight:bold">Warning</p>
#     Slice notation is <b>exclusive</b> of the final index.
# </div>

# This means that slices will include every value **up to** your `stop` index and not this index itself, like a half-open interval `[start, end)`. For example,

# In[ ]:


b[3]


# reveals a different value than

# In[ ]:


b[0:3]


# Finally, a few more examples of this notation before reintroducing our 2-d array `a`.

# In[ ]:


b[2:]  # m=2 through the end, can leave off the number


# In[ ]:


b[:3]  # similarly, the same as our b[0:3]


# ### Multidimensional slicing
# This entire syntax can be extended to each dimension of multidimensional arrays.

# In[ ]:


a


# First let's pull out rows `0` through `2`, and then every `:` column for each of those

# In[ ]:


a[0:2, :]


# Similarly, let's get all rows for just column `2`,

# In[ ]:


a[:, 2]


# or just take a look at the full row `:`, for every second column, `::2`,

# In[ ]:


a[:, ::2]


# For any shape of array, you can use `...` to capture full slices of every non-specified dimension. Consider the 3-D array,

# In[ ]:


c = a.reshape(2, 2, 3)
c


# In[ ]:


c[0, ...]


# and so this is equivalent to

# In[ ]:


c[0, :, :]


# for extracting every dimension across our first row. We can also flip this around,

# In[ ]:


c[..., -1]


# to investigate every preceding dimension along our the last entry of our last axis, the same as `c[:, :, -1]`.

# ---

# ## Summary
# In this notebook we introduced NumPy and the `ndarray` that is so crucial to the entirety of the scientific Python community ecosystem. We created some arrays, used some of NumPy's own mathematical functions to manipulate them, and then introduced the world of NumPy indexing and selecting for even multi-dimensional arrays.
# 
# ### What's next?
# This notebook is the gateway to nearly every other Pythia resource here. This information is crucial for understanding SciPy, pandas, xarray, and more. Continue into NumPy to explore some more intermediate and advanced topics!

# ## Resources and references
# - [NumPy User Guide](http://docs.scipy.org/doc/numpy/user/)
# - [SciPy Lecture Notes](https://scipy-lectures.org/)
