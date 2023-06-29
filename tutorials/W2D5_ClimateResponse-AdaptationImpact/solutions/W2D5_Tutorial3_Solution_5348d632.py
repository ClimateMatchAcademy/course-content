from sklearn.inspection import permutation_importance

perm_feat_imp = permutation_importance(trained_model, X_test,y_test,
                           n_repeats=10,
                           random_state=0)


plot_permutation_feature_importance(perm_feat_imp, X_test)