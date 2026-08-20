import streamlit as st

from utils.data_utils import load_data

from utils.layout import init_streamlit_state_values, init_sidebar

st.session_state = init_streamlit_state_values(st.session_state, st.secrets)

st.session_state["csv"] = st.file_uploader("Upload a file", type=["csv"])

if st.session_state["csv"]:
    st.session_state["data"] = load_data(st.session_state["csv"])
    st.write(f"Loaded: {st.session_state["csv"].name}")

init_sidebar()
