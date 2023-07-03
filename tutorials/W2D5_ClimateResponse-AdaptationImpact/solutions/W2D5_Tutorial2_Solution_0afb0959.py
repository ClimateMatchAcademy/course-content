

# Create a new instance of the LinearRegression class
reg_model = LinearRegression()

# Train the model on the training data
reg_model.fit(df_cleaned_train,cases_train)

# Print the R^2 score of the trained model on the training data
print('r^2 on training data is: ')
print(reg_model.score(df_cleaned_train,cases_train))

# Print the R^2 score of the trained model on the test data
print('r^2 on test data is: ')
print(reg_model.score(df_cleaned_test,cases_test))

# Create a scatter plot of the predicted values vs. the actual values for the test data
plt.scatter(cases_test,reg_model.predict(df_cleaned_test))

# Add axis labels to the scatter plot
plt.xlabel('Actual Number of Dengue Cases')
plt.ylabel('Predicted Number of Dengue Cases')
plt.title('Predicted values vs. the actual values for the test data')