import streamlit as st
import numpy as np

from utils.layout import init_streamlit_state_values, init_sidebar

st.session_state = init_streamlit_state_values(st.session_state, st.secrets)
from utils.model_utils import make_prediction

if "model" in st.session_state.keys():
    st.write("You have a model! Let's make a prediction.")

    region = st.selectbox(
        label="Region",
        options=[
            "Asia",
            "Rest of Europe",
            "Africa",
            "Central America and Caribbean",
            "South America",
            "Oceania",
            "European Union",
            "Middle East",
            "North America",
        ],
    )
    year = st.slider(label="Year", min_value=1990, max_value=2030)
    gdp = st.number_input(label="GDP per capita", step=1, value=1, min_value=1)
    population = st.number_input(label="Population (Millions)", step=1, value=1, min_value=1)
    schooling = st.number_input(label="Average number of schooling years", format="%0.1f")
    developed = st.checkbox(label="Developed country?")
    if not st.session_state["exclude_sensitive"]:
        under_five_mort = st.number_input(
            label="Under-five deaths per 1000 population", format="%0.1f"
        )
        adult_mort = st.number_input(
            label="Adult (15-60) deaths per 1000 population", format="%0.4f"
        )
        alcohol = st.number_input(
            label="Litres of pure alcohol consumed per capita", format="%0.2f"
        )
        hepatitis_b = st.number_input(
            label="Hepatitis-B immunisation coverage amongst 1-year-olds", step=1
        )
        measles = st.number_input(label="Reported measles cases per 1000 population", step=1)
        bmi = st.number_input(label="Average population BMI", format="%0.1f")
        diphtheria = st.number_input(label="DTP3 immunisation coverage amongst 1-year-olds", step=1)
        hiv = st.number_input(
            label="HIV incidents per 1000 population among 15-49 year-olds", format="%0.2f"
        )
        thinness = st.number_input(
            label="Percentage of thinness among 10-19 year olds", format="%0.1f"
        )
    if st.button(label="Predict life expectancy"):
        new_data = [year]
        if not st.session_state["exclude_sensitive"]:
            new_data.extend(
                [under_five_mort, adult_mort, alcohol, hepatitis_b, measles, bmi, diphtheria, hiv]
            )
        new_data.extend([np.log(gdp), population])
        if not st.session_state["exclude_sensitive"]:
            new_data.append(thinness)
        region_as = region == "Asia"
        region_ca = region == "Central America and Caribbean"
        region_eu = region == "European Union"
        region_me = region == "Middle East"
        region_na = region == "North America"
        region_oc = region == "Oceania"
        region_re = region == "Rest of Europe"
        region_sa = region == "South America"
        new_data.extend(
            [
                schooling,
                developed,
                region_as,
                region_ca,
                region_eu,
                region_me,
                region_na,
                region_oc,
                region_re,
                region_sa,
            ]
        )

        life_pred = make_prediction(
            st.session_state["data"],
            st.session_state["model"],
            new_data,
            st.session_state["scaler"],
            exclude_sensitive=st.session_state["exclude_sensitive"],
        )
        st.write(life_pred)

else:
    st.write("No model created. Use the button in the sidebar to create one.")

init_sidebar()
