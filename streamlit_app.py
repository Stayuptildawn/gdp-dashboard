import streamlit as st
import pandas as pd
import os

# Configure the main layout before anything else
st.set_page_config(
    page_title="UPM Innovation Platform",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from styles import load_global_css

# Load global CSS so all pages share the same base styling
load_global_css()

# --- Authentication-related session state ---
if "authenticated" not in st.session_state:
    # Default to logged-out only when the session starts for the first time
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

# --- Load ideas from CSV only ---
if "home_docs" not in st.session_state:
    try:
        csv_path = "data/ideas.csv"
        
        if os.path.exists(csv_path):
            # Load ideas from CSV
            df = pd.read_csv(csv_path)
            
            # Convert date columns to datetime
            for col in ["From date", "To date", "Date published"]:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Sort by id descending so newest ideas appear first
            df = df.sort_values('id', ascending=False).reset_index(drop=True)
            
            st.session_state.home_docs = df
        else:
            # No CSV file found - create empty dataframe with proper structure
            st.session_state.home_docs = pd.DataFrame(columns=[
                "id", "Status", "From date", "To date", "Document name",
                "Date published", "Issue Number", "Name", "Category",
                "Description", "Detailed Description",
                "Estimated Impact / Target Audience", "Owner"
            ])
            
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.session_state.home_docs = pd.DataFrame()

# --- Route based on authentication status ---
if not st.session_state.authenticated:
    # When the user is not logged in, redirect to login page
    st.switch_page("pages/login.py")
else:
    # User is authenticated - redirect to dashboard (Ideas page)
    st.switch_page("pages/dashboard.py")
