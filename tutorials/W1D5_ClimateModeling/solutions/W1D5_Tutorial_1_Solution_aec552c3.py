
# define the Stefan-Boltzmann Constant, noting we are using 'e' for scientific notation
sigma = 5.67e-8 # W m^-2 K^-4

# define the emission temperature based on observtions of global mean surface temperature
T = 288 # K

# loop through values of tau
for tau in [0.2,0.6127,0.8]:

  # plug into equation
  OLR = tau *sigma*(T**4)

  # display answer
  print('Transmissivity:',tau,',     ' 'OLR: ' ,OLR, 'W m^2')