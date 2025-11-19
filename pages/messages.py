import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from data.fake_messages import make_fake_contacts, make_fake_messages, CONTACTS
# Add header
from pages.header import show_header
# -----------------------------------------
# MAIN STREAMLIT UI
# -----------------------------------------

st.set_page_config(layout="wide")

# Show the header at the top, with Messages active
show_header("Messages")

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

    for idx, row in contacts_df.iterrows():
        contact_name = row["name"]
        contact_subject = row.get("subject", "")
        # Count unread messages for this contact
        unread_count = messages_df[(messages_df["sender"] == contact_name) & (messages_df["receiver"] == "User") & (messages_df["read"] == False)].shape[0]

        col1, col2 = st.columns([3, 1])
        with col1:
            contact_html = f"""
            <div style='display:flex; align-items:center; width:100%;'>
                <div style='flex:1; min-width:0;'>
                    <span style='font-size:17px; font-weight:600;'>{contact_name}</span>
                    <span style='font-size:14px; color:#555; font-weight:400; margin-left:8px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:140px; display:inline-block;'>{contact_subject}</span>
                </div>
                {f"<div style='margin-left:12px;'><span style='background:#4CAF50; color:#fff; border-radius:50%; padding:4px 10px; font-size:15px; font-weight:600; display:inline-block;'>{unread_count}</span></div>" if unread_count > 0 else ""}
            </div>
            """
            st.markdown(contact_html, unsafe_allow_html=True)
        with col2:
            if st.button("Open", key=f"open_{contact_name}"):
                st.session_state.selected_contact = contact_name
                # Mark all messages in this thread as read
                mask = (
                    (st.session_state.messages["sender"] == contact_name) &
                    (st.session_state.messages["receiver"] == "User") &
                    (st.session_state.messages["read"] == False)
                )
                st.session_state.messages.loc[mask, "read"] = True
                st.rerun()
        # Add a divider after each contact except the last
        if idx < len(contacts_df) - 1:
            st.markdown("<hr style='margin:2px 0;'>", unsafe_allow_html=True)


# ====================
# RIGHT COLUMN DETAILS
# ====================
with right:
    if st.session_state.selected_contact is None:
        st.info("Click a contact to view messages.")
    else:
        selected = st.session_state.selected_contact
        st.subheader(f"Messages with {selected}")

        relevant = messages_df[(messages_df["sender"] == selected) | (messages_df["receiver"] == selected)].sort_values("timestamp")

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
        # Build all messages as a single HTML string inside a flexbox column-reverse scrollable box
        st.markdown("""
        <style>
        #chat-scroll-box {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #eee;
            border-radius: 12px;
            padding: 10px;
            background: #fafafa;
            display: flex;
            flex-direction: column-reverse;
            scroll-behavior: smooth;
        }
        </style>
        """, unsafe_allow_html=True)
        chat_html = "<div id='chat-scroll-box'>"
        # Render messages in reverse order
        for _, msg in relevant.iloc[::-1].iterrows():
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

