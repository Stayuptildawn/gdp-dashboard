import streamlit as st
import pandas as pd
import os
from styles import login as login_styles

def show():
    """Display the login page"""
    
    # Load login-specific CSS
    login_styles.load_css()
    
    # Ensure folders exist
    os.makedirs("elements", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Load user database from CSV
    user_db_path = "data/users.csv"
    if not os.path.exists(user_db_path):
        df = pd.DataFrame([{"username": "admin", "password": "aA1234"}])
        df.to_csv(user_db_path, index=False)
    else:
        df = pd.read_csv(user_db_path)
    
    # Create centered layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        # Welcome header
        st.markdown("""
        <div class="login-header">
            <h1 style="font-size: 2.8rem; font-weight: 800; color: #1a1a1a; margin: 0; margin-bottom: 0.3rem;">WELCOME</h1>
            <p style="font-size: 0.95rem; color: #6b7280; margin-bottom: 1.5rem; margin-top: 0;">Please enter your details.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Email input - Use proper label
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown("<label class='input-label'>Email</label>", unsafe_allow_html=True)
        email = st.text_input("Email", key="email_form", label_visibility="collapsed", placeholder="Enter your email")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Password input - Use proper label
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown("<label class='input-label'>Password</label>", unsafe_allow_html=True)
        password = st.text_input("Password", key="password_form", label_visibility="collapsed", type="password", placeholder="Enter your password")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Remember me and Forgot password row
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown("""
            <div style="margin: 0.8rem 0 1rem 0;">
                <label style="display: flex; align-items: center; cursor: pointer; font-size: 0.9rem; color: #374151;">
                    <input type="checkbox" id="remember_me_check" style="margin-right: 0.5rem; cursor: pointer; width: 16px; height: 16px;">
                    <span>Remember me</span>
                </label>
            </div>
            """, unsafe_allow_html=True)
            remember_me = st.checkbox("Remember me", key="remember_me", label_visibility="collapsed")
        with col_b:
            st.markdown('<div class="forgot-link" style="text-align: right; margin-top: 0.8rem;">', unsafe_allow_html=True)
            if st.button("Forgot password", key="forgot_btn", width="content"):
                st.info("Password reset functionality coming soon!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Sign in button - Use width='stretch'
        st.markdown('<div class="button-group">', unsafe_allow_html=True)
        login = st.button("Sign in", key="login_btn", width="stretch", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SSO button - Use width='stretch'
        st.markdown('<div class="button-group">', unsafe_allow_html=True)
        sso = st.button("Sign in with SSO", key="sso_btn", width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sign up link
        st.markdown(
            '<div class="signup-text">Don\'t have an account? <a href="#" class="signup-link">Sign up fo free!</a></div>',
            unsafe_allow_html=True
        )
    
    with col2:
        # Right side illustration - NO width parameter for st.image()
        if os.path.exists("elements/Right Side.png"):
            st.markdown('<div class="illustration-container">', unsafe_allow_html=True)
            st.image("elements/Right Side.png")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Login logic
    if login:
        if email and password:
            user_row = df[(df["username"] == email) & (df["password"] == password)]
            if not user_row.empty:
                st.session_state.authenticated = True
                st.session_state.username = email
                st.rerun()
            else:
                st.error("❌ Invalid login credentials. Please try again.")
        else:
            st.warning("⚠️ Please enter both email and password.")
