#!/usr/bin/env python
# coding: utf-8

# # Times and Dates in Python

# ---

# ## Overview
# 
# Time is an essential component of nearly all geoscience data. Timescales commonly used in science can have many different orders of magnitude, from mere microseconds to millions or even billions of years.  Some of these magnitudes are listed below:
# 
# - microseconds for lightning
# - hours for a supercell thunderstorm
# - days for a global weather model
# - millennia and beyond for the earth's climate
# 
# To properly analyze geoscience data, you must have a firm understanding of how to handle time in Python. 
# 
# In this notebook, we will:
# 
# 1. Introduce the [time](https://docs.python.org/3/library/time.html) and [datetime](https://docs.python.org/3/library/datetime.html) modules from the Python Standard Library
# 1. Look at formatted input and output of dates and times
# 1. See how we can do simple arithmetic on date and time data, by making use of the `timedelta` object
# 1. Briefly make use of the [pytz](https://pypi.org/project/pytz/) module to handle some thorny time zone issues in Python.

# ## Prerequisites
# 
# | Concepts | Importance | Notes |
# | --- | --- | --- |
# | [Python Quickstart](../../foundations/quickstart) | Necessary | Understanding strings |
# | Basic Python string formatting | Helpful | Try this [Real Python string formatting tutorial](https://realpython.com/python-string-formatting/) |
# 
# - **Time to learn**: 30 minutes

# ---

# ## Imports
# 
# For the examples on this page, we import three modules from the Python Standard Library, as well as one third-party module.  The import syntax used here, as well as a discussion on this syntax and an overview of these modules, can be found in the next section.

# In[ ]:


# Python Standard Library packages
# We'll discuss below WHY we alias the packages this way
import datetime as dt
import math
import time as tm

# Third-party package for time zone handling, we'll discuss below!
import pytz


# ## `Time` Versus `Datetime` modules 
# 
# ### Some core terminology
# 
# Every Python installation comes with a Standard Library, which includes many helpful modules; in these examples, we cover the [time](https://docs.python.org/3/library/time.html) and [datetime](https://docs.python.org/3/library/datetime.html) modules. Unfortunately, the use of dates and times in Python can be disorienting.  There are many different terms used in Python relating to dates and times, and many such terms apply to multiple scopes, such as modules, classes, and functions. For example:
# 
# -   `datetime` **module** has a `datetime` **class**
# -   `datetime` **module** has a `time` **class**
# -   `datetime` **module** has a `date` **class**
# -   `time` **module** has a `time` function, which returns (almost always) [Unix time](#What-is-Unix-Time?)
# -   `datetime` **class** has a `date` method, which returns a `date` object
# -   `datetime` **class** has a `time` method, which returns a `time` object
# 
# This confusion can be partially alleviated by aliasing our imported modules, we did above:
# 
# ```
# import datetime as dt
# import time as tm
# ```
# 
# We can now reference the `datetime` module (aliased to `dt`) and `datetime` class unambiguously.

# In[ ]:


pisecond = dt.datetime(2021, 3, 14, 15, 9, 26)
print(pisecond)


# Our variable `pisecond` now stores a particular date and time, which just happens to be $\pi$-day 2021 down to the nearest second (3.1415926...).

# In[ ]:


now = tm.time()
print(now)


# The variable `now` holds the current time in seconds since January 1, 1970 00:00 UTC.  For more information on this important, but seemingly esoteric time format, see the section on this page called "[What is Unix Time](#What-is-Unix-Time?)". In addition, if you are not familiar with UTC, there is a section on this page called "[What is UTC](#What-is-UTC?)".

# ### `time` module
# 
# The `time` module is well-suited for measuring [Unix time](#What-is-Unix-Time?). For example, when you are calculating how long it takes a Python function to run, you can employ the `time()` function, which can be found in the `time` module, to obtain Unix time before and after the function completes.  You can then take the difference of those two times to determine how long the function was running. (Measuring the runtime of a block of code this way is known as "benchmarking".)

# In[ ]:


start = tm.time()
tm.sleep(1)  # The sleep function will stop the program for n seconds
end = tm.time()
diff = end - start
print(f"The benchmark took {diff} seconds")


# <div class="admonition alert alert-info">
#     <p class="admonition-title" style="font-weight:bold">Info</p>
#     You can use the `timeit` module and the `timeit` Jupyter magic for more accurate benchmarking.  Documentation on these can be found <a href="https://docs.python.org/3/library/timeit.html">here</a>.
# </div>

# ### What is Unix Time?
# 
# Unix time is an example of system time, which is how a computer tracks the passage of time. Computers do not inherently know human representations of time; as such, they store time as a large binary number, indicating a number of time units after a set date and time.  This is much easier for a computer to keep track of.  In the case of Unix time, the time unit is seconds, and the set date and time is the epoch.  Therefore, Unix time is the number of seconds since the epoch.  The epoch is defined as January 1, 1970 00:00 [UTC](#What-is-UTC?).  This is quite confusing for humans, but again, computers store time in a way that makes sense for them. It is represented "under the hood" as a [floating point number](https://en.wikipedia.org/wiki/Floating_point) which is how computers represent real (ℝ) numbers.

# ### `datetime` module
# 
# The `datetime` module handles time with the Gregorian calendar (the calendar we, as humans, are familiar with); it is independent of Unix time. The `datetime` module uses an [object-oriented](#Thirty-second-introduction-to-Object-Oriented-programming) approach; it contains the `date`, `time`, `datetime`, `timedelta`, and `tzinfo` classes.
# 
# -   `date` class represents the day, month, and year
# -   `time` class represents the time of day
# -   `datetime` class is a combination of the `date` and `time` classes
# -   `timedelta` class represents a time duration
# -   `tzinfo` class represents time zones, and is an abstract class.
# 
# The `datetime` module is effective for:
# 
# -   performing date and time arithmetic and calculating time duration
# -   reading and writing date and time strings with various formats
# -   handling time zones (with the help of third-party libraries)
# 
# The `time` and `datetime` modules overlap in functionality, but in your geoscientific work, you will probably be using the `datetime` module more than the `time` module.

# We'll delve into more details below, but here's a quick example of writing out our `pisecond` datetime object as a formatted string. Suppose we wanted to write out just the date, and write it in the _month/day/year_ format typically used in the US. We can do this using the `strftime()` method.  This method formats datetime objects using format specifiers.  An example of its usage is shown below:

# In[ ]:


print('Pi day occurred on:', pisecond.strftime(format='%m/%d/%Y'))


# ## Reading and writing dates and times
# 
# ### Parsing lightning data timestamps with the `datetime.strptime` method
# 
# In this example, we are analyzing [US NLDN lightning data](https://ghrc.nsstc.nasa.gov/uso/ds_docs/vaiconus/vaiconus_dataset.html). Here is a sample row of data:
# 
#     06/27/07 16:18:21.898 18.739 -88.184 0.0 kA 0 1.0 0.4 2.5 8 1.2 13 G
# 
# Part of the task involves parsing the `06/27/07 16:18:21.898` time string into a `datetime` object. (Although it is outside the scope of this page's tutorial, a full description of this lightning data format can be found [here](https://ghrc.nsstc.nasa.gov/uso/ds_docs/vaiconus/vaiconus_dataset.html#a6).) In order to parse this string or others that follow the same format, you will need to employ the [datetime.strptime()](https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime) method from the `datetime` module. This method takes two arguments: 
# 1. the date/time string you wish to parse
# 2. the format which describes exactly how the date and time are arranged. 
# 
# [The full range of formatting options for strftime() and strptime() is described in the Python documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior). In most cases, finding the correct formatting options inherently takes some degree of experimentation to get right. This is a situation where Python shines; you can use the IPython interpreter, or a Jupyter notebook, to quickly test numerous formatting options. Beyond the official documentation, Google and [Stack Overflow](https://stackoverflow.com/) are your friends in this process. 
# 
# After some trial and error (as described above), you can find that, in this example, the format string `'%m/%d/%y %H:%M:%S.%f'` will convert the date and time in the data to the correct format.

# In[ ]:


strike_time = dt.datetime.strptime('06/27/07 16:18:21.898', '%m/%d/%y %H:%M:%S.%f')
# print strike_time to see if we have properly parsed our time
print(strike_time)


# ### Example usage of the `datetime` object
# 
# Why did we bother doing this? This is a deceptively simple example; it may appear that we only took the string `06/27/07 16:18:21.898` and reformatted it to `2007-06-27 16:18:21.898000`.
# 
# However, our new variable, `strike_time`, is in fact a `datetime` object that we can manipulate in many useful ways. 
# 
# Here are a few quick examples of the advantages of a datetime object:

# #### Controlling the output format with `strftime()`
# 
# The following example shows how to write out the time only, without a date, in a particular format:
# ```
# 16h 18m 21s
# ```
# 
# We can do this with the [datetime.strftime()](https://docs.python.org/2/library/datetime.html#datetime.date.strftime) method, which takes a format identical to the one we employed for `strptime()`. After some trial and error from the IPython interpreter, we arrive at `'%Hh %Mm %Ss'`:

# In[ ]:


print(strike_time.strftime(format='%Hh %Mm %Ss'))


# #### A simple query of just the year:
# 
# Here's a useful shortcut that doesn't even need a format specifier:

# In[ ]:


strike_time.year


# This works because the `datetime` object stores the data as individual attributes: 
# `year`, `month`, `day`, `hour`, `minute`, `second`, `microsecond`.

# #### See how many days have elapsed since the strike:
# 
# This example shows how to find the number of days since an event; in this case, the lightning strike described earlier:

# In[ ]:


(dt.datetime.now() - strike_time).days


# The above example illustrates some simple arithmetic with `datetime` objects.  This commonly-used feature will be covered in more detail in the next section.

# ## Calculating coastal tides with the `timedelta` class
# 
# In these examples, we will look at current data pertaining to coastal tides during a [tropical cyclone storm surge](http://www.nhc.noaa.gov/surge/).
# 
# The [lunar day](http://oceanservice.noaa.gov/education/kits/tides/media/supp_tide05.html) is 24 hours and 50 minutes; there are two low tides and two high tides in that time duration. If we know the time of the current high tide, we can easily calculate the occurrence of the next low and high tides by using the [timedelta class](https://docs.python.org/3/library/datetime.html#timedelta-objects). (In reality, the *exact time* of tides is influenced by local coastal effects, in addition to the laws of celestial mechanics, but we will ignore that fact for this exercise.)
# 
# The `timedelta` class is initialized by supplying time duration, usually supplied with [keyword arguments](https://docs.python.org/3/glossary.html#term-argument), to clearly express the length of time. The `timedelta` class allows you to perform arithmetic with dates and times using standard operators (i.e., `+`, `-`, `*`, `/`).  You can use these operators with a `timedelta` object, and either another `timedelta` object, a datetime object, or a numeric literal, to obtain objects representing new dates and times.
# 
# This convenient language feature is known as [operator overloading](https://en.wikipedia.org/wiki/Operator_overloading), and is another example of Python offering built-in functionality to make programming easier. (In some other languages, such as Java, you would have to call a method to perform such operations, which significantly obfuscates the code.) 
# 
# In addition, you can use these arithmetic operators with two datetime objects, as shown above with [lightning-strike data](#See-how-many-days-have-elapsed-since-the-strike:), to create `timedelta` objects. Let's examine all these features in the following code block.

# In[ ]:


high_tide = dt.datetime(2016, 6, 1, 4, 38, 0)
lunar_day = dt.timedelta(hours=24, minutes=50)
tide_duration = lunar_day / 4  # Here we do some arithmetic on the timedelta object!
next_low_tide = (
    high_tide + tide_duration
)  # Here we add a timedelta object to a datetime object
next_high_tide = high_tide + (2 * tide_duration)  # and so on
tide_length = next_high_tide - high_tide
print(f"The time between high and low tide is {tide_duration}.")
print(f"The current high tide is {high_tide}.")
print(f"The next low tide is {next_low_tide}.")
print(f"The next high tide {next_high_tide}.")
print(f"The tide length is {tide_length}.")
print(f"The type of the 'tide_length' variable is {type(tide_length)}.")


# To illustrate that the difference of two times yields a `timedelta` object, we can use a built-in Python function called `type()`, which returns the type of its argument.  In the above example, we call `type()` in the last `print` statement, and it returns the type of `timedelta`.

# ## Dealing with Time Zones
# 
# Time zones can be a source of confusion and frustration in geoscientific data and in computer programming in general. Core date and time libraries in various programming languages, including Python, inevitably have design flaws, relating to time zones, date and time formatting, and other inherently complex issues.  Third-party libraries are often created to fix the limitations of the core libraries, but this approach is frequently unsuccessful. To avoid time-zone-related issues, it is best to handle data in UTC; if data cannot be handled in UTC, efforts should be made to consistently use the same time zone for all data.  However, this is not always possible; events such as severe weather are expected to be reported in a local time zone, which is not always consistent.
# 
# ### What is UTC?
# 
# "[UTC](https://en.wikipedia.org/wiki/Coordinated_Universal_Time)" is a combination of the French and English abbreviations for Coordinated Universal Time.  It is, in practice, equivalent to Greenwich Mean Time (GMT), the time zone at 0 degrees longitude.  (The prime meridian, 0 degrees longitude, runs through Greenwich, a district of London, England.) In geoscientific data, times are often in UTC, although you should always verify that this is actually true to avoid time zone issues.
# 
# ### Time Zone Naive Versus Time Zone Aware `datetime` Objects
# 
# When you create `datetime` objects in Python, they are "time zone naive", or, if the subject of time zones is assumed, simply "naive".  This means that they are unaware of the time zone of the date and time they represent; time zone naive is the opposite of time zone aware. In many situations, you can happily go forward without this detail getting in the way of your work. As the [Python documentation states](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects):
# >Naive objects are easy to understand and to work with, at the cost of ignoring some aspects of reality. 
# 
# However, if you wish to convey time zone information, you will have to make your `datetime` objects time zone aware. The `datetime` library is able to easily convert the time zone to UTC, also converting the object to a time zone aware state, as shown below:

# In[ ]:


naive = dt.datetime.now()
aware = dt.datetime.now(dt.timezone.utc)
print(f"I am time zone naive {naive}.")
print(f"I am time zone aware {aware}.")


# Notice that `aware` has `+00:00` appended at the end, indicating zero hours offset from UTC.
# 
# Our `naive` object shows the local time on whatever computer was used to run this code. If you're reading this online, chances are the code was executed on a cloud server that already uses UTC.  If this is the case, `naive` and `aware` will differ only at the microsecond level, due to round-off error.
# 
# In the code above, we used `dt.timezone.utc` to initialize the UTC timezone for our `aware` object. Unfortunately, at this time, the Python Standard Library does not fully support initializing datetime objects with arbitrary time zones; it also does not fully support conversions between time zones for datetime objects.  However, there exist third-party libraries that provide some of this functionality; one such library is covered below.

# ### Full time zone support with the `pytz` module
# 
# For improved handling of time zones in Python, you will need the third-party [pytz](https://pypi.org/project/pytz/) module, whose classes build upon, or, in object-oriented programming terms, inherit from, classes from the `datetime` module.
# 
# In this next example, we repeat the above exercise, but this time, we use a method from the `pytz` module to initialize the `aware` object in a different time zone:

# In[ ]:


naive = dt.datetime.now()
aware = dt.datetime.now(pytz.timezone('US/Mountain'))
print(f"I am time zone naive: {naive}.")
print(f"I am time zone aware: {aware}.")


# The `pytz.timezone()` method takes a time zone string; if this string is formatted correctly, the method returns a `tzinfo` object, which can be used when making a datetime object time zone aware.  This initializes the time zone for the newly aware object to a specific time zone matching the time zone string. The `-06:00` indicates that we are now operating in a time zone six hours behind UTC.
# 
# ### Print Time with a Different Time Zone
# 
# If you have data that are in UTC, and wish to convert them to another time zone (in this example, US Mountain Time Zone), you will again need to make use of the `pytz` module.
# 
# First, we will create a new datetime object with the [utcnow()](https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow) method.  Despite the name of this method, the newly created object is time zone naive.  Therefore, we must invoke the object's [replace()](https://docs.python.org/3/library/datetime.html#datetime.datetime.replace) method and specify UTC with a `tzinfo` object in order to make the object time zone aware. As described above, we can use the `pytz` module's timezone() method to create a new `tzinfo` object, again using the time zone string 'US/Mountain' (US Mountain Time Zone). To convert the datetime object `utc` from UTC to Mountain Time, we can then run the [astimezone()](https://docs.python.org/3/library/datetime.html#datetime.datetime.astimezone) method.

# In[ ]:


utc = dt.datetime.utcnow().replace(tzinfo=pytz.utc)
print("The UTC time is {}.".format(utc.strftime('%B %d, %Y, %-I:%M%p')))
mountaintz = pytz.timezone("US/Mountain")
ny = utc.astimezone(mountaintz)
print("The 'US/Mountain' time is {}.".format(ny.strftime('%B %d, %Y, %-I:%M%p')))


# In the above example, we also use the `strftime()` method to format the date and time string in a human-friendly format.

# ---

# ## Summary
# 
# The Python Standard Library contains several modules for dealing with date and time data. We saw how we can avoid some name ambiguities by aliasing the module names; this can be done with import statements like `import datetime as dt` and `import time as tm`. The `tm.time()` method just returns the current [Unix time](#What-is-Unix-Time?) in seconds -- which can be useful for measuring elapsed time, but not all that useful for working with geophysical data.
# 
# The `datetime` module contains various classes for storing, converting, comparing, and formatting date and time data on the Gregorian calendar. We saw how we can parse data files with date and time strings into `dt.datetime` objects using the `dt.datetime.strptime()` method. We also saw how to perform arithmetic using date and time data; this uses the `dt.timedelta` class to represent intervals of time.
# 
# Finally, we looked at using the third-party [pytz](https://pypi.org/project/pytz/) module to handle time zone awareness and conversions.
# 
# ### What's Next?
# 
# In subsequent tutorials, we will dig deeper into different time and date formats, and discuss how they are handled by important Python modules such as Numpy, Pandas, and Xarray.

# ## Resources and References
# 
# This page was based on and adapted from material in [Unidata's Python Training](https://unidata.github.io/python-training/python/times_and_dates/).
# 
# For further reading on these modules, take a look at the official documentation for:
# - [time](https://docs.python.org/3/library/time.html)
# - [datetime](https://docs.python.org/3/library/datetime.html)
# - [pytz](https://pypi.org/project/pytz/)
# 
# For more information on Python string formatting, try:
# - [Python string documentation](https://docs.python.org/3/library/string.html)
# - RealPython's [string formatting tutorial](https://realpython.com/python-string-formatting/) (nicely written)

# In[ ]:




