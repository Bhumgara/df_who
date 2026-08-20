import streamlit as st

from utils.data_utils import load_data
from utils.model_utils import create_model

import glob

import os
from dotenv import load_dotenv

import kagglehub


def render_header(page_title: str, page_subtitle: str = "") -> None:
    """
    Render a consistent header + divider at the top of every page.

    Call this as the first line inside Home.py and every file in pages/,
    so all pages share the same chrome without duplicating markup.

    `page_title`:    Main heading shown at the top of the page.

    `page_subtitle`: Optional one-line description shown under the title.
    """
    st.title(page_title)
    if page_subtitle:
        st.caption(page_subtitle)
    st.divider()


def bordered_section(title: str = "") -> "st.delta_generator.DeltaGenerator":
    """
    Return a bordered container to visually group a block of content.

    ```
    Usage:
        with bordered_section("Section title"):
            st.write("...")
    ```

    `title`: Optional heading rendered inside the border, above the content.
    """
    container = st.container(border=True)
    if title:
        container.subheader(title)
    return container


def init_streamlit_state_values(curr_session_state, stl_secrets):
    load_dotenv()
    if "csv" not in curr_session_state:
        # curr_session_state["csv"] = os.getenv("DATA_CSV")
        curr_session_state["csv"] = stl_secrets["DATA_CSV"]

    if "prod" not in curr_session_state:
        # curr_session_state["prod"] = bool(os.getenv("PROD"))
        curr_session_state["prod"] = bool(stl_secrets["PROD"])

    if "data" not in curr_session_state:
        if curr_session_state["prod"]:
            dataset_dir = kagglehub.dataset_download(curr_session_state["csv"])
            csvs = glob.glob(os.path.join(dataset_dir, "*.csv"))
            if not csvs:
                raise FileNotFoundError(f"No CSV files found in downloaded dataset: {dataset_dir}")
        curr_session_state["data"] = load_data(csvs[0])
    return curr_session_state


def init_sidebar():
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
