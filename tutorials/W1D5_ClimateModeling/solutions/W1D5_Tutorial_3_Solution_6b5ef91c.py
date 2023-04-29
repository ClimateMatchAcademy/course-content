
# one year expressed in seconds
one_yr = 60. * 60. * 24. * 365.

# legend labels
labels = ['dt = half-year','dt = one year','dt = five years']

# define the number of timesteps (years) to run the model
numtsteps = np.array([10,5,1])*3

 # for converting number of seconds in a year
sec_2_yr = 3.154e7

# loop through each choice of time step
for dd,dt in enumerate([one_yr*0.5,one_yr,one_yr*5]):

  # define empty arrays to store the time series of temperature and the corresponding years
  T_series = np.zeros((numtsteps[dd]+1))
  t_series = np.zeros((numtsteps[dd]+1))

  # define the intial temperature
  T_series[0] = 288.

  # run the model
  for n in range(numtsteps[dd]):
      t_series[n+1] = (n+1)*dt/sec_2_yr
      T_series[n+1] = step_forward( T_series[n], alpha = alpha, tau = tau )

  plt.plot(t_series, T_series, label = labels[dd])

plt.xlabel('Years')
plt.ylabel('Global mean temperature (K)');
plt.legend()
