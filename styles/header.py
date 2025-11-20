import streamlit as st


def load_css():
    st.markdown(
        """
    <style>
      :root { 
        --blue: #1677ff; 
      }

      /* ===== Top header (white card) ===== */
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

      .user-icon {
        font-size: 26px;
        margin-bottom: 4px;
      }
      
      .user-name {
        font-weight: 600; 
        color: #111; 
        font-size: 14px;
        text-align: right;
      }

      /* ===== Navigation bar (blue strip) ===== */
      .navbar {
        background: var(--blue);
        border-radius: 12px;
        padding: 8px 14px;
        box-shadow: 0 3px 10px rgba(0,0,0,.06);
        margin: 12px 0 18px 0;

        display: flex;
        flex-direction: row;
        align-items: center;
        flex-wrap: nowrap;          /* stay on ONE row */
        gap: 10px;
        overflow-x: auto;           /* if too many items, scroll horizontally */
        white-space: nowrap;        /* prevent internal line breaks */
      }

      .navbar a.navlink,
      .navbar span.sep {
        color: #ffffff;
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
      }

      .navbar a.navlink {
        padding: 4px 12px;
        border-radius: 999px;
        display: inline-block;
      }

      .navbar a.navlink:hover {
        background: rgba(255,255,255,0.16);
      }

      .navbar a.navlink.active {
        background: #ffffff;
        color: var(--blue);
      }

      .navbar .sep {
        opacity: 0.9;
      }
    </style>
    """,
        unsafe_allow_html=True,
    )
