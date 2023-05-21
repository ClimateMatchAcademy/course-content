# This code block will plot the CO2 and temperature data as two
# time series
# read SST data
SST = pd.read_table('/content/drive/Shareddrives/Academy/Courses/Climate/Climatematch/02-Curriculum/Climatematch Content Folder/W2D2 - Projects Day /Shakun2015_SST.txt')
SST.set_index('Age', inplace=True)

# read CO2 data
CO2 = pd.read_table('/content/drive/Shareddrives/Academy/Courses/Climate/Climatematch/02-Curriculum/Climatematch Content Folder/W2D2 - Projects Day /antarctica2015co2composite_cleaned.txt')
CO2.set_index('age_gas_calBP', inplace=True)

#%% plot
# set up two subplots in a grid of 2 rows and 1 column
# also make sure the two plots share the same x(time) axis
fig, axes = plt.subplots(2, 1, sharex=True)
# move the two subplots closer to each other
fig.subplots_adjust(hspace=-0.5)
axes[0].plot(SST.index, SST['SST stack'], color='C4')
axes[1].plot(CO2.index/1000, CO2['co2_ppm'], color='C1')

#%% beautification
# since sharex=True in plt.subplots(), this sets the x axis limit for both panels
axes[1].set_xlim((0, 805))
# axis labels
axes[1].set_xlabel('Age (ka BP)')
axes[0].set_ylabel(r'Sea Surface Temperature'
                   '\n'
                   'detrended (°C)',
                   color='C4')
axes[1].set_ylabel(r'CO${}_\mathrm{2}$ (ppm)',
                   color='C1')
# despine makes the plots look cleaner
sns.despine(ax=axes[0], top=True, right=False, bottom=True, left=True)
sns.despine(ax=axes[1], top=True, right=True, bottom=False, left=False)
# clean up top panel x axis ticks
axes[0].xaxis.set_ticks_position('none')
# move top panel xlabel to the right side
axes[0].yaxis.set_label_position('right')
# the following code ensures the subplots don't overlap
for ax in axes:
    ax.set_zorder(10)
    ax.set_facecolor('none')
# color the axis
axes[0].spines['right'].set_color('C4')
axes[1].spines['left'].set_color('C1')
axes[0].tick_params(axis='y', colors='C4')
axes[1].tick_params(axis='y', colors='C1')