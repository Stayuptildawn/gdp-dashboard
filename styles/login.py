import streamlit as st

def load_css():
    """Load CSS specific to the login page"""
    st.markdown("""
    <style>
    /* Remove default Streamlit padding */
    .main > div {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Login page background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Center the entire layout */
    .block-container {
        max-width: 1200px;
        padding-top: 5rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Input groups */
    .input-group {
        margin-bottom: 1.2rem;
    }
    
    .input-label {
        display: block;
        font-size: 0.95rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    /* Style text inputs */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        color: #1f2937;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ef4444;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
        outline: none;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af;
    }
    
    /* Hide Streamlit-generated labels */
    .stTextInput > label {
        display: none;
    }
    
    /* Hide the actual checkbox (we're using HTML version) */
    .stCheckbox {
        display: none;
    }
    
    /* Forgot password link - smaller and inline */
    .forgot-link button {
        background: transparent !important;
        border: none !important;
        color: #374151 !important;
        font-size: 0.85rem !important;
        padding: 0 !important;
        text-decoration: none !important;
        box-shadow: none !important;
        font-weight: 400 !important;
        height: auto !important;
    }
    
    .forgot-link button:hover {
        color: #ef4444 !important;
        text-decoration: underline !important;
    }
    
    /* Button group spacing - reduced */
    .button-group {
        margin: 0.75rem 0;
    }
    
    /* Primary button (Sign in) - match reference width */
    .stButton > button[kind="primary"] {
        background-color: #ef4444 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 1.5rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(239, 68, 68, 0.2) !important;
        width: 100% !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #dc2626 !important;
        box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3) !important;
    }
    
    /* Secondary button (SSO) - match reference width */
    .stButton > button:not([kind="primary"]) {
        background-color: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 0.65rem 1.5rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:not([kind="primary"]):hover {
        background-color: #f9fafb !important;
        border-color: #9ca3af !important;
    }
    
    /* Sign up text */
    .signup-text {
        text-align: center;
        margin-top: 1.5rem;
        font-size: 0.9rem;
        color: #6b7280;
    }
    
    .signup-link {
        color: #ef4444;
        text-decoration: none;
        font-weight: 600;
    }
    
    .signup-link:hover {
        text-decoration: underline;
    }
    
    /* Illustration container */
    .illustration-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    /* Column spacing */
    div[data-testid="column"] {
        padding: 1rem;
    }

    .error-message {
        background-color: #ef4444;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 8px;
        margin-top: -2.0rem;
        margin-bottom: 1rem;
        width: fit-content;
        margin-left: auto;
        font-size: 0.85rem;
    }

    .warning-message {
        background-color: #FFD700;
        color: black;
        padding: 0.3rem 1rem;
        border-radius: 8px;
        margin-top: -2.0rem;
        margin-bottom: 1rem;
        width: fit-content;
        margin-left: auto;
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)
