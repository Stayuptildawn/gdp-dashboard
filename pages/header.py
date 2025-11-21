import os
import streamlit as st
from styles import header as header_styles


def show_header(active_page=None):
    """Renders the top header and returns the active page name."""
    header_styles.load_css()

    username = st.session_state.get("username", "User")
    logo_path = "elements/upm_logo.png"
    is_authenticated = st.session_state.get("authenticated", False)
    role = st.session_state.get("role", None)  # admin / investor / student / None

    # ===== White header card =====
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    c1, c2 = st.columns([0.75, 0.25])

    with c1:
        lc, rc = st.columns([0.10, 0.90])
        with lc:
            if os.path.exists(logo_path):
                import base64
                with open(logo_path, "rb") as f:
                    logo_b64 = base64.b64encode(f.read()).decode()
                st.markdown(
                    f'<img src="data:image/png;base64,{logo_b64}" '
                    f'style="width: 100%; max-width: 70px; height: auto; margin-top: 8px;">',
                    unsafe_allow_html=True,
                )
        with rc:
            st.markdown(
                """
                <div class="title">
                  <h1>Innovation Department of UPM</h1>
                  <p>Platform of Managing Ideas of Entrepreneurs</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with c2:
        if is_authenticated:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; padding: 1rem 0; gap: 0.75rem;">
                    <div style="font-size: 2rem;">👤</div>
                    <div style="flex: 1;">
                        <div style="font-size: 0.9rem; color: #374151; font-weight: 500;">Hello, {username}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            sc1, sc2 = st.columns(2)
            with sc1:
                if st.button("Settings", key="header_settings", width="stretch"):
                    st.switch_page("pages/profile.py")
            with sc2:
                if st.button("Logout", key="header_logout", width="stretch"):
                    st.session_state.authenticated = False
                    st.session_state.username = None
                    st.session_state.role = None
                    st.switch_page("streamlit_app.py")

    st.markdown("</div>", unsafe_allow_html=True)

    # ===== Blue navbar - conditional based on authentication & role =====
    if is_authenticated:
        # Always available when logged in
        nav_items = [
            {"label": "Ideas", "page": "pages/dashboard.py", "icon": "💡"},
        ]

        # Only for admin + student
        if role in ["admin", "student"]:
            nav_items.extend(
                [
                    {"label": "My Ideas", "page": "pages/myideas.py", "icon": "📝"},
                    {"label": "New Idea", "page": "pages/publish_idea.py", "icon": "➕"},
                ]
            )
        
        # Only for investor (only My Ideas no New Idea)
        elif role == "investor":
            nav_items.extend(
                [
                    {"label": "My Ideas", "page": "pages/myideas.py", "icon": "📝"},
                ]
            )

        # Extra pages – same for all authenticated roles
        nav_items.extend(
            [
                {"label": "Experiments", "page": "pages/experiments.py", "icon": "🔬"},
                {"label": "Sprints", "page": "pages/sprints.py", "icon": "⚡"},
                {"label": "Team", "page": "pages/team.py", "icon": "👥"},
                {"label": "Reports/Analytics", "page": "pages/reports.py", "icon": "📊"},
                {"label": "Profile", "page": "pages/profile.py", "icon": "👤"},
                {"label": "Messages", "page": "pages/messages.py", "icon": "💬"},
            ]
        )
    else:
        nav_items = [
            {"label": "Login", "page": "pages/login.py", "icon": "🔐"},
        ]

    st.markdown('<div class="navbar">', unsafe_allow_html=True)

    cols = st.columns(len(nav_items))
    for col, item in zip(cols, nav_items):
        with col:
            st.page_link(
                item["page"],
                label=item["label"],
                icon=item["icon"],
                width="stretch",
            )

    st.markdown("</div>", unsafe_allow_html=True)

    return active_page
