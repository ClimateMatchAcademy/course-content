
# separate the positive and negative classes
pos_inds = np.where(y_train == 1)  # indices of positive class (i.e positive class will have y_train as 1)
neg_inds = np.where(y_train == 0)  # indices of negative class (i.e positive class will have y_train as 0)

# create subplots for each feature
for i in range(12):
    plt.subplot(3, 4, i+1)  # create a subplot
    # plot histograms of the positive and negative classes for the current feature
    n, bins, patches = plt.hist(X_train[:, i][pos_inds], alpha=.5)  # histogram of the positive class
    plt.hist(X_train[:, i][neg_inds], bins=bins, alpha=.5)         # histogram of the negative class
    plt.title(feature_names[i])  # set the title of the subplot to the current feature number

plt.tight_layout()  # adjust spacing between subplots
plt.show()          # display the subplots

# calculate % by (number of positive/(number of positive + number of negative)); can use len to
print('Percentage of positive samples: ' + str(len(pos_inds)/(len(pos_inds)+len(neg_inds))))