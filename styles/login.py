import streamlit as st



def load_css():
    """Loads up the CSS for the login page"""
    st.markdown("""
    <style>
    /* Get rid of that default padding Streamlit adds */
    .main > div {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Background color for the login page */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Keep everything centered and not too wide */
    .block-container {
        max-width: 1200px;
        padding-top: 5rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Spacing for each input field */
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
    
    /* Make the text inputs look nice */
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
    
    /* Streamlit adds labels we don't want, so hide them */
    .stTextInput > label {
        display: none;
    }
    
    /* We're using a custom checkbox, so hide the default one */
    .stCheckbox {
        display: none;
    }
    
    /* Style for the "forgot password" link */
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
    
    /* Add some space around the button group */
    .button-group {
        margin: 0.75rem 0;
    }
    
    /* Main "Sign in" button styling */
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
    
    /* SSO button - less prominent than the main one */
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
    
    /* "Don't have an account?" text at the bottom */
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
    
    /* Container for the side illustration */
    .illustration-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    /* Padding between columns */
    div[data-testid="column"] {
        padding: 1rem;
    }


    /* Red error messages */
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


    /* Yellow warning messages */
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
    
    /* ==================== MODAL POPUP STUFF ==================== */
    
    /* Dark background overlay when modal is open */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        animation: fadeIn 0.3s ease;
        cursor: pointer;
    }
    
    /* Smooth fade-in effect */
    @keyframes fadeIn {
        from { 
            opacity: 0; 
        }
        to { 
            opacity: 1; 
        }
    }
    
    /* The actual modal box - clicking here won't close it */
    .modal-content {
        background: white;
        border-radius: 12px;
        padding: 0;
        max-width: 90%;
        max-height: 80vh;
        overflow: auto;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        animation: slideUp 0.3s ease;
        position: relative;
        cursor: default;
    }
    
    /* Slide up animation when modal appears */
    @keyframes slideUp {
        from {
            transform: translateY(50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    /* Images inside the modal */
    .modal-content img {
        display: block;
        width: 100%;
        height: auto;
        border-radius: 12px;
    }
    
    /* ==================== END MODAL STUFF ==================== */
    </style>
    """, unsafe_allow_html=True)
