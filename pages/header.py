import os
import streamlit as st
from styles import header as header_styles


def show_header():
    """Display the header with logo, title, user info, and navigation"""
    
    # Load header-specific CSS
    header_styles.load_css()

    username = st.session_state.get("username", "User")
    logo_path = "elements/upm_logo.png"

    # ===== Header Section (white background with blue title) =====
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    c1, c2 = st.columns([0.75, 0.25])

    with c1:
        lc, rc = st.columns([0.12, 0.88])
        with lc:
            if os.path.exists(logo_path):
                # FIXED: Removed use_container_width and kept only width=48
                st.image(logo_path, width=48)
            else:
                st.write("")
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
        st.markdown(f"""
            <div class="user-section">
                <!-- Left column: User icon and logout -->
                <div class="user-column">
                    <div class="user-icon">👤</div>
                    <form action="?logout=true" method="post" style="margin:0;">
                        <button class="logout-btn">Logout</button>
                    </form>
                </div>
                <!-- Right column: Username and settings -->
                <div class="user-column">
                    <div class="user-name">Hello, {username}</div>
                    <form action="?page=Settings" method="get" style="margin:0;">
                        <button class="settings-btn">Settings</button>
                    </form>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ===== Navbar Section (blue background with links) =====
    NAV_ITEMS = ["Home", "Ideas", "My Ideas"]

    # Get active tab from URL query parameters or default to 'Home'
    active = st.query_params.get("page", "Home")

    links = []
    for i, name in enumerate(NAV_ITEMS):
        href = f"?page={name.replace(' ', '%20')}"
        cls = "navlink active" if name == active else "navlink"
        links.append(f'<a class="{cls}" href="{href}">{name}</a>')
        if i < len(NAV_ITEMS) - 1:
            links.append('<span class="sep">|</span>')

    st.markdown(f'<div class="navbar">{"".join(links)}</div>', unsafe_allow_html=True)

    # Return active tab for use in dashboard
    return active
