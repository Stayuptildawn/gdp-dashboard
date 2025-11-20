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
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

# --- ALWAYS Load ideas from CSV (remove the "if" check) ---
# This ensures data is loaded every time, not just once
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
        if "id" in df.columns:
            df = df.sort_values('id', ascending=False).reset_index(drop=True)
        
        st.session_state.home_docs = df
    else:
        # No CSV file found - create empty dataframe
        st.session_state.home_docs = pd.DataFrame(columns=[
            "id", "Status", "From date", "To date", "Document name",
            "Date published", "Issue Number", "Name", "Category",
            "Description", "Detailed Description",
            "Estimated Impact / Target Audience", "Owner", "Visibility Setting"
        ])
        
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.session_state.home_docs = pd.DataFrame(columns=[
        "id", "Status", "From date", "To date", "Document name",
        "Date published", "Issue Number", "Name", "Category",
        "Description", "Detailed Description",
        "Estimated Impact / Target Audience", "Owner", "Visibility Setting"
    ])

# --- Route based on authentication status ---
if not st.session_state.authenticated:
    # Allow access to home.py without login (shows public ideas only)
    st.switch_page("pages/home.py")
else:
    # User is authenticated - redirect to home page (shows all ideas)
    st.switch_page("pages/home.py")
