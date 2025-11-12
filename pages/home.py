# pages/home.py
import streamlit as st
import pandas as pd
from data.fake_docs import STATUSES


from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode


def get_selected_id(sel):
    # Case 1: list of dicts (this is what st_aggrid usually gives us)
    if isinstance(sel, list):
        return sel[0]["id"] if len(sel) > 0 else None
    # Case 2: pandas DataFrame (sometimes it comes back as this)
    try:
        import pandas as pd
        if isinstance(sel, pd.DataFrame):
            return sel.iloc[0]["id"] if not sel.empty else None
    except Exception:
        pass
    return None


def _init_state():
    if "home_docs" not in st.session_state:
        st.error("Looks like the data didn't load properly. Try refreshing the page or head back to the main menu.")
        st.stop()


def show():
    _init_state()


    # Get a copy of the data and make sure dates are actual datetime objects for filtering
    df = st.session_state.home_docs.copy()
    for c in ["From date", "To date", "Date published"]:
        df[c] = pd.to_datetime(df[c])  # convert to datetime


    st.subheader("Documents")
    # Show success message if someone just submitted an edit
    flash_msg = st.session_state.pop("flash_success", None)
    if flash_msg:
        st.success(flash_msg)


    # Filter controls at the top
    c1, c2, c3, c4 = st.columns([1,1,1,2])
    with c1:
        status = st.multiselect("Status", STATUSES, default=["Accepted"])
    with c2:
        fd = st.date_input("From date", value=None)
    with c3:
        td = st.date_input("To date", value=None)
    with c4:
        q = st.text_input("Search (name / doc / issue)")


    m = df["Status"].isin(status)
    if fd: m &= df["From date"] >= pd.to_datetime(fd)
    if td: m &= df["To date"] <= pd.to_datetime(td)
    if q:
        ql = q.lower()
        m &= (
            df["Document name"].str.lower().str.contains(ql) |
            df["Name"].str.lower().str.contains(ql) |
            df["Issue Number"].str.lower().str.contains(ql)
        )
    df = df[m].reset_index(drop=True)


    # Hide the long text fields from the table - we only need those in the edit view
    hidden_cols = [
        "Description",
        "Detailed Description",
        "Estimated Impact / Target Audience",
    ]
    display_df = df.drop(columns=[c for c in hidden_cols if c in df.columns])


    # Format dates as strings so they display nicely in the grid
    grid_df = display_df.copy()
    for c in ["From date", "To date", "Date published"]:
        grid_df[c] = grid_df[c].dt.strftime("%Y-%m-%d")   # or "%d/%m/%Y"


    # Set up the AgGrid table
    gb = GridOptionsBuilder.from_dataframe(display_df)


  
    # Style the Status column with colored badges
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
    gb.configure_column("Status", cellStyle=cell_style, width=140)
    gb.configure_selection(
        selection_mode='single',   # only let them select one row at a time
        use_checkbox=True          # show checkboxes for selection
    )


    grid_opts = gb.build()
    grid_opts["domLayout"] = "normal"
    grid_opts["pagination"] = True
    grid_opts["paginationPageSize"] = 10
    grid_opts["suppressRowClickSelection"] = True
    grid_opts["rowSelection"] = "single"
    grid_opts["quickFilterText"] = q or ""


    resp = AgGrid(
        display_df,
        gridOptions=grid_opts,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        height=520,
        theme="balham"
    )
    # Action buttons below the table
    sel = resp.get("selected_rows", [])
    selected_id = get_selected_id(sel)


    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        st.button("🔎 Open", disabled=selected_id is None,
                on_click=lambda: (_ for _ in ()).throw(SystemExit))  # TODO: implement this 
    with c2:
        if st.button("✏️ Edit selected", disabled=selected_id is None):
            st.query_params["page"] = "My Ideas"
            st.query_params["edit_id"] = str(selected_id)
            st.rerun()
    with c3:
        if st.button("🗑 Delete", disabled=selected_id is None):
            st.query_params["page"] = "Home"
            st.query_params["delete_id"] = str(selected_id)
            st.rerun()
