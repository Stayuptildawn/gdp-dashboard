import streamlit as st

def load_css():
    """Load global base CSS styles for the entire app"""
    st.markdown("""
    <style>
      :root {
        --blue: #0a74ff;
        --blue-dark: #075fd1;
        --bg: #ffffff;
        --text: #0b1324;
        --muted: #64748b;
      }
      
      /* Global background and text colors */
      html, body { 
        background: var(--bg) !important; 
        color: var(--text); 
      }
      
      /* Remove default Streamlit padding */
      div.block-container { 
        padding-top: 0rem !important; 
        background: var(--bg) !important; 
      }
      
      /* Hide default Streamlit header */
      header[data-testid="stHeader"] { 
        background: none !important; 
        height: 0px; 
      }
      
      section.main > div { 
        padding-top: 0rem !important; 
      }
      
      /* Global button styles */
      .stButton > button { 
        border-radius: 12px; 
        font-weight: 600; 
      }
    </style>
    """, unsafe_allow_html=True)
