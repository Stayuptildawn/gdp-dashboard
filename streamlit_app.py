import streamlit as st

# Configure the main layout before anything else
st.set_page_config(layout="wide")

from styles import load_global_css
from pages import dashboard, login, home, edit_idea, publish_idea, myIdeas
from pages import header
from data.fake_docs import make_fake_docs


# Load global CSS so all pages share the same base styling
load_global_css()


# --- Authentication-related session state ---
if "authenticated" not in st.session_state:
    # Default to logged-out only when the session starts for the first time
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None


# --- Shared data (ideas table) that multiple pages depend on ---
# This avoids “no data in session” errors when a page loads first.
if "home_docs" not in st.session_state:
    st.session_state.home_docs = make_fake_docs(30)


# --- Public vs private part of the app ---
if not st.session_state.authenticated:
    # When the user is not logged in, only show the login page
    login.show()

else:
    # Draw the shared header at the top of every authenticated view.
    # The header returns which tab is currently active: "Home", "Ideas", "My Ideas", etc.
    active_page = header.show_header()

    # Route to the right content area based on that active tab
    if active_page == "Home":
        # High-level overview / landing page after login
        home.show()

    elif active_page == "Ideas":
        # Main ideas dashboard / list of all ideas
        dashboard.show()

    elif active_page == "My Ideas":
        # Per-user list of ideas (drafts + published)
        myIdeas.show()

    elif active_page == "New Idea":
        # Idea submission form for the currently logged-in user
        publish_idea.show()

    elif active_page == "Experiments":
        # Placeholder until you create pages/experiments.py with a show() function
        st.title("Experiments")
        st.write("This is a placeholder for the Experiments page.")

    elif active_page == "Sprints":
        # Placeholder for sprint planning / tracking
        st.title("Sprints")
        st.write("This is a placeholder for the Sprints page.")

    elif active_page == "Team":
        # Placeholder for team overview
        st.title("Team")
        st.write("This is a placeholder for the Team page.")

    elif active_page == "Reports/Analytics":
        # Placeholder for reports and analytics dashboards
        st.title("Reports & Analytics")
        st.write("This is a placeholder for the Reports / Analytics page.")

    elif active_page == "Profile":
        # Placeholder for user profile and settings
        st.title("Profile")
        st.write("This is a placeholder for the Profile page.")

    else:
        # If the URL contains an unknown page name, fall back to Home for safety
        home.show()
