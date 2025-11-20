# pages/home.py
import streamlit as st

# IMPORTANT: Must be first Streamlit command
st.set_page_config(
    page_title="UPM Innovation Platform",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import pandas as pd
import os
from pages import header
from styles.home import load_css
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

# CRITICAL: Reload data from CSV BEFORE anything else
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
        st.error(f"Error loading data: {e}")

# Define statuses locally
STATUSES = ["On Review", "Accepted", "Rejected"]

# Check authentication status
is_authenticated = st.session_state.get("authenticated", False)

# Show the header navigation (with or without login)
if is_authenticated:
    header.show_header("Home")
else:
    # Show simplified header for public access
    st.markdown("""
    <div style="background: white; padding: 1rem; margin-bottom: 2rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0; color: #1e40af;">UPM Innovation Platform</h2>
            <div>
                <a href="?login=true" style="text-decoration: none;">
                    <button style="background: #1e40af; color: white; padding: 0.5rem 1rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600;">
                        🔐 Login
                    </button>
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if login button was clicked
    if st.query_params.get("login") == "true":
        st.switch_page("pages/login.py")

# Load custom CSS for home page
load_css()

# Check if data exists
if "home_docs" not in st.session_state:
    st.error("No data loaded. Please restart the application.")
    st.stop()

# Get base dataframe with datetime conversion
df = st.session_state.home_docs.copy()

# Filter by visibility: Only show public ideas if not logged in
if not is_authenticated:
    if "Visibility Setting" in df.columns:
        df = df[df["Visibility Setting"] == "Public"].copy()
    st.info("🔓 Viewing public ideas only. Login to see all ideas and manage your own.")

for c in ["From date", "To date", "Date published"]:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors='coerce')

# Flash success message
flash_msg = st.session_state.pop("flash_success", None)
if flash_msg:
    st.success(flash_msg)

# ========== SECTION 1: STATISTICS & OVERVIEW (TOP) ==========
st.title("🏠 Innovation Dashboard")
st.markdown("### Overview & Statistics")

# Statistics cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_ideas = len(df)
    st.metric(
        label="💡 Total Ideas" + (" (Public)" if not is_authenticated else ""),
        value=total_ideas,
        delta=None
    )

with col2:
    if "Status" in df.columns:
        accepted = len(df[df["Status"] == "Accepted"])
        acceptance_rate = f"{(accepted/total_ideas*100):.0f}%" if total_ideas > 0 else "0%"
        st.metric(
            label="✅ Accepted",
            value=accepted,
            delta=acceptance_rate
        )

with col3:
    if "Status" in df.columns:
        on_review = len(df[df["Status"] == "On Review"])
        st.metric(
            label="🔄 On Review",
            value=on_review,
            delta=f"{(on_review/total_ideas*100):.0f}%" if total_ideas > 0 else "0%"
        )

with col4:
    if "Category" in df.columns:
        categories = df["Category"].nunique()
        st.metric(
            label="📊 Categories",
            value=categories
        )

# Category breakdown
st.markdown("---")
st.markdown("### 📈 Category Distribution")

if "Category" in df.columns and len(df) > 0:
    cat_col1, cat_col2 = st.columns([2, 3])
    
    with cat_col1:
        # Category counts
        category_counts = df["Category"].value_counts()
        for cat, count in category_counts.items():
            percentage = (count / total_ideas * 100)
            st.markdown(f"**{cat}**: {count} ideas ({percentage:.1f}%)")
    
    with cat_col2:
        # Status breakdown by category
        if "Status" in df.columns:
            status_by_cat = df.groupby(["Category", "Status"]).size().unstack(fill_value=0)
            st.dataframe(status_by_cat, width="stretch")

# Recent activity
st.markdown("---")
st.markdown("### 🕒 Recent Activity")

if "Date published" in df.columns and len(df) > 0:
    recent_df = df.nlargest(5, "Date published")[["Name", "Category", "Status", "Date published"]]
    recent_df["Date published"] = recent_df["Date published"].dt.strftime("%Y-%m-%d")
    st.dataframe(recent_df, width="stretch", hide_index=True)

st.markdown("---")

# ========== SECTION 2: ALL IDEAS TABLE (BOTTOM) ==========
st.markdown("### 📋 All Ideas" + (" (Public Only)" if not is_authenticated else ""))

# -------- Filters --------
filter_cols = st.columns([1.2, 0.4, 0.4, 0.4])
with filter_cols[0]:
    q = st.text_input("Search (name / description)", key="home_search")
with filter_cols[1]:
    fd = st.date_input("From date", value=None, key="home_from")
with filter_cols[2]:
    td = st.date_input("To date", value=None, key="home_to")
with filter_cols[3]:
    cat_options = sorted(df["Category"].dropna().unique()) if "Category" in df.columns else []
    category = st.selectbox("Category", options=["All"] + cat_options, index=0, key="home_category")

# Apply filters
filtered_df = df.copy()
m = pd.Series([True] * len(filtered_df))
if fd:
    m &= filtered_df["From date"] >= pd.to_datetime(fd)
if td:
    m &= filtered_df["To date"] <= pd.to_datetime(td)
if category and category != "All":
    m &= filtered_df["Category"] == category
if q:
    ql = q.lower()
    m &= (
        filtered_df["Name"].str.lower().str.contains(ql, na=False) |
        filtered_df["Description"].str.lower().str.contains(ql, na=False)
    )
filtered_df = filtered_df[m].reset_index(drop=True)

if len(filtered_df) == 0:
    st.info("No ideas match your filters. Try adjusting your search criteria.")
    st.stop()

# Show filtered count
st.caption(f"Showing {len(filtered_df)} of {len(df)} ideas")

# Prepare display dataframe
display_df = pd.DataFrame()
if "Name" in filtered_df.columns:
    display_df["Title"] = filtered_df["Name"]
if "Date published" in filtered_df.columns:
    display_df["Date published"] = filtered_df["Date published"].dt.strftime("%Y-%m-%d")
if "Description" in filtered_df.columns:
    display_df["Short Description"] = filtered_df["Description"]
if "Category" in filtered_df.columns:
    display_df["Category"] = filtered_df["Category"]
if "Status" in filtered_df.columns:
    display_df["Status"] = filtered_df["Status"]

# ---- AgGrid configuration ----
gb = GridOptionsBuilder.from_dataframe(display_df)

# Make Short Description wider
if "Short Description" in display_df.columns:
    gb.configure_column("Short Description", width=800)

# Configure sortable columns
if "Title" in display_df.columns:
    gb.configure_column(
        field="Title",
        sortable=True,
        suppressMenu=True
    )
if "Date published" in display_df.columns:
    gb.configure_column(
        field="Date published",
        sortable=True,
        suppressMenu=True
    )

# Status column styling
if "Status" in display_df.columns:
    cell_style = JsCode("""
    function(params){
        const v = params.value;
        const base = {'border-radius':'999px','padding':'2px 8px','font-weight':'600','display':'inline-block'};
        if (v === 'On Review') return {...base, 'background':'#e6f0ff','color':'#1d4ed8', 'textAlign':'center'};
        if (v === 'Accepted')  return {...base, 'background':'#e9f9ee','color':'#079455', 'textAlign':'center'};
        if (v === 'Rejected')  return {...base, 'background':'#ffeaea','color':'#ce2b2b', 'textAlign':'center'};
        return base;
    }
    """)
    gb.configure_column("Status", cellStyle=cell_style)

# Disable selection
gb.configure_selection(selection_mode='disabled')

# Build grid options
grid_opts = gb.build()
grid_opts["domLayout"] = "normal"
grid_opts["pagination"] = True
grid_opts["paginationPageSize"] = 10

# Render AgGrid
AgGrid(
    display_df,
    gridOptions=grid_opts,
    allow_unsafe_jscode=True,
    fit_columns_on_grid_load=True,
    height=400,
    theme="balham"
)
