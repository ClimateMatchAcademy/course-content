
def evaluate_model_performance(trained_model, X_test, y_test):
    """
    Evaluate the performance of a trained model on a given test set.

    Parameters:
    trained_model (sklearn estimator): A trained scikit-learn estimator.
    X_test (array-like): Test input data.
    y_test (array-like): True labels for the test data.

    Returns:
    test_recall (float): The recall score on the test set.
    test_precision (float): The precision score on the test set.
    """
    # Use the trained model to make predictions on the test set
    pred_test = trained_model.predict(X_test)

    # Calculate the recall and precision scores on the test set
    test_recall = skm.recall_score(y_test, pred_test)
    test_precision = skm.precision_score(y_test, pred_test)

    # Return the recall and precision scores
    return test_recall, test_precision

# Evaluate the performance of the trained model on the test set
## Uncomment the code below to test your function
test_recall, test_precision = evaluate_model_performance(trained_model, X_test, y_test)
