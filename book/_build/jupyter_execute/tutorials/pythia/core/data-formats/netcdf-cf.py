#!/usr/bin/env python
# coding: utf-8

# ![NetCDF Logo](https://www.unidata.ucar.edu/images/logos/netcdf-400x400.png "NetCDF Logo")

# # NetCDF and CF: The Basics
# ---

# ## Overview
# This tutorial will begin with an introduction to netCDF. The CF data model will then be covered, and finally, important implementation details for netCDF.  The structure of the tutorial is as follows:
# 
# 1. Demonstrating gridded data
# 1. Demonstrating observational data

# ## Prerequisites
# 
# | Concepts | Importance | Notes |
# | --- | --- | --- |
# | [Numpy Basics](../numpy/numpy-basics) | Necessary | |
# | [Datetime](../datetime) | Necessary | |
# 
# - **Time to learn**: 50 minutes

# ---

# ## Imports
# 
# Some of these imports will be familiar from previous tutorials.  However, some of them likely look foreign; these will be covered in detail later in this tutorial.

# In[ ]:


from datetime import datetime, timedelta

import numpy as np
from cftime import date2num
from netCDF4 import Dataset
from pyproj import Proj


# <a name="gridded"></a>
# ## Gridded Data

# Let's say we're working with some numerical weather forecast model output. First, we need to store the data in the netCDF format. Second, we need to ensure that the metadata follows the Climate and Forecasting conventions.  These steps ensure that a dataset is available to as many scientific data tools as is possible. The examples in this section illustrate these steps in detail.
# 
# To start, let's assume the following about our data:
# * There are three spatial dimensions (`x`, `y`, and `press`) and one temporal dimension (`times`).
# * The native coordinate system of the model is on a regular 3km x 3km grid (`x` and `y`) that represents the Earth on a Lambert conformal projection.
# * The vertical dimension (`press`) consists of several discrete pressure levels in units of hPa.
# * The time dimension consists of twelve consecutive hours (`times`), beginning at 2200 UTC on the current day.
# 
# The following code generates the dimensional arrays just discussed:

# In[ ]:


start = datetime.utcnow().replace(hour=22, minute=0, second=0, microsecond=0)
times = np.array([start + timedelta(hours=h) for h in range(13)])

x = np.arange(-150, 153, 3)
y = np.arange(-100, 100, 3)

press = np.array([1000, 925, 850, 700, 500, 300, 250])


# In addition to dimensional arrays, we also need a variable of interest, which holds the data values at each unique dimensional index. In these examples, this variable is called `temps`, and holds temperature data. Note that the dimensions correspond to the ones we just created above.

# In[ ]:


temps = np.random.randn(times.size, press.size, y.size, x.size)


# ### Creating the file and dimensions
# 
# The first step in setting up a new netCDF file is to create a new file in netCDF format and set up the shared dimensions we'll be using in the file. We'll be using the `netCDF4` library to do all of the requisite netCDF API calls.

# In[ ]:


nc = Dataset('forecast_model.nc', 'w', format='NETCDF4_CLASSIC', diskless=True)


# <div class='admonition alert alert-info'>
#     <p class='admonition-title' style='font-weight:bold;'>Info</p>
#     <p>The netCDF file created in the above example resides in memory, not disk, due to the <code>diskless=True</code> argument. In order to create this file on disk, you must either remove this argument, or add the <code>persist=True</code> argument.</p>
# </div>

# <div class='admonition alert alert-danger'>
#     <p class='admonition-title' style='font-weight:bold;'>Danger</p>
#     <p>If you open an existing file with <code>'w'</code> as the second argument, any data already in the file will be overwritten. If you would like to edit the file, or add to it, open it using <code>'a'</code> as the second argument.</p>
# </div>

# We start the setup of this new netCDF file by creating and adding global attribute metadata.  These particular metadata elements are not required, but are recommended by the CF standard.  In addition, adding these elements to the file is simple, and helps users keep track of the data. Therefore, it is helpful to add these metadata elements, as shown below:

# In[ ]:


nc.Conventions = 'CF-1.7'
nc.title = 'Forecast model run'
nc.institution = 'Unidata'
nc.source = 'WRF-1.5'
nc.history = str(datetime.utcnow()) + ' Python'
nc.references = ''
nc.comment = ''


# This next example shows a plain-text representation of our netCDF file as it exists currently:
# ```
# netcdf forecast_model {
#   attributes:
#     :Conventions = "CF-1.7" ;
#     :title = "Forecast model run" ;
#     :institution = "Unidata" ;
#     :source = "WRF-1.5" ;
#     :history = "2019-07-16 02:21:52.005718 Python" ;
#     :references = "" ;
#     :comment = "" ;
# }
# ```

# <div class="admonition alert alert-info">
#     <p class="admonition-title" style="font-weight:bold">Info</p>
#     This plain-text representation is known as netCDF Common Data Format Language, or <strong>CDL</strong>.
# </div>
# 
# 

# Variables are an important part of every netCDF file; they are used to define data fields. However, before we can add any variables to our file, we must first define the dimensions of the data. In this example, we create dimensions called `x`, `y`, and `pressure`, and set the size of each dimension to the size of the corresponding data array. We then create an additional dimension, `forecast_time`, and set the size as None.  This defines the dimension as "unlimited", meaning that if additional data values are added later, the netCDF file grows along this dimension.

# In[ ]:


nc.createDimension('forecast_time', None)
nc.createDimension('x', x.size)
nc.createDimension('y', y.size)
nc.createDimension('pressure', press.size)
nc


# When we view our file's CDL representation now, we can verify that the dimensions were successfully added to the netCDF file:
# ```
# netcdf forecast_model {
#   dimensions:
#     forecast_time = UNLIMITED (currently 13) ;
#     x = 101 ;
#     y = 67 ;
#     pressure = 7 ;
#   attributes:
#     :Conventions = "CF-1.7" ;
#     :title = "Forecast model run" ;
#     :institution = "Unidata" ;
#     :source = "WRF-1.5" ;
#     :history = "2019-07-16 02:21:52.005718 Python" ;
#     :references = "" ;
#     :comment = "" ;
# }
# ```

# ### Creating and filling a variable

# Thus far, we have only added basic information to this netCDF dataset; namely, the dataset dimensions and some broad metadata. As described briefly above, variables are used to define data fields in netCDF files. Here, we create a `netCDF4 variable` to hold a data field; in this case, the forecast air temperature. In order to create this netCDF4 variable, we must specify the data type of the values in the data field. We also must specify which dimensions contained in the netCDF file are relevant to this data field. Finally, we can specify whether or not to compress the data using a form of `zlib`.

# In[ ]:


temps_var = nc.createVariable(
    'Temperature',
    datatype=np.float32,
    dimensions=('forecast_time', 'pressure', 'y', 'x'),
    zlib=True,
)


# We have now created a netCDF4 variable, but it does not yet define a data field. In this example, we use Python to associate our temperature data with the new variable:

# In[ ]:


temps_var[:] = temps
temps_var


# You can also associate data with a variable sporadically. This example illustrates how to only associate one value per time step with the variable created earlier:

# In[ ]:


next_slice = 0
for temp_slice in temps:
    temps_var[next_slice] = temp_slice
    next_slice += 1


# At this point, this is the CDL representation of our dataset:
# ```
# netcdf forecast_model {
#   dimensions:
#     forecast_time = UNLIMITED (currently 13) ;
#     x = 101 ;
#     y = 67 ;
#     pressure = 7 ;
#   variables:
#     float Temperature(forecast_time, pressure, y, x) ;
#   attributes:
#     :Conventions = "CF-1.7" ;
#     :title = "Forecast model run" ;
#     :institution = "Unidata" ;
#     :source = "WRF-1.5" ;
#     :history = "2019-07-16 02:21:52.005718 Python" ;
#     :references = "" ;
#     :comment = "" ;
# }
# ```
# We can also define metadata for this variable in the form of attributes; some specific attributes are required by the CF conventions. For example, the CF conventions require a `units` attribute to be set for all variables that represent a dimensional quantity. In addition, the value of this attribute must be parsable by the [UDUNITS](https://www.unidata.ucar.edu/software/udunits/) library. In this example, the temperatures are in Kelvin, so we set the units attribute to `'Kelvin'`. Next, we set the `long_name` and `standard_name` attributes, which are recommended for most datasets, but optional. The `long_name` attribute contains a longer and more detailed description of a variable. On the other hand, the `standard_name` attribute names a variable using descriptive words from a predefined word list contained in the CF conventions. Defining these attributes allows users of your datasets to understand what each variable in a dataset represents. Sometimes, data fields do not have valid data values at every dimension point. In this case, the standard is to use a filler value for these missing data values, and to set the `missing_value` attribute to this filler value. In this case, however, there are no missing values, so the `missing_value` attribute can be set to any unused value, or not set at all.
# 
# There are many different sets of recommendations for attributes on netCDF variables. For example, here is NASA's set of recommended attributes:

# > **NASA Dataset Interoperability Recommendations:**
# >
# > Section 2.2 - Include Basic CF Attributes
# >
# > Include where applicable: `units`, `long_name`, `standard_name`, `valid_min` / `valid_max`, `scale_factor` / `add_offset` and others.

# In[ ]:


temps_var.units = 'Kelvin'
temps_var.standard_name = 'air_temperature'
temps_var.long_name = 'Forecast air temperature'
temps_var.missing_value = -9999
temps_var


# Here is the variable section of our dataset's CDL, with the new attributes added:
# ```
#   variables:
#     float Temperature(forecast_time, pressure, y, x) ;
#       Temperature:units = "Kelvin" ;
#       Temperature:standard_name = "air_temperature" ;
#       Temperature:long_name = "Forecast air temperature" ;
#       Temperature:missing_value = -9999.0 ;
# ```

# ### Coordinate variables

# Dimensions in a netCDF file only define size and alignment metadata. In order to properly orient data in time and space, it is necessary to create "coordinate variables", which define data values along each dimension. A coordinate variable is typically created as a one-dimensional variable, and has the same name as the corresponding dimension.
# 
# To start, we define variables which define our `x` and `y` coordinate values. It is recommended to include certain attributes for each coordinate variable. First, you should include a `standard_name`, which allows for associating the variable with projections, among other things. (Projections will be covered in detail later in this page.) Second, you can include an `axis` attribute, which clearly defines the spatial or temporal direction referred to by the coordinate variable. This next example demonstrates how to set up these attributes:

# In[ ]:


x_var = nc.createVariable('x', np.float32, ('x',))
x_var[:] = x
x_var.units = 'km'
x_var.axis = 'X'  # Optional
x_var.standard_name = 'projection_x_coordinate'
x_var.long_name = 'x-coordinate in projected coordinate system'

y_var = nc.createVariable('y', np.float32, ('y',))
y_var[:] = y
y_var.units = 'km'
y_var.axis = 'Y'  # Optional
y_var.standard_name = 'projection_y_coordinate'
y_var.long_name = 'y-coordinate in projected coordinate system'


# Our dataset contains vertical data of air pressure as well, so we must define a coordinate variable for this axis; we can simply call this new variable `pressure`. Since this axis represents air pressure data, we can set a `standard_name` of `'air_pressure'`.  With this `standard_name` attribute set, it should be obvious to users of this dataset that this variable represents a vertical axis, but for extra clarification, we also set the `axis` attribute as `'Z'`. We can also specify one more attribute, called `positive`.  This attribute indicates whether the variable values increase or decrease as the dimension values increase.  Setting this attribute is optional for some data; air pressure is one example.  However, we still set the attribute here, for the sake of completeness.

# In[ ]:


press_var = nc.createVariable('pressure', np.float32, ('pressure',))
press_var[:] = press
press_var.units = 'hPa'
press_var.axis = 'Z'  # Optional
press_var.standard_name = 'air_pressure'
press_var.positive = 'down'  # Optional


# Time coordinates must contain a `units` attribute; this attribute is a string value, and must have a form similar to the string`'seconds since 2019-01-06 12:00:00.00'`. 'seconds', 'minutes', 'hours', and 'days' are the most commonly used time intervals in these strings. It is not recommended to use 'months' or 'years' in time strings, as the length of these time intervals can vary.
# 
# Before we can write data, we need to first convert our list of Python `datetime` objects to numeric values usable in time strings. We can perform this conversion by setting a time string in the format described above, then using the `date2num` method from the `cftime` library.  An example of this is shown below:

# In[ ]:


time_units = f'hours since {times[0]:%Y-%m-%d 00:00}'
time_vals = date2num(times, time_units)
time_vals


# Now that the time string is set up, we have all of the necessary information to set up the attributes for a `forecast_time` coordinate variable.  The creation of this variable is shown in the following example:

# In[ ]:


time_var = nc.createVariable('forecast_time', np.int32, ('forecast_time',))
time_var[:] = time_vals
time_var.units = time_units
time_var.axis = 'T'  # Optional
time_var.standard_name = 'time'  # Optional
time_var.long_name = 'time'


# This next example shows the CDL representation of the netCDF file's variables at this point. It is clear that much more information is now contained in this representation:
# ```
#   dimensions:
#     forecast_time = UNLIMITED (currently 13) ;
#     x = 101 ;
#     y = 67 ;
#     pressure = 7 ;
#   variables:
#     float x(x) ;
#       x:units = "km" ;
#       x:axis = "X" ;
#       x:standard_name = "projection_x_coordinate" ;
#       x:long_name = "x-coordinate in projected coordinate system" ;
#     float y(y) ;
#       y:units = "km" ;
#       y:axis = "Y" ;
#       y:standard_name = "projection_y_coordinate" ;
#       y:long_name = "y-coordinate in projected coordinate system" ;
#     float pressure(pressure) ;
#       pressure:units = "hPa" ;
#       pressure:axis = "Z" ;
#       pressure:standard_name = "air_pressure" ;
#       pressure:positive = "down" ;
#     float forecast_time(forecast_time) ;
#       forecast_time:units = "hours since 2019-07-16 00:00" ;
#       forecast_time:axis = "T" ;
#       forecast_time:standard_name = "time" ;
#       forecast_time:long_name = "time" ;
#     float Temperature(forecast_time, pressure, y, x) ;
#       Temperature:units = "Kelvin" ;
#       Temperature:standard_name = "air_temperature" ;
#       Temperature:long_name = "Forecast air temperature" ;
#       Temperature:missing_value = -9999.0 ;
# ```

# ### Auxiliary Coordinates

# Our data are still not CF-compliant, because they do not contain latitude and longitude information, which is needed to properly locate the data. In order to add location data to a netCDF file, we must create so-called "auxiliary coordinate variables" for latitude and longitude. (In this case, the word "auxiliary" means that the variables are not simple one-dimensional variables.)
# 
# In this next example, we use the `Proj` function, found in the `pyproj` library, to create projections of our coordinates. We can then use these projections to generate latitude and longitude values for our data.

# In[ ]:


X, Y = np.meshgrid(x, y)
lcc = Proj({'proj': 'lcc', 'lon_0': -105, 'lat_0': 40, 'a': 6371000.0, 'lat_1': 25})
lon, lat = lcc(X * 1000, Y * 1000, inverse=True)


# Now that we have latitude and longitude values, we can create variables for those values. Both of these variables are two-dimensional; the dimensions in question are `y` and `x`. In order to convey that it contains the longitude information, we must set up the longitude variable with a `units` attribute of `'degrees_east'`. In addition, we can provide further clarity by setting a `standard_name` attribute of `'longitude'`. The case is the same for latitude, except the units are `'degrees_north'` and the `standard_name` is `'latitude'`.

# In[ ]:


lon_var = nc.createVariable('lon', np.float64, ('y', 'x'))
lon_var[:] = lon
lon_var.units = 'degrees_east'
lon_var.standard_name = 'longitude'  # Optional
lon_var.long_name = 'longitude'

lat_var = nc.createVariable('lat', np.float64, ('y', 'x'))
lat_var[:] = lat
lat_var.units = 'degrees_north'
lat_var.standard_name = 'latitude'  # Optional
lat_var.long_name = 'latitude'


# Now that the auxiliary coordinate variables are created, we must identify them as coordinates for the `Temperature` variable. In order to identify the variables in this way, we set the `coordinates` attribute of the `Temperature` variable to a space-separated list of variables to identify, as shown below:

# In[ ]:


temps_var.coordinates = 'lon lat'


# The portion of the CDL showing the new latitude and longitude variables, as well as the updated `Temperature` variable, is listed below:
# ```
#   double lon(y, x);
#     lon:units = "degrees_east";
#     lon:long_name = "longitude coordinate";
#     lon:standard_name = "longitude";
#   double lat(y, x);
#     lat:units = "degrees_north";
#     lat:long_name = "latitude coordinate";
#     lat:standard_name = "latitude";
#   float Temperature(time, y, x);
#     Temperature:units = "Kelvin" ;
#     Temperature:standard_name = "air_temperature" ;
#     Temperature:long_name = "Forecast air temperature" ;
#     Temperature:missing_value = -9999.0 ;
#     Temperature:coordinates = "lon lat";
# ```

# ### Coordinate System Information

# Since the grid containing our data uses a Lambert conformal projection, adding this information to the dataset's metadata can clear up some possible confusion. We can most easily add this metadata information by making use of a "grid mapping" variable. A grid mapping variable is a "placeholder" variable containing all required grid-mapping information. Other variables that need to access this information can then reference this placeholder variable in their `grid_mapping` attribute.
# 
# In this example, we create a grid-mapping variable; this new variable is then set up for a Lambert-conformal conic projection on a spherical globe. By setting this variable's `grid_mapping_name` attribute, we can indicate which CF-supported grid mapping this variable refers to. There are additional attributes that can also be set; however, the available options depend on the specific mapping.

# In[ ]:


proj_var = nc.createVariable('lambert_projection', np.int32, ())
proj_var.grid_mapping_name = 'lambert_conformal_conic'
proj_var.standard_parallel = 25.0
proj_var.latitude_of_projection_origin = 40.0
proj_var.longitude_of_central_meridian = -105.0
proj_var.semi_major_axis = 6371000.0
proj_var


# Now that we have created a grid-mapping variable, we can specify the grid mapping by setting the `grid_mapping attribute` to the variable name. In this example, we set the `grid_mapping` attribute on the `Temperature` variable:

# In[ ]:


temps_var.grid_mapping = 'lambert_projection'  # or proj_var.name


# Here is the portion of the CDL containing the modified `Temperature` variable, as well as the new grid-mapping `lambert_projection` variable:
# ```
#   variables:
#     int lambert_projection ;
#       lambert_projection:grid_mapping_name = "lambert_conformal_conic ;
#       lambert_projection:standard_parallel = 25.0 ;
#       lambert_projection:latitude_of_projection_origin = 40.0 ;
#       lambert_projection:longitude_of_central_meridian = -105.0 ;
#       lambert_projection:semi_major_axis = 6371000.0 ;
#     float Temperature(forecast_time, pressure, y, x) ;
#       Temperature:units = "Kelvin" ;
#       Temperature:standard_name = "air_temperature" ;
#       Temperature:long_name = "Forecast air temperature" ;
#       Temperature:missing_value = -9999.0 ;
#       Temperature:coordinates = "lon lat" ;
#       Temperature:grid_mapping = "lambert_projection" ;
# ```

# ### Cell Bounds
# 
# The use of "bounds" attributes is not required, but highly recommended. Here is a relevant excerpt from the NASA Dataset Interoperability Recommendations:
# > **NASA Dataset Interoperability Recommendations:**
# >
# > Section 2.3 - Use CF "bounds" attributes
# >
# > CF conventions state: "When gridded data does not represent the point values of a field but instead represents some characteristic of the field within cells of finite 'volume,' a complete description of the variable should include metadata that describes the domain or extent of each cell, and the characteristic of the field that the cell values represent."
# 
# In this set of examples, consider a rain gauge which is read every three hours, but only dumped every six hours. The netCDF file for this gauge's data readings might look like this:
#   
# ```
# netcdf precip_bucket_bounds {
#   dimensions:
#       lat = 12 ;
#       lon = 19 ;
#       time = 8 ;
#       tbv = 2;
#   variables:
#       float lat(lat) ;
#       float lon(lon) ;
#       float time(time) ;
#         time:units = "hours since 2019-07-12 00:00:00.00";
#         time:bounds = "time_bounds" ;
#       float time_bounds(time,tbv)
#       float precip(time, lat, lon) ;
#         precip:units = "inches" ;
#   data:
#     time = 3, 6, 9, 12, 15, 18, 21, 24;
#     time_bounds = 0, 3, 0, 6, 6, 9, 6, 12, 12, 15, 12, 18, 18, 21, 18, 24;
# }
# ```
# 
# Considering the coordinate variable for time, and the `bounds` attribute set for this variable, the below graph illustrates the times of the gauge's data readings:
# ```
# |---X
# |-------X
#         |---X
#         |-------X
#                 |---X
#                 |-------X
#                         |---X
#                         |-------X
# 0   3   6   9  12  15  18  21  24
# ```

# <a name="obs"></a>
# ## Observational Data
# 
# Thus far, we have only worked with data arranged on grids. One common type of data, called "in-situ" or "observational" data, is usually arranged in other ways. The CF conventions for this type of data are called *Conventions for DSG (Discrete Sampling Geometries)*.
# 
# For data that are regularly sampled (e.g., from a vertical profiler site), this is straightforward. For these examples, we will be using vertical profile data from three hypothetical profilers, located in Boulder, Norman, and Albany. These hypothetical profilers report data for every 10 m of altitude, from altitudes of 10 m up to (but not including) 1000 m. This first example illustrates how to set up latitude, longitude, altitude, and other necessary data for these profilers:

# In[ ]:


lons = np.array([-97.1, -105, -73.8])
lats = np.array([35.25, 40, 42.75])
heights = np.linspace(10, 1000, 10)
temps = np.random.randn(lats.size, heights.size)
stids = ['KBOU', 'KOUN', 'KALB']


# ### Creation and basic setup
# First, we create a new netCDF file, and define dimensions for it, corresponding to altitude and latitude. Since we are working with observational profile data, we define these dimensions as `heights` and `station`. We then set the global `featureType` attribute to `'profile'`, which defines the file as holding profile data. In these examples, the term "profile data" is defined as "an ordered set of data points along a vertical line at a fixed horizontal position and fixed time". In addition, we define a placeholder dimension called str_len, which helps with storing station IDs as strings.

# In[ ]:


nc.close()
nc = Dataset('obs_data.nc', 'w', format='NETCDF4_CLASSIC', diskless=True)
nc.createDimension('station', lats.size)
nc.createDimension('heights', heights.size)
nc.createDimension('str_len', 4)
nc.Conventions = 'CF-1.7'
nc.featureType = 'profile'
nc


# After this initial setup, the current state of our netCDF file is described in the following CDL:
# ```
# netcdf obs_data {
#   dimensions:
#     station = 3 ;
#     heights = 10 ;
#     str_len = 4 ;
#   attributes:
#     :Conventions = "CF-1.7" ;
#     :featureType = "profile" ;
# }
# ```
# This example illustrates the setup of coordinate variables for latitude and longitude:

# In[ ]:


lon_var = nc.createVariable('lon', np.float64, ('station',))
lon_var.units = 'degrees_east'
lon_var.standard_name = 'longitude'

lat_var = nc.createVariable('lat', np.float64, ('station',))
lat_var.units = 'degrees_north'
lat_var.standard_name = 'latitude'


# When a coordinate variable refers to an instance of a feature, netCDF standards refer to it as an "instance variable". The latitude and longitude coordinate variables declared above are examples of instance variables. In this next example, we create an instance variable for altitude, referred to here as `heights`:

# In[ ]:


heights_var = nc.createVariable('heights', np.float32, ('heights',))
heights_var.units = 'meters'
heights_var.standard_name = 'altitude'
heights_var.positive = 'up'
heights_var[:] = heights


# ### Station IDs
# Using the placeholder dimension defined earlier, we can write the station IDs of our profilers to a variable as well. The variable used to store these station IDs is two-dimensional; however, one of these dimensions only holds metadata designed to aid in converting strings to character arrays. We can also assign the attribute `cf_role` to this variable, with a value of `'profile_id'`.  If certain software programs read this netCDF file, this attribute assists in identifying individual profiles.

# In[ ]:


stid_var = nc.createVariable('stid', 'c', ('station', 'str_len'))
stid_var.cf_role = 'profile_id'
stid_var.long_name = 'Station identifier'
stid_var[:] = stids


# After adding station ID information, our file's updated CDL should resemble this example:
# ```
# netcdf obs_data {
#   dimensions:
#     station = 3 ;
#     heights = 10 ;
#     str_len = 4 ;
#   variables:
#     double lon(station) ;
#       lon:units = "degrees_east" ;
#       lon:standard_name = "longitude" ;
#     double lat(station) ;
#       lat:units = "degrees_north" ;
#       lat:standard_name = "latitude" ;
#     float heights(heights) ;
#       heights:units = "meters" ;
#       heights:standard_name = "altitude";
#       heights:positive = "up" ;
#     char stid(station, str_len) ;
#       stid:cf_role = "profile_id" ;
#       stid:long_name = "Station identifier" ;
#   attributes:
#     :Conventions = "CF-1.7" ;
#     :featureType = "profile" ;
# }
# ```

# ### Writing the field
# The final setup step for this netCDF file is to write our actual profile data to the file. In addition, we add an additional scalar variable, which holds the time of data capture for each profile:

# In[ ]:


time_var = nc.createVariable('time', np.float32, ())
time_var.units = 'minutes since 2019-07-16 17:00'
time_var.standard_name = 'time'
time_var[:] = [5.0]

temp_var = nc.createVariable('temperature', np.float32, ('station', 'heights'))
temp_var.units = 'celsius'
temp_var.standard_name = 'air_temperature'
temp_var.coordinates = 'lon lat heights time'


# The auxiliary coordinate variables in this netCDF file are not proper coordinate variables, and are all associated with the `station` dimension. Therefore, the names of these variables must be listed in an attribute called `coordinates`. The final CDL of the variables, including the `coordinates` attribute, is shown below:
# ```
#   variables:
#     double lon(station) ;
#       lon:units = "degrees_east" ;
#       lon:standard_name = "longitude" ;
#     double lat(station) ;
#       lat:units = "degrees_north" ;
#       lat:standard_name = "latitude" ;
#     float heights(heights) ;
#       heights:units = "meters" ;
#       heights:standard_name = "altitude";
#       heights:positive = "up" ;
#     char stid(station, str_len) ;
#       stid:cf_role = "profile_id" ;
#       stid:long_name = "Station identifier" ;
#     float time ;
#       time:units = "minutes since 2019-07-16 17:00" ;
#       time:standard_name = "time" ;
#     float temperature(station, heights) ;
#       temperature:units = "celsius" ;
#       temperature:standard_name = "air_temperature" ;
#       temperature:coordinates = "lon lat heights time" ;
# ```
# 
# These standards for storing DSG data in netCDF files can be used for profiler data, as shown in these examples, as well as timeseries and trajectory data, and any combination of these types of data models. You can also use these standards for datasets with differing amounts of data in each feature, using so-called "ragged" arrays. For more information on ragged arrays, or other elements of the CF DSG standards, see the [main documentation page](http://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/cf-conventions.html#discrete-sampling-geometries), or try some of the [annotated DSG examples](http://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/cf-conventions.html#appendix-examples-discrete-geometries).

# ---

# ## Summary
# We have created examples of and discussed the structure of **netCDF** `Datasets`, both gridded and in-situ. In addition, we covered the Climate and Forecasting (**CF**) Conventions, and the setup of netCDF files that follow these conventions. netCDF `Datasets` are self-describing; in other words, their attributes, or *metadata*, are included. Other libraries in the Python scientific software ecosystem, such as `xarray` and `MetPy`, are therefore easily able to read in, write to, and analyze these `Datasets`.
# 
# ### What's Next?
# In subsequent notebooks, we will work with netCDF `Datasets` built from actual, non-example data sources, both model and in-situ.

# <a name="references"></a>
# ## Resources and References
# 
# - [CF Conventions doc (1.7)](http://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/cf-conventions.html)
# - [Jonathan Gregory's old CF presentation](http://cfconventions.org/Data/cf-documents/overview/viewgraphs.pdf)
# - [NASA ESDS "Dataset Interoperability Recommendations for Earth Science"](https://earthdata.nasa.gov/user-resources/standards-and-references/dataset-interoperability-recommendations-for-earth-science)
# - [CF Data Model (cfdm) python package tutorial](https://ncas-cms.github.io/cfdm/tutorial.html)
# - [Tim Whiteaker's cfgeom python package (GitHub repo)](https://github.com/twhiteaker/CFGeom) and [(tutorial)]( https://twhiteaker.github.io/CFGeom/tutorial.html)
# - [netCDF4 Documentation](https://unidata.github.io/netcdf4-python/)

# In[ ]:




