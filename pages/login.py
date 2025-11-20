import streamlit as st

# IMPORTANT: Must be first Streamlit command
st.set_page_config(
    page_title="UPM Innovation Platform - Login",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import pandas as pd
import os
from datetime import datetime, timedelta
from styles import login as login_styles


def show_popup_modal(image_path, modal_key="error_modal"):
    """Shows a popup modal with an image - closes when you click outside it"""
    if st.session_state.get(modal_key, False):
        import base64
        
        # Convert the image to base64 so we can embed it
        image_base64 = ""
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                image_base64 = base64.b64encode(img_file.read()).decode()
        
        # Make a unique ID for this specific modal
        modal_id = f"modal_{modal_key}"
        
        # Render the modal with a form that closes it when clicked outside
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
        
        # Check if we should close the modal based on the URL parameter
        if st.query_params.get("close_modal") == modal_key:
            # Close the modal but keep the login attempts intact
            st.session_state[modal_key] = False
            st.query_params.clear()
            st.rerun()


def get_login_attempts_file():
    """Returns the path where we store login attempt data"""
    return "data/login_attempts.csv"


def load_login_attempts():
    """Load up the login attempts from the CSV file"""
    attempts_file = get_login_attempts_file()
    if os.path.exists(attempts_file):
        try:
            df = pd.read_csv(attempts_file)
            # Make sure timestamps are actual datetime objects
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            # File got corrupted somehow, just start fresh
            return pd.DataFrame(columns=['username', 'timestamp'])
    return pd.DataFrame(columns=['username', 'timestamp'])


def save_login_attempts(df):
    """Save the login attempts back to the CSV file"""
    attempts_file = get_login_attempts_file()
    df.to_csv(attempts_file, index=False)


def check_rate_limit(username):
    """Check if someone's tried logging in too many times"""
    now = datetime.now()
    
    # Load their previous attempts
    df_attempts = load_login_attempts()
    
    # Just look at this specific user
    user_attempts = df_attempts[df_attempts['username'] == username]
    
    # Only care about attempts from the last 15 minutes
    recent_attempts = user_attempts[
        now - user_attempts['timestamp'] < timedelta(minutes=15)
    ]
    
    # If they've failed 5 times, they're locked out
    if len(recent_attempts) >= 5:
        return True
    
    # Clean up old attempts while we're here to keep the file tidy
    df_attempts = df_attempts[
        now - df_attempts['timestamp'] < timedelta(minutes=15)
    ]
    save_login_attempts(df_attempts)
    
    return False


def add_failed_attempt(username):
    """Log a failed login attempt to the CSV"""
    df_attempts = load_login_attempts()
    
    # Add this new failed attempt
    new_attempt = pd.DataFrame({
        'username': [username],
        'timestamp': [datetime.now()]
    })
    
    df_attempts = pd.concat([df_attempts, new_attempt], ignore_index=True)
    
    # Write it back to the file
    save_login_attempts(df_attempts)


def clear_login_attempts(username):
    """Wipe out all failed attempts for a user (they logged in successfully)"""
    df_attempts = load_login_attempts()
    
    # Remove everything for this user
    df_attempts = df_attempts[df_attempts['username'] != username]
    
    # Save the cleaned up data
    save_login_attempts(df_attempts)


# Main page execution (no function wrapper)
# Load the styling for the login page
login_styles.load_css()

# Make sure these folders exist before we try to use them
os.makedirs("elements", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Load up the user database from CSV
user_db_path = "data/users.csv"
if not os.path.exists(user_db_path):
    df = pd.DataFrame([{"username": "admin", "password": "aA1234", "status": "active"}])
    df.to_csv(user_db_path, index=False)
else:
    df = pd.read_csv(user_db_path)

# Show popups if we've triggered them
if st.session_state.get('show_rate_limit_modal', False):
    show_popup_modal("elements/loginRateLimit.png", "show_rate_limit_modal")

if st.session_state.get('show_acc_deleted_modal', False):
    show_popup_modal("elements/loginAccDeleted.png", "show_acc_deleted_modal")

# Split the page into two columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    # Big welcome message at the top
    st.markdown("""
    <div class="login-header">
        <h1 style="font-size: 2.8rem; font-weight: 800; color: #1a1a1a; margin: 0; margin-bottom: 0.3rem;">WELCOME</h1>
        <p style="font-size: 0.95rem; color: #6b7280; margin-bottom: 1.5rem; margin-top: 0;">Please enter your details.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Email input field
    st.markdown('<div class="input-group">', unsafe_allow_html=True)
    st.markdown("<label class='input-label'>Email</label>", unsafe_allow_html=True)
    email = st.text_input("Email", key="email_form", label_visibility="collapsed", placeholder="Enter your email")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not email and st.session_state.get('login_warning'):
        st.markdown(f'<div class="warning-message">{st.session_state.login_warning}</div>', unsafe_allow_html=True)
    elif st.session_state.get('login_error'):
        st.markdown(f'<div class="error-message">{st.session_state.login_error}</div>', unsafe_allow_html=True)

    # Password input field
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

    # Remember me checkbox and forgot password link side by side
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
        if st.button("Forgot password", key="forgot_btn"):
            st.info("We're still working on the password reset feature - hang tight!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main sign in button
    st.markdown('<div class="button-group">', unsafe_allow_html=True)
    login = st.button("Sign in", key="login_btn", type="primary", width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SSO option
    st.markdown('<div class="button-group">', unsafe_allow_html=True)
    sso = st.button("Sign in with SSO", key="sso_btn", width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sign up link at the bottom
    st.markdown(
        '<div class="signup-text">Don\'t have an account? <a href="#" class="signup-link">Sign up for free!</a></div>',
        unsafe_allow_html=True
    )

with col2:
    # Nice illustration on the right side
    if os.path.exists("elements/Right Side.png"):
        st.markdown('<div class="illustration-container">', unsafe_allow_html=True)
        st.image("elements/Right Side.png")
        st.markdown('</div>', unsafe_allow_html=True)

# Set up session state variables if they don't exist yet
if 'login_error' not in st.session_state:
    st.session_state.login_error = ''
if 'login_warning' not in st.session_state:
    st.session_state.login_warning = ''
if 'show_rate_limit_modal' not in st.session_state:
    st.session_state.show_rate_limit_modal = False
if 'show_acc_deleted_modal' not in st.session_state:
    st.session_state.show_acc_deleted_modal = False

# Handle the login button click
if login:
    # Clear out any old error messages (but keep the modal states)
    st.session_state.login_error = ''
    st.session_state.login_warning = ''
    
    if email and password:
        # First thing - check if they've been trying too much
        if check_rate_limit(email):
            # Show the rate limit popup if we haven't already
            if not st.session_state.get('show_rate_limit_modal', False):
                st.session_state.show_rate_limit_modal = True
                st.rerun()
            # Don't let them proceed - they're locked out
        else:
            # See if this user exists in the database
            user_row = df[df["username"] == email]
            
            if not user_row.empty:
                # Check if their account is still active
                account_status = user_row.iloc[0].get('status', 'active')
                
                if account_status != 'active':
                    # Their account got deleted or disabled
                    if not st.session_state.get('show_acc_deleted_modal', False):
                        st.session_state.show_acc_deleted_modal = True
                        st.rerun()
                else:
                    # Now check if the password matches
                    if user_row.iloc[0]['password'] == password:
                        # They got it right! Log them in and clear everything
                        st.session_state.authenticated = True
                        st.session_state.username = email
                        st.session_state.login_error = ''
                        st.session_state.login_warning = ''
                        st.session_state.show_rate_limit_modal = False
                        st.session_state.show_acc_deleted_modal = False
                        # Wipe their failed attempts since they got in
                        clear_login_attempts(email)
                        # Redirect to home page
                        st.switch_page("pages/home.py")
                    else:
                        # Wrong password - log this failed attempt
                        add_failed_attempt(email)
                        st.session_state.login_error = "That email or password doesn't look right"
            else:
                # No user found with that email - log it as failed
                add_failed_attempt(email)
                st.session_state.login_error = "That email or password doesn't look right"
    else:
        st.session_state.login_warning = "Please fill in both fields"
    
    st.rerun()
