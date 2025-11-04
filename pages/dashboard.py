import streamlit as st
from styles import dashboard as dashboard_styles
from pages.header import show_header

def show():
    """Display the dashboard page with header and content"""
    
    # Load dashboard-specific CSS
    dashboard_styles.load_css()
   
    # Render header and get active tab from URL
    active = show_header()

    # Save active tab to session state
    st.session_state["active_tab"] = active

    # ===== Content based on active tab =====
    st.markdown('<div class="dashboard-content">', unsafe_allow_html=True)
    
    if active == "Home":
        st.write("🏠 Home content here.")
    elif active == "My Ideas":
        st.write("💡 This is the My Ideas section.")
    elif active == "Ideas":
        st.write("🧠 Ideas page.")
    else:
        st.write("🏠 Home content here.")
    
    st.markdown('</div>', unsafe_allow_html=True)
