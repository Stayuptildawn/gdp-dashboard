import streamlit as st
from styles import dashboard as dashboard_styles


def show():
    """
    Main Ideas dashboard:
      - Assumes header + navigation are already rendered by streamlit_app.py
      - Shows filters and the ideas table using st.session_state.home_docs
    """

    # Page-specific CSS (card padding etc.)
    dashboard_styles.load_css()

    st.markdown('<div class="dashboard-content">', unsafe_allow_html=True)

    st.subheader("Ideas")

    # Example: simple filters row (adapt to your existing implementation)
    col_search, col_from, col_to, col_cat = st.columns([3, 1.5, 1.5, 1.5])

    with col_search:
        search = st.text_input("Search (name / description)", key="ideas_search")
    with col_from:
        from_date = st.text_input("From date", placeholder="YYYY/MM/DD", key="ideas_from")
    with col_to:
        to_date = st.text_input("To date", placeholder="YYYY/MM/DD", key="ideas_to")
    with col_cat:
        category = st.selectbox("Category", ["All"], key="ideas_category")

    st.markdown("</div>", unsafe_allow_html=True)

    # Below here put your existing table rendering logic using st.session_state.home_docs
    # Example placeholder:
    df = st.session_state.get("home_docs")
    if df is not None:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No ideas data loaded yet.")
