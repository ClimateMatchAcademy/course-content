
# bin size of 500
tang_bin_500 = ts_tang.bin(bin_size = 500)

# bin size of 1000
tang_bin_1000 = ts_tang.bin(bin_size = 1000)

# plot
fig,ax=plt.subplots() # assign a new plot axis
ts_tang.plot(ax=ax,label='Original',invert_yaxis=True)
tang_bin.plot(ax=ax,label='Binned Default')
tang_bin_500.plot(ax=ax,label='Binned 500yrs')
tang_bin_1000.plot(ax=ax,label='Binned 1000yrs')