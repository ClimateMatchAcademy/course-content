
# initialize a GEV distribution
law_ns_scale = sd.GEV()

# fit the GEV to the data, while specifying that the scale parameter ('scale') is meant to be a covariate ('_c') of the time axis (data.index)
_ = law_ns_scale.fit(data.ssh.values, c_scale = np.arange(data.index.size))

# plot results
data.ssh.plot(c='k')
_ = plt.plot(data.index,estimate_return_level(1-1/2,law_ns_scale),label='2-year return level')
_ = plt.plot(data.index,estimate_return_level(1-1/10,law_ns_scale),label='10-year return level')
_ = plt.plot(data.index,estimate_return_level(1-1/50,law_ns_scale),label='50-year return level')
_ = plt.plot(data.index,estimate_return_level(1-1/100,law_ns_scale),label='100-year return level')
_ = plt.plot(data.index,estimate_return_level(1-1/500,law_ns_scale),label='500-year return level')
plt.legend()
plt.grid(True)
plt.title('Scale as Function of Time')