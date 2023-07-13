#!/usr/bin/env python
# coding: utf-8

# <center><img src="https://github.com/pandas-dev/pandas/raw/main/web/pandas/static/img/pandas.svg" alt="pandas Logo" style="width: 800px;"/></center>
# 
# # Introduction to Pandas
# ---

# ## Overview
# 1. Introduction to pandas data structures
# 1. How to slice and dice pandas dataframes and dataseries
# 1. How to use pandas for exploratory data analysis
# 
# ## Prerequisites
# 
# | Concepts | Importance | Notes |
# | --- | --- | --- |
# | [Python Quickstart](../../foundations/quickstart) | Necessary | Intro to `dict` |
# | [Numpy Basics](../numpy/numpy-basics) | Necessary | |
# 
# * **Time to learn**: 60 minutes

# ---

# ## Imports

# You will often see the nickname `pd` used as an abbreviation for pandas in the import statement, just like `numpy` is often imported as `np`. We also import the `DATASETS` class from `pythia_datasets`, which allows us to use example datasets created for Pythia.

# In[ ]:


import pandas as pd
from pythia_datasets import DATASETS


# ## The pandas [`DataFrame`](https://pandas.pydata.org/docs/user_guide/dsintro.html#dataframe)...
# ...is a **labeled**, two-dimensional columnar structure, similar to a table, spreadsheet, or the R `data.frame`.
# 
# ![dataframe schematic](https://github.com/pandas-dev/pandas/raw/main/doc/source/_static/schemas/01_table_dataframe.svg "Schematic of a pandas DataFrame")
# 
# The `columns` that make up our `DataFrame` can be lists, dictionaries, NumPy arrays, pandas `Series`, or many other data types not mentioned here. Within these `columns`, you can have data values of many different data types used in Python and NumPy, including text, numbers, and dates/times. The first column of a `DataFrame`, shown in the image above in dark gray, is uniquely referred to as an `index`; this column contains information characterizing each row of our `DataFrame`. Similar to any other `column`, the `index` can label rows by text, numbers, datetime objects, and many other data types. Datetime objects are a quite popular way to label rows.
# 
# For our first example using Pandas DataFrames, we start by reading in some data in comma-separated value (`.csv`) format. We retrieve this dataset from the Pythia DATASETS class (imported at the top of this page); however, the dataset was originally contained within the NCDC teleconnections database. This dataset contains many types of geoscientific data, including El Nino/Southern Oscillation indices. For more information on this dataset, review the description [here](https://www.ncdc.noaa.gov/teleconnections/enso/indicators/sst/).

# <div class="admonition alert alert-info">
#     <p class="admonition-title" style="font-weight:bold">Info</p>
#     As described above, we are retrieving the datasets for these examples from Project Pythia's custom library of example data. In order to retrieve datasets from this library, you must use the statement <code>from pythia_datasets import DATASETS</code>. This is shown and described in the Imports section at the top of this page. The <code>fetch()</code> method of the <code>DATASETS</code> class will automatically download the data file specified as a string argument, in this case <code>enso_data.csv</code>, and cache the file locally, assuming the argument corresponds to a valid Pythia example dataset. This is illustrated in the following example.
# </div>

# In[ ]:


filepath = DATASETS.fetch('enso_data.csv')


# Once we have a valid path to a data file that Pandas knows how to read, we can open it, as shown in the following example:

# In[ ]:


df = pd.read_csv(filepath)


# If we print out our `DataFrame`, it will render as text by default, in a tabular-style ASCII output, as shown in the following example. However, if you are using a Jupyter notebook, there exists a better way to print `DataFrames`, as described below.

# In[ ]:


print(df)


# As described above, there is a better way to print Pandas `DataFrames`. If you are using a Jupyter notebook, you can run a code cell containing the `DataFrame` object name, by itself, and it will display a nicely rendered table, as shown below.

# In[ ]:


df


# The `DataFrame` index, as described above, contains information characterizing rows; each row has a unique ID value, which is displayed in the index column.  By default, the IDs for rows in a `DataFrame` are represented as sequential integers, which start at 0.

# In[ ]:


df.index


# At the moment, the index column of our `DataFrame` is not very helpful for humans. However, Pandas has clever ways to make index columns more human-readable. The next example demonstrates how to use optional keyword arguments to convert `DataFrame` index IDs to a human-friendly datetime format.

# In[ ]:


df = pd.read_csv(filepath, index_col=0, parse_dates=True)

df


# In[ ]:


df.index


# Each of our data rows is now helpfully labeled by a datetime-object-like index value; this means that we can now easily identify data values not only by named columns, but also by date labels on rows. This is a sneak preview of the `DatetimeIndex` functionality of Pandas; this functionality enables a large portion of Pandas' timeseries-related usage. Don't worry; `DatetimeIndex` will be discussed in full detail later on this page. In the meantime, let's look at the columns of data read in from the `.csv` file:

# In[ ]:


df.columns


# ## The pandas [`Series`](https://pandas.pydata.org/docs/user_guide/dsintro.html#series)...
# 
# ...is essentially any one of the columns of our `DataFrame`. A `Series` also includes the index column from the source `DataFrame`, in order to provide a label for each value in the `Series`.
# 
# ![pandas Series](https://github.com/pandas-dev/pandas/raw/main/doc/source/_static/schemas/01_table_series.svg "Schematic of a pandas Series")
# 
# The pandas `Series` is a fast and capable 1-dimensional array of nearly any data type we could want, and it can behave very similarly to a NumPy `ndarray` or a Python `dict`. You can take a look at any of the `Series` that make up your `DataFrame`, either by using its column name and the Python `dict` notation, or by using dot-shorthand with the column name:

# In[ ]:


df["Nino34"]


# <div class="alert alert-block alert-info">
# <b>Tip:</b> You can also use the dot notation illustrated below to specify a column name, but this syntax is mostly provided for convenience. For the most part, this notation is interchangeable with the dictionary notation; however, if the column name is not a valid Python identifier (e.g., it starts with a number or space), you cannot use dot notation.</div>

# In[ ]:


df.Nino34


# ## Slicing and Dicing the `DataFrame` and `Series`
# 
# In this section, we will expand on topics covered in the previous sections on this page. One of the most important concepts to learn about Pandas is that it allows you to _**access anything by its associated label**_, regardless of data organization structure.

# ### Indexing a `Series`
# 
# As a review of previous examples, we'll start our next example by pulling a `Series` out of our `DataFrame` using its column label.

# In[ ]:


nino34_series = df["Nino34"]

nino34_series


# You can use syntax similar to that of NumPy `ndarrays` to index, select, and subset with Pandas `Series`, as shown in this example:

# In[ ]:


nino34_series[3]


# You can also use labels alongside Python dictionary syntax to perform the same operations:

# In[ ]:


nino34_series["1982-04-01"]


# You can probably figure out some ways to extend these indexing methods, as shown in the following examples:

# In[ ]:


nino34_series[0:12]


# <div class="admonition alert alert-info">
#     <p class="admonition-title" style="font-weight:bold">Info</p>
#     Index-based slices are <b>exclusive</b> of the final value, similar to Python's usual indexing rules.
# </div>

# However, there are many more ways to index a `Series`. The following example shows a powerful and useful indexing method:

# In[ ]:


nino34_series["1982-01-01":"1982-12-01"]


# This is an example of label-based slicing. With label-based slicing, Pandas will automatically find a range of values based on the labels you specify.

# <div class="admonition alert alert-info">
#     <p class="admonition-title" style="font-weight:bold">Info</p>
#     As opposed to index-based slices, label-based slices are <b>inclusive</b> of the final value.
# </div>

# If you already have some knowledge of xarray, you will quite likely know how to create `slice` objects by hand. This can also be used in pandas, as shown below.  If you are completely unfamiliar with xarray, it will be covered on a [later Pythia tutorial page](../xarray).

# In[ ]:


nino34_series[slice("1982-01-01", "1982-12-01")]


# ### Using `.iloc` and `.loc` to index
# 
# In this section, we introduce ways to access data that are preferred by Pandas over the methods listed above. When accessing by label, it is preferred to use the `.loc` method, and when accessing by index, the `.iloc` method is preferred. These methods behave similarly to the notation introduced above, but provide more speed, security, and rigor in your value selection. Using these methods can also help you avoid [chained assignment warnings](https://pandas.pydata.org/docs/user_guide/indexing.html#returning-a-view-versus-a-copy) generated by pandas.

# In[ ]:


nino34_series.iloc[3]


# In[ ]:


nino34_series.iloc[0:12]


# In[ ]:


nino34_series.loc["1982-04-01"]


# In[ ]:


nino34_series.loc["1982-01-01":"1982-12-01"]


# ### Extending to the `DataFrame`
# 
# These subsetting capabilities can also be used in a full `DataFrame`; however, if you use the same syntax, there are issues, as shown below:

# In[ ]:


df["1982-01-01"]


# <div class="admonition alert alert-danger">
#     <p class="admonition-title" style="font-weight:bold">Danger</p>
#     Attempting to use <code>Series</code> subsetting with a <code>DataFrame</code> can crash your program. A proper way to subset a <code>DataFrame</code> is shown below.
# </div>

# When indexing a `DataFrame`, pandas will not assume as readily the intention of your code. In this case, using a row label by itself will not work; **with `DataFrames`, labels are used for identifying columns**.

# In[ ]:


df["Nino34"]


# As shown below, you also cannot subset columns in a `DataFrame` using integer indices:

# In[ ]:


df[0]


# From earlier examples, we know that we can use an index or label with a `DataFrame` to pull out a column as a `Series`, and we know that we can use an index or label with a `Series` to pull out a single value.  Therefore, by chaining brackets, we can pull any individual data value out of the `DataFrame`.

# In[ ]:


df["Nino34"]["1982-04-01"]


# In[ ]:


df["Nino34"][3]


# However, subsetting data using this chained-bracket technique is not preferred by Pandas. As described above, Pandas prefers us to use the `.loc` and `.iloc` methods for subsetting.  In addition, these methods provide a clearer, more efficient way to extract specific data from a `DataFrame`, as illustrated below:

# In[ ]:


df.loc["1982-04-01", "Nino34"]


# <div class="admonition alert alert-info">
#     <p class="admonition-title" style="font-weight:bold">Info</p>
#     When using this syntax to pull individual data values from a DataFrame, make sure to list the row first, and then the column.
# </div>

# The `.loc` and `.iloc` methods also allow us to pull entire rows out of a `DataFrame`, as shown in these examples:

# In[ ]:


df.loc["1982-04-01"]


# In[ ]:


df.loc["1982-01-01":"1982-12-01"]


# In[ ]:


df.iloc[3]


# In[ ]:


df.iloc[0:12]


# In the next example, we illustrate how you can use slices of rows and lists of columns to create a smaller `DataFrame` out of an existing `DataFrame`:

# In[ ]:


df.loc[
    "1982-01-01":"1982-12-01",  # slice of rows
    ["Nino12", "Nino3", "Nino4", "Nino34"],  # list of columns
]


# <div class="admonition alert alert-info">
#     <p class="admonition-title" style="font-weight:bold">Info</p>
#     There are certain limitations to these subsetting techniques. For more information on these limitations, as well as a comparison of <code>DataFrame</code> and <code>Series</code> indexing methods, see the <a href="https://pandas.pydata.org/docs/user_guide/indexing.html">Pandas indexing documentation.</a>
# </div>

# ## Exploratory Data Analysis
# 
# ### Get a Quick Look at the Beginning/End of your `DataFrame`
# Pandas also gives you a few shortcuts to quickly investigate entire `DataFrames`. The `head` method shows the first five rows of a `DataFrame`, and the `tail` method shows the last five rows of a `DataFrame`.

# In[ ]:


df.head()


# In[ ]:


df.tail()


# ### Quick Plots of Your Data
# A good way to explore your data is by making a simple plot. Pandas contains its own `plot` method; this allows us to plot Pandas series without needing `matplotlib`.  In this example, we plot the `Nino34` series of our `df` `DataFrame` in this way:

# In[ ]:


df.Nino34.plot();


# Before, we called `.plot()`, which generated a single line plot. Line plots can be helpful for understanding some types of data, but there are other types of data that can be better understood with different plot types. For example, if your data values form a distribution, you can better understand them using a histogram plot.
# 
# The code for plotting histogram data differs in two ways from the code above for the line plot. First, two series are being used from the `DataFrame` instead of one.  Second, after calling the `plot` method, we call an additional method called `hist`, which converts the plot into a histogram.

# In[ ]:


df[['Nino12', 'Nino34']].plot.hist();


# The histogram plot helped us better understand our data; there are clear differences in the distributions. To even better understand this type of data, it may also be helpful to create a box plot. This can be done using the same line of code, with one change: we call the `box` method instead of `hist`.

# In[ ]:


df[['Nino12', 'Nino34']].plot.box();


# Just like the histogram plot, this box plot indicates a clear difference in the distributions. Using multiple types of plot in this way can be useful for verifying large datasets. The pandas plotting methods are capable of creating many different types of plots. To see how to use the plotting methods to generate each type of plot, please review the [pandas plot documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html).

# #### Customize your Plot
# The pandas plotting methods are, in fact, wrappers for similar methods in matplotlib. This means that you can customize pandas plots by including keyword arguments to the plotting methods.  These keyword arguments, for the most part, are equivalent to their matplotlib counterparts.

# In[ ]:


df.Nino34.plot(
    color='black',
    linewidth=2,
    xlabel='Year',
    ylabel='ENSO34 Index (degC)',
    figsize=(8, 6),
);


# Although plotting data can provide a clear visual picture of data values, sometimes a more quantitative look at data is warranted. As elaborated on in the next section, this can be achieved using the `describe` method.  The `describe` method is called on the entire `DataFrame`, and returns various summarized statistics for each column in the `DataFrame`.
# ### Basic Statistics
# 
# We can garner statistics for a `DataFrame` by using the `describe` method. When this method is called on a `DataFrame`, a set of statistics is returned in tabular format.  The columns match those of the `DataFrame`, and the rows indicate different statistics, such as minimum.

# In[ ]:


df.describe()


# You can also view specific statistics using corresponding methods. In this example, we look at the mean values in the entire `DataFrame`, using the `mean` method.  When such methods are called on the entire `DataFrame`, a `Series` is returned. The indices of this `Series` are the column names in the `DataFrame`, and the values are the calculated values (in this case, mean values) for the `DataFrame` columns.

# In[ ]:


df.mean()


# If you want a specific statistic for only one column in the `DataFrame`, pull the column out of the `DataFrame` with dot notation, then call the statistic function (in this case, mean) on that column, as shown below:

# In[ ]:


df.Nino34.mean()


# ### Subsetting Using the Datetime Column
# 
# Slicing is a useful technique for subsetting a `DataFrame`, but there are also other options that can be equally useful. In this section, some of these additional techniques are covered.
# 
# If your `DataFrame` uses datetime values for indices, you can select data from only one month using `df.index.month`. In this example, we specify the number 1, which only selects data from January.

# In[ ]:


# Uses the datetime column
df[df.index.month == 1]


# This example shows how to create a new column containing the month portion of the datetime index for each data row. The value returned by `df.index.month` is used to obtain the data for this new column:

# In[ ]:


df['month'] = df.index.month


# This next example illustrates how to use the new month column to calculate average monthly values over the other data columns. First, we use the `groupby` method to group the other columns by the month.  Second, we take the average (mean) to obtain the monthly averages. Finally, we plot the resulting data as a line plot by simply calling `plot()`.

# In[ ]:


df.groupby('month').mean().plot();


# ### Investigating Extreme Values

# If you need to search for rows that meet a specific criterion, you can use **conditional indexing**.  In this example, we search for rows where the Nino34 anomaly value (`Nino34anom`) is greater than 2:

# In[ ]:


df[df.Nino34anom > 2]


# This example shows how to use the `sort_values` method on a `DataFrame`. This method sorts values in a `DataFrame` by the column specified as an argument.

# In[ ]:


df.sort_values('Nino34anom')


# You can also reverse the ordering of the sort by specifying the `ascending` keyword argument as `False`:

# In[ ]:


df.sort_values('Nino34anom', ascending=False)


# ### Resampling
# In these examples, we illustrate a process known as resampling. Using resampling, you can change the frequency of index data values, reducing so-called 'noise' in a data plot. This is especially useful when working with timeseries data; plots can be equally effective with resampled data in these cases. The resampling performed in these examples converts monthly values to yearly averages. This is performed by passing the value '1Y' to the `resample` method.

# In[ ]:


df.Nino34.plot();


# In[ ]:


df.Nino34.resample('1Y').mean().plot();


# ### Applying operations to a DataFrame
# 
# One of the most commonly used features in Pandas is the performing of calculations to multiple data values in a `DataFrame` simultaneously. Let's first look at a familiar concept: a function that converts single values.  The following example uses such a function to convert temperature values from degrees Celsius to Kelvin.

# In[ ]:


def convert_degc_to_kelvin(temperature_degc):
    """
    Converts from degrees celsius to Kelvin
    """

    return temperature_degc + 273.15


# In[ ]:


# Convert a single value
convert_degc_to_kelvin(0)


# The following examples instead illustrate a new concept: using such functions with `DataFrames` and `Series`. For the first example, we start by creating a `Series`; in order to do so, we subset the `DataFrame` by the `Nino34` column. This has already been done earlier in this page; we do not need to create this `Series` again. We are using this particular `Series` for a reason: the data values are in degrees Celsius.

# In[ ]:


nino34_series


# Here, we look at a portion of an existing `DataFrame` column. Notice that this column portion is a Pandas `Series`.

# In[ ]:


type(df.Nino12[0:10])


# As shown in the following example, each Pandas `Series` contains a representation of its data in numpy format. Therefore, it is possible to convert a Pandas `Series` into a numpy array; this is done using the `.values` method:

# In[ ]:


type(df.Nino12.values[0:10])


# This example illustrates how to use the temperature-conversion function defined above on a `Series` object. Just as calling the function with a single value returns a single value, calling the function on a `Series` object returns another `Series` object. The function performs the temperature conversion on each data value in the `Series`, and returns a `Series` with all values converted.

# In[ ]:


convert_degc_to_kelvin(nino34_series)


# If we call the `.values` method on the `Series` passed to the function, the `Series` is converted to a numpy array, as described above. The function then converts each value in the numpy array, and returns a new numpy array with all values sorted.

# <div class="admonition alert alert-warning">
#     <p class="admonition-title" style="font-weight:bold">Warning</p>
#     It is recommended to only convert <code>Series</code> to NumPy arrays when necessary; doing so removes the label information that enables much of the Pandas core functionality.
# </div>

# In[ ]:


convert_degc_to_kelvin(nino34_series.values)


# As described above, when our temperature-conversion function accepts a `Series` as an argument, it returns a `Series`. We can directly assign this returned `Series` to a new column in our `DataFrame`, as shown below:

# In[ ]:


df['Nino34_degK'] = convert_degc_to_kelvin(nino34_series)


# In[ ]:


df.Nino34_degK


# In this final example, we demonstrate the use of the `to_csv` method to save a `DataFrame` as a `.csv` file. This example also demonstrates the `read_csv` method, which reads `.csv` files into Pandas `DataFrames`.

# In[ ]:


df.to_csv('nino_analyzed_output.csv')


# In[ ]:


pd.read_csv('nino_analyzed_output.csv', index_col=0, parse_dates=True)


# ---
# ## Summary
# * Pandas is a very powerful tool for working with tabular (i.e., spreadsheet-style) data
# * There are multiple ways of subsetting your pandas dataframe or series
# * Pandas allows you to refer to subsets of data by label, which generally makes code more readable and more robust
# * Pandas can be helpful for exploratory data analysis, including plotting and basic statistics
# * One can apply calculations to pandas dataframes and save the output via `csv` files
# 
# ### What's Next?
# In the next notebook, we will look more into using pandas for more in-depth data analysis.
# 
# ## Resources and References
# 1. [NOAA NCDC ENSO Dataset Used in this Example](https://www.ncdc.noaa.gov/teleconnections/enso/indicators/sst/)
# 1. [Getting Started with Pandas](https://pandas.pydata.org/docs/getting_started/index.html#getting-started)
# 1. [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html#user-guide)
