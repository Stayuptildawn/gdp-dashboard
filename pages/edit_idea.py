import streamlit as st
import pandas as pd
import os
from datetime import date
from pages import header
from styles import edit_idea as edit_idea


# Show the header navigation
header.show_header("My Ideas")


# --- helpers ---
def _persist_changes(form, status="On Review", set_date=True):
    """Save the changes to the dataframe, CSV, and head back to My Ideas page."""
    try:
        df = st.session_state.get("home_docs")
        edit_id = st.session_state.get("edit_id")
        if df is not None and edit_id is not None and "id" in df.columns:
            idx = df.index[df["id"] == edit_id]
            if len(idx) > 0:
                i = idx[0]
                df.at[i, "Name"] = (form["title"] or "").strip()
                df.at[i, "Category"] = form["category"]
                df.at[i, "Description"] = (form["short_desc"] or "").strip()[:200]
                df.at[i, "Detailed Description"] = (form["detailed_desc"] or "")
                df.at[i, "Estimated Impact / Target Audience"] = (form["estimated_impact"] or "")
                if set_date:
                    df.at[i, "Date published"] = date.today()
                df.at[i, "Status"] = status
                st.session_state.home_docs = df
                
                # Save to CSV
                csv_path = "data/ideas.csv"
                os.makedirs("data", exist_ok=True)
                df.to_csv(csv_path, index=False)
                
    except Exception as e:
        st.error(f"Couldn't save your changes right now. Give it another try? (Error: {e})")
        st.stop()

    st.session_state["flash_success"] = "Your changes have been saved!"
    st.session_state.edit_validate = False
    st.session_state.pop("edit_id", None)
    st.switch_page("pages/myideas.py")

def _get_selected_idea():
    """Grab the selected idea and map it to the form fields.
    Returns empty defaults if nothing's found.
    """
    # Make sure we have the data loaded
    if "home_docs" not in st.session_state:
        st.error("Hmm, couldn't load your ideas. Try refreshing the page.")
        return None

    df = st.session_state.home_docs
    edit_id = st.session_state.get("edit_id")

    if edit_id is None:
        st.warning("No idea selected for editing.")
        return None

    try:
        row = df.loc[df["id"] == edit_id].iloc[0]
    except Exception:
        st.error(f"Could not find idea with ID {edit_id}")
        return None

    # Pull the data from the table and map it to what the form expects
    return {
        "id": int(row["id"]),
        "Idea Title": str(row.get("Name", "")),
        "Category of the idea": str(row.get("Category", "")),
        "Short Description": str(row.get("Description", ""))[:200],
        "Detailed Description": str(row.get("Detailed Description", "")),
        "Estimated Impact / Target Audience": str(row.get("Estimated Impact / Target Audience", "")),
        "Document name": str(row.get("Document name", "")),
        "Visibility Setting": "Public",
    }


# Load the styling to keep input borders consistent
edit_idea.load_css()
st.subheader("1. Edit Idea")

# Set up validation flag for showing warnings
if "edit_validate" not in st.session_state:
    st.session_state.edit_validate = False

# Fill in the form with the idea we're editing, if there is one
idea = _get_selected_idea()

if idea is None:
    st.error("No idea found to edit. Redirecting to My Ideas...")
    import time
    time.sleep(2)
    st.switch_page("pages/myideas.py")
    st.stop()

defaults = {
    "Idea Title": "",
    "Category of the idea": "",
    "Short Description": "",
    "Detailed Description": "",
    "Estimated Impact / Target Audience": "",
    "Document name": "",
    "Visibility Setting": "Public",
}
data = {**defaults, **(idea or {})}

c1, c2 = st.columns(2)

with c1:
    # Build the category dropdown from existing data plus some fallback options
    options = []
    try:
        options = sorted(set(st.session_state.home_docs.get("Category", pd.Series()).dropna().astype(str)))
    except Exception:
        pass
    fallback = ["TRANSPORT", "HEALTH", "ENERGY", "AI", "Business", "Technology", "Social"]
    options = list(dict.fromkeys([*(options or []), *fallback]))
    selected_idx = options.index(data["Category of the idea"]) if data["Category of the idea"] in options else 0
    
    # Form inputs
    title = st.text_input("Idea Title *", value=data["Idea Title"])
    title_warn = st.empty()
    category = st.selectbox("Category of the idea *", options, index=selected_idx)
    short_desc = st.text_area("Short Description (max 200 chars) *", value=data["Short Description"], height=100)
    short_warn = st.empty()
    detailed_desc = st.text_area("Detailed Description *", value=data["Detailed Description"], height=200)
    detailed_warn = st.empty()

    # Show warning messages under any empty required fields
    if st.session_state.get("edit_validate") and not (title or "").strip():
        title_warn.markdown(f'<div class="warning-message">{st.session_state.get("edit_warning", "Please fill in all required fields")}</div>', unsafe_allow_html=True)
    if st.session_state.get("edit_validate") and not (short_desc or "").strip():
        short_warn.markdown(f'<div class="warning-message">{st.session_state.get("edit_warning", "Please fill in all required fields")}</div>', unsafe_allow_html=True)
    if st.session_state.get("edit_validate") and not (detailed_desc or "").strip():
        detailed_warn.markdown(f'<div class="warning-message">{st.session_state.get("edit_warning", "Please fill in all required fields")}</div>', unsafe_allow_html=True)

    st.markdown("<h6>Upload Files</h6>", unsafe_allow_html=True)
    displayed_doc = data.get("Document name") or "No document attached"
    st.markdown(f"""
    <div style="border: 1px dashed #ccc; padding: 2rem; text-align: center;">
        <span style="font-size: 3rem;">⬆️</span>
        <p style="margin:0; font-weight:600; word-break:break-word;">{displayed_doc}</p>
    </div>
    """, unsafe_allow_html=True)

estimated_impact = st.text_input("Estimated Impact / Target Audience *", value=data["Estimated Impact / Target Audience"], placeholder="e.g., Students, SMEs, City residents")
impact_warn = st.empty()
if st.session_state.get("edit_validate") and not (estimated_impact or "").strip():
    impact_warn.markdown(f'<div class="warning-message">{st.session_state.get("edit_warning", "Please fill in all required fields")}</div>', unsafe_allow_html=True)

vis_opts = ["Public", "Private"]
vis_idx = vis_opts.index(data["Visibility Setting"]) if data["Visibility Setting"] in vis_opts else 0
visibility = st.selectbox("Visibility Setting", vis_opts, index=vis_idx)

with c2:
    st.subheader("2. Terms & Conditions")
    terms = st.checkbox("I have read and accept the Terms and Conditions.")
    # Warning shows up right under the checkbox if they forgot to check it
    terms_warn = st.empty()
    if terms:
        st.session_state.pop("edit_terms_error", None)
    elif st.session_state.get("edit_terms_error"):
        terms_warn.markdown('<div class="error-message">You need to accept the terms and conditions.</div>', unsafe_allow_html=True)

    sc1, sc2 = st.columns(2)
    form = {
        "title": title,
        "category": category,
        "short_desc": short_desc,
        "detailed_desc": detailed_desc,
        "estimated_impact": estimated_impact,
        "visibility": visibility,
    }
    
    with sc1:
        if st.button("Save as Draft", width="stretch"):
            _persist_changes(form, status="On Review", set_date=True)
    
    with sc2:
        if st.button("Submit", type="primary", width="stretch"):
            # Check if all the required fields are filled in
            required_ok = all([
                (title or "").strip(),
                (short_desc or "").strip(),
                (detailed_desc or "").strip(),
                (estimated_impact or "").strip(),
            ])

            if not required_ok or not terms:
                st.session_state.edit_validate = True
                st.session_state.edit_warning = "Please fill in all required fields"
                # Keep track so the error still shows after the page refreshes
                st.session_state.edit_terms_error = not terms
                st.rerun()
            else:
                # Save everything back to the table
                _persist_changes(form, status="Accepted", set_date=True)
    
    st.info("💡 Once submitted, your idea will be visible to everyone. Don't worry - you can edit it anytime from 'My Ideas'.")

# Cancel button at the bottom
if st.button("← Cancel", width=False):
    st.session_state.pop("edit_id", None)
    st.switch_page("pages/myideas.py")
