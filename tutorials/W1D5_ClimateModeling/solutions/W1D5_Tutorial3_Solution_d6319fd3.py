
# define albedo
alpha = 0.2 # unitless number

# define transmissivity (calculated previously from observations in tutorial 1)
tau = 0.6127 # unitless number between 0 and 1

# define the time interval, one year expressed in seconds
dt = 60. * 60. * 24. * 365.

# define the number of timesteps (years) to run the model
numtsteps = 15

# for converting number of seconds in a year
sec_2_yr = 3.154e7

# define empty arrays to store the time series of temperature and the corresponding years
T_series = np.zeros((numtsteps+1))
t_series = np.zeros((numtsteps+1))

# define the intial temperature
T_series[0] = 288.

# run the model
for n in range(numtsteps):
    t_series[n+1] = (n+1)*dt/sec_2_yr
    T_series[n+1] = step_forward( T_series[n], alpha = alpha, tau = tau )

plt.plot(t_series, T_series)

plt.xlabel('Years')
plt.ylabel('Global mean temperature (K)');