try:
    import joblib
except ImportError:
    from sklearn.externals import joblib

loaded_model = joblib.load('predictor.pkl')

X_TEST = [[1, 2, 5]]
outcome = loaded_model.predict(X=X_TEST)
coefficients = loaded_model.coef_

print('Outcome : {}\nCoefficients : {}'.format(outcome, coefficients))