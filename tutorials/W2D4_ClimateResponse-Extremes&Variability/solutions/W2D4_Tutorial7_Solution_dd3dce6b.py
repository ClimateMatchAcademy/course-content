
# initialize a GEV distribution
law_ns_shape = sd.GEV()

# fit the GEV to the data, while specifying that the shape parameter ('shape') is meant to be a covariate ('_c') of the time axis (data.index)
_ = law_ns_shape.fit(data.ssh.values, c_shape = np.arange(data.index.size))

# plot results
data.ssh.plot(c='k')
_ = plt.plot(data.index,estimate_return_level(1-1/2,law_ns_shape),label='2-year return level')
_ = plt.plot(data.index,estimate_return_level(1-1/10,law_ns_shape),label='10-year return level')
_ = plt.plot(data.index,estimate_return_level(1-1/50,law_ns_shape),label='50-year return level')
_ = plt.plot(data.index,estimate_return_level(1-1/100,law_ns_shape),label='100-year return level')
_ = plt.plot(data.index,estimate_return_level(1-1/500,law_ns_shape),label='500-year return level')
plt.legend()
plt.grid(True)
plt.title('Shape as Function of Time')