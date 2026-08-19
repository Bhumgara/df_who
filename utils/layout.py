import streamlit as st


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
