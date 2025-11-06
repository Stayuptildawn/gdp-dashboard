import streamlit as st
from data.fake_docs import make_fake_docs
from styles import dashboard as dashboard_styles
from pages.header import show_header
from pages import home as home_page, publish_idea
from pages import edit_idea as edit_idea_page

def _qp_get(name, default=None):
    v = st.query_params.get(name, default)
    # Normalize list -> first element
    if isinstance(v, (list, tuple)):
        return v[0] if v else default
    return v

def _init_docs_once():
    if "home_docs" not in st.session_state:
        st.session_state.home_docs = make_fake_docs(35)

def show():
    """Display the dashboard page with header and content"""
    
    st.set_page_config(layout="wide")
    _init_docs_once()

    # Load dashboard-specific CSS
    dashboard_styles.load_css()
   
    # Render header and get active tab from URL
    active = show_header()

    # --- read and normalize QPs
    active_qp = _qp_get("page")
    active_ss = st.session_state.get("active_tab")
    active = active_qp or active_ss or "Home"

    edit_id_qp = _qp_get("edit_id")
    if edit_id_qp is not None:
        try:
            st.session_state["edit_id"] = int(edit_id_qp)
        except Exception:
            st.session_state["edit_id"] = str(edit_id_qp)


    # Save active tab to session state
    st.session_state["active_tab"] = active
   

    # ===== Content based on active tab =====
    st.markdown('<div class="dashboard-content">', unsafe_allow_html=True)
    
    if active == "Home":
        home_page.show()
    elif active == "My Ideas":
        
        if "edit_id" in st.session_state:
            edit_idea_page.show()
        else:
            st.write("🧠 My Ideas page.")
    elif active == "Ideas":
            publish_idea.show()
    else:
        st.write("🏠 Home content here.")
    
    st.markdown('</div>', unsafe_allow_html=True)
