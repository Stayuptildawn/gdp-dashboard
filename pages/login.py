import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from styles import login as login_styles


def show_popup_modal(image_path, modal_key="error_modal"):
    """Display a centered popup modal with an image that closes on outside click"""
    if st.session_state.get(modal_key, False):
        import base64
        
        # Convert image to base64
        image_base64 = ""
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                image_base64 = base64.b64encode(img_file.read()).decode()
        
        # Generate unique key for this modal instance
        modal_id = f"modal_{modal_key}"
        
        # Render modal with form submission for closing
        st.markdown(f"""
        <div class="modal-overlay" id="{modal_id}">
            <form method="get" action="?close_modal={modal_key}" style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; margin: 0; padding: 0;">
                <button type="submit" style="position: absolute; width: 100%; height: 100%; background: transparent; border: none; cursor: pointer; padding: 0; margin: 0;"></button>
                <div class="modal-content" style="position: relative; z-index: 2; pointer-events: auto;">
                    <img src="data:image/png;base64,{image_base64}" alt="Error" style="max-width: 100%; height: auto; display: block; border-radius: 12px; pointer-events: none;">
                </div>
            </form>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if modal should be closed via query parameter
        if st.query_params.get("close_modal") == modal_key:
            # Close the modal but DON'T reset login attempts
            st.session_state[modal_key] = False
            st.query_params.clear()
            st.rerun()


def get_login_attempts_file():
    """Get the path to login attempts CSV file"""
    return "data/login_attempts.csv"


def load_login_attempts():
    """Load login attempts from CSV file"""
    attempts_file = get_login_attempts_file()
    if os.path.exists(attempts_file):
        try:
            df = pd.read_csv(attempts_file)
            # Convert timestamp strings to datetime objects
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            # If file is corrupted, create new one
            return pd.DataFrame(columns=['username', 'timestamp'])
    return pd.DataFrame(columns=['username', 'timestamp'])


def save_login_attempts(df):
    """Save login attempts to CSV file"""
    attempts_file = get_login_attempts_file()
    df.to_csv(attempts_file, index=False)


def check_rate_limit(username):
    """Check if user has exceeded login attempt rate limit"""
    now = datetime.now()
    
    # Load attempts from file
    df_attempts = load_login_attempts()
    
    # Filter attempts for this user
    user_attempts = df_attempts[df_attempts['username'] == username]
    
    # Remove attempts older than 15 minutes
    recent_attempts = user_attempts[
        now - user_attempts['timestamp'] < timedelta(minutes=15)
    ]
    
    # Check if rate limited (5 failed attempts)
    if len(recent_attempts) >= 5:
        return True
    
    # Clean up old attempts from the file (optional optimization)
    df_attempts = df_attempts[
        now - df_attempts['timestamp'] < timedelta(minutes=15)
    ]
    save_login_attempts(df_attempts)
    
    return False


def add_failed_attempt(username):
    """Record a failed login attempt to CSV file"""
    df_attempts = load_login_attempts()
    
    # Add new attempt
    new_attempt = pd.DataFrame({
        'username': [username],
        'timestamp': [datetime.now()]
    })
    
    df_attempts = pd.concat([df_attempts, new_attempt], ignore_index=True)
    
    # Save to file
    save_login_attempts(df_attempts)


def clear_login_attempts(username):
    """Clear all login attempts for a user (on successful login)"""
    df_attempts = load_login_attempts()
    
    # Remove all attempts for this user
    df_attempts = df_attempts[df_attempts['username'] != username]
    
    # Save to file
    save_login_attempts(df_attempts)


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
        df = pd.DataFrame([{"username": "admin", "password": "aA1234", "status": "active"}])
        df.to_csv(user_db_path, index=False)
    else:
        df = pd.read_csv(user_db_path)
    
    # Display popup modals if triggered
    if st.session_state.get('show_rate_limit_modal', False):
        show_popup_modal("elements/loginRateLimit.png", "show_rate_limit_modal")
    
    if st.session_state.get('show_acc_deleted_modal', False):
        show_popup_modal("elements/loginAccDeleted.png", "show_acc_deleted_modal")
    
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
        
        # Email input
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown("<label class='input-label'>Email</label>", unsafe_allow_html=True)
        email = st.text_input("Email", key="email_form", label_visibility="collapsed", placeholder="Enter your email")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if not email and st.session_state.get('login_warning'):
            st.markdown(f'<div class="warning-message">{st.session_state.login_warning}</div>', unsafe_allow_html=True)
        elif st.session_state.get('login_error'):
            st.markdown(f'<div class="error-message">{st.session_state.login_error}</div>', unsafe_allow_html=True)

        # Password input
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown("<label class='input-label'>Password</label>", unsafe_allow_html=True)
        password = st.text_input("Password", key="password_form", label_visibility="collapsed", type="password", placeholder="Enter your password")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if not password and st.session_state.get('login_warning'):
            st.markdown(f'<div class="warning-message">{st.session_state.login_warning}</div>', unsafe_allow_html=True)
            st.session_state.login_warning = ''
        elif st.session_state.get('login_error'):
            st.markdown(f'<div class="error-message">{st.session_state.login_error}</div>', unsafe_allow_html=True)
            st.session_state.login_error = ''

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
        
        # Sign in button
        st.markdown('<div class="button-group">', unsafe_allow_html=True)
        login = st.button("Sign in", key="login_btn", width="stretch", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SSO button
        st.markdown('<div class="button-group">', unsafe_allow_html=True)
        sso = st.button("Sign in with SSO", key="sso_btn", width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sign up link
        st.markdown(
            '<div class="signup-text">Don\'t have an account? <a href="#" class="signup-link">Sign up fo free!</a></div>',
            unsafe_allow_html=True
        )
    
    with col2:
        # Right side illustration
        if os.path.exists("elements/Right Side.png"):
            st.markdown('<div class="illustration-container">', unsafe_allow_html=True)
            st.image("elements/Right Side.png")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize session state for error messages
    if 'login_error' not in st.session_state:
        st.session_state.login_error = ''
    if 'login_warning' not in st.session_state:
        st.session_state.login_warning = ''
    if 'show_rate_limit_modal' not in st.session_state:
        st.session_state.show_rate_limit_modal = False
    if 'show_acc_deleted_modal' not in st.session_state:
        st.session_state.show_acc_deleted_modal = False

    # Login logic
    if login:
        # Clear only text error messages, not modal states
        st.session_state.login_error = ''
        st.session_state.login_warning = ''
        
        if email and password:
            # Check rate limit FIRST - before any other checks
            if check_rate_limit(email):
                # Show rate limit modal if not already shown
                if not st.session_state.get('show_rate_limit_modal', False):
                    st.session_state.show_rate_limit_modal = True
                    st.rerun()
                return  # Stop processing - user is rate limited
            
            # Check if user exists
            user_row = df[df["username"] == email]
            
            if not user_row.empty:
                # Check account status
                account_status = user_row.iloc[0].get('status', 'active')
                
                if account_status != 'active':
                    # Show account deleted modal if not already shown
                    if not st.session_state.get('show_acc_deleted_modal', False):
                        st.session_state.show_acc_deleted_modal = True
                        st.rerun()
                    return  # Stop processing - account is disabled
                
                # Check password
                if user_row.iloc[0]['password'] == password:
                    # Successful login - ONLY NOW reset everything
                    st.session_state.authenticated = True
                    st.session_state.username = email
                    st.session_state.login_error = ''
                    st.session_state.login_warning = ''
                    st.session_state.show_rate_limit_modal = False
                    st.session_state.show_acc_deleted_modal = False
                    # Clear failed attempts on successful login
                    clear_login_attempts(email)
                else:
                    # Wrong password - add failed attempt
                    add_failed_attempt(email)
                    st.session_state.login_error = "Invalid email or password"
            else:
                # User not found - add failed attempt
                add_failed_attempt(email)
                st.session_state.login_error = "Invalid email or password"
        else:
            st.session_state.login_warning = "Fill the compulsory fields!"
        
        st.rerun()
