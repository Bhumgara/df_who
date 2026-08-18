import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import statsmodels.tools

def feature_eng(df, exclude_sensitive=False):
    BAD_COLS = ['Infant_deaths', 'Economy_status_Developed', 'Economy_status_Developing', 'Country', 'Diphtheria', 'Thinness_five_nine_years', 'Population_mln', 'Polio', 'Measles', 'Alcohol_consumption']
    SENSITIVE_COLS = ['Hepatitis_B', 'BMI', 'Incidents_HIV', 'Thinness_ten_nineteen_years']
    df = df.copy()
    df = pd.get_dummies(df, columns = ['Region'], drop_first = True, prefix = 'region', dtype=float)
    df = sm.add_constant(df)
    df = df.drop(columns=BAD_COLS)
    if exclude_sensitive:
        df = df.drop(columns=SENSITIVE_COLS)
    return df

def model_stats(X, y):
    y_pred = results.predict(X)
    rmse = statsmodels.tools.eval_measures.rmse(y, y_pred)
    return results.rsquared, rmse

def create_model(exclude_sensitive=False):
    df = pd.read_csv('Life Expectancy Data.csv')
    feature_cols = list(df.columns)
    feature_cols.remove('Life_expectancy')
    X = df[feature_cols]
    y = df['Life_expectancy']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    X_train = feature_eng(X_train, exclude_sensitive=exclude_sensitive)
    X_test = feature_eng(X_test, exclude_sensitive=exclude_sensitive)
    lin_reg = sm.OLS(y_train, X_train)
    results = lin_reg.fit()
    train_r2, train_rmse = model_stats(X_train, y_train)
    test_r2, test_rmse = model_stats(X_test, y_test)
    return results, train_r2, train_rmse, test_r2, test_rmse

def make_prediction(results, cols, X):
    df_X = pd.DataFrame(X, columns=cols)
    y = results.predict(df_X)
    return y