import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from utils.model_utils import create_model
from utils.viz_utils import plot_correlation, plot_residuals, plot_actual_vs_predicted

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
            st.session_stats["include_sensitive"] = (not sensitive)
