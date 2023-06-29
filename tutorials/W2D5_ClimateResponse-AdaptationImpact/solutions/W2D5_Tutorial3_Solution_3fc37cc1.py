
# Import the MLPClassifier from the neural_network module in the sklearn library
from sklearn.neural_network import MLPClassifier

# Set a random seed to ensure reproducibility of results
np.random.seed(144)

# Fit the MLPClassifier model on the training data
trained_model = MLPClassifier().fit(X_train, y_train)

# Print the training accuracy and test accuracy of the model
print(' Training Accuracy: ',  trained_model.score(X_train,y_train))
print(' Test Accuracy:     ',  trained_model.score(X_test,y_test))