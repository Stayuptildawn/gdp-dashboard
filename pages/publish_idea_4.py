import streamlit as st
import pandas as pd
import time
from styles import edit_idea as edit_idea
from data.fake_docs import make_fake_docs


def show():
    # Load page-specific CSS so inputs have persistent black borders
    edit_idea.load_css()
    st.subheader("1. Idea Submission Form")

    # Initialize validation flag (used to show inline warnings)
    if "publish_validate" not in st.session_state:
        st.session_state.publish_validate = False

    # Initialize publishing flag to prevent duplicate submissions
    if "is_publishing" not in st.session_state:
        st.session_state.is_publishing = False

    # Ensure the documents table exists
    if "home_docs" not in st.session_state:
        st.session_state.home_docs = make_fake_docs(30)

    # Initialize form data in session state for field persistence on validation failure
    if "publish_form_data" not in st.session_state:
        st.session_state.publish_form_data = {
            "Idea Title": "",
            "Category of the idea": "",
            "Short Description": "",
            "Detailed Description": "",
            "Estimated Impact / Target Audience": "",
            "Document name": "",
            "Visibility Setting": "Public",
        }
    
    # Use session state data for persistence on validation failure
    defaults = st.session_state.publish_form_data

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
        
        # Find selected index for category
        selected_idx = 0
        if defaults["Category of the idea"] in options:
            selected_idx = options.index(defaults["Category of the idea"])
        
        # Inputs - use keys to preserve values across reruns
        title = st.text_input("Idea Title", value=defaults["Idea Title"], key="publish_title")
        title_warn = st.empty()
        category = st.selectbox("Category of the idea", options, index=selected_idx, key="publish_category")
        short_desc = st.text_area("Short Description (max 200 chars)", value=defaults["Short Description"], height=100, key="publish_short_desc")
        short_warn = st.empty()
        detailed_desc = st.text_area("Detailed Description", value=defaults["Detailed Description"], height=200, key="publish_detailed_desc")
        detailed_warn = st.empty()

        # Update session state with current values for persistence
        st.session_state.publish_form_data["Idea Title"] = title
        st.session_state.publish_form_data["Category of the idea"] = category
        st.session_state.publish_form_data["Short Description"] = short_desc
        st.session_state.publish_form_data["Detailed Description"] = detailed_desc

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

    estimated_impact = st.text_input("Estimated Impact / Target Audience", value=defaults["Estimated Impact / Target Audience"], placeholder="e.g., Students, SMEs, City residents", key="publish_impact")
    impact_warn = st.empty()
    
    # Update session state
    st.session_state.publish_form_data["Estimated Impact / Target Audience"] = estimated_impact
    
    if st.session_state.get("publish_validate") and not (estimated_impact or "").strip():
        impact_warn.markdown(f'<div class="warning-message">{st.session_state.get("publish_warning", "Fill the compulsory fields!")}</div>', unsafe_allow_html=True)
    
    vis_opts = ["Public", "Private"]
    vis_idx = vis_opts.index(defaults["Visibility Setting"]) if defaults["Visibility Setting"] in vis_opts else 0
    visibility = st.selectbox("Visibility Setting", vis_opts, index=vis_idx, key="publish_visibility")
    
    # Update session state
    st.session_state.publish_form_data["Visibility Setting"] = visibility

    with c2:
        st.subheader("2. Terms & Conditions")
        terms = st.checkbox("I have read and accept the Terms and Conditions.", key="publish_terms")
        
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("Save as Draft", disabled=st.session_state.is_publishing):
                # Validate at least title is present for draft
                if not (title or "").strip():
                    st.warning("⚠️ Please provide at least an Idea Title to save as draft.")
                else:
                    try:
                        df = st.session_state.get("home_docs")
                        if df is not None:
                            # Generate a new unique ID
                            new_id = df["id"].max() + 1 if len(df) > 0 else 1
                            
                            # Create new row with Draft status
                            new_row = {
                                "id": new_id,
                                "Status": "Draft",
                                "From date": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                                "To date": "",
                                "Document name": "",
                                "Date published": "",
                                "Issue Number": "",
                                "Name": (title or "").strip(),
                                "Category": category,
                                "Description": (short_desc or "").strip()[:200],
                                "Detailed Description": (detailed_desc or ""),
                                "Estimated Impact / Target Audience": (estimated_impact or ""),
                            }
                            
                            # Add the new row to dataframe
                            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                            
                            # Save back
                            st.session_state.home_docs = df
                            
                            # Clear form data
                            st.session_state.publish_form_data = {
                                "Idea Title": "",
                                "Category of the idea": "",
                                "Short Description": "",
                                "Detailed Description": "",
                                "Estimated Impact / Target Audience": "",
                                "Document name": "",
                                "Visibility Setting": "Public",
                            }
                            
                            st.success("💾 Idea saved as draft! You can edit it later from 'My Ideas'")
                            st.session_state.publish_validate = False
                            
                            # Delay and redirect
                            time.sleep(1.5)
                            st.query_params["page"] = "Home"
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"❌ Failed to save draft. Please try again. Error: {str(e)}")
                        
        with sc2:
            if st.button("Publish", type="primary", disabled=st.session_state.is_publishing):
                # Set publishing flag to prevent duplicate submissions
                st.session_state.is_publishing = True
                
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
                    st.session_state.is_publishing = False
                    st.rerun()
                else:
                    # Add new idea to the table
                    try:
                        df = st.session_state.get("home_docs")
                        if df is not None:
                            # Generate a new unique ID
                            new_id = df["id"].max() + 1 if len(df) > 0 else 1
                            
                            # Create new row - Status "Accepted" means published
                            new_row = {
                                "id": new_id,
                                "Status": "Accepted",
                                "From date": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                                "To date": "",
                                "Document name": "",
                                "Date published": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                                "Issue Number": f"{new_id}.00/000PLN",
                                "Name": (title or "").strip(),
                                "Category": category,
                                "Description": (short_desc or "").strip()[:200],
                                "Detailed Description": (detailed_desc or ""),
                                "Estimated Impact / Target Audience": (estimated_impact or ""),
                            }
                            
                            # Add the new row to dataframe
                            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                            
                            # Save back
                            st.session_state.home_docs = df
                            
                            st.success("🎉 Idea published successfully!")
                            
                            # Clear form data after successful publish
                            st.session_state.publish_form_data = {
                                "Idea Title": "",
                                "Category of the idea": "",
                                "Short Description": "",
                                "Detailed Description": "",
                                "Estimated Impact / Target Audience": "",
                                "Document name": "",
                                "Visibility Setting": "Public",
                            }
                            
                            # Small delay to show success message
                            time.sleep(1.5)
                            
                    except Exception as e:
                        st.error(f"❌ Failed to publish idea. Please try again. Error: {str(e)}")
                        st.session_state.is_publishing = False
                        st.stop()

                    # Clear validation and reset publishing flag
                    st.session_state.publish_validate = False
                    st.session_state.is_publishing = False
                    
                    # Navigate back to Home
                    st.query_params["page"] = "Home"
                    st.rerun()
        
        st.info("💡 Your idea will be published and visible to others. You can edit it anytime in 'My Ideas'")

    # Render a top-level terms error if flagged (so it persists after rerun)
    if st.session_state.pop("publish_terms_error", False):
        st.markdown('<div class="error-message">⚠️ Please accept the terms and conditions.</div>', unsafe_allow_html=True)


# Call the show function when the page loads
if __name__ == "__main__":
    show()
