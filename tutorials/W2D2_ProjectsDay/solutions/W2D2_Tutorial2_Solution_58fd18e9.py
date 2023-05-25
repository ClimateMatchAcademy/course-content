# In this code block, we will make a scatter plot of CO2 and temperature
# and fit a linear regression model through the data

def age_model_interp(CO2_age, CO2, SST_age):
  '''
  This helper function linearly interpolates CO2 data, which
  have a very high temporal resolution, to temperature data,
  which have a relatively low resolution
  '''
  f = interpolate.interp1d(CO2_age, CO2, fill_value='extrapolate')
  all_ages = f(SST_age)
  return all_ages

# read SST data
SST = pd.read_table('/content/drive/Shareddrives/Academy/Courses/Climate/Climatematch/02-Curriculum/Climatematch Content Folder/W2D2 - Projects Day /Shakun2015_SST.txt')
SST.set_index('Age', inplace=True)

# read CO2 data
CO2 = pd.read_table('/content/drive/Shareddrives/Academy/Courses/Climate/Climatematch/02-Curriculum/Climatematch Content Folder/W2D2 - Projects Day /antarctica2015co2composite_cleaned.txt')
CO2.set_index('age_gas_calBP', inplace=True)

# interpolate CO2 data to SST age
CO2_interpolated = age_model_interp(CO2.index/1000, CO2['co2_ppm'], SST.index)

#%% plot
# set up two subplots in a grid of 2 rows and 1 column
# also make sure the two plots share the same x(time) axis
fig, ax = plt.subplots(1, 1, sharex=True)

ax.scatter(CO2_interpolated, SST['SST stack'], color='gray')

#%% regression
X = CO2_interpolated
X = sm.add_constant(X)  # let's add an intercept (beta_0) to our model
y = SST['SST stack']
mod = sm.OLS(y, X)    # ordinary least sqaure
res = mod.fit()       # Fit model
print(res.summary())   # Summarize model
x_fit = np.arange(180, 280)
y_fit = x_fit * res.params[1] + res.params[0]  # ordinary least square
ax.plot(x_fit, y_fit, color='k')

#%% beautification
# axis labels
ax.set_xlabel(r'CO${}_\mathrm{2}$ (ppm)')
ax.set_ylabel(r'Sea Surface Temperature'
                    '\n'
                    'detrended (°C)')