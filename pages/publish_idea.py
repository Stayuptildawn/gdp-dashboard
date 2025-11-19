import streamlit as st
import pandas as pd
import time
from styles import edit_idea as edit_idea
from data.fake_docs import make_fake_docs


def show():
    """
    Idea submission page:
    - Lets users draft or publish ideas
    - Validates required fields
    - Stores the current user as Owner so 'My Ideas' can filter correctly
    """

    # Small hint at the top so users know what '*' means
    st.markdown(
        '<span style="color: #ef4444; font-weight: bold;">*</span> indicates a required field.',
        unsafe_allow_html=True,
    )

    # Page-specific styling (borders, spacing, etc.)
    edit_idea.load_css()
    st.subheader("1. Idea Submission Form")

    # Keep track of validation state and ongoing publish operations
    if "publish_validate" not in st.session_state:
        st.session_state.publish_validate = False
    if "is_publishing" not in st.session_state:
        st.session_state.is_publishing = False

    # Ensure we have the ideas table in memory; in a real app, this would likely come from a DB
    if "home_docs" not in st.session_state:
        st.session_state.home_docs = make_fake_docs(30)

    # Session-backed form data so user input survives reruns
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
    defaults = st.session_state.publish_form_data

    # Split form and side panel
    c1, c2 = st.columns(2)

    # ------------------ LEFT COLUMN: MAIN FORM ------------------ #
    with c1:
        # Build category choices dynamically, then merge with a sensible fallback list
        try:
            options = sorted(
                set(
                    st.session_state.home_docs.get("Category", pd.Series())
                    .dropna()
                    .astype(str)
                )
            )
        except Exception:
            options = []
        fallback = ["TRANSPORT", "HEALTH", "ENERGY", "AI", "Business", "Technology", "Social"]
        options = list(dict.fromkeys([*(options or []), *fallback]))

        selected_idx = 0
        if defaults["Category of the idea"] in options:
            selected_idx = options.index(defaults["Category of the idea"])

        # Idea title (required)
        title = st.text_input(
            "Idea Title *",
            value=defaults["Idea Title"],
            key="publish_title",
        )
        title_warn = st.empty()

        # Category (required)
        category = st.selectbox(
            "Category of the idea *",
            options,
            index=selected_idx,
            key="publish_category",
        )

        # Short description (required)
        short_desc = st.text_area(
            "Short Description (max 200 chars) *",
            value=defaults["Short Description"],
            height=100,
            key="publish_short_desc",
        )
        short_warn = st.empty()

        # Detailed description (required)
        detailed_desc = st.text_area(
            "Detailed Description *",
            value=defaults["Detailed Description"],
            height=200,
            key="publish_detailed_desc",
        )
        detailed_warn = st.empty()

        # Save current values to session so they survive reruns
        st.session_state.publish_form_data["Idea Title"] = title
        st.session_state.publish_form_data["Category of the idea"] = category
        st.session_state.publish_form_data["Short Description"] = short_desc
        st.session_state.publish_form_data["Detailed Description"] = detailed_desc

        # Show inline warnings only once validation has been triggered
        if st.session_state.get("publish_validate") and not (title or "").strip():
            title_warn.markdown(
                '<div class="warning-message">Fill the compulsory fields!</div>',
                unsafe_allow_html=True,
            )
        if st.session_state.get("publish_validate") and not (short_desc or "").strip():
            short_warn.markdown(
                '<div class="warning-message">Fill the compulsory fields!</div>',
                unsafe_allow_html=True,
            )
        if st.session_state.get("publish_validate") and not (detailed_desc or "").strip():
            detailed_warn.markdown(
                '<div class="warning-message">Fill the compulsory fields!</div>',
                unsafe_allow_html=True,
            )

        # Upload section is currently a visual placeholder only
        st.markdown("<h6>Upload Files</h6>", unsafe_allow_html=True)
        displayed_doc = "No document attached"
        st.markdown(
            f"""
        <div style="border: 1px dashed #ccc; padding: 2rem; text-align: center;">
            <span style="font-size: 3rem;">⬆️</span>
            <p style="margin:0; font-weight:600; word-break:break-word;">{displayed_doc}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Estimated impact / target audience (required)
    estimated_impact = st.text_input(
        "Estimated Impact / Target Audience *",
        value=defaults["Estimated Impact / Target Audience"],
        placeholder="e.g., Students, SMEs, City residents",
        key="publish_impact",
    )
    impact_warn = st.empty()
    st.session_state.publish_form_data["Estimated Impact / Target Audience"] = estimated_impact

    if st.session_state.get("publish_validate") and not (estimated_impact or "").strip():
        impact_warn.markdown(
            '<div class="warning-message">Fill the compulsory fields!</div>',
            unsafe_allow_html=True,
        )

    # Visibility setting is optional (for future use)
    vis_opts = ["Public", "Private"]
    vis_idx = vis_opts.index(defaults["Visibility Setting"]) if defaults["Visibility Setting"] in vis_opts else 0
    visibility = st.selectbox(
        "Visibility Setting", vis_opts, index=vis_idx, key="publish_visibility"
    )
    st.session_state.publish_form_data["Visibility Setting"] = visibility

    # ------------------ RIGHT COLUMN: TERMS + ACTIONS ------------------ #
    with c2:
        st.subheader("2. Terms & Conditions")

        # User must accept these for a full publish
        terms_label = "I have read and accept the Terms and Conditions. *"
        terms = st.checkbox(terms_label, key="publish_terms")

        sc1, sc2 = st.columns(2)

        # --- Save as Draft button --- #
        with sc1:
            if st.button("Save as Draft", disabled=st.session_state.is_publishing):
                # For drafts, only require a title to avoid friction
                if not (title or "").strip():
                    st.warning("⚠️ Please provide at least an Idea Title to save as draft.")
                else:
                    try:
                        df = st.session_state.get("home_docs")
                        if df is not None:
                            new_id = df["id"].max() + 1 if len(df) > 0 else 1
                            import random

                            days_to_add = random.randint(30, 180)
                            to_date = (
                                pd.Timestamp.now() + pd.Timedelta(days=days_to_add)
                            ).strftime("%d/%m/%Y %H:%M")

                            # IMPORTANT: Owner is stored for user-specific filtering
                            new_row = {
                                "id": new_id,
                                "Status": "Draft",
                                "From date": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                                "To date": to_date,
                                "Document name": f"DRAFT/{new_id}/{category[:3].upper()}",
                                "Date published": "",
                                "Issue Number": "",
                                "Name": (title or "").strip(),
                                "Category": category,
                                "Description": (short_desc or "").strip()[:200],
                                "Detailed Description": (detailed_desc or ""),
                                "Estimated Impact / Target Audience": (estimated_impact or ""),
                                "Owner": st.session_state.get("username", "unknown"),
                            }

                            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                            st.session_state.home_docs = df

                            # Reset the form so the user starts clean next time
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
                            time.sleep(1.5)
                            st.query_params["page"] = "Home"
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to save draft. Please try again. Error: {str(e)}")

        # --- Publish button --- #
        with sc2:
            if st.button("Publish", type="primary", disabled=st.session_state.is_publishing):
                # Simple flag to reduce the chance of double-click publishing
                st.session_state.is_publishing = True

                # All required fields must be filled and terms accepted
                required_ok = all(
                    [
                        (title or "").strip(),
                        (short_desc or "").strip(),
                        (detailed_desc or "").strip(),
                        (estimated_impact or "").strip(),
                    ]
                )
                if not required_ok or not terms:
                    st.session_state.publish_validate = True
                    st.session_state.publish_warning = "Fill the compulsory fields!"
                    st.session_state.publish_terms_error = not terms
                    st.session_state.is_publishing = False
                    st.rerun()
                else:
                    try:
                        df = st.session_state.get("home_docs")
                        if df is not None:
                            new_id = df["id"].max() + 1 if len(df) > 0 else 1
                            import random

                            days_to_add = random.randint(30, 180)
                            to_date = (
                                pd.Timestamp.now() + pd.Timedelta(days=days_to_add)
                            ).strftime("%d/%m/%Y %H:%M")

                            # IMPORTANT: Owner saved here as well
                            new_row = {
                                "id": new_id,
                                "Status": "Accepted",
                                "From date": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                                "To date": to_date,
                                "Document name": f"PROFORMA/{new_id}/{category[:3].upper()}",
                                "Date published": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                                "Issue Number": f"{new_id}.00/{random.randint(100,999)}PLN",
                                "Name": (title or "").strip(),
                                "Category": category,
                                "Description": (short_desc or "").strip()[:200],
                                "Detailed Description": (detailed_desc or ""),
                                "Estimated Impact / Target Audience": (estimated_impact or ""),
                                "Owner": st.session_state.get("username", "unknown"),
                            }

                            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                            st.session_state.home_docs = df

                            st.success("🎉 Idea published successfully!")
                            st.session_state.publish_form_data = {
                                "Idea Title": "",
                                "Category of the idea": "",
                                "Short Description": "",
                                "Detailed Description": "",
                                "Estimated Impact / Target Audience": "",
                                "Document name": "",
                                "Visibility Setting": "Public",
                            }
                            time.sleep(1.5)
                    except Exception as e:
                        st.error(f"❌ Failed to publish idea. Please try again. Error: {str(e)}")
                        st.session_state.is_publishing = False
                        st.stop()

                    # Reset validation and publishing flag, then send user back home
                    st.session_state.publish_validate = False
                    st.session_state.is_publishing = False
                    st.query_params["page"] = "Home"
                    st.rerun()

        st.info(
            "💡 Your idea will be published and visible to others. "
            "You can edit it anytime in 'My Ideas'"
        )

    # If terms were missing on the last attempt, keep the error visible after rerun
    if st.session_state.pop("publish_terms_error", False):
        st.markdown(
            '<div class="error-message">⚠️ Please accept the terms and conditions.</div>',
            unsafe_allow_html=True,
        )


# Allow running this file directly for local testing
if __name__ == "__main__":
    show()
