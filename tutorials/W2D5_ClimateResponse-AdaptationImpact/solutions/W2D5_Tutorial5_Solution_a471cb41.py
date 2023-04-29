
# Train a random forest regression model
# use the RandomForestRegressor we imported earlier

rf = RandomForestRegressor()
rf.fit(df_cleaned_train, cases_train)

# Evaluate the model's performance on the training and testing data
print('Accuracy on training data is: ')
print(rf.score(df_cleaned_train, cases_train))

print('Accuracy on test data is: ')
print(rf.score(df_cleaned_test, cases_test))

# Plot the predicted vs. actual total cases on the test data
plt.scatter(cases_test, rf.predict(df_cleaned_test))
plt.xlabel('Actual Total Cases')
plt.ylabel('Predicted Total Cases')
plt.title('Random Forest Regression')
plt.show()