import streamlit as st

# Set page layout to wide mode - MUST be first
st.set_page_config(layout="wide")

from styles import load_global_css
from pages import dashboard, login

# Load global CSS
load_global_css()

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Page routing logic
if not st.session_state.authenticated:
    login.show()
else:
    dashboard.show()
