import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /*
         Make borders always visible with rounded corners by styling the WRAPPERS,
         not just the input elements (Streamlit wraps inputs in extra divs).
        */

        /* Text input wrapper */
        div[data-testid="stTextInput"] > div > div {
            border: 1px solid #000 !important;
            border-radius: 8px !important;
            box-shadow: none !important;
            background: #fff !important;
            overflow: hidden;
        }
        /* Remove native borders so wrapper border is visible */
        div[data-testid="stTextInput"] input {
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        /* Text area wrapper */
        div[data-testid="stTextArea"] > div > div {
            border: 1px solid #000 !important;
            border-radius: 8px !important;
            box-shadow: none !important;
            background: #fff !important;
            overflow: hidden;
        }
        div[data-testid="stTextArea"] textarea {
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        /* Keep border black on focus */
        div[data-testid="stTextInput"] > div > div:focus-within,
        div[data-testid="stTextArea"] > div > div:focus-within {
            border: 1px solid #000 !important;
            box-shadow: none !important;
        }

        /* Selectbox (baseweb) wrapper */
        div[data-baseweb="select"] > div {
            border: 1px solid #000 !important;
            border-radius: 8px !important;
            box-shadow: none !important;
            background: #fff !important;
        }
        /* Prevent red focus/outline on the combobox */
        div[data-baseweb="select"] div[role="combobox"] {
            outline: none !important;
        }
        div[data-baseweb="select"] > div:focus-within {
            border: 1px solid #000 !important;
            box-shadow: none !important;
        }

        /* Inline messages (match login styling exactly) */
        .error-message {
            background-color: #ef4444;
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 8px;
            margin-top: -1.0rem;
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
            margin-top: -1.0rem;
            margin-bottom: 1rem;
            width: fit-content;
            margin-left: auto;
            font-size: 0.85rem;
        }
    </style>
    """, unsafe_allow_html=True)
