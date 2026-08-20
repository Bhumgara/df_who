import pandas as pd
import numpy as np


def clean_data(df):
    """
    Clean and format a dataset by handling NaN values, correcting data types,
    and validating ranges.

    Parameters
    ----------
    df : pd.DataFrame
        Raw input DataFrame

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame
    """
    # Make a copy to avoid modifying original
    df_clean = df.copy()

    # 1. Handle data types
    # Convert Year to int
    df_clean["Year"] = df_clean["Year"].astype(int)

    # Convert numerical columns to float
    numerical_cols = [
        "Infant_deaths",
        "Under_five_deaths",
        "Adult_mortality",
        "Alcohol_consumption",
        "Hepatitis_B",
        "Measles",
        "BMI",
        "Polio",
        "Diphtheria",
        "Incidents_HIV",
        "GDP_per_capita",
        "Population_mln",
        "Thinness_ten_nineteen_years",
        "Thinness_five_nine_years",
        "Schooling",
        "Life_expectancy",
    ]

    for col in numerical_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(float)

    # Convert economy status to int
    for col in ["Economy_status_Developed", "Economy_status_Developing"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(int)

    # 2. Handle NaN values
    # Drop rows where target variable is NaN
    if "Life_expectancy" in df_clean.columns:
        df_clean = df_clean.dropna(subset=["Life_expectancy"])

    # Impute numerical columns with median
    for col in numerical_cols:
        if col in df_clean.columns and col != "Life_expectancy":
            median_val = df_clean[col].median()
            df_clean[col] = df_clean[col].fillna(median_val)

    # Drop rows with NaN in categorical columns
    categorical_cols = ["Country", "Region"]
    for col in categorical_cols:
        if col in df_clean.columns:
            df_clean = df_clean.dropna(subset=[col])

    # 3. Validate and clip impossible ranges
    # Life expectancy: 0-120
    if "Life_expectancy" in df_clean.columns:
        df_clean["Life_expectancy"] = df_clean["Life_expectancy"].clip(0, 120)

    # BMI: 10-50 (reasonable human range)
    if "BMI" in df_clean.columns:
        df_clean["BMI"] = df_clean["BMI"].clip(10, 50)

    # Alcohol consumption: 0-20 (liters per year, realistic max)
    if "Alcohol_consumption" in df_clean.columns:
        df_clean["Alcohol_consumption"] = df_clean["Alcohol_consumption"].clip(0, 50)

    # Infant deaths: 0-1000 (per 1000 births)
    if "Infant_deaths" in df_clean.columns:
        df_clean["Infant_deaths"] = df_clean["Infant_deaths"].clip(0, 1000)

    # Under five deaths: 0-1000 (per 1000 population)
    if "Under_five_deaths" in df_clean.columns:
        df_clean["Under_five_deaths"] = df_clean["Under_five_deaths"].clip(0, 1000)

    # Adult mortality: 0-1000 (per 1000 population)
    if "Adult_mortality" in df_clean.columns:
        df_clean["Adult_mortality"] = df_clean["Adult_mortality"].clip(0, 1000)

    # Vaccination rates (Hepatitis_B, Polio, Diphtheria, Measles): 0-100
    for col in ["Hepatitis_B", "Polio", "Diphtheria", "Measles"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].clip(0, 100)

    # Schooling: 0-25 (years spent for people 25+)
    if "Schooling" in df_clean.columns:
        df_clean["Schooling"] = df_clean["Schooling"].clip(0, 25)

    # Thinness percentages: 0-100
    for col in ["Thinness_ten_nineteen_years", "Thinness_five_nine_years"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].clip(0, 100)

    # GDP per capita: 50-500000 (USD, realistic range)
    if "GDP_per_capita" in df_clean.columns:
        df_clean["GDP_per_capita"] = df_clean["GDP_per_capita"].clip(50, 500000)

    # Population: 0.1-2000 (millions)
    if "Population_mln" in df_clean.columns:
        df_clean["Population_mln"] = df_clean["Population_mln"].clip(0.1, 2000)

    # HIV incidents: 0-1000 (per 1000 population)
    if "Incidents_HIV" in df_clean.columns:
        df_clean["Incidents_HIV"] = df_clean["Incidents_HIV"].clip(0, 1000)

    # 4. Reset index after dropping rows
    df_clean = df_clean.reset_index(drop=True)

    return df_clean


def load_data(filepath):
    """
    Read in filepath as a parameter
    and return the dataframe as well as define
    what the target column is
    """
    df = pd.read_csv(filepath)
    df = clean_data(df=df)
    return df


def format_data(df):
    df_ex = df.copy()
    y = df_ex["Life_expectancy"]
    df_ex.drop(columns=["Life_expectancy"], inplace=True)
    return df_ex, y
