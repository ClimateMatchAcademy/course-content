
fig, ax = plt.subplots()
# multiply Qglobal by 1000 to put in units of grams water vapor per kg of air
ax.plot(Qglobal*1000., Qglobal.lev, label = 'Specific humidity (g/kg)')
# multiply by 1E6 to get units of ppmv = parts per million by volume
ax.plot(radmodel.absorber_vmr['O3']*1E6,radmodel.lev, label = 'Ozone (ppmv)')

# pressure decreases logarithmically with height in the atmosphere
# invert the axis so the largest value of pressure is lowest
ax.invert_yaxis()
# set y axis to a log scale
plt.yscale('log')

ax.set_ylabel('Pressure (hPa)')

# turn on the grid lines
ax.grid()

# turn on legend
plt.legend()