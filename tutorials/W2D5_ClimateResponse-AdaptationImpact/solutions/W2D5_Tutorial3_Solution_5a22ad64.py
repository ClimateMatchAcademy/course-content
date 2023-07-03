

# Separate the positive and negative classes
pos_inds = np.where(y_train == 1)  # Indices of positive class
neg_inds = np.where(y_train == 0)  # Indices of negative class

# Create subplots for each feature
for i in range(12):
    plt.subplot(3, 4, i+1)  # Create a subplot
    # Plot histograms of the positive and negative classes for the current feature
    n, bins, patches = plt.hist(X_train[:, i][pos_inds], alpha=.5)  # Histogram of the positive class
    plt.hist(X_train[:, i][neg_inds], bins=bins, alpha=.5)         # Histogram of the negative class
    plt.title(f"Feature {i+1}")  # Set the title of the subplot to the current feature number

plt.tight_layout()  # Adjust spacing between subplots
plt.show()          # Display the subplots

print('Percentage of positive samples: ' + str(len(pos_inds)/(len(pos_inds)+len(neg_inds))) )