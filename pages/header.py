import os
import streamlit as st
from styles import header as header_styles


def show_header():
    """Renders the top header and returns the active page name."""
    header_styles.load_css()

    username = st.session_state.get("username", "User")
    logo_path = "elements/upm_logo.png"

    # ===== White header card =====
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    c1, c2 = st.columns([0.75, 0.25])

    with c1:
        lc, rc = st.columns([0.12, 0.88])
        with lc:
            if os.path.exists(logo_path):
                st.image(logo_path, width=48)
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
        uc1, uc2 = st.columns([0.35, 0.65])
        with uc1:
            st.markdown('<div class="user-icon">👤</div>', unsafe_allow_html=True)
        with uc2:
            st.markdown(
                f'<div class="user-name">Hello, {username}</div>',
                unsafe_allow_html=True,
            )
            if st.button("Settings", key="header_settings"):
                st.query_params["page"] = "Profile"
                st.rerun()
            if st.button("Logout", key="header_logout"):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.query_params.clear()
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ===== Blue navbar (single flex row, no wrapping) =====
    NAV_ITEMS = [
        "Home",
        "Ideas",
        "My Ideas",
        "New Idea",          # <- add this
        "Experiments",
        "Sprints",
        "Team",
        "Reports/Analytics",
        "Profile",
    ]

    active = st.query_params.get("page", "Home")

    links = []
    for i, name in enumerate(NAV_ITEMS):
        href = f"?page={name.replace(' ', '%20')}"
        cls = "navlink active" if name == active else "navlink"
        links.append(f'<a class="{cls}" href="{href}">{name}</a>')
        if i < len(NAV_ITEMS) - 1:
            links.append('<span class="sep">|</span>')

    st.markdown(
        f'<div class="navbar">{" ".join(links)}</div>',
        unsafe_allow_html=True,
    )

    return active
