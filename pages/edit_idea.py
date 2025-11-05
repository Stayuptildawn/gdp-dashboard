import streamlit as st
import pandas as pd
from styles import edit_idea as edit_idea
from data.fake_docs import make_fake_docs

def _get_selected_idea():
    """Return a dict with fields mapped for the edit form from the selected idea.
    Falls back to empty defaults when not available.
    """
    # Ensure the documents table exists (fallback if user navigates directly)
    if "home_docs" not in st.session_state:
        st.session_state.home_docs = make_fake_docs(30)

    df = st.session_state.home_docs
    edit_id = st.session_state.get("edit_id")

    if edit_id is None:
        return None

    try:
        row = df.loc[df["id"] == edit_id].iloc[0]
    except Exception:
        return None

    # Map dataset columns to form fields
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


def show():
    # Load page-specific CSS so inputs have persistent black borders
    edit_idea.load_css()
    st.subheader("1. Idea Submission Form")

    # Initialize validation flag (used to show inline warnings)
    if "edit_validate" not in st.session_state:
        st.session_state.edit_validate = False

    # Prefill with selected idea if present
    idea = _get_selected_idea()
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
        # Build category options dynamically from dataset + sensible fallbacks
        options = []
        try:
            options = sorted(set(st.session_state.home_docs.get("Category", pd.Series()).dropna().astype(str)))
        except Exception:
            pass
        fallback = ["TRANSPORT", "HEALTH", "ENERGY", "AI", "Business", "Technology", "Social"]
        options = list(dict.fromkeys([*(options or []), *fallback]))
        selected_idx = options.index(data["Category of the idea"]) if data["Category of the idea"] in options else 0
        # Inputs
        title = st.text_input("Idea Title", value=data["Idea Title"])
        title_warn = st.empty()
        category = st.selectbox("Category of the idea", options, index=selected_idx)
        short_desc = st.text_area("Short Description (max 200 chars)", value=data["Short Description"], height=100)
        short_warn = st.empty()
        detailed_desc = st.text_area("Detailed Description", value=data["Detailed Description"], height=200)
        detailed_warn = st.empty()

        # Inline warnings below inputs when validation is active (show next to each control)
        if st.session_state.get("edit_validate") and not (title or "").strip():
            title_warn.markdown(f'<div class="warning-message">{st.session_state.get("edit_warning", "Fill the compulsory fields!")}</div>', unsafe_allow_html=True)
        if st.session_state.get("edit_validate") and not (short_desc or "").strip():
            short_warn.markdown(f'<div class="warning-message">{st.session_state.get("edit_warning", "Fill the compulsory fields!")}</div>', unsafe_allow_html=True)
        if st.session_state.get("edit_validate") and not (detailed_desc or "").strip():
            detailed_warn.markdown(f'<div class="warning-message">{st.session_state.get("edit_warning", "Fill the compulsory fields!")}</div>', unsafe_allow_html=True)

        st.markdown("<h6>Upload Files</h6>", unsafe_allow_html=True)
        displayed_doc = data.get("Document name") or "No document attached"
        st.markdown(f"""
        <div style="border: 1px dashed #ccc; padding: 2rem; text-align: center;">
            <span style="font-size: 3rem;">⬆️</span>
            <p style=\"margin:0; font-weight:600; word-break:break-word;\">{displayed_doc}</p>
        </div>
        """, unsafe_allow_html=True)

    estimated_impact = st.text_input("Estimated Impact / Target Audience", value=data["Estimated Impact / Target Audience"], placeholder="e.g., Students, SMEs, City residents")
    impact_warn = st.empty()
    if st.session_state.get("edit_validate") and not (estimated_impact or "").strip():
        impact_warn.markdown(f'<div class="warning-message">{st.session_state.get("edit_warning", "Fill the compulsory fields!")}</div>', unsafe_allow_html=True)
    vis_opts = ["Public", "Private"]
    vis_idx = vis_opts.index(data["Visibility Setting"]) if data["Visibility Setting"] in vis_opts else 0
    visibility = st.selectbox("Visibility Setting", vis_opts, index=vis_idx)

    with c2:
        st.subheader("2. Terms & Conditions")
        terms = st.checkbox("I have read and accept the Term and Conditions.")
        
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("Save as Draft"):
                st.success("Idea saved as draft!")
        with sc2:
            if st.button("Submit", type="primary"):
                # Trigger validation for empty required fields
                required_ok = all([
                    (title or "").strip(),
                    (short_desc or "").strip(),
                    (detailed_desc or "").strip(),
                    (estimated_impact or "").strip(),
                ])

                if not required_ok or not terms:
                    st.session_state.edit_validate = True
                    st.session_state.edit_warning = "Fill the compulsory fields!"
                    # store a flag so the error shows after rerun
                    st.session_state.edit_terms_error = not terms
                    st.rerun()
                else:
                    # Persist updates back to the table
                    try:
                        df = st.session_state.get("home_docs")
                        edit_id = st.session_state.get("edit_id")
                        if df is not None and edit_id is not None and "id" in df.columns:
                            idx = df.index[df["id"] == edit_id]
                            if len(idx) > 0:
                                i = idx[0]
                                df.at[i, "Name"] = (title or "").strip()
                                df.at[i, "Category"] = category
                                df.at[i, "Description"] = (short_desc or "").strip()[:200]
                                df.at[i, "Detailed Description"] = (detailed_desc or "")
                                df.at[i, "Estimated Impact / Target Audience"] = (estimated_impact or "")
                                # Save back
                                st.session_state.home_docs = df
                    except Exception as e:
                        st.error(f"Failed to update idea: {e}")
                        st.stop()

                    # Clear validation and navigate back to Home
                    st.session_state.edit_validate = False
                    st.query_params["page"] = "Home"
                    try:
                        del st.query_params["edit_id"]
                    except Exception:
                        pass
                    st.session_state.pop("edit_id", None)
                    st.rerun()
        st.info("Your idea will be public or visible to others. You can edit it anytime in 'My Ideas'")

    # Render a top-level terms error if flagged (so it persists after rerun)
    if st.session_state.pop("edit_terms_error", False):
        st.markdown('<div class="error-message">Please accept the terms and conditions.</div>', unsafe_allow_html=True)

