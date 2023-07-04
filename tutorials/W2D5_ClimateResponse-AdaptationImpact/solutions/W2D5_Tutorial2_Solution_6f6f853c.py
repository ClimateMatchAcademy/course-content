
# train a random forest regression model

# use the RandomForestRegressor we imported earlier
rf = RandomForestRegressor()

# run fit on 'df_cleaned_train' and 'cases_train'
_ = rf.fit(df_cleaned_train, cases_train)

# evaluate the model's performance on the training and testing data
# calculate accuracy by calling rf.score() on 'df_cleaned_train' and 'cases_train'
print('R^2 on training data is: ')
print(rf.score(df_cleaned_train, cases_train))

print('R^2 on test data is: ')
print(rf.score(df_cleaned_test, cases_test))

# add 1:1 line
axes = plt.gca()
plt.plot(np.array(axes.get_xlim()), np.array(axes.get_xlim()), 'k-')

# plot the predicted vs. actual total cases on the test data
_ = plt.scatter(cases_test, rf.predict(df_cleaned_test))
plt.xlabel('Actual Total Cases')
plt.ylabel('Predicted Total Cases')
plt.title('Random Forest Regression')
plt.show()