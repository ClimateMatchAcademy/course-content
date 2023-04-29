
# define the observed reflected radiation based on observations from the IPCC AR6 Figure 7.2
F_ref = 100 # W m^-2

# loop through values of insolation
for Q in [300,340,380]:

  # plug into equation
  alpha = (F_ref/Q) # unitless number between 0 and 1

  # display answer
  print('Insolation:',Q,',        ','albedo: ' ,alpha)