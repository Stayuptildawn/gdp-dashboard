import streamlit as st
import pandas as pd
from styles import edit_idea as edit_idea
from data.fake_docs import make_fake_docs


def show():
    # Load page-specific CSS so inputs have persistent black borders
    edit_idea.load_css()
    st.subheader("1. Idea Submission Form")

    # Initialize validation flag (used to show inline warnings)
    if "publish_validate" not in st.session_state:
        st.session_state.publish_validate = False

    # Ensure the documents table exists
    if "home_docs" not in st.session_state:
        st.session_state.home_docs = make_fake_docs(30)

    # Start with empty fields for new idea
    defaults = {
        "Idea Title": "",
        "Category of the idea": "",
        "Short Description": "",
        "Detailed Description": "",
        "Estimated Impact / Target Audience": "",
        "Document name": "",
        "Visibility Setting": "Public",
    }

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
        
        # Inputs - all start empty
        title = st.text_input("Idea Title", value=defaults["Idea Title"])
        title_warn = st.empty()
        category = st.selectbox("Category of the idea", options, index=0)
        short_desc = st.text_area("Short Description (max 200 chars)", value=defaults["Short Description"], height=100)
        short_warn = st.empty()
        detailed_desc = st.text_area("Detailed Description", value=defaults["Detailed Description"], height=200)
        detailed_warn = st.empty()

        # Inline warnings below inputs when validation is active
        if st.session_state.get("publish_validate") and not (title or "").strip():
            title_warn.markdown(f'<div class="warning-message">{st.session_state.get("publish_warning", "Fill the compulsory fields!")}</div>', unsafe_allow_html=True)
        if st.session_state.get("publish_validate") and not (short_desc or "").strip():
            short_warn.markdown(f'<div class="warning-message">{st.session_state.get("publish_warning", "Fill the compulsory fields!")}</div>', unsafe_allow_html=True)
        if st.session_state.get("publish_validate") and not (detailed_desc or "").strip():
            detailed_warn.markdown(f'<div class="warning-message">{st.session_state.get("publish_warning", "Fill the compulsory fields!")}</div>', unsafe_allow_html=True)

        st.markdown("<h6>Upload Files</h6>", unsafe_allow_html=True)
        displayed_doc = "No document attached"
        st.markdown(f"""
        <div style="border: 1px dashed #ccc; padding: 2rem; text-align: center;">
            <span style="font-size: 3rem;">⬆️</span>
            <p style="margin:0; font-weight:600; word-break:break-word;">{displayed_doc}</p>
        </div>
        """, unsafe_allow_html=True)

    estimated_impact = st.text_input("Estimated Impact / Target Audience", value=defaults["Estimated Impact / Target Audience"], placeholder="e.g., Students, SMEs, City residents")
    impact_warn = st.empty()
    if st.session_state.get("publish_validate") and not (estimated_impact or "").strip():
        impact_warn.markdown(f'<div class="warning-message">{st.session_state.get("publish_warning", "Fill the compulsory fields!")}</div>', unsafe_allow_html=True)
    
    vis_opts = ["Public", "Private"]
    visibility = st.selectbox("Visibility Setting", vis_opts, index=0)

    with c2:
        st.subheader("2. Terms & Conditions")
        terms = st.checkbox("I have read and accept the Terms and Conditions.")
        
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("Save as Draft"):
                st.success("Idea saved as draft!")
        with sc2:
            if st.button("Publish", type="primary"):
                # Trigger validation for empty required fields
                required_ok = all([
                    (title or "").strip(),
                    (short_desc or "").strip(),
                    (detailed_desc or "").strip(),
                    (estimated_impact or "").strip(),
                ])

                if not required_ok or not terms:
                    st.session_state.publish_validate = True
                    st.session_state.publish_warning = "Fill the compulsory fields!"
                    # store a flag so the error shows after rerun
                    st.session_state.publish_terms_error = not terms
                    st.rerun()
                else:
                    # Add new idea to the table
                    try:
                        df = st.session_state.get("home_docs")
                        if df is not None:
                            # Generate a new unique ID
                            new_id = df["id"].max() + 1 if len(df) > 0 else 1
                            
                            # Create new row
                            new_row = {
                                "id": new_id,
                                "Name": (title or "").strip(),
                                "Category": category,
                                "Description": (short_desc or "").strip()[:200],
                                "Detailed Description": (detailed_desc or ""),
                                "Estimated Impact / Target Audience": (estimated_impact or ""),
                                "Document name": "",
                                "Status": "Published",
                                "Date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                            }
                            
                            # Add the new row to dataframe
                            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                            
                            # Save back
                            st.session_state.home_docs = df
                            
                            st.success("🎉 Idea published successfully!")
                    except Exception as e:
                        st.error(f"Failed to publish idea: {e}")
                        st.stop()

                    # Clear validation and navigate back to Home
                    st.session_state.publish_validate = False
                    st.query_params["page"] = "Home"
                    st.rerun()
        
        st.info("Your idea will be published and visible to others. You can edit it anytime in 'My Ideas'")

    # Render a top-level terms error if flagged (so it persists after rerun)
    if st.session_state.pop("publish_terms_error", False):
        st.markdown('<div class="error-message">Please accept the terms and conditions.</div>', unsafe_allow_html=True)


# Call the show function when the page loads
if __name__ == "__main__":
    show()
