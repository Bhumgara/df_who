import streamlit as st

from utils.layout import render_header, bordered_section

st.set_page_config(
    page_title="WHO Life Expectancy Explorer",
    layout="wide",
)

# --- Header ---
render_header(
    page_title="WHO Life Expectancy Explorer",
    page_subtitle="Predicting life expectancy from WHO development indicators",
)

# --- Project overview ---
with bordered_section("About this project"):
    st.write("""
        Life expectancy is a statistical measurement used to estimate an individual's lifespan.

        At an individual level, life expectancy is important for determining plans, support, and care. At a larger-group level, it has significant socioeconomic implications.

        At a country level, life expectancy data can be used to derive insights, perform analytics, and support further studies into population needs and risk factors.
        """)
    st.write("""
        #### Goals
        The data analytics team must produce predictions of life expectancy across countries globally.

        The data was provided by the World Health Organisation (WHO). It contains records from:

        - 2000 to 2015.
        - 179 countries.
        """)

st.write("")

# --- What you can do here ---
with bordered_section("What you can do here"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Get a prediction**")
        st.write("Take your own data records and input them for a prediction of life expectancy.")

    with col2:
        st.markdown("**Rebuild the model**")
        st.write(
            "You can rebuild either a sensitive or insensitve model version with your own set random state."
        )

    with col3:
        st.markdown("**Compare model metrics**")
        st.write("You can compare how the two models, sensitive and insensitive compare.")

st.write("")

# --- Challenges & oddities ---
# TODO: replace with real write-up, e.g. multicollinearity found via VIF, and the sensitive-vs-insensitive feature framing.
with bordered_section("Challenges & oddities"):
    st.write("""
        #### Multicollinearity choices
        We identified three pairs of potential features that largely increased VIF due to high correlation.
        Below, with the assistance of AI research tools, and thorough research, we have identified two to three reasons for keeping one factor over the other.
        """)
    st.write("""
        ##### Choosing Diptheria over Polio
        > Gold Standard for Routine Health Systems: The World Health Organisation (WHO) officially uses DTP3 coverage as the primary international benchmark to measure the strength and reach of a country's routine everyday healthcare system. [WHO Indicator: DTP3 immunization coverage among 1-year-olds (%)](https://www.who.int/data/gho/indicator-metadata-registry/imr-details/88) [Poliomyelitis vaccination coverage - Reference](https://immunizationdata.who.int/global/wiise-detail-page/poliomyelitis-vaccination-coverage?CODE=Global&ANTIGEN=&YEAR=)

        > Shows clinic quality: Polio drops are often handed out quickly on the street, but DTP3 shots require an actual clinic visit. High DTP3 rates prove a country has real, clean hospitals for mothers and babies, which naturally keeps people living longer.
        """)

    st.write("""
        ##### Choosing Under-five deaths over Infant deaths
        > Captures Broader Socioeconomic Strain: Under-five deaths captures the extended risks a child faces as they transition to solid foods and interact with the environment, making it a better reflection of long-term malnutrition, unsafe water, and poverty.

        > Mathematical Inclusivity: Because under-five deaths mathematically includes infant deaths, choosing this variable ensures you do not lose the infant data; you simply expand it to include the critical toddler years. [WHO Indicator: Under-five mortality rate (per 1000 live births)](https://www.who.int/data/gho/indicator-metadata-registry/imr-details/7)
        """)

    st.write("""
        ##### Choosing Thinness 10-19 over Thinness 5-9
        > Captures Adolescent Growth Spurts: The 10-19 age bracket spans puberty, a critical developmental window where nutritional deficits cause severe, permanent stunting and lifelong health impacts.

        > Reflects School-Age and Independence Risks: This older cohort reflects the cumulative impact of school nutrition programmes (or lack thereof) and independent dietary habits, showing how health shifts as children grow outside early maternal care.

        > Showcases Continuance of Life Expectancy: Extending the tracked window to age 5 bridges the gap to overall life expectancy. Since the sharpest drop in early-life mortality happens before age 5, capturing survival past this critical threshold serves as a stronger baseline for predicting long-term survival and overall lifespan trends.
                
        """)

    st.info("TODO: replace this callout with a specific oddity")

with bordered_section("Assumptions"):
    st.subheader("Data validity")
    st.write("Our presumption is that the dataset we've been provided is up-to-date.")
    st.write(
        "After combing through the data we can confirm that the data is clean, and that there are no expected outliers."
    )
    st.subheader("Metadata")
    st.write(
        "The original metadata provided was out-of-date, so we have since sourced fresher and more relevant metadata descriptions."
    )
    st.subheader("Audience")
    st.write(
        "We have assumed that the audience have a decent-level of technical knowledge, so we shouldn't reduce complexity for non-technical users."
    )
    st.write(
        "We're using our own judgement to decide which features should be used, we cannot ask client as this has been delegated to us."
    )
