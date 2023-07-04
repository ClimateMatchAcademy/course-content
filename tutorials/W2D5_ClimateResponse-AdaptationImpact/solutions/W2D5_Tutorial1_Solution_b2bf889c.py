
# generate 100 numbers from a Gaussian distribution with zero mean
x_1_test2 = np.random.randn(data_points)
x_2_test2 = np.random.randn(data_points)

# create an array of x values
regressors_test2 = np.array([x_1_test2, x_2_test2])

# assuming a different relationship (beta = .8), we can calculate the true y values:
beta = 0.8
y_test2 = y_func(np.array([beta, 1 - beta]), regressors_test2, alpha)

# use the logistic regression model to make predictions on the new x values
preds = logreg_model.predict(regressors_test2.T)

# calculate the confusion matrix for the model's predictions
cm = confusion_matrix(y_test2, preds)

# visualize the confusion matrix as an image with labeled ticks
_ = plt.imshow(cm)
plt.xticks([0, 1])
plt.yticks([0, 1])
plt.ylabel("true category")
plt.xlabel("predicted category")
# Add colorbar
_ = plt.colorbar()

# Print the percent of correct predictions by the logistic regression model
"Percent correct is " + str(100 * logreg_model.score(regressors_test2.T, y_test2))