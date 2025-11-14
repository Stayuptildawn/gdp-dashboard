import streamlit as st


def load_css():
    """Loads CSS specific to the dashboard page"""
    st.markdown("""
    <style>
    /* Add any dashboard-specific styling here if needed */
    .dashboard-content {
        padding: 20px;
        background: #ffffff;
        border-radius: 12px;
        margin-top: 10px;
    }
    
    .dashboard-section {
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
