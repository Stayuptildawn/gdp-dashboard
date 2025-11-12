import streamlit as st


def load_css():
    """Loads the CSS for the header and navigation bar"""
    st.markdown("""
    <style>
      :root { 
        --blue: #1677ff; 
      }
      
      /* ===== Top header stuff (white box at the top) ===== */
      .app-header {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 14px 16px;
        display: flex; 
        align-items: center; 
        justify-content: space-between;
        box-shadow: 0 4px 10px rgba(0,0,0,.05);
      }
      
      /* Make the logo look nice */
      .logo-img { 
        height: 48px; 
        width: auto; 
        border-radius: 8px; 
      }
      
      /* App title and subtitle */
      .title h1 { 
        margin: 0; 
        font-size: 22px; 
        font-weight: 800; 
        color: var(--blue); 
      }
      
      .title p { 
        margin: 0; 
        font-size: 13px; 
        color: #475569; 
      }


      /* ===== Navigation bar (blue strip below header) ===== */
      .navbar {
        background: var(--blue);
        border-radius: 12px;
        padding: 6px 10px;
        white-space: nowrap;
        overflow-x: auto;
        box-shadow: 0 3px 10px rgba(0,0,0,.06);
        margin: 8px 0 14px 0;
      }
      
      /* Style for the nav links and those little separators */
      .navbar a.navlink, .navbar span.sep {
        color: #fff;
        text-decoration: none;
        font-weight: 700;
        font-size: 16px;
        line-height: 28px;
      }
      
      .navbar a.navlink {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 10px;
        transition: all .2s ease;
      }
      
      .navbar a.navlink:hover { 
        text-decoration: underline; 
      }


      /* Dark pill around the current active page */
      .navbar a.navlink.active {
        background: rgba(0,0,0,.85);
        box-shadow: 0 2px 6px rgba(0,0,0,.12);
      }


      .navbar .sep { 
        opacity: .8; 
        margin: 0 10px; 
      }
      
      /* ===== User info and buttons on the right ===== */
      .user-section {
        display: grid; 
        grid-template-columns: auto auto; 
        gap: 4px 16px; 
        align-items: center;
      }
      
      .user-column {
        text-align: center;
      }
      
      .user-icon {
        font-size: 18px;
      }
      
      .user-name {
        font-weight: 600; 
        color: #111; 
        font-size: 14px;
      }
      
      /* Black logout button */
      .logout-btn {
        background: #111;
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 12px;
        padding: 4px 10px;
        cursor: pointer;
        margin-top: 4px;
      }
      
      /* Gray settings button */
      .settings-btn {
        background: #848484;
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 12px;
        padding: 4px 10px;
        cursor: pointer;
        margin-top: 4px;
      }
      
      .logout-btn:hover {
        background: #000;
      }
      
      .settings-btn:hover {
        background: #6b6b6b;
      }
    </style>
    """, unsafe_allow_html=True)
