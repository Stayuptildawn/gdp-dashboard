import streamlit as st

# IMPORTANT: Must be first Streamlit command
st.set_page_config(
    page_title="UPM Innovation Platform - My Ideas",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import pandas as pd
import os
from pages import header
from st_aggrid import AgGrid, GridOptionsBuilder

# Reload data from CSV to ensure it's current
csv_path = "data/ideas.csv"
if os.path.exists(csv_path):
    try:
        df_reload = pd.read_csv(csv_path)
        for col in ["From date", "To date", "Date published"]:
            if col in df_reload.columns:
                df_reload[col] = pd.to_datetime(df_reload[col], errors='coerce')
        if "id" in df_reload.columns:
            df_reload = df_reload.sort_values('id', ascending=False).reset_index(drop=True)
        st.session_state.home_docs = df_reload
    except Exception as e:
        st.error(f"Error reloading data: {e}")


def get_selected_id(sel):
    """Extract the selected ID from AgGrid selection"""
    if isinstance(sel, list):
        return sel[0]["id"] if len(sel) > 0 else None
    try:
        if isinstance(sel, pd.DataFrame):
            return sel.iloc[0]["id"] if not sel.empty else None
    except Exception:
        pass
    return None


# Show the header navigation with "My Ideas" as active page
header.show_header("My Ideas")

# Defensive checks so the page fails in a friendly way
if "username" not in st.session_state or not st.session_state.username:
    st.error("You need to be logged in to see your ideas.")
    st.stop()

if "home_docs" not in st.session_state or st.session_state.home_docs is None:
    st.error("There is no idea data available in this session yet.")
    st.stop()

role = st.session_state.get("role", "student")

if role == "investor":
    st.title("My Saved Ideas")
else:
    st.title("My Ideas")

username = st.session_state.username
role = st.session_state.get("role", "student")
df = st.session_state.home_docs.copy()

if role == "investor":
    # For investors: use saved_ideas.csv (username, idea_id)
    saved_csv = "data/saved_ideas.csv"
    if not os.path.exists(saved_csv):
        st.info("You haven't saved any ideas yet. Go to 'Ideas' and click 'Save to My Ideas' on an idea you like.")
        st.stop()

    saved_df = pd.read_csv(saved_csv)
    if "idea_id" not in saved_df.columns:
        st.error("Saved ideas file is missing the 'idea_id' column.")
        st.stop()

    saved_ids = saved_df.loc[saved_df["username"] == username, "idea_id"].tolist()
    if not saved_ids:
        st.info("You haven't saved any ideas yet. Go to 'Ideas' and click 'Save to My Ideas'.")
        st.stop()

    my_ideas = df[df["id"].isin(saved_ids)].copy()
else:
    # Admin + Students: use Owner column
    if "Owner" not in df.columns:
        st.warning(
            "The ideas table does not have an 'Owner' column yet, "
            "so 'My Ideas' cannot be filtered by user. Showing all ideas for now."
        )
        my_ideas = df.copy()
    else:
        my_ideas = df[df["Owner"] == username].copy()


# Flash message from edit
flash_msg = st.session_state.pop("flash_success", None)
if flash_msg:
    st.success(flash_msg)

if my_ideas.empty:
    st.info("📝 You have not submitted any ideas yet. Click 'New Idea' in the navigation to create your first idea!")
    st.stop()

# Ensure datetime columns
for c in ["From date", "To date", "Date published"]:
    if c in my_ideas.columns:
        my_ideas[c] = pd.to_datetime(my_ideas[c], errors='coerce')

# Filters row
col_search, col_status = st.columns([3, 1.5])

with col_search:
    search = st.text_input("Search my ideas", key="myideas_search")
with col_status:
    status_options = ["All"]
    if "Status" in my_ideas.columns:
        status_options += sorted(my_ideas["Status"].dropna().unique().tolist())
    status_filter = st.selectbox("Status", options=status_options, index=0, key="myideas_status")

# Apply filters - FIXED: Create mask after my_ideas is filtered by owner
m = pd.Series([True] * len(my_ideas), index=my_ideas.index)  # Match the index
if status_filter and status_filter != "All":
    m &= (my_ideas["Status"] == status_filter)
if search:
    ql = search.lower()
    m &= (
        my_ideas["Name"].str.lower().str.contains(ql, na=False) |
        my_ideas["Description"].str.lower().str.contains(ql, na=False)
    )

# Apply the mask
my_ideas = my_ideas[m].reset_index(drop=True)

if len(my_ideas) == 0:
    st.info("No ideas match your filters.")
    st.stop()

# Prepare display dataframe
display_df = pd.DataFrame()
if "id" in my_ideas.columns:
    display_df["id"] = my_ideas["id"]
if "Name" in my_ideas.columns:
    display_df["Title"] = my_ideas["Name"]
if "Date published" in my_ideas.columns:
    display_df["Date published"] = my_ideas["Date published"].dt.strftime("%Y-%m-%d")
if "Status" in my_ideas.columns:
    display_df["Status"] = my_ideas["Status"]
if "Category" in my_ideas.columns:
    display_df["Category"] = my_ideas["Category"]
if "Description" in my_ideas.columns:
    display_df["Short Description"] = my_ideas["Description"]

# AgGrid configuration
gb = GridOptionsBuilder.from_dataframe(display_df)

# Hide ID column but keep for selection
if "id" in display_df.columns:
    gb.configure_column("id", hide=True)

# Make Short Description wider
if "Short Description" in display_df.columns:
    gb.configure_column("Short Description", width=800)

# Configure sortable columns with checkbox
if "Title" in display_df.columns:
    gb.configure_column(
        field="Title",
        sortable=True,
        suppressMenu=True,
        checkboxSelection=True
    )
if "Date published" in display_df.columns:
    gb.configure_column(
        field="Date published",
        sortable=True,
        suppressMenu=True
    )

# Selection configuration
gb.configure_selection(
    selection_mode='single',
    use_checkbox=True
)

# Build grid options
grid_opts = gb.build()
grid_opts["domLayout"] = "normal"
grid_opts["pagination"] = True
grid_opts["paginationPageSize"] = 10
grid_opts["suppressRowClickSelection"] = True
grid_opts["rowSelection"] = "single"

# Render AgGrid
resp = AgGrid(
    display_df,
    gridOptions=grid_opts,
    update_on=['selectionChanged'],
    allow_unsafe_jscode=True,
    fit_columns_on_grid_load=True,
    height=420,
    theme="balham"
)

# Action buttons
sel = resp.get("selected_rows", [])
selected_id = get_selected_id(sel)
c1, c2, c3 = st.columns([1, 1, 1])

if role == "investor":
    # Investors: open or remove from saved list
    with c1:
        if st.button("🔎 Open", disabled=selected_id is None):
            st.session_state.open_id = selected_id
            st.switch_page("pages/openIdea.py")

    with c2:
        if st.button("❌ Remove from My Ideas", disabled=selected_id is None):
            saved_csv = "data/saved_ideas.csv"
            if os.path.exists(saved_csv):
                saved_df = pd.read_csv(saved_csv)
                mask = ~(
                    (saved_df["username"] == username) &
                    (saved_df["idea_id"] == selected_id)
                )
                saved_df = saved_df[mask]
                saved_df.to_csv(saved_csv, index=False)
                st.success("Idea removed from 'My Ideas'.")
                st.rerun()
            else:
                st.error("No saved ideas file found.")
else:
    # Admin + Students: keep existing Edit / Publish / Delete behavior
    with c1:
        if st.button("✏️ Edit selected", disabled=selected_id is None):
            st.session_state.edit_id = selected_id
            st.switch_page("pages/edit_idea.py")

    with c2:
        if st.button("📤 Publish", disabled=selected_id is None):
            df_main = st.session_state.home_docs
            idx = df_main.index[df_main["id"] == selected_id]
            if len(idx) > 0:
                df_main.at[idx[0], "Status"] = "Accepted"
                st.session_state.home_docs = df_main

                csv_path = "data/ideas.csv"
                os.makedirs("data", exist_ok=True)
                df_main.to_csv(csv_path, index=False)

                st.success("Idea published successfully!")
                st.rerun()

    with c3:
        if st.button("🗑 Delete", disabled=selected_id is None):
            df_main = st.session_state.home_docs
            df_main = df_main[df_main["id"] != selected_id]
            st.session_state.home_docs = df_main.reset_index(drop=True)

            csv_path = "data/ideas.csv"
            os.makedirs("data", exist_ok=True)
            df_main.to_csv(csv_path, index=False)

            st.success("Idea deleted successfully!")
            st.rerun()
