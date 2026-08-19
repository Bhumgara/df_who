import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import statsmodels.tools

# Columns that are dropped regardless:
# Country is a text column and there are too many of them to one-hot encode
# Economy_status_Developing is redundant because it is the direct opposite of Economy_status_Developed
# Infant_deaths is heavily correlated with Under_five deaths
# Polio is heavily correlated with Diphtheria
# Thinness_five_nine_years is heavily correlated with Thinness_ten_nineteen_years
BAD_COLS = ['Infant_deaths', 'Economy_status_Developing', 'Country', 'Thinness_five_nine_years', 'Polio']

# Columns that are dropped if the user wants to exclude sensitive information
SENSITIVE_COLS = ["Under_five_deaths", "Adult_mortality", "Alcohol_consumption", "Hepatitis_B", "Measles", "BMI", "Diphtheria", "Incidents_HIV", "Thinness_ten_nineteen_years"]

# One-hot encodes Region, adds the constant and drops unneeded columns
def feature_eng(df, exclude_sensitive=False):
    df = df.copy()
    df = pd.get_dummies(df, columns = ['Region'], drop_first = True, prefix = 'region', dtype=float)
    df = sm.add_constant(df)
    df = df.drop(columns=BAD_COLS)
    if exclude_sensitive:
        df = df.drop(columns=SENSITIVE_COLS)
    return df

# Predicts using the model to find R^2 and RMSE, reusable for train and test
def model_stats(X, y, results):
    y_pred = results.predict(X)
    rmse = statsmodels.tools.eval_measures.rmse(y, y_pred)
    return results.rsquared, rmse

# Main function called by the Streamlit app
# Outputs the model and stats on the train & test data
def create_model(exclude_sensitive=False):
    df = pd.read_csv('Life Expectancy Data.csv')
    feature_cols = list(df.columns)
    feature_cols.remove('Life_expectancy')
    X = df[feature_cols]
    y = df['Life_expectancy']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    X_train = feature_eng(X_train, exclude_sensitive=exclude_sensitive)
    X_test = feature_eng(X_test, exclude_sensitive=exclude_sensitive)
    X = feature_eng(X, exclude_sensitive=exclude_sensitive)
    lin_reg = sm.OLS(y_train, X_train)
    results = lin_reg.fit()
    train_r2, train_rmse = model_stats(X_train, y_train, results)
    test_r2, test_rmse = model_stats(X_test, y_test, results)
    full_r2, full_rmse = model_stats(X, y, results)
    return results, train_r2, train_rmse, test_r2, test_rmse, full_r2, full_rmse

# results is the already-built model
# X is an array of input values, assumed to already be in order
# exclude_sensitive should have the same value as was inputted for create_model
def make_prediction(results, X, exclude_sensitive=False):
    df = pd.read_csv('Life Expectancy Data.csv')
    feature_cols = list(df.columns)
    feature_cols.remove(BAD_COLS)
    if exclude_sensitive:
        feature_cols.remove(SENSITIVE_COLS)
    df_X = pd.DataFrame([X], columns=feature_cols)
    y = results.predict(df_X)
    return y