
def calculate_performance(X_train, X_test, y_train, y_test):
    """
    Calculates performance with missing features and only one feature using logistic regression.

    Args:
        X_train (ndarray): The training data.
        X_test (ndarray): The testing data.
        y_train (ndarray): The training labels.
        y_test (ndarray): The testing labels.

    Returns:
        missing_feature_performance (list): A list of performance scores for each missing feature.
        only_feature_performance (list): A list of performance scores for each individual feature.
    """

    missing_feature_performance = []  # Create empty list to store performance scores for each missing feature
    only_feature_performance = []  # Create empty list to store performance scores for each individual feature

    for feature in range(X_train.shape[1]):  # Iterate through each feature in the dataset
        # Remove the feature from both the training and test set
        X_train_reduced = np.delete(X_train, feature, 1)  # Remove feature from training set
        X_test_reduced = np.delete(X_test, feature, 1)  # Remove feature from test set
        reduced_trained_model = LogisticRegression().fit(X_train_reduced, y_train)  # Train a logistic regression model on the reduced training set
        missing_feature_performance.append(reduced_trained_model.score(X_test_reduced, y_test))  # Calculate the score on the reduced test set and append to list

        # Select only the feature from both the training and test set
        X_train_reduced = X_train[:, feature].reshape(-1, 1)  # Select only feature from training set
        X_test_reduced = X_test[:, feature].reshape(-1, 1)  # Select only feature from test set
        reduced_trained_model = LogisticRegression().fit(X_train_reduced, y_train)  # Train a logistic regression model on the reduced training set
        only_feature_performance.append(reduced_trained_model.score(X_test_reduced, y_test))  # Calculate the score on the reduced test set and append to list

    return missing_feature_performance, only_feature_performance

## Uncomment the code below to test your function
#missing_feature_performance, only_feature_performance = calculate_performance(X_train, X_test, y_train, y_test) # Call calculate_performance() function with the training and testing data and the corresponding labels
#plot_feature_performance(missing_feature_performance, only_feature_performance) # Plot the performance scores for each missing feature and each individual feature