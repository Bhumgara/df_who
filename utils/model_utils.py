"""
create_model is the main function.

Required input: whether to include sensitive columns, csv file name

Output:
results: model to make future predictions
--> Used for the Get Prediction function
X: post-FE columns (including const)
--> Used for plot_correlation and compute_vif
stats_df: DataFrame containing the R^2, RMSE and MAE of the model on the train, test and full data
--> Not used in the visualisation functions
pred_test, y_test: the model's predictions on the test data & the actual test data
--> Both used for plot_residuals and plot_actual_vs_predicted
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import statsmodels.tools

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.preprocessing import StandardScaler

from statsmodels.stats.outliers_influence import variance_inflation_factor

from utils.data_utils import format_data

# Columns that are dropped regardless:
# Country is a text column and there are too many of them to one-hot encode
# Economy_status_Developing is redundant because it is the direct opposite of Economy_status_Developed
# Infant_deaths is heavily correlated with Under_five deaths
# Polio is heavily correlated with Diphtheria
# Thinness_five_nine_years is heavily correlated with Thinness_ten_nineteen_years
BAD_COLS = [
    "Infant_deaths",
    "Economy_status_Developing",
    "Country",
    "Thinness_five_nine_years",
    "Polio",
]

# Columns that are dropped if the user wants to exclude sensitive information
SENSITIVE_COLS = [
    "Under_five_deaths",
    "Adult_mortality",
    "Alcohol_consumption",
    "Hepatitis_B",
    "Measles",
    "BMI",
    "Diphtheria",
    "Incidents_HIV",
    "Thinness_ten_nineteen_years",
]


def feature_eng(df, exclude_sensitive=False):
    """
    One-hot encodes Region and drops unneeded columns
    Transforms GDP per capita into log for better performance
    """
    df = df.copy()
    df["GDP_per_capita"] = np.log(df["GDP_per_capita"])
    df = pd.get_dummies(df, columns=["Region"], drop_first=True, prefix="region", dtype=float)
    df = df.drop(columns=BAD_COLS)
    if exclude_sensitive:
        df = df.drop(columns=SENSITIVE_COLS)
    return df


def model_stats(X, y, results, type):
    """
    Predicts using the model to find R^2, RMSE and MAE, reusable for train and test
    """
    y_pred = results.predict(X)
    rmse = statsmodels.tools.eval_measures.rmse(y, y_pred)

    return {
        "Split": type,
        "R_Squared": round(results.rsquared, 4),
        "RMSE": round(statsmodels.tools.eval_measures.rmse(y, y_pred), 4),
        "MAE": round(statsmodels.tools.eval_measures.meanabs(y, y_pred), 4),
    }, y_pred


def create_model(df, exclude_sensitive=False):
    """
    Main function called by the Streamlit app
    Outputs the model and stats on the train & test data
    """

    X, y = format_data

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    X_train = feature_eng(X_train, exclude_sensitive=exclude_sensitive)
    X_test = feature_eng(X_test, exclude_sensitive=exclude_sensitive)
    X = feature_eng(X, exclude_sensitive=exclude_sensitive)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    X_full = scaler.transform(X)

    X_train = sm.add_constant(X_train)
    X_test = sm.add_constant(X_test)
    X_full = sm.add_constant(X_full)

    lin_reg = sm.OLS(y_train, X_train)
    results = lin_reg.fit()

    train_stats, pred_train = model_stats(X_train, y_train, results, "Train data")
    test_stats, pred_test = model_stats(X_test, y_test, results, "Test data")
    full_stats, pred_full = model_stats(X_full, y, results, "Full data")
    stats_df = pd.DataFrame([train_stats, test_stats, full_stats])

    X = X.select_dtypes(include="number")

    return results, X, stats_df, pred_test, y_test


def make_prediction(results, X, exclude_sensitive=False, csv="Life Expectancy Data.csv"):
    """
    results is the already-built model
    X is an array of input values, assumed to already be in order
    exclude_sensitive should have the same value as was inputted for create_model
    """
    df = pd.read_csv(csv)
    feature_cols = list(df.columns)
    feature_cols.remove(BAD_COLS)
    if exclude_sensitive:
        feature_cols.remove(SENSITIVE_COLS)
    df_X = pd.DataFrame([X], columns=feature_cols)
    y = results.predict(df_X)
    return y
