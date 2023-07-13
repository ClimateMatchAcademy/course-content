#!/usr/bin/env python
# coding: utf-8

# <img src=https://github.com/numpy/numpy/raw/main/branding/logo/primary/numpylogo.svg width=250 alt="NumPy Logo"></img>
# # Intermediate NumPy
# ---

# ## Overview
# 1. Working with multiple dimensions
# 1. Subsetting of irregular arrays with booleans
# 1. Sorting, or indexing with indices

# ## Prerequisites
# 
# | Concepts | Importance | Notes |
# | --- | --- | --- |
# | [NumPy Basics](numpy-basics) | Necessary | |
# 
# * **Time to learn**: 20 minutes
# ---

# ## Imports
# We will be including [Matplotlib](../matplotlib) to illustrate some of our examples, but you don't need knowledge of it to complete this notebook.

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np


# ## Using axes to slice arrays
# 
# Here we introduce an important concept when working with NumPy: the axis. This indicates the particular dimension along which a function should operate (provided the function does something taking multiple values and converts to a single value). 
# 
# Let's look at a concrete example with `sum`:

# In[ ]:


a = np.arange(12).reshape(3, 4)
a


# This calculates the total of all values in the array.

# In[ ]:


np.sum(a)


# <div class="admonition alert alert-info">
#     <p class="title" style="font-weight:bold">Info</p>
#     Some of NumPy's functions can be accessed as `ndarray` methods!
# </div>

# In[ ]:


a.sum()


# Now, with a reminder about how our array is shaped,

# In[ ]:


a.shape


# we can specify `axis` to get _just_ the sum across each of our rows.

# In[ ]:


np.sum(a, axis=0)


# Or do the same and take the sum across columns:

# In[ ]:


np.sum(a, axis=1)


# After putting together some data and introducing some more advanced calculations, let's demonstrate a multi-layered example: calculating temperature advection. If you're not familiar with this (don't worry!), we'll be looking to calculate
# 
# \begin{equation*}
# \text{advection} = -\vec{v} \cdot \nabla T
# \end{equation*}
# 
# and to do so we'll start with some random $T$ and $\vec{v}$ values,

# In[ ]:


temp = np.random.randn(100, 50)
u = np.random.randn(100, 50)
v = np.random.randn(100, 50)


# We can calculate the `np.gradient` of our new $T(100x50)$ field as two separate component gradients,

# In[ ]:


gradient_x, gradient_y = np.gradient(temp)


# In order to calculate $-\vec{v} \cdot \nabla T$, we will use `np.dstack` to turn our two separate component gradient fields into one multidimensional field containing $x$ and $y$ gradients at each of our $100x50$ points,

# In[ ]:


grad_vectors = np.dstack([gradient_x, gradient_y])
print(grad_vectors.shape)


# and then do the same for our separate $u$ and $v$ wind components,

# In[ ]:


wind_vectors = np.dstack([u, v])
print(wind_vectors.shape)


# Finally, we can calculate the dot product of these two multidimensional fields of wind and temperature gradient components by hand as an element-wise multiplication, `*`, and then a `sum` of our separate components at each point (i.e., along the last `axis`),

# In[ ]:


advection = (wind_vectors * -grad_vectors).sum(axis=-1)
print(advection.shape)


# ## Indexing arrays with boolean values
# 
# ### Array comparisons
# NumPy can easily create arrays of boolean values and use those to select certain values to extract from an array

# In[ ]:


# Create some synthetic data representing temperature and wind speed data
np.random.seed(19990503)  # Make sure we all have the same data
temp = 20 * np.cos(np.linspace(0, 2 * np.pi, 100)) + 50 + 2 * np.random.randn(100)
speed = np.abs(
    10 * np.sin(np.linspace(0, 2 * np.pi, 100)) + 10 + 5 * np.random.randn(100)
)


# In[ ]:


plt.plot(temp, 'tab:red')
plt.plot(speed, 'tab:blue');


# By doing a comparison between a NumPy array and a value, we get an
# array of values representing the results of the comparison between
# each element and the value

# In[ ]:


temp > 45


# This, which is its own NumPy array of `boolean` values, can be used as an index to another array of the same size. We can even use it as an index within the original `temp` array we used to compare,

# In[ ]:


temp[temp > 45]


# <div class="admonition alert alert-info">
#     <p class="admonition-title" style="font-weight:bold">Info</p>
#     This only returns the values from our original array meeting the indexing conditions, nothing more! Note the size,
# </div>

# In[ ]:


temp[temp > 45].shape


# <div class="admonition alert alert-warning">
#     <p class="admonition-title" style="font-weight:bold">Warning</p>
#     Indexing arrays with arrays requires them to be the same size!
# </div>

# If we store this array somewhere new,

# In[ ]:


temp_45 = temp[temp > 45]


# In[ ]:


temp_45[temp < 45]


# We find that our original `(100,)` shape array is too large to subset our new `(60,)` array.

# If their sizes _do_ match, the boolean array can come from a totally different array!

# In[ ]:


speed > 10


# In[ ]:


temp[speed > 10]


# ### Replacing values
# To extend this, we can use this conditional indexing to _assign_ new values to certain positions within our array, somewhat like a masking operation.

# In[ ]:


# Make a copy so we don't modify the original data
temp2 = temp.copy()
speed2 = speed.copy()

# Replace all places where speed is <10 with NaN (not a number)
temp2[speed < 10] = np.nan
speed2[speed < 10] = np.nan


# In[ ]:


plt.plot(temp2, 'tab:red');


# and to put this in context,

# In[ ]:


plt.plot(temp, 'r:')
plt.plot(temp2, 'r')
plt.plot(speed, 'b:')
plt.plot(speed2, 'b');


# If we use parentheses to preserve the order of operations, we can combine these conditions with other bitwise operators like the `&` for `bitwise_and`,

# In[ ]:


multi_mask = (temp < 45) & (speed > 10)
multi_mask


# In[ ]:


temp[multi_mask]


# Heat index is only defined for temperatures >= 80F and relative humidity values >= 40%. Using the data generated below, we can use boolean indexing to extract the data where heat index has a valid value.

# In[ ]:


# Here's the "data"
np.random.seed(19990503)
temp = 20 * np.cos(np.linspace(0, 2 * np.pi, 100)) + 80 + 2 * np.random.randn(100)
relative_humidity = np.abs(
    20 * np.cos(np.linspace(0, 4 * np.pi, 100)) + 50 + 5 * np.random.randn(100)
)

# Create a mask for the two conditions described above
good_heat_index = (temp >= 80) & (relative_humidity >= 0.4)

# Use this mask to grab the temperature and relative humidity values that together
# will give good heat index values
print(temp[good_heat_index])


# Another bitwise operator we can find helpful is Python's `~` complement operator, which can give us the **inverse** of our specific mask to let us assign `np.nan` to every value _not_ satisfied in `good_heat_index`.

# In[ ]:


plot_temp = temp.copy()
plot_temp[~good_heat_index] = np.nan
plt.plot(plot_temp, 'tab:red');


# ## Indexing using arrays of indices
# 
# You can also use a list or array of indices to extract particular values--this is a natural extension of the regular indexing. For instance, just as we can select the first element:

# In[ ]:


temp[0]


# We can also extract the first, fifth, and tenth elements as a list:

# In[ ]:


temp[[0, 4, 9]]


# One of the ways this comes into play is trying to sort NumPy arrays using `argsort`. This function returns the indices of the array that give the items in sorted order. So for our `temp`,

# In[ ]:


inds = np.argsort(temp)
inds


# i.e., our lowest value is at index `52`, next `57`, and so on. We can use this array of indices as an index for `temp`,

# In[ ]:


temp[inds]


# to get a sorted array back!

# With some clever slicing, we can pull out the last 10, or 10 highest, values of `temp`,

# In[ ]:


ten_highest = inds[-10:]
print(temp[ten_highest])


# There are other NumPy `arg` functions that return indices for operating; check out the [NumPy docs](https://numpy.org/doc/stable/reference/routines.sort.html) on sorting your arrays!

# ---

# ## Summary
# In this notebook we introduced the power of understanding the dimensions of our data by specifying math along `axis`, used `True` and `False` values to subset our data according to conditions, and used lists of positions within our array to sort our data.
# 
# ### What's Next
# Taking some time to practice this is valuable to be able to quickly manipulate arrays of information in useful or scientific ways.

# ## Resources and references
# The [NumPy Users Guide](https://numpy.org/devdocs/user/quickstart.html#less-basic) expands further on some of these topics, as well as suggests various [Tutorials](https://numpy.org/learn/), lectures, and more at this stage.
