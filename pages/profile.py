import streamlit as st
from pages import header

header.show_header("Profile")
st.title("Profile")

username = st.session_state.get("username", "User")
st.write(f"Welcome, {username}!")

st.subheader("Account Settings")
st.text_input("Username", value=username)
st.text_input("Email", value=f"{username}@upm.es")
st.button("Save Changes")
