#!/usr/bin/env python
# coding: utf-8

# # Quickstart: Zero to Python

# Brand new to Python? Here are some quick examples of what Python code looks like.
# 
# This is **not** meant to be a comprehensive Python tutorial, just something to whet your appetite.

# ## Run this code from your browser!
# 
# Of course you can simply read through these examples, but it's more fun to ***run them yourself***:
# 
# - Find the **"Rocket Ship"** icon, **located near the top-right of this page**. Hover over this icon to see the drop-down menu.
# - Click the `Binder` link from the drop-down menu.
# - This page will open up as a [Jupyter notebook](jupyter.html) in a working Python environment in the cloud.
# - Press <kbd>Shift</kbd>+<kbd>Enter</kbd> to execute each code cell
# - Feel free to make changes and play around!

# ## A very first Python program
# 
# A Python program can be a single line:

# In[ ]:


print("Hello interweb")


# ## Loops in Python

# Let's start by making a `for` loop with some formatted output:

# In[ ]:


for n in range(3):
    print(f"Hello interweb, this is iteration number {n}")


# A few things to note:
# 
# - Python defaults to counting from 0 (like C) rather than from 1 (like Fortran).
# - Function calls in Python always use parentheses: `print()`
# - The colon `:` denotes the beginning of a definition (here of the repeated code under the `for` loop).
# - Code blocks are identified through indentations.
# 
# To emphasize this last point, here is an example with a two-line repeated block:

# In[ ]:


for n in range(3):
    print("Hello interweb!")
    print(f"This is iteration number {n}.")
print('And now we are done.')


# ## Basic flow control
# 
# Like most languages, Python has an `if` statement for logical decisions:

# In[ ]:


if n > 2:
    print("n is greater than 2!")
else:
    print("n is not greater than 2!")


# Python also defines the `True` and `False` logical constants:

# In[ ]:


n > 2


# There's also a `while` statement for conditional looping:

# In[ ]:


m = 0
while m < 3:
    print(f"This is iteration number {m}.")
    m += 1
print(m < 3)


# ## Basic Python data types
# 
# Python is a very flexible language, and many advanced data types are introduced through packages (more on this below). But some of the basic types include: 

# ### Integers (`int`)
# 
# The number `m` above is a good example. We can use the built-in function `type()` to inspect what we've got in memory:

# In[ ]:


print(type(m))


# ### Floating point numbers (`float`)
# 
# Floats can be entered in decimal notation:

# In[ ]:


print(type(0.1))


# or in scientific notation:

# In[ ]:


print(type(4e7))


# where `4e7` is the Pythonic representation of the number $ 4 \times 10^7 $.

# ### Character strings (`str`)
# 
# You can use either single quotes `''` or double quotes `" "` to denote a string:

# In[ ]:


print(type("orange"))


# In[ ]:


print(type('orange'))


# ### Lists
# 
# A list is an ordered container of objects denoted by **square brackets**:

# In[ ]:


mylist = [0, 1, 1, 2, 3, 5, 8]


# Lists are useful for lots of reasons including iteration:

# In[ ]:


for number in mylist:
    print(number)


# Lists do **not** have to contain all identical types:

# In[ ]:


myweirdlist = [0, 1, 1, "apple", 4e7]
for item in myweirdlist:
    print(type(item))


# This list contains a mix of `int` (integer), `float` (floating point number), and `str` (character string).

# Because a list is *ordered*, we can access items by integer index:

# In[ ]:


myweirdlist[3]


# remembering that we start counting from zero!

# Python also allows lists to be created dynamically through *list comprehension* like this:

# In[ ]:


squares = [i**2 for i in range(11)]
squares


# ### Dictionaries (`dict`)
# 
# A dictionary is a collection of *labeled objects*. Python uses curly braces `{}` to create dictionaries:

# In[ ]:


mypet = {
    "name": "Fluffy",
    "species": "cat",
    "age": 4,
}
type(mypet)


# We can then access items in the dictionary by label using square brackets:

# In[ ]:


mypet["species"]


# We can iterate through the keys (or labels) of a `dict`:

# In[ ]:


for key in mypet:
    print("The key is:", key)
    print("The value is:", mypet[key])


# ## Arrays of numbers with NumPy
# 
# The vast majority of scientific Python code makes use of *packages* that extend the base language in many useful ways.
# 
# Almost all scientific computing requires ordered arrays of numbers, and fast methods for manipulating them. That's what [NumPy](../core/numpy.md) does in the Python world.
# 
# Using any package requires an `import` statement, and (optionally) a nickname to be used locally, denoted by the keyword `as`:

# In[ ]:


import numpy as np


# Now all our calls to `numpy` functions will be preceeded by `np.`

# Create a linearly space array of numbers:

# In[ ]:


# linspace() takes 3 arguments: start, end, total number of points
numbers = np.linspace(0.0, 1.0, 11)
numbers


# We've just created a new type of object defined by [NumPy](../core/numpy.md):

# In[ ]:


type(numbers)


# Do some arithmetic on that array:

# In[ ]:


numbers + 1


# Sum up all the numbers:

# In[ ]:


np.sum(numbers)


# ## Some basic graphics with Matplotlib
# 
# [Matplotlib](../core/matplotlib.md) is the standard package for producing publication-quality graphics, and works hand-in-hand with [NumPy](../core/numpy.md) arrays.
# 
# We usually use the `pyplot` submodule for day-to-day plotting commands:

# In[ ]:


import matplotlib.pyplot as plt


# Define some data and make a line plot:

# In[ ]:


theta = np.linspace(0.0, 360.0)
sintheta = np.sin(np.deg2rad(theta))

plt.plot(theta, sintheta, label='y = sin(x)', color='purple')
plt.grid()
plt.legend()
plt.xlabel('Degrees')
plt.title('Our first Pythonic plot', fontsize=14)


# ## What now?
# 
# That was a whirlwind tour of some basic Python usage. 
# 
# Read on for more details on how to install and run Python and necessary packages on your own laptop.

# ## Resources and references
# 
# - [Official Python tutorial (Python Docs)](https://docs.python.org/3/tutorial/index.html)
