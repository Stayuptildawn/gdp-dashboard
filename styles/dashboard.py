import streamlit as st

def load_css():
    """Load CSS specific to the dashboard page"""
    st.markdown("""
    <style>
    /* Dashboard-specific styles can go here */
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
