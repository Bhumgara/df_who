import streamlit as st

from utils.model_utils import create_model

from utils.data_utils import load_data

if "model" in st.session_state.keys():
    st.write("You have a model! Let's make a prediction.")
else:
    st.write("No model created. Use the button in the sidebar to create one.")

st.session_state["csv"] = st.file_uploader("Upload a file", type=["csv"])

if st.session_state["csv"]:
    st.session_state["data"] = load_data(st.session_state["csv"])
    st.write(f"Loaded: {st.session_state["csv"].name}")

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
