
import streamlit as st
import pandas as pd

def show():
    """
    Shows the 'My Ideas' page, filtered so each user only sees their own ideas.
    Assumes:
      - st.session_state.username is set after login
      - st.session_state.home_docs is a DataFrame with at least:
            ['id', 'Name', 'Category', 'Status', 'Estimated Impact / Target Audience', 'Owner']
    """

    # Defensive checks so the page fails in a friendly way
    if "username" not in st.session_state or not st.session_state.username:
        st.error("You need to be logged in to see your ideas.")
        return

    if "home_docs" not in st.session_state or st.session_state.home_docs is None:
        st.error("There is no idea data available in this session yet.")
        return

    username = st.session_state.username
    df = st.session_state.home_docs

    # If your owner column has a different name, change "Owner" below
    if "Owner" not in df.columns:
        st.warning(
            "The ideas table does not have an 'Owner' column yet, "
            "so 'My Ideas' cannot be filtered by user."
        )
        st.dataframe(df, use_container_width=True)
        return

    # Filter rows where the Owner matches the current user
    my_ideas = df[df["Owner"] == username].copy()

    st.title("My Ideas")

    if my_ideas.empty:
        st.info("You have not submitted any ideas yet. Try publishing a new one from the Ideas section.")
        return

    # Pick the columns you want to show in the table
    display_cols = [
        "id",
        "Name",
        "Category",
        "Status",
        "Estimated Impact / Target Audience",
        "From date",
        "To date",
    ]
    existing_cols = [c for c in display_cols if c in my_ideas.columns]

    # Nicely formatted table of only this user’s ideas
    st.dataframe(
        my_ideas[existing_cols].sort_values(by="From date", ascending=False),
        use_container_width=True,
    )
