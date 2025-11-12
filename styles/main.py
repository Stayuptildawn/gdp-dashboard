import streamlit as st


def load_css():
    """Loads the base CSS that applies to the whole app"""
    st.markdown("""
    <style>
      :root {
        --blue: #0a74ff;
        --blue-dark: #075fd1;
        --bg: #ffffff;
        --text: #0b1324;
        --muted: #64748b;
      }
      
      /* Set up background and text colors everywhere */
      html, body { 
        background: var(--bg) !important; 
        color: var(--text); 
      }
      
      /* Streamlit adds padding by default - we don't want that */
      div.block-container { 
        padding-top: 0rem !important; 
        background: var(--bg) !important; 
      }
      
      /* Get rid of Streamlit's default header */
      header[data-testid="stHeader"] { 
        background: none !important; 
        height: 0px; 
      }
      
      section.main > div { 
        padding-top: 0rem !important; 
      }
      
      /* Make all buttons look consistent */
      .stButton > button { 
        border-radius: 12px; 
        font-weight: 600; 
      }
    </style>
    """, unsafe_allow_html=True)
