import streamlit as st


def load_css():
    st.markdown("""
    <style>
        /*
         Streamlit wraps inputs in extra divs, so we need to style those wrappers
         to get clean borders with rounded corners that actually show up.
        */


        /* Text input box borders */
        div[data-testid="stTextInput"] > div > div {
            border: 1px solid #000 !important;
            border-radius: 8px !important;
            box-shadow: none !important;
            background: #fff !important;
            overflow: hidden;
        }
        /* Get rid of the default input border so our wrapper border shows */
        div[data-testid="stTextInput"] input {
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }


        /* Same thing for text areas */
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


        /* Don't let the border change color when someone clicks into the field */
        div[data-testid="stTextInput"] > div > div:focus-within,
        div[data-testid="stTextArea"] > div > div:focus-within {
            border: 1px solid #000 !important;
            box-shadow: none !important;
        }


        /* Dropdown/select boxes (these use baseweb under the hood) */
        div[data-baseweb="select"] > div {
            border: 1px solid #000 !important;
            border-radius: 8px !important;
            box-shadow: none !important;
            background: #fff !important;
        }
        /* Stop that annoying red outline from appearing when focused */
        div[data-baseweb="select"] div[role="combobox"] {
            outline: none !important;
        }
        div[data-baseweb="select"] > div:focus-within {
            border: 1px solid #000 !important;
            box-shadow: none !important;
        }


        /* Red error messages - styled the same as on login page */
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
