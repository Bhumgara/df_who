import streamlit as st
import matplotlib.pyplot as plt

from utils.viz_utils import plot_correlation, plot_residuals, plot_actual_vs_predicted

from utils.layout import init_streamlit_state_values, init_sidebar

st.session_state = init_streamlit_state_values(st.session_state, st.secrets)

if "model" in st.session_state.keys():
    st.write("You have a model! Let's look at the stats.")

    st.subheader("Model Performance")

    st.dataframe(st.session_state["stats_df"])

    st.subheader("Feature Column Correlation")

    annot_threshold = st.slider(
        "Annotation threshold (magnitude)",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Only show annotations where absolute correlation exceeds this value",
    )

    st.pyplot(plt.figure(figsize=(16, 8)), plot_correlation(st.session_state["X"], annot_threshold))

    st.subheader("Residual Distribution")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    st.pyplot(fig, plot_residuals(st.session_state["pred_test"], st.session_state["y_test"], axes))

    st.subheader("Actual vs Prediction Comparison")

    st.pyplot(
        plt.figure(figsize=(16, 8)),
        plot_actual_vs_predicted([(st.session_state["pred_test"], st.session_state["y_test"])]),
    )
else:
    st.write("No model created. Use the button in the sidebar to create one.")

init_sidebar()
