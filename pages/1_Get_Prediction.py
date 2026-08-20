import streamlit as st
import numpy as np

from utils.model_utils import create_model, make_prediction

if "model" in st.session_state.keys():
    st.write("You have a model! Let's make a prediction.")

    include_sensitive = st.checkbox(label="Include sensitive columns?")

    region = st.selectbox(label="Region", options=['Asia', 'Rest of Europe', 'Africa',
       'Central America and Caribbean', 'South America', 'Oceania',
       'European Union', 'Middle East', 'North America'])
    year = st.slider(label="Year", min_value=1990, max_value=2030)
    gdp = st.number_input(label="GDP per capita", step=100)
    population = st.number_input(label="Population", step=100000)
    schooling = st.number_input(label="Average number of schooling years", format="%0.1f")
    developed = st.checkbox(label="Developed country?")
    if include_sensitive:
        under_five_mort = st.number_input(label="Under-five deaths per 1000 population", format="%0.1f")
        adult_mort = st.number_input(label="Adult (15-60) deaths per 1000 population", format="%0.4f")
        alcohol = st.number_input(label="Litres of pure alcohol consumed per capita", format="%0.2f")
        hepatitis_b = st.number_input(label="Hepatitis-B immunisation coverage amongst 1-year-olds", step=1)
        measles = st.number_input(label="Reported measles cases per 1000 population", step=1)
        bmi = st.number_input(label="Average population BMI", format="%0.1f")
        diphtheria = st.number_input(label="DTP3 immunisation coverage amongst 1-year-olds", step=1)
        hiv = st.number_input(label="HIV incidents per 1000 population among 15-49 year-olds", format="%0.2f")
        thinness = st.number_input(label="Percentage of thinness among 10-19 year olds", format="%0.1f")
    if st.button(label="Predict life expectancy"):
        new_data = [year]
        if include_sensitive:
            new_data.extend(under_five_mort, adult_mort, alcohol, hepatitis_b, measles, bmi, diphtheria, hiv)
        new_data.extend(np.log(gdp), population)
        if include_sensitive:
            new_data.append(thinness)
        new_data.extend(schooling, developed)
            
else:
    st.write("No model created. Use the button in the sidebar to create one.")

with st.sidebar:
    st.write(
        "Some advanced population data may include protected information. Only uncheck this box if you wish to include this data for better accuracy."
    )
    sensitive = st.checkbox(label="Exclude sensitive data?", value=True)
    if st.button(label="Rebuild model"):
        with st.spinner("Training model..."):
            model, X, stats_df, pred_test, y_test = create_model(
                st.session_state["data"], exclude_sensitive=sensitive
            )

            st.write("Model complete! Head to other pages to use this model.")

            # stash results in session_state so other parts of the app
            st.session_state["model"] = model
            st.session_state["X"] = X
            st.session_state["stats_df"] = stats_df
            st.session_state["pred_test"] = pred_test
            st.session_state["y_test"] = y_test
            st.session_stats["exclude_sensitive"] = sensitive
