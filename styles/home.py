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

      /* Filter row input/select visible borders and rounded corners */
      .stTextInput input {
        border: 1.5px solid #bdbdbd !important;
        border-radius: 6px !important;
        box-shadow: none !important;
        background-color: white !important;
      }
      .stDateInput input[type="text"] {
        border: 1.5px solid #bdbdbd !important;
        border-radius: 6px !important;
        box-shadow: none !important;
        background-color: white !important;
      }
      .stSelectbox div[data-baseweb="select"] > div {
        border: 1.5px solid #bdbdbd !important;
        border-radius: 6px !important;
        box-shadow: none !important;
        background-color: white !important;
      }

      /* Filter button wrapper and button styling for alignment */
      .filter-btn-wrap {
        display: flex;
        align-items: flex-start;
        height: 100%;
      }
      .filter-btn {
        background: #00B4D8;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 18px;
        font-weight: 600;
        font-size: 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        margin-left: 10px;
        margin-top: 28px;
      }
    </style>
    """, unsafe_allow_html=True)
