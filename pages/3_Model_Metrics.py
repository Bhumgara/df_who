import streamlit as st

from utils.model_utils import create_model

if "model" in st.session_state.keys():
    st.write("You have a model! Let's look at the stats.")
else:
    st.write("No model created. Use the button in the sidebar to create one.")

with st.sidebar:
    st.write("Some advanced population data may include protected information. Only check this box if you wish to include this data for better accuracy.")
    sensitive = st.checkbox(label="Include sensitive data?", value=False)
    if st.button(label="Rebuild model"):
        with st.spinner("Training model..."):
            model, X, stats_df, pred_test, y_test = create_model(exclude_sensitive=sensitive)
    
            st.write("Model complete! Reload or head to other pages to use this model.")
        
            # stash results in session_state so other parts of the app
            st.session_state["model"] = model
            st.session_state["X"] = X
            st.session_state["stats_df"] = stats_df
            st.session_state["pred_test"] = pred_test
            st.session_state["y_test"] = y_test