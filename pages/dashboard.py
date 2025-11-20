import streamlit as st
from pages import header
from styles import dashboard as dashboard_styles
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder


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


# Show the header navigation with "Ideas" as active page
header.show_header("Ideas")

# Page-specific CSS
dashboard_styles.load_css()

st.markdown('<div class="dashboard-content">', unsafe_allow_html=True)

st.subheader("Ideas")

# Initialize session state
if "home_docs" not in st.session_state:
    st.warning("No ideas data loaded yet. Please check your data source.")
    st.stop()

# Get base dataframe
df = st.session_state.home_docs.copy()

# Debug: Show how many ideas we have
st.write(f"Total ideas loaded: {len(df)}")

# Ensure datetime columns
for c in ["From date", "To date", "Date published"]:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors='coerce')

# Flash message from edit
flash_msg = st.session_state.pop("flash_success", None)
if flash_msg:
    st.success(flash_msg)

# Filters row
col_search, col_from, col_to, col_cat = st.columns([3, 1.5, 1.5, 1.5])

with col_search:
    search = st.text_input("Search (name / description)", key="ideas_search")
with col_from:
    from_date = st.date_input("From date", value=None, key="ideas_from")
with col_to:
    to_date = st.date_input("To date", value=None, key="ideas_to")
with col_cat:
    cat_options = sorted(df["Category"].dropna().unique()) if "Category" in df.columns else []
    category = st.selectbox("Category", options=["All"] + cat_options, index=0, key="ideas_category")

# Apply filters
m = pd.Series([True] * len(df))
if from_date:
    m &= df["From date"] >= pd.to_datetime(from_date)
if to_date:
    m &= df["To date"] <= pd.to_datetime(to_date)
if category and category != "All":
    m &= df["Category"] == category
if search:
    ql = search.lower()
    m &= (
        df["Name"].str.lower().str.contains(ql, na=False) |
        df["Description"].str.lower().str.contains(ql, na=False)
    )
df = df[m].reset_index(drop=True)

st.markdown("</div>", unsafe_allow_html=True)

# Debug: Show filtered count
st.write(f"Ideas after filters: {len(df)}")

if len(df) == 0:
    st.info("No ideas match your filters. Try adjusting your search criteria.")
    st.stop()

# Prepare display dataframe
display_df = pd.DataFrame()
if "id" in df.columns:
    display_df["id"] = df["id"]
if "Name" in df.columns:
    display_df["Title"] = df["Name"]
if "Date published" in df.columns:
    display_df["Date published"] = df["Date published"].dt.strftime("%Y-%m-%d")
if "Description" in df.columns:
    display_df["Short Description"] = df["Description"]
if "Category" in df.columns:
    display_df["Category"] = df["Category"]

# AgGrid configuration
gb = GridOptionsBuilder.from_dataframe(display_df)

# Hide ID column but keep for selection
if "id" in display_df.columns:
    gb.configure_column("id", hide=True)

# Make Short Description wider
if "Short Description" in display_df.columns:
    gb.configure_column("Short Description", width=1000)

# Configure sortable columns
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
    height=520,
    theme="balham"
)

# Action buttons
sel = resp.get("selected_rows", [])
selected_id = get_selected_id(sel)

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    st.button("🔎 Open", disabled=selected_id is None)
with c2:
    if st.button("✏️ Edit selected", disabled=selected_id is None):
        st.session_state.edit_id = selected_id
        st.switch_page("pages/edit_idea.py")
with c3:
    if st.button("🗑 Delete", disabled=selected_id is None):
        # Delete the idea from session state
        df_main = st.session_state.home_docs
        df_main = df_main[df_main["id"] != selected_id]
        st.session_state.home_docs = df_main.reset_index(drop=True)
        st.success("Idea deleted successfully!")
        st.rerun()
