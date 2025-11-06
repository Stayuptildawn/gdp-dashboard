import streamlit as st
import pandas as pd
import time
from styles import edit_idea as edit_idea
from datetime import date



def show():
    # Load the CSS to keep those input borders looking consistent
    edit_idea.load_css()
    st.subheader("1. Idea Submission Form")


    # Set up validation flag so we can show warnings when needed
    if "publish_validate" not in st.session_state:
        st.session_state.publish_validate = False


    # Flag to stop people from accidentally submitting twice
    if "is_publishing" not in st.session_state:
        st.session_state.is_publishing = False


    # Make sure we actually have the documents table to work with
    if "home_docs" not in st.session_state:
        st.error("Hmm, looks like the data table isn't loaded. Try refreshing the page.")
        st.stop()


    # Keep form data in session so fields don't get wiped if validation fails
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
    
    # Pull the saved values for the form fields
    defaults = st.session_state.publish_form_data


    c1, c2 = st.columns(2)


    with c1:
        # Build the category dropdown from existing data plus some backup options
        options = []
        try:
            options = sorted(set(st.session_state.home_docs.get("Category", pd.Series()).dropna().astype(str)))
        except Exception:
            pass
        fallback = ["TRANSPORT", "HEALTH", "ENERGY", "AI", "Business", "Technology", "Social"]
        options = list(dict.fromkeys([*(options or []), *fallback]))
        
        # Figure out which category should be selected
        selected_idx = 0
        if defaults["Category of the idea"] in options:
            selected_idx = options.index(defaults["Category of the idea"])
        
        # All the input fields - keys help keep values between page refreshes
        title = st.text_input("Idea Title", value=defaults["Idea Title"], key="publish_title")
        title_warn = st.empty()
        category = st.selectbox("Category of the idea", options, index=selected_idx, key="publish_category")
        short_desc = st.text_area("Short Description (max 200 chars)", value=defaults["Short Description"], height=100, key="publish_short_desc")
        short_warn = st.empty()
        detailed_desc = st.text_area("Detailed Description", value=defaults["Detailed Description"], height=200, key="publish_detailed_desc")
        detailed_warn = st.empty()


        # Save whatever they typed so it doesn't disappear
        st.session_state.publish_form_data["Idea Title"] = title
        st.session_state.publish_form_data["Category of the idea"] = category
        st.session_state.publish_form_data["Short Description"] = short_desc
        st.session_state.publish_form_data["Detailed Description"] = detailed_desc


        # Show warnings under empty fields when validation kicks in
        if st.session_state.get("publish_validate") and not (title or "").strip():
            title_warn.markdown(f'<div class="warning-message">{st.session_state.get("publish_warning", "Please fill in all required fields")}</div>', unsafe_allow_html=True)
        if st.session_state.get("publish_validate") and not (short_desc or "").strip():
            short_warn.markdown(f'<div class="warning-message">{st.session_state.get("publish_warning", "Please fill in all required fields")}</div>', unsafe_allow_html=True)
        if st.session_state.get("publish_validate") and not (detailed_desc or "").strip():
            detailed_warn.markdown(f'<div class="warning-message">{st.session_state.get("publish_warning", "Please fill in all required fields")}</div>', unsafe_allow_html=True)


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
    
    # Keep this field saved too
    st.session_state.publish_form_data["Estimated Impact / Target Audience"] = estimated_impact
    
    if st.session_state.get("publish_validate") and not (estimated_impact or "").strip():
        impact_warn.markdown(f'<div class="warning-message">{st.session_state.get("publish_warning", "Please fill in all required fields")}</div>', unsafe_allow_html=True)
    
    vis_opts = ["Public", "Private"]
    vis_idx = vis_opts.index(defaults["Visibility Setting"]) if defaults["Visibility Setting"] in vis_opts else 0
    visibility = st.selectbox("Visibility Setting", vis_opts, index=vis_idx, key="publish_visibility")
    
    # Store visibility setting
    st.session_state.publish_form_data["Visibility Setting"] = visibility


    with c2:
        st.subheader("2. Terms & Conditions")
        terms = st.checkbox("I have read and accept the Terms and Conditions.", key="publish_terms")
        
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("Save as Draft", disabled=st.session_state.is_publishing):
                # At minimum, we need a title to save a draft
                if not (title or "").strip():
                    st.warning("⚠️ You'll need to add at least a title to save this as a draft.")
                else:
                    try:
                        df = st.session_state.get("home_docs")
                        if df is not None:
                            # Create a new ID for this entry
                            new_id = df["id"].max() + 1 if len(df) > 0 else 1
                            
                            # Build the draft row
                            # Pick a random end date somewhere between 1-6 months out
                            import random
                            days_to_add = random.randint(30, 180)
                            to_date = (pd.Timestamp.now() + pd.Timedelta(days=days_to_add)).strftime("%d/%m/%Y %H:%M")
                            
                            new_row = {
                                "id": new_id,
                                "Status": "On Review",
                                "From date": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                                "To date": to_date,
                                "Document name": f"DRAFT/{new_id}/{category[:3].upper()}",
                                "Date published": date.today(),
                                "Issue Number":  f"{new_id}.00/{random.randint(100,999)}PLN",
                                "Name": (title or "").strip(),
                                "Category": category,
                                "Description": (short_desc or "").strip()[:200],
                                "Detailed Description": (detailed_desc or ""),
                                "Estimated Impact / Target Audience": (estimated_impact or ""),
                            }
                            
                            # Append it to the table
                            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                            
                            # Update the main data
                            st.session_state.home_docs = df
                            
                            # Wipe the form clean
                            st.session_state.publish_form_data = {
                                "Idea Title": "",
                                "Category of the idea": "",
                                "Short Description": "",
                                "Detailed Description": "",
                                "Estimated Impact / Target Audience": "",
                                "Document name": "",
                                "Visibility Setting": "Public",
                            }
                            
                            st.success("💾 Draft saved! You can find it later in 'My Ideas' to finish it up.")
                            st.session_state.publish_validate = False
                            
                            # Wait a sec then head back to home
                            time.sleep(1.5)
                            st.query_params["page"] = "Home"
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"❌ Oops, something went wrong saving your draft. Give it another shot? (Error: {str(e)})")
                        
        with sc2:
            if st.button("Publish", type="primary", disabled=st.session_state.is_publishing):
                # Lock it so they don't double-submit
                st.session_state.is_publishing = True
                
                # Check if all the required fields are filled out
                required_ok = all([
                    (title or "").strip(),
                    (short_desc or "").strip(),
                    (detailed_desc or "").strip(),
                    (estimated_impact or "").strip(),
                ])


                if not required_ok or not terms:
                    st.session_state.publish_validate = True
                    st.session_state.publish_warning = "Please fill in all required fields"
                    # Remember to show the terms error after page refreshes
                    st.session_state.publish_terms_error = not terms
                    st.session_state.is_publishing = False
                    st.rerun()
                else:
                    # Good to go - let's add this idea to the table
                    try:
                        df = st.session_state.get("home_docs")
                        if df is not None:
                            # Make a new ID
                            new_id = df["id"].max() + 1 if len(df) > 0 else 1
                            
                            # Create the published entry (Status "Accepted" means it's live)
                            # Random end date 1-6 months from now
                            import random
                            days_to_add = random.randint(30, 180)
                            to_date = (pd.Timestamp.now() + pd.Timedelta(days=days_to_add)).strftime("%d/%m/%Y %H:%M")
                            
                            new_row = {
                                "id": new_id,
                                "Status": "Accepted",
                                "From date": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                                "To date": to_date,
                                "Document name": f"PROFORMA/{new_id}/{category[:3].upper()}",
                                "Date published":  date.today(),
                                "Issue Number": f"{new_id}.00/{random.randint(100,999)}PLN",
                                "Name": (title or "").strip(),
                                "Category": category,
                                "Description": (short_desc or "").strip()[:200],
                                "Detailed Description": (detailed_desc or ""),
                                "Estimated Impact / Target Audience": (estimated_impact or ""),
                            }
                            
                            # Add to the dataframe
                            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                            
                            # Save it back
                            st.session_state.home_docs = df
                            
                            st.success("🎉 Your idea is now live! Nice work.")
                            
                            # Reset the form
                            st.session_state.publish_form_data = {
                                "Idea Title": "",
                                "Category of the idea": "",
                                "Short Description": "",
                                "Detailed Description": "",
                                "Estimated Impact / Target Audience": "",
                                "Document name": "",
                                "Visibility Setting": "Public",
                            }
                            
                            # Give them a moment to see the success message
                            time.sleep(1.5)
                            
                    except Exception as e:
                        st.error(f"❌ Couldn't publish your idea right now. Mind trying again? (Error: {str(e)})")
                        st.session_state.is_publishing = False
                        st.stop()


                    # Clean up and unlock the button
                    st.session_state.publish_validate = False
                    st.session_state.is_publishing = False
                    
                    # Send them back to the home page
                    st.query_params["page"] = "Home"
                    st.rerun()
        
        st.info("💡 Once published, your idea will be visible to everyone. Don't worry though - you can always edit it later from 'My Ideas'.")


    # Show the terms error at the top if they forgot to check the box
    if st.session_state.pop("publish_terms_error", False):
        st.markdown('<div class="error-message">⚠️ You need to accept the terms and conditions before publishing.</div>', unsafe_allow_html=True)



# Run the page when this file is loaded
if __name__ == "__main__":
    show()
