import streamlit as st
import pandas as pd
import os

# Ensure folders exist
os.makedirs("elements", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Load user database from CSV
user_db_path = "data/users.csv"
if not os.path.exists(user_db_path):
    # Create a starter CSV file with admin user if it doesn't exist
    df = pd.DataFrame([{"username": "admin", "password": "aA1234"}])
    df.to_csv(user_db_path, index=False)
else:
    df = pd.read_csv(user_db_path)

# --- UI code (use elements PNGs as before, omitted here for brevity) ---

# Example login check (insert after user presses the "Sign in" button)
if st.button("Sign in"):
    user_row = df[(df["username"] == email) & (df["password"] == password)]
    if not user_row.empty:
        st.success(f"Welcome, {email}!")
    else:
        st.error("Invalid login.")

# --- rest of the image and layout code ---

# Custom CSS for layout and appearance
st.markdown("""
    <style>
    .main { padding: 0 !important; }
    .stApp {
        background-color: #fafafa;
    }
    .login-container {
        display: flex; flex-direction: row; height: 100vh; align-items: center; justify-content: space-between;
    }
    .login-left {
        width: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center;
        padding-left: 10vw;
    }
    .login-right {
        width: 50%; display: flex; align-items: center; justify-content: center;
    }
    .form-group { margin-bottom: 18px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="login-container">', unsafe_allow_html=True)

# Left side (login form and elements)
st.markdown('<div class="login-left">', unsafe_allow_html=True)
st.image("elements/Headline.png")
st.image("elements/Email Form.png", use_column_width=False)
email = st.text_input("", key="email_form", label_visibility="collapsed", placeholder="Enter your email")
st.image("elements/Password Form.png", use_column_width=False)
password = st.text_input("", key="password_form", label_visibility="collapsed", type="password", placeholder="Enter your password")
st.image("elements/Remember & Forgot.png", use_column_width=False)
remember_me = st.checkbox("Remember me", key="remember_me")
forgot = st.button("Forgot password")
st.image("elements/Sign in Button.png", use_column_width=False)
login = st.button("Sign in")
st.image("elements/Sign in Button Google.png", use_column_width=False)
sso = st.button("Sign in with SSO")
st.image("elements/Don’t have an account_ Sign up fo free!.png", use_column_width=False)
st.markdown('</div>', unsafe_allow_html=True)

# Right side (illustration)
st.markdown('<div class="login-right">', unsafe_allow_html=True)
st.image("elements/Right Side.png", use_column_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)
