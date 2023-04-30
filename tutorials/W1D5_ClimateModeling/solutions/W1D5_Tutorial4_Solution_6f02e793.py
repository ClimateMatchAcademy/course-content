
# create a array ot temperatures to evaluates the ASR and OLR at
T = np.arange(220,320,2)

#create empty arrays to fill with values later
ASR = np.zeros_like(T)
OLR = np.zeros_like(T)

# define the slope of the ramp function
m = (0.7-0.3)/(280-250)

# define the observed insolation
Q_vals = [305,340,450,500]# W m^-2

# define the transmissivity (calculated previously from observations)
tau=0.6114 # unitless number between 0 and 1

# define the Stefan-Boltzmann Constant, noting we are using 'e' for scientific notation
sigma = 5.67e-8 # W m^-2 K^-4

for Q in Q_vals:
  # calculate ASR and OLR for different values of T
  for tt, temp in enumerate(T):

      # define the ramp function for albedo
      if temp > 280:
          alpha=0.3
      elif temp>=250:
          alpha=0.3+m*(280-temp)
      else:
          alpha=0.7

      ASR[tt] = (1-alpha)*Q
      OLR[tt] = tau * sigma * temp**4

  # make plots
  plt.plot(T,ASR, label = 'ASR for Q = ' + str(Q))
plt.plot(T,OLR, label = 'OLR')

plt.title('', fontsize=16)
plt.xlabel('Temperature (K)', fontsize=14)
plt.ylabel('Radiative Flux',fontsize=14)
plt.legend()