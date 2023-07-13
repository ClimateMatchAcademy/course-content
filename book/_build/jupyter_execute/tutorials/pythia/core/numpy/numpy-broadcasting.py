#!/usr/bin/env python
# coding: utf-8

# <img src=https://github.com/numpy/numpy/raw/main/branding/logo/primary/numpylogo.svg width=250 alt="NumPy Logo"></img>
# # NumPy Broadcasting
# ---

# ## Overview
# Before we begin, it is important to know that broadcasting is a valuable part of the power that NumPy provides. However, there's no looking past the fact that broadcasting can be conceptually difficult to digest. This information can be helpful and very powerful, but it may be more prudent to first start learning the other label-based elements of the Python ecosystem, [Pandas](../pandas) and [Xarray](../xarray).  This can make understanding NumPy broadcasting easier or simpler when using real-world data. When you are ready to learn about NumPy broadcasting, this section is organized as follows:
# 
# 1. An introduction to broadcasting
# 1. Avoiding loops with vectorization

# ## Prerequisites
# 
# | Concepts | Importance | Notes |
# | --- | --- | --- |
# | [NumPy Basics](numpy-basics) | Necessary | |
# | [Intermediate NumPy](intermediate-numpy) | Helpful | |
# | [Conceptual guide to broadcasting](https://numpy.org/doc/stable/user/theory.broadcasting.html#array-broadcasting-in-numpy) | Helpful | |
# 
# * **Time to learn**: 30 minutes
# ---

# ## Imports
# 
# As always, when working with NumPy, it must be imported first:

# In[ ]:


import numpy as np


# ## Using broadcasting to implicitly loop over data

# ### What is broadcasting?
# Broadcasting is a useful NumPy tool that allows us to perform operations between arrays with different shapes, provided that they are compatible with each other in certain ways. To start, we can create an array below and add 5 to it:

# In[ ]:


a = np.array([10, 20, 30, 40])
a + 5


# This works even though 5 is not an array. It behaves as expected, adding 5 to each of the elements in `a`. This also works if 5 is an array:

# In[ ]:


b = np.array([5])
a + b


# This takes the single element in `b` and adds it to each of the elements in `a`. This won't work for just any `b`, though; for instance, the following won't work:

# In[ ]:


b = np.array([5, 6, 7])
a + b


# It does work if `a` and `b` are the same shape:

# In[ ]:


b = np.array([5, 5, 10, 10])
a + b


# What if what we really want is pairwise addition of a and b? Without broadcasting, we could accomplish this by looping:

# In[ ]:


b = np.array([1, 2, 3, 4, 5])


# In[ ]:


result = np.empty((5, 4), dtype=np.int32)
for row, valb in enumerate(b):
    for col, vala in enumerate(a):
        result[row, col] = vala + valb
result


# We can also do this by manually repeating the arrays to the proper shape for the result, using `np.tile`. This avoids the need to manually loop:

# In[ ]:


aa = np.tile(a, (5, 1))
aa


# In[ ]:


# Turn b into a column array, then tile it
bb = np.tile(b.reshape(5, 1), (1, 4))
bb


# In[ ]:


aa + bb


# ### Giving NumPy room for broadcasting
# We can also do this using broadcasting, which is where NumPy implicitly repeats the array without using additional memory. With broadcasting, NumPy takes care of repeating for you, provided dimensions are "compatible". This works as follows:
# 1. Check the number of dimensions of the arrays. If they are different, *prepend* dimensions of size one until the arrays are the same dimension shape.
# 2. Check if each of the dimensions are compatible. This works as follows:
#   - Each dimension is checked.
#   - If one of the arrays has a size of 1 in the checked dimension, or both arrays have the same size in the checked dimension, the check passes.
#   - If all dimension checks pass, the dimensions are compatible.
# 
# For example, consider the following arrays:

# In[ ]:


a.shape


# In[ ]:


b.shape


# Right now, these arrays both have the same number of dimensions.  They both have only one dimension, but that dimension is incompatible.  We can solve this by appending a dimension using `np.newaxis` when indexing, like this:

# In[ ]:


bb = b[:, np.newaxis]
bb.shape


# In[ ]:


a + bb


# In[ ]:


(a + bb).shape


# We can also make the code more succinct by performing the newaxis and addition operations in a single line, like this:

# In[ ]:


a + b[:, np.newaxis]


# ### Extending to higher dimensions
# The same broadcasting ability and rules also apply for arrays of higher dimensions. Consider the following arrays `x`, `y`, and `z`, which are all different dimensions. We can use newaxis and broadcasting to perform $x^2 + y^2 + z^2$:

# In[ ]:


x = np.array([1, 2])
y = np.array([3, 4, 5])
z = np.array([6, 7, 8, 9])


# First, we extend the `x` array using newaxis, and then square it.  Then, we square `y`, and broadcast it onto the extended `x` array:

# In[ ]:


d_2d = x[:, np.newaxis] ** 2 + y**2


# In[ ]:


d_2d.shape


# Finally, we further extend this new 2-D array to a 3-D array using newaxis, square the `z` array, and then broadcast `z` onto the newly extended array:

# In[ ]:


d_3d = d_2d[..., np.newaxis] + z**2


# In[ ]:


d_3d.shape


# As described above, we can also perform these operations in a single line of code, like this:

# In[ ]:


h = x[:, np.newaxis, np.newaxis] ** 2 + y[np.newaxis, :, np.newaxis] ** 2 + z**2


# We can use the shape method to see the shape of the array created by the single line of code above.  As you can see, it matches the shape of the array created by the multi-line process above:

# In[ ]:


h.shape


# We can also use the all method to confirm that both arrays contain the same data:

# In[ ]:


np.all(h == d_3d)


# Broadcasting is often useful when you want to do calculations with coordinate values, which are often given as 1-D arrays corresponding to positions along a particular array dimension. For example, we can use broadcasting to help with taking range and azimuth values for radar data (1-D separable polar coordinates) and converting to x,y pairs relative to the radar location.

# Given the 3-D temperature field and 1-D pressure coordinates below, let's calculate $T * exp(P / 1000)$. We will need to use broadcasting to make the arrays compatible.  The following code demonstrates how to use newaxis and broadcasting to perform this calculation:

# In[ ]:


pressure = np.array([1000, 850, 500, 300])
temps = np.linspace(20, 30, 24).reshape(4, 3, 2)
pressure.shape, temps.shape


# In[ ]:


pressure[:, np.newaxis, np.newaxis].shape


# In[ ]:


temps * np.exp(pressure[:, np.newaxis, np.newaxis] / 1000)


# ## Vectorize calculations to avoid explicit loops

# When working with arrays of data, loops over the individual array elements is a fact of life. However, for improved runtime performance, it is important to avoid performing these loops in Python as much as possible, and let NumPy handle the looping for you. Avoiding these loops frequently, but not always, results in shorter and clearer code as well.

# ### Look ahead/behind
# 
# One common pattern for vectorizing is in converting loops that work over the current point, in addition to the previous point and/or the next point. This comes up when doing finite-difference calculations, e.g., approximating derivatives:
# 
# \begin{equation*}
# f'(x) = f_{i+1} - f_{i}
# \end{equation*}

# In[ ]:


a = np.linspace(0, 20, 6)
a


# We can calculate the forward difference for this array using a manual loop, like this:

# In[ ]:


d = np.zeros(a.size - 1)
for i in range(len(a) - 1):
    d[i] = a[i + 1] - a[i]
d


# It would be nice to express this calculation without a loop, if possible. To see how to go about this, let's consider the values that are involved in calculating `d[i]`; in other words, the values `a[i+1]` and `a[i]`. The values over the loop iterations are:
# 
# |  i  | a[i+1] | a[i] |
# | --- |  ----  | ---- |
# |  0  |    4   |   0  |
# |  1  |    8   |   4  |
# |  2  |   12   |   8  |
# |  3  |   16   |  12  |
# |  4  |   20   |  16  |
# 
# We can then express the series of values for `a[i+1]` as follows:

# In[ ]:


a[1:]


# We can also express the series of values for `a[i]` as follows:

# In[ ]:


a[:-1]


# This means that we can express the forward difference using the following statement:

# In[ ]:


a[1:] - a[:-1]


# It should be noted that using slices in this way returns only a **view** on the original array. In other words, you can use the slices to modify the original data, either intentionally or accidentally.  Also, this is a quick operation that does not involve a copy and does not bloat memory usage.

# #### 2nd Derivative
#     
# A finite-difference estimate of the 2nd derivative is given by the following equation (ignoring $\Delta x$):
# 
# \begin{equation*}
# f''(x) = 2
# f_i - f_{i+1} - f_{i-1}
# \end{equation*}
# 
# Let's write some vectorized code to calculate this finite difference for `a`, using slices.  Analyze the code below, and compare the result to the values you would expect to see from the 2nd derivative of `a`.

# In[ ]:


2 * a[1:-1] - a[:-2] - a[2:]


# ### Blocking
# 
# Another application that can become more efficient using vectorization is operating on blocks of data. Let's start by creating some temperature data (rounding to make it easier to see and recognize the values):

# In[ ]:


temps = np.round(20 + np.random.randn(10) * 5, 1)
temps


# Let's start by writing a loop to take a 3-point running mean of the data. We'll do this by iterating over all points in the array and averaging the 3 points centered on each point. We'll simplify the problem by avoiding dealing with the cases at the edges of the array:

# In[ ]:


avg = np.zeros_like(temps)
for i in range(1, len(temps) - 1):
    sub = temps[i - 1 : i + 2]
    avg[i] = sub.mean()


# In[ ]:


avg


# As with the case of doing finite differences, we can express this using slices of the original array instead of loops:

# In[ ]:


# i - 1            i          i + 1
(temps[:-2] + temps[1:-1] + temps[2:]) / 3


# Another option to solve this type of problem is to use the powerful NumPy tool `as_strided` instead of slicing. This tool can result in some odd behavior, so take care when using it.  However, the trade-off is that the `as_strided` tool can be used to perform powerful operations. What we're doing here is altering how NumPy is interpreting the values in the memory that underpins the array. Take this array, for example:

# In[ ]:


temps


# Using `as_strided`, we can create a view of this array with a new, bigger shape, with rows made up of overlapping values. We do this by specifying a new shape of 8x3.  There are 3 columns, for fitting blocks of data containing 3 values each, and 8 rows, to correspond to the 8 blocks of data of that size that are possible in the original 1-D array. We can then use the `strides` argument to control how NumPy walks between items in each dimension. The last item in the strides tuple simply states that the number of bytes to walk between items is just the size of an item. (Increasing this last item would skip items.) The first item says that when we go to a new element (in this example, a new row), only advance the size of a single item. This is what gives us overlapping rows. The code for these operations looks like this:

# In[ ]:


block_size = 3
new_shape = (len(temps) - block_size + 1, block_size)
bytes_per_item = temps.dtype.itemsize
temps_strided = np.lib.stride_tricks.as_strided(
    temps, shape=new_shape, strides=(bytes_per_item, bytes_per_item)
)
temps_strided


# Now that we have this view of the array with the rows representing overlapping blocks, we can operate across the rows with `mean` and the `axis=-1` argument to get our running average:

# In[ ]:


temps_strided.mean(axis=-1)


# It should be noted that there are no copies going on here, so if we change a value at a single indexed location, the change actually shows up in multiple locations:

# In[ ]:


temps_strided[0, 2] = 2000
temps_strided


# ### Finding the difference between min and max
# 
# Another operation that crops up when slicing and dicing data is trying to identify a set of indices along a particular axis, contained within a larger multidimensional array. For instance, say we have a 3-D array of temperatures, and we want to identify the location of the $-10^oC$ isotherm within each column:

# In[ ]:


pressure = np.linspace(1000, 100, 25)
temps = np.random.randn(25, 30, 40) * 3 + np.linspace(25, -100, 25).reshape(-1, 1, 1)


# NumPy has the function `argmin()`, which returns the index of the minimum value. We can use this to find the minimum absolute difference between the value and -10:

# In[ ]:


# Using axis=0 to tell it to operate along the pressure dimension
inds = np.argmin(np.abs(temps - -10), axis=0)
inds


# In[ ]:


inds.shape


# Great! We now have an array representing the index of the point closest to $-10^oC$ in each column of data. We can use this new array as a lookup index for our pressure coordinate array to find the pressure level for each column:

# In[ ]:


pressure[inds]


# Now, we can try to find the closest actual temperature value using the new array:

# In[ ]:


temps[inds, :, :].shape


# Unfortunately, this replaced the pressure dimension (size 25) with the shape of our index array (30 x 40), giving us a 30 x 40 x 30 x 40 array.  Obviously, if scientifically relevant data values were being used, this result would almost certainly make such data invalid. One solution would be to set up a loop with the `ndenumerate` function, like this:

# In[ ]:


output = np.empty(inds.shape, dtype=temps.dtype)
for (i, j), val in np.ndenumerate(inds):
    output[i, j] = temps[val, i, j]
output


# Of course, what we really want to do is avoid the explicit loop. Let's temporarily simplify the problem to a single dimension. If we have a 1-D array, we can pass a 1-D array of indices (a full range), and get back the same as the original data array:

# In[ ]:


pressure[np.arange(pressure.size)]


# In[ ]:


np.all(pressure[np.arange(pressure.size)] == pressure)


# We can use this to select all the indices on the other dimensions of our temperature array. We will also need to use the magic of broadcasting to combine arrays of indices across dimensions.

# This can be written as a vectorized solution.  For example:

# In[ ]:


y_inds = np.arange(temps.shape[1])[:, np.newaxis]
x_inds = np.arange(temps.shape[2])
temps[inds, y_inds, x_inds]


# Now, we can use this new array to find, for example, the relative humidity at the $-10^oC$ isotherm:

# In[ ]:


np.all(output == temps[inds, y_inds, x_inds])


# ---

# ## Summary
# We've previewed some advanced NumPy capabilities, with a focus on _vectorization_; in other words, using clever broadcasting and data windowing techniques to enhance the speed and readability of our calculation code. By making use of vectorization, you can reduce explicit construction of loops in your code, and improve speed of calculation throughout the execution of such code.
# 
# ### What's next
# This is an advanced NumPy topic; however, it is important to learn this topic in order to design calculation code that maximizes scalability and speed. If you would like to explore this topic further, please review the links below. We also suggest diving into label-based indexing and subsetting with [Pandas](../pandas) and [Xarray](../xarray), where some of this broadcasting can be simplified, or have added context.

# ## Resources and references
# * [NumPy Broadcasting Documentation](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)
