import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import warnings
warnings.filterwarnings("ignore")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cage Rebar Analysis",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
}

/* Background */
.stApp {
    background: #0a0e1a;
    color: #e8eaf0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f1422 !important;
    border-right: 1px solid #1e2540;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #1a2035 0%, #0f1422 100%);
    border: 1px solid #2a3560;
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #f0a500, #e05c00, #c0392b);
}
.main-header h1 {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: 0.04em;
    color: #ffffff;
    margin: 0 0 4px 0;
    text-transform: uppercase;
}
.main-header p {
    color: #7a8aaa;
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.kpi-card {
    background: #111827;
    border: 1px solid #1e2a42;
    border-radius: 10px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #f0a500; }
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
}
.kpi-card.orange::after { background: #f0a500; }
.kpi-card.blue::after   { background: #3b82f6; }
.kpi-card.green::after  { background: #22c55e; }
.kpi-card.red::after    { background: #ef4444; }
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5a6a8a;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
}
.kpi-sub {
    font-size: 0.78rem;
    color: #5a6a8a;
    margin-top: 6px;
}

/* Section titles */
.section-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #f0a500;
    margin: 0 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2540;
}

/* Upload area */
.upload-wrapper {
    background: #111827;
    border: 2px dashed #2a3560;
    border-radius: 12px;
    padding: 48px 32px;
    text-align: center;
    margin: 40px auto;
    max-width: 600px;
}
.upload-wrapper h2 {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
}
.upload-wrapper p {
    color: #5a6a8a;
    font-size: 0.9rem;
}

/* Tables */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* Buttons */
.stDownloadButton button {
    background: #f0a500 !important;
    color: #000000 !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 22px !important;
}
.stDownloadButton button:hover {
    background: #e09500 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #111827;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1e2540;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #5a6a8a !important;
    background: transparent !important;
    border-radius: 6px !important;
}
.stTabs [aria-selected="true"] {
    background: #f0a500 !important;
    color: #000000 !important;
}

/* Metric override */
[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #1e2540;
    border-radius: 10px;
    padding: 16px 20px;
}
</style>
""", unsafe_allow_html=True)


# ── Bar Type logic ─────────────────────────────────────────────────────────────
def assign_bar_type(layer):
    if pd.isna(layer):
        return "Other"
    layer = str(layer)
    if layer[:1] in ("F", "N"):        return "Mesh"
    elif layer[:2] == "LK" or layer[:1] == "S": return "Shear Link"
    elif layer[:2] == "LB":            return "Loose Bar"
    elif layer[:2] == "VS":            return "VS Sub-Assembly"
    elif layer[:2] == "HS":            return "HS Sub-Assembly"
    elif layer[:3] == "PRL":           return "Preload"
    else:                              return "Other"


# ── Download helpers ───────────────────────────────────────────────────────────
@st.cache_data
def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

@st.cache_data
def to_excel(df):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    return buf.getvalue()


# ── Load & process ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Processing data…")
def load_data(file_bytes, filename):
    if filename.endswith(".csv"):
        df = pd.read_csv(BytesIO(file_bytes))
    else:
        df = pd.read_excel(BytesIO(file_bytes))

    # Add Bar Type if not present
    if "Bar Type" not in df.columns:
        if "Layer" in df.columns:
            df["Bar Type"] = df["Layer"].apply(assign_bar_type)

    # Numeric coercion
    for col in ["ATK Rebar - Weight", "Total Bar Weight", "GF", "GM", "DHD"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# ── Cage Summary ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Building Cage Summary…")
def build_cage_summary(df):
    if "Correct reference" not in df.columns or "Bar Type" not in df.columns:
        return pd.DataFrame()

    grp = df.groupby("Correct reference")

    summary = pd.DataFrame()
    summary["Cage Reference"]   = grp.size().index
    summary["Total Bars"]       = grp.size().values
    summary["Mesh Bars"]        = grp.apply(lambda x: (x["Bar Type"] == "Mesh").sum()).values
    summary["Non-Mesh Bars"]    = summary["Total Bars"] - summary["Mesh Bars"]
    summary["Shear Links"]      = grp.apply(lambda x: (x["Bar Type"] == "Shear Link").sum()).values
    summary["Mesh & Shear Only"]= (summary["Non-Mesh Bars"] - summary["Shear Links"] == 0).map({True: "Yes", False: "No"})
    summary["Loose Bars"]       = grp.apply(lambda x: (x["Bar Type"] == "Loose Bar").sum()).values
    summary["VS Bars"]          = grp.apply(lambda x: (x["Bar Type"] == "VS Sub-Assembly").sum()).values
    summary["HS Bars"]          = grp.apply(lambda x: (x["Bar Type"] == "HS Sub-Assembly").sum()).values
    summary["Preload Bars"]     = grp.apply(lambda x: (x["Bar Type"] == "Preload").sum()).values
    summary["LSAP Bars"]        = summary["Loose Bars"] + summary["VS Bars"] + summary["HS Bars"] + summary["Preload Bars"]
    summary = summary.reset_index(drop=True)
    return summary


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════════════════════

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏗️ Cage Rebar Analysis</h1>
    <p>Upload your combined CSV or Excel file to generate dashboard, cage summary, and download reports</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="section-title">📁 Upload File</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "CSV or Excel file",
        type=["csv", "xlsx"],
        label_visibility="collapsed"
    )

    if uploaded:
        st.success(f"✅ {uploaded.name}")
        st.markdown("---")
        st.markdown('<p class="section-title">🔍 Filters</p>', unsafe_allow_html=True)

# ── No file state ─────────────────────────────────────────────────────────────
if not uploaded:
    st.markdown("""
    <div class="upload-wrapper">
        <h2>⬆️ Upload Your Data</h2>
        <p>Drag and drop your <strong>Cage_Analysis_Combined.csv</strong> or any Excel file<br>
        into the sidebar to get started</p>
        <br>
        <p style="color:#3b5080; font-size:0.8rem;">Supports CSV · XLSX &nbsp;|&nbsp; Up to 1M+ rows</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Load data ─────────────────────────────────────────────────────────────────
df = load_data(uploaded.read(), uploaded.name)

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    bar_types = sorted(df["Bar Type"].dropna().unique()) if "Bar Type" in df.columns else []
    selected_types = st.multiselect("Bar Type", bar_types, default=bar_types)

    if "Correct reference" in df.columns:
        cage_search = st.text_input("Search Cage Reference", placeholder="e.g. 2HL230601")
    else:
        cage_search = ""

    st.markdown("---")
    st.caption(f"**{len(df):,}** total rows loaded")

# Apply filters
filtered = df.copy()
if selected_types and "Bar Type" in df.columns:
    filtered = filtered[filtered["Bar Type"].isin(selected_types)]
if cage_search and "Correct reference" in df.columns:
    filtered = filtered[filtered["Correct reference"].str.contains(cage_search, case=False, na=False)]

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_bars   = len(filtered)
total_cages  = filtered["Correct reference"].nunique() if "Correct reference" in filtered.columns else 0
total_mesh   = (filtered["Bar Type"] == "Mesh").sum() if "Bar Type" in filtered.columns else 0
total_nonmesh= total_bars - total_mesh
total_weight = filtered["Total Bar Weight"].sum() if "Total Bar Weight" in filtered.columns else 0
total_shear  = (filtered["Bar Type"] == "Shear Link").sum() if "Bar Type" in filtered.columns else 0
total_lsap   = filtered["Bar Type"].isin(["Loose Bar","VS Sub-Assembly","HS Sub-Assembly","Preload"]).sum() if "Bar Type" in filtered.columns else 0
avg_nonmesh  = round(total_nonmesh / total_cages, 1) if total_cages else 0
avg_lsap     = round(total_lsap / total_cages, 1) if total_cages else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="kpi-card orange">
        <div class="kpi-label">Total Cages</div>
        <div class="kpi-value">{total_cages:,}</div>
        <div class="kpi-sub">Unique cage references</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="kpi-card blue">
        <div class="kpi-label">Total Bars</div>
        <div class="kpi-value">{total_bars:,}</div>
        <div class="kpi-sub">All bar types</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="kpi-card green">
        <div class="kpi-label">Non-Mesh Bars</div>
        <div class="kpi-value">{total_nonmesh:,}</div>
        <div class="kpi-sub">Excl. mesh panels</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="kpi-card red">
        <div class="kpi-label">Total Bar Weight</div>
        <div class="kpi-value">{total_weight:,.0f}</div>
        <div class="kpi-sub">Sum of all weights</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col5, col6, col7, col8 = st.columns(4)
with col5:
    st.metric("Mesh Bars", f"{total_mesh:,}")
with col6:
    st.metric("Shear Links", f"{total_shear:,}")
with col7:
    st.metric("LSAP Bars", f"{total_lsap:,}")
with col8:
    st.metric("Avg Non-Mesh / Cage", f"{avg_nonmesh:,}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊  Charts", "🏗️  Cage Summary", "📋  Raw Data"])

# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown('<p class="section-title">Bar Type Breakdown</p>', unsafe_allow_html=True)
        if "Bar Type" in filtered.columns:
            bt_counts = filtered["Bar Type"].value_counts().reset_index()
            bt_counts.columns = ["Bar Type", "Count"]
            fig1 = px.bar(
                bt_counts, x="Count", y="Bar Type", orientation="h",
                color="Bar Type",
                color_discrete_sequence=["#f0a500","#3b82f6","#22c55e","#ef4444","#a855f7","#06b6d4","#f97316"],
                template="plotly_dark",
            )
            fig1.update_layout(
                paper_bgcolor="#111827", plot_bgcolor="#111827",
                showlegend=False, margin=dict(l=0, r=0, t=10, b=0),
                font=dict(family="Barlow", color="#e8eaf0"),
                yaxis=dict(gridcolor="#1e2540"),
                xaxis=dict(gridcolor="#1e2540"),
            )
            st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.markdown('<p class="section-title">Bar Type % Share</p>', unsafe_allow_html=True)
        if "Bar Type" in filtered.columns:
            fig2 = px.pie(
                bt_counts, values="Count", names="Bar Type",
                color_discrete_sequence=["#f0a500","#3b82f6","#22c55e","#ef4444","#a855f7","#06b6d4","#f97316"],
                template="plotly_dark", hole=0.45,
            )
            fig2.update_layout(
                paper_bgcolor="#111827", plot_bgcolor="#111827",
                margin=dict(l=0, r=0, t=10, b=0),
                font=dict(family="Barlow", color="#e8eaf0"),
                legend=dict(bgcolor="#111827"),
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Weight by Bar Type
    if "Total Bar Weight" in filtered.columns and "Bar Type" in filtered.columns:
        st.markdown('<p class="section-title">Total Weight by Bar Type</p>', unsafe_allow_html=True)
        wt = filtered.groupby("Bar Type")["Total Bar Weight"].sum().reset_index()
        wt.columns = ["Bar Type", "Total Weight"]
        wt = wt.sort_values("Total Weight", ascending=False)
        fig3 = px.bar(
            wt, x="Bar Type", y="Total Weight",
            color="Bar Type",
            color_discrete_sequence=["#f0a500","#3b82f6","#22c55e","#ef4444","#a855f7","#06b6d4","#f97316"],
            template="plotly_dark",
        )
        fig3.update_layout(
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            showlegend=False, margin=dict(l=0, r=0, t=10, b=0),
            font=dict(family="Barlow", color="#e8eaf0"),
            xaxis=dict(gridcolor="#1e2540"),
            yaxis=dict(gridcolor="#1e2540"),
        )
        st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<p class="section-title">Cage Summary</p>', unsafe_allow_html=True)

    cage_summary = build_cage_summary(filtered)

    if cage_summary.empty:
        st.warning("Could not build Cage Summary — make sure your data has 'Correct reference' and 'Bar Type' columns.")
    else:
        # Search within cage summary
        cage_filter = st.text_input("🔍 Filter by Cage Reference", placeholder="Type to search…", key="cage_sum_search")
        if cage_filter:
            cage_summary = cage_summary[cage_summary["Cage Reference"].str.contains(cage_filter, case=False, na=False)]

        st.markdown(f"**{len(cage_summary):,}** cages shown")
        st.dataframe(cage_summary, use_container_width=True, height=500)

        st.markdown("<br>", unsafe_allow_html=True)
        dl1, dl2, _ = st.columns([1, 1, 3])
        with dl1:
            st.download_button(
                "⬇️ Download CSV",
                data=to_csv(cage_summary),
                file_name="Cage_Summary.csv",
                mime="text/csv",
            )
        with dl2:
            st.download_button(
                "⬇️ Download Excel",
                data=to_excel(cage_summary),
                file_name="Cage_Summary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<p class="section-title">Raw Data</p>', unsafe_allow_html=True)

    # Column selector
    all_cols = list(filtered.columns)
    selected_cols = st.multiselect("Columns to show", all_cols, default=all_cols, key="col_select")
    display_df = filtered[selected_cols] if selected_cols else filtered

    st.markdown(f"**{len(display_df):,}** rows  ·  **{len(selected_cols)}** columns")

    # Show first 10,000 rows in browser (performance)
    show_df = display_df.head(10_000)
    if len(display_df) > 10_000:
        st.info(f"Showing first 10,000 rows for performance. Download to get all {len(display_df):,} rows.")

    st.dataframe(show_df, use_container_width=True, height=500)

    st.markdown("<br>", unsafe_allow_html=True)
    dl3, dl4, _ = st.columns([1, 1, 3])
    with dl3:
        st.download_button(
            "⬇️ Download CSV",
            data=to_csv(display_df),
            file_name="Cage_Analysis_Filtered.csv",
            mime="text/csv",
        )
    with dl4:
        st.download_button(
            "⬇️ Download Excel",
            data=to_excel(display_df),
            file_name="Cage_Analysis_Filtered.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
