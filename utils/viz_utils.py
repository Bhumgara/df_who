import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

from utils.data_utils import load_data, format_data


def features_sets(df):
    """
    Read in the dataframe and split the dataframe
    into insensitive and sensitive feature sets.
    Return the two dataframes
    """
    # Insensitive data
    df_insens = df[["GDP_per_capita", "Population_mln", "Economy_status_Developed", "Schooling"]]

    # Sensitive data
    df_sens = df[
        [
            "Infant_deaths",
            "Adult_mortality",
            "Alcohol_consumption",
            "Hepatitis_B",
            "Measles",
            "BMI",
            "Polio",
            "Incidents_HIV",
            "Thinness_ten_nineteen_years",
            "Economy_status_Developed",
            "Schooling",
            "GDP_per_capita",
            "Population_mln",
        ]
    ]

    return df_insens, df_sens


def plot_correlation(feature_df, prov_annot_threshold):
    """
    Plot a seaborn correlation heatmap for the given feature DataFrame.
    """
    annot_threshold = 0
    if len(feature_df.columns) > 7:
        annot_threshold = prov_annot_threshold

    corr_matrix = feature_df.corr()

    annot_df = corr_matrix.applymap(lambda x: f"{x:.2f}" if np.abs(x) > annot_threshold else "")
    sns.heatmap(corr_matrix, annot=annot_df, fmt="")
    plt.title("Correlation heatmap")
    plt.tight_layout()
    plt.show()


def fit_ols(X, y):
    """
    Fit an OLS model using statsmodels and print the summary.

    Read in feature dataframe(X) and target series(y)

    Return OLS results and a matrix with the constant which
    is needed for VIF
    """
    X_const = sm.add_constant(X)
    results = sm.OLS(y, X_const).fit()
    print(results.summary())
    return results, X_const


def compute_vif(X_const):
    """
    Compute VIF for every column in the matrix.

    Reads in the matrix with constant

    Returns a VIF dataframe and prints the VIF values
    for the dataframe
    """
    # Calculates VIF for each variable
    vif_values = [variance_inflation_factor(X_const.values, i) for i in range(X_const.shape[1])]

    # Tidies up VIF_values into a dataframe
    vif_df = pd.Series(vif_values, index=X_const.columns).rename("VIF").to_frame().round(2)

    print(vif_df)
    return vif_df


def train_evaluate(X, y):
    """
    Split, scale, train a LinearRegression, and return predictions + metrics.

    Takes in dataframe (X), target series(y)

    Returns test set predictions(test_pred), test set actuals (y_test), metrics (metrics_df)
    scaler (fitted StandardScaler) and model (fitted LinearRegression)
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LinearRegression().fit(X_train_scaled, y_train)
    train_pred = model.predict(X_train_scaled)
    test_pred = model.predict(X_test_scaled)

    # Returns metrics for given parameters
    def _row(split, y_true, y_pred):
        return {
            "Split": split,
            "R²": round(metrics.r2_score(y_true, y_pred), 4),
            "RMSE": round(metrics.root_mean_squared_error(y_true, y_pred), 4),
            "MAE": round(metrics.mean_absolute_error(y_true, y_pred), 4),
            "MAPE%": round(metrics.mean_absolute_percentage_error(y_true, y_pred) * 100, 2),
        }

    metrics_df = pd.DataFrame([_row("Train", y_train, train_pred), _row("Test", y_test, test_pred)])
    return test_pred, y_test, metrics_df, scaler, model


def plot_residuals(test_pred, y_test, axes):
    """
    Plot residuals vs fitted values and a residual histogram.
    """
    residuals = y_test - test_pred

    axes[0].scatter(test_pred, residuals, alpha=0.3)
    axes[0].axhline(0, color="red", linestyle="--")
    axes[0].set_xlabel("Predicted life expectancy")
    axes[0].set_ylabel("Residual")
    axes[0].set_title("Model — residuals vs fitted")

    sns.histplot(residuals, bins=40, ax=axes[1])
    axes[1].set_title("Residual distribution")

    plt.tight_layout()
    plt.show()


def compare_models(insens_metrics, sens_metrics):  # FIX 1: typo 'inens_metrics' -> 'insens_metrics'
    """
    Build a side-by-side test-set comparison table for the two models.

    Reads in insensitive (insens_metrics) and sensitive (sens_metrics) metrics
    from train_evaluate to compare the two.

    Returns a dataframe with one row per model showing test scores (comparison)
    """

    # Function takes model name (label = 'insens' or 'sens', n_features(feature size) and mdf(metrics from train_evaluate)
    def _test_row(label, n_features, mdf):
        row = mdf.set_index("Split").loc["Test"].to_dict()
        return {"Model": label, "Features": n_features, **row}

    comparison = pd.DataFrame(
        [
            _test_row("Insensitive", 4, insens_metrics),
            _test_row("Sensitive", 13, sens_metrics),
        ]
    ).rename(
        columns={"R²": "Test R²", "RMSE": "Test RMSE", "MAE": "Test MAE", "MAPE%": "Test MAPE%"}
    )

    print("\nModel comparison (test set):")
    print(comparison.to_string(index=False))

    return comparison


def plot_actual_vs_predicted(pairs):
    """
    Scatter plot of actual vs predicted life expectancy.

    Reads in a list of test_pred and y_true tuples (pairs)
    """

    for test_pred, y_true in pairs:
        plt.scatter(y_true, test_pred, alpha=0.3)
        lo = min(y_true.min(), test_pred.min()) - 1
        hi = max(y_true.max(), test_pred.max()) + 1
        plt.plot([lo, hi], [lo, hi], "r--", label="Perfect fit")

    plt.xlabel("Actual life expectancy")
    plt.ylabel("Predicted life expectancy")

    plt.tight_layout()
    plt.show()


def run_full_analysis(filepath):
    """
    Run the complete life expectancy analysis pipeline. This function
    loads the data, defines feature sets, calculates the simple model,
    the complex model, checks for multicollinearity, and produces model
    comparisons and visualisations

    Reads in filepath

    Returns all the dictionaries with keys for the functions called.
    """
    # -- Load -------------------------------------------------------------
    df = load_data(filepath)

    df, y = format_data(df)

    # -- Feature sets -----------------------------------------------------
    df_insens, df_sens = features_sets(df)

    # -- Section 1 — Insensitive model ------------------------------------
    plot_correlation(df_insens)

    results_insens, X_insens = fit_ols(df_insens, y)

    vif_insens = compute_vif(X_insens)

    test_pred_insens, y_test_insens, insens_metrics, _, _ = train_evaluate(df_insens, y)
    print(insens_metrics)

    plot_residuals(test_pred_insens, y_test_insens)

    # -- Section 2 — Sensitive model --------------------------------------
    plot_correlation(df_sens)

    results_sens, X_sens = fit_ols(df_sens, y)

    vif_sens = compute_vif(X_sens)

    test_pred_sens, y_test_sens, sens_metrics, _, _ = train_evaluate(df_sens, y)
    print("\nComplex model metrics:")
    print(sens_metrics)

    plot_residuals(test_pred_sens, y_test_sens)

    # -- Section 3 — Model Comparison -------------------------------------
    comparison = compare_models(insens_metrics, sens_metrics)

    plot_actual_vs_predicted(
        [
            (test_pred_insens, y_test_insens, "Simple model"),
            (test_pred_sens, y_test_sens, "Complex model"),
        ]
    )

    return {
        "df": df,
        "y": y,
        "df_insens": df_insens,
        "df_sens": df_sens,
        "results_insens": results_insens,
        "results_sens": results_sens,
        "vif_insens": vif_insens,
        "vif_sens": vif_sens,
        "insens_metrics": insens_metrics,
        "sens_metrics": sens_metrics,
        "comparison": comparison,
        "test_pred_insens": test_pred_insens,
        "y_test_insens": y_test_insens,
        "test_pred_sens": test_pred_sens,
        "y_test_sens": y_test_sens,
    }


if __name__ == "__main__":
    run_full_analysis("Life Expectancy Data.csv")
