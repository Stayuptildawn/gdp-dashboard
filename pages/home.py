# pages/home.py
import streamlit as st
import pandas as pd
from data.fake_docs import STATUSES

from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

def get_selected_id(sel):
    # Caso 1: lista de dicts (comportamiento típico de st_aggrid)
    if isinstance(sel, list):
        return sel[0]["id"] if len(sel) > 0 else None
    # Caso 2: DataFrame de pandas
    try:
        import pandas as pd
        if isinstance(sel, pd.DataFrame):
            return sel.iloc[0]["id"] if not sel.empty else None
    except Exception:
        pass
    return None

def _init_state():
    if "home_docs" not in st.session_state:
        st.error("No hay datos en sesión. Vuelve al inicio.")
        st.stop()
    # Initialize sort states: None, 'asc', 'desc'
    if "title_sort" not in st.session_state:
        st.session_state.title_sort = None
    if "date_sort" not in st.session_state:
        st.session_state.date_sort = None

def show():
    _init_state()

    # --- base df with real datetime for filtering
    df = st.session_state.home_docs.copy()
    for c in ["From date", "To date", "Date published"]:
        df[c] = pd.to_datetime(df[c])  # ensure dtype

    st.subheader("Documents")
    # Flash success message from edit_idea submit
    flash_msg = st.session_state.pop("flash_success", None)
    if flash_msg:
        st.success(flash_msg)

    # -------- Filters
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


    # Only show: Title (from Name), Date published, Short Description (from Description), Category
    display_df = pd.DataFrame()
    if "Name" in df.columns:
        display_df["Title"] = df["Name"]
    if "Date published" in df.columns:
        display_df["Date published"] = df["Date published"].dt.strftime("%Y-%m-%d")
    if "Description" in df.columns:
        display_df["Short Description"] = df["Description"]
    if "Category" in df.columns:
        display_df["Category"] = df["Category"]

    # ---- AgGrid config
    gb = GridOptionsBuilder.from_dataframe(display_df)
    # Make Short Description column much wider
    if "Short Description" in display_df.columns:
        gb.configure_column("Short Description", width=1000)



    # Enable AgGrid sort/filter icons for Title and Date published, but override their sort/filter events
    # so that clicking the icon cycles through the three states only (A→Z, Z→A, none for Title; Earliest→Latest, Latest→Earliest, none for Date published)
    # This is achieved by using AgGrid's onSortChanged event and a Streamlit callback
    if "Title" in display_df.columns:
        gb.configure_column(
            field = "Title",
            sortable=True,
            suppressMenu=True
        )
    if "Date published" in display_df.columns:
        gb.configure_column(
            field="Date published",
            sortable=True,
            suppressMenu=True
        )

    # Status value
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
    gb.configure_selection(
        selection_mode='single',   # one single line
        use_checkbox=True          # checkboxes
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
    # ---- Accion bar out of the iframe
    sel = resp.get("selected_rows", [])
    selected_id = get_selected_id(sel)

    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        st.button("🔎 Open", disabled=selected_id is None,
                on_click=lambda: (_ for _ in ()).throw(SystemExit))  # placeholder 
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

  