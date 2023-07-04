
# define the emission temperature of the sun
T_sun = 5800  # K

# define constants used in Planck's Law
h = 6.626075e-34    # J s
c = 2.99792e+8      # m s^-1
k = 1.3804e-23      # W K^-1

# define the function for Planck's Law that returns the intensity as well
# as the peak wavelength defined by Wien's Law
def planck(wavelength, temperature):
    a = 2.0*h*c**2
    b = h*c/(wavelength*k*temperature)
    intensity = a/ ( (wavelength**5) * (np.exp(b) - 1.0) )

    lpeak = (2.898 * 1e-3)/temperature

    return intensity,lpeak

# generate x-axis in increments from 1um to 100 micrometer in 1 nm increments
# starting at 1 nm to avoid wav = 0, which would result in division by zero.
wavelengths = np.arange(1e-7, 4e-6, 1e-9)

# intensity and peak radiating wavelength at different temperatures
intensity, lpeak = planck(wavelengths, T_sun)

# get the intensity at peak wavelength to limit the lines
Ipeak, _ = planck(lpeak, T_sun)


# plot an approximation of the visible range by defining a dictionary with
# wavelength ranges and colors
rainbow_dict= { (.4, .44): '#8b00ff', (.44, .46): '#4b0082',
                (.46, .5): '#0000ff', (.5, .57): '#00ff00',
                (.57, .59): '#ffff00', (.59, .62): '#ff7f00',
                (.62, .75): '#ff0000'}
for wv_range, rgb in rainbow_dict.items():
    plt.axvspan(*wv_range, color=rgb,ec = 'none')


# add in wiens law
plt.vlines(x=lpeak*1e6,ymin = 0,ymax = Ipeak,color= 'k', ls = '--', lw = 3)


# plot intensity curve
plt.plot(wavelengths*1e6, intensity, lw = 4, label = 'T=' + str(T_sun) + 'K', color= 'k')


plt.xlabel('Wavelength ($\mu m$)', fontsize=20, labelpad=30)
plt.ylabel('$B_\lambda(\lambda,T)$ $(W/(m^3 steradian)$',fontsize = 20)

plt.xticks(fontsize = 16)
plt.yticks(fontsize = 16)

plt.title ('Spectral Radiance')

# add legend
plt.legend(bbox_to_anchor=(.5, .5))