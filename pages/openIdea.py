import streamlit as st

# IMPORTANT
st.set_page_config(
    page_title="UPM Innovation Platform - Idea Details",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import pandas as pd
from pages import header
from styles import edit_idea as edit_idea  # reuse same CSS


# Show the header navigation
header.show_header("Ideas")

# Load styling
edit_idea.load_css()
st.subheader("1. Idea Details")


def _get_selected_idea():
    """Read-only version: get idea from open_id and map to fields."""
    if "home_docs" not in st.session_state:
        st.error("Hmm, couldn't load ideas. Try refreshing the page.")
        return None

    df = st.session_state.home_docs
    open_id = st.session_state.get("open_id")

    if open_id is None:
        st.warning("No idea selected to open.")
        return None

    try:
        row = df.loc[df["id"] == open_id].iloc[0]
    except Exception:
        st.error(f"Could not find idea with ID {open_id}")
        return None

    return {
        "id": int(row["id"]),
        "Idea Title": str(row.get("Name", "")),
        "Category of the idea": str(row.get("Category", "")),
        "Short Description": str(row.get("Description", ""))[:200],
        "Detailed Description": str(row.get("Detailed Description", "")),
        "Estimated Impact / Target Audience": str(row.get("Estimated Impact / Target Audience", "")),
        "Document name": str(row.get("Document name", "")),
        "Visibility Setting": str(row.get("Visibility Setting", "Public")),
        "Status": str(row.get("Status", "")),
        "Owner": str(row.get("Owner", "")),
        "Date published": str(row.get("Date published", "")),
    }


idea = _get_selected_idea()

if idea is None:
    st.error("No idea found to open. Redirecting to Ideas...")
    import time
    time.sleep(2)
    st.switch_page("pages/dashboard.py")
    st.stop()

c1, c2 = st.columns(2)

with c1:
    st.text_input("Idea Title", value=idea["Idea Title"], disabled=True)
    st.selectbox("Category of the idea", [idea["Category of the idea"]], index=0, disabled=True)
    st.text_area("Short Description (max 200 chars)", value=idea["Short Description"], height=100, disabled=True)
    st.text_area("Detailed Description", value=idea["Detailed Description"], height=200, disabled=True)

    st.markdown("<h6>Upload Files</h6>", unsafe_allow_html=True)
    displayed_doc = idea.get("Document name") or "No document attached"
    st.markdown(
        f"""
    <div style="border: 1px dashed #ccc; padding: 2rem; text-align: center;">
        <span style="font-size: 3rem;">⬆️</span>
        <p style="margin:0; font-weight:600; word-break:break-word;">{displayed_doc}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c2:
    st.text_input(
        "Estimated Impact / Target Audience",
        value=idea["Estimated Impact / Target Audience"],
        disabled=True,
    )
    st.selectbox("Visibility Setting", [idea["Visibility Setting"]], index=0, disabled=True)

    st.markdown("### Meta information")
    st.text_input("Status", value=idea.get("Status", ""), disabled=True)
    st.text_input("Owner", value=idea.get("Owner", ""), disabled=True)
    st.text_input("Date published", value=idea.get("Date published", ""), disabled=True)

st.markdown("---")

# Back button
if st.button("← Back to Ideas", use_container_width=False):
    st.session_state.pop("open_id", None)
    st.switch_page("pages/dashboard.py")
