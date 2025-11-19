import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from data.fake_messages import make_fake_contacts, make_fake_messages, CONTACTS
# -----------------------------------------
# MAIN STREAMLIT UI
# -----------------------------------------

st.set_page_config(layout="wide")

# Load data once
if "contacts" not in st.session_state:
    st.session_state.contacts = make_fake_contacts(5)

if "messages" not in st.session_state:
    st.session_state.messages = make_fake_messages(30, CONTACTS)

# Selected contact
if "selected_contact" not in st.session_state:
    st.session_state.selected_contact = None

contacts_df = st.session_state.contacts
messages_df = st.session_state.messages

# Layout
left, right = st.columns([1, 2])


# ================
# LEFT COLUMN LIST
# ================
with left:
    st.header("My Messages")

    for _, row in contacts_df.iterrows():
        contact_name = row["name"]
        contact_messages = messages_df[messages_df["sender"] == contact_name]

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{contact_name}**")
        with col2:
            if st.button("Open", key=f"open_{contact_name}"):
                st.session_state.selected_contact = contact_name


# ====================
# RIGHT COLUMN DETAILS
# ====================
with right:
    if st.session_state.selected_contact is None:
        st.info("Click a contact to view messages.")
    else:
        selected = st.session_state.selected_contact
        st.subheader(f"Messages with {selected}")

        relevant = messages_df[(messages_df["sender"] == selected) | (messages_df["receiver"] == selected)]

        # Custom CSS for compact chat bubbles
        st.markdown("""
            <style>
            .chat-bubble {
                display: inline-block;
                padding: 8px 14px;
                border-radius: 16px;
                margin-bottom: 2px;
                font-size: 15px;
                max-width: 70%;
                word-break: break-word;
            }
            .sent {
                background-color: #DCF8C6;
                margin-left: 30%;
                text-align: right;
            }
            .received {
                background-color: #FFF;
                border: 1px solid #eee;
                margin-right: 30%;
                text-align: left;
            }
            .timestamp {
                font-size: 11px;
                color: #888;
                margin-top: 0px;
                margin-bottom: 6px;
            }
            </style>
        """, unsafe_allow_html=True)

        user_name = "User"
        # Build all messages as a single HTML string inside the scrollable box
        chat_html = "<div id='chat-scroll-box' style='height:400px; overflow-y:auto; border:1px solid #eee; border-radius:12px; padding:10px; background:#fafafa;'>"
        for _, msg in relevant.iterrows():
            is_sent = msg["sender"] == user_name
            bubble_class = "sent" if is_sent else "received"
            align = "right" if is_sent else "left"
            chat_html += (
                f"<div style='width:100%; display:flex; justify-content:{align};'>"
                f"<div class='chat-bubble {bubble_class}'>"
                f"{msg['text']}<br>"
                f"<span class='timestamp'>{msg['timestamp'].strftime('%Y-%m-%d %H:%M')}</span>"
                f"</div></div>"
            )
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)

        # Message input and send logic using a form to avoid StreamlitAPIException
        with st.form(key="send_message_form", clear_on_submit=True):
            new_message = st.text_input("Send message", placeholder="Type here...", key="send_message_input")
            submitted = st.form_submit_button("Send")
            if submitted and new_message:
                new_row = {
                    "sender": user_name,
                    "receiver": selected,
                    "category": "",
                    "text": new_message,
                    "timestamp": datetime.now(),
                    "read": True,
                }
                st.session_state.messages = pd.concat([
                    st.session_state.messages,
                    pd.DataFrame([new_row])
                ], ignore_index=True)
                st.rerun()

