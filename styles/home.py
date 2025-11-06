# styles/home.py
import streamlit as st


def load_css():
    st.markdown("""
    <style>
      /* Each row in the home table */
      .home-row {border:1px solid #e9edf3; border-radius:12px; padding:12px; margin-bottom:10px; background:#fff;}
      .home-row:hover {box-shadow:0 2px 10px rgba(0,0,0,0.06);}
      
      /* Status badges - base styling */
      .badge {padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600; display:inline-block;}
      
      /* Blue badge for items under review */
      .b-review {background:#e6f0ff; color:#1d4ed8;}
      
      /* Green badge for accepted items */
      .b-accepted {background:#e9f9ee; color:#079455;}
      
      /* Red badge for rejected items */
      .b-rejected {background:#ffeaea; color:#ce2b2b;}
      
      /* Muted/secondary text */
      .muted {color:#667085; font-size:12px;}
      
      /* Grid layout for the columns - adjust widths here if needed */
      .cols {display:grid; grid-template-columns: 140px 120px 120px 1.2fr 140px 160px 160px 220px; gap:12px; align-items:center;}
      
      /* Main title text in each row */
      .row-title {font-weight:600;}
      
      /* Smaller subtitle text below the title */
      .row-sub {font-size:12px; color:#667085;}
      
      /* Action buttons container - aligned to the right */
      .toolbar {display:flex; gap:8px; justify-content:flex-end;}
      
      /* Round corners on all buttons */
      .stButton>button {border-radius:8px;}
    </style>
    """, unsafe_allow_html=True)
