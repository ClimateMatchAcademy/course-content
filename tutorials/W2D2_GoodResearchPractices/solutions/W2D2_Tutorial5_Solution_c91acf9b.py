# set up a random number generator
rng = np.random.default_rng()
# x is one hundred random numbers between 0 and 1
x = rng.random(100)
# y is one hundred random numbers according to the relationship y = 1.6x + 0.5
y = 1.6*x + rng.random(100)

#%% plot
plt.scatter(x, y, color='gray')

#%% regression
x = sm.add_constant(x)  # let's add an intercept (b in y=mx+b) to our model
mod = sm.OLS(y, x)    # ordinary least sqaure
res = mod.fit()       # Fit model
print(res.summary())   # Summarize model
plt.plot(x, x*res.params[1]+res.params[0], color='k')