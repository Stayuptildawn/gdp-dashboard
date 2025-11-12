import streamlit as st
from data.fake_docs import make_fake_docs
from styles import dashboard as dashboard_styles
from pages.header import show_header
from pages import home as home_page, publish_idea
from pages import edit_idea as edit_idea_page


def _qp_get(name, default=None):
    v = st.query_params.get(name, default)
    # Sometimes we get a list back, so just grab the first item if that happens
    if isinstance(v, (list, tuple)):
        return v[0] if v else default
    return v


def _init_docs_once():
    if "home_docs" not in st.session_state:
        st.session_state.home_docs = make_fake_docs(35)


def show():
    """Shows the main dashboard with header and page content"""
    
    st.set_page_config(layout="wide")
    _init_docs_once()


    # Load up the dashboard styling
    dashboard_styles.load_css()
   
    # Show the header and get which page they're on from the URL
    active = show_header()


    # Figure out which tab is active by checking URL params and session state
    active_qp = _qp_get("page")
    active_ss = st.session_state.get("active_tab")
    active = active_qp or active_ss or "Home"


    edit_id_qp = _qp_get("edit_id")
    if edit_id_qp is not None:
        try:
            st.session_state["edit_id"] = int(edit_id_qp)
        except Exception:
            st.session_state["edit_id"] = str(edit_id_qp)



    # Remember which tab they're on
    st.session_state["active_tab"] = active
   


    # Show the right content based on which tab is active
    st.markdown('<div class="dashboard-content">', unsafe_allow_html=True)
    
    if active == "Home":
        home_page.show()
    elif active == "My Ideas":
        
        if "edit_id" in st.session_state:
            edit_idea_page.show()
        else:
            st.write("🧠 This is where you'll see all your ideas - we're still building this part!")
    elif active == "Ideas":
            publish_idea.show()
    else:
        st.write("🏠 Welcome to the dashboard - select a tab above to get started.")
    
    st.markdown('</div>', unsafe_allow_html=True)
