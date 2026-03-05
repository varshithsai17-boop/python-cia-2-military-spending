"""
app.py — Streamlit Dashboard for Military Expenditure Analysis
===============================================================
Interactive dashboard visualising global military spending data
sourced from Wikipedia (SIPRI 2024 & IISS 2025).

Launch:
  streamlit run app/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Military Expenditure Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        padding: 1rem 0;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

@st.cache_data
def load_data():
    sipri = pd.read_csv(os.path.join(DATA_DIR, "military_spending_sipri_2024.csv"))
    iiss = pd.read_csv(os.path.join(DATA_DIR, "military_spending_iiss_2025.csv"))
    gdp_sipri = pd.read_csv(os.path.join(DATA_DIR, "gdp_pct_sipri_2024.csv"))
    gdp_iiss = pd.read_csv(os.path.join(DATA_DIR, "gdp_pct_iiss_2020.csv"))

    # Add regions
    region_map = {
        'United States': 'North America', 'Canada': 'North America', 'Mexico': 'North America',
        'Brazil': 'South America', 'Colombia': 'South America',
        'China': 'Asia', 'India': 'Asia', 'Japan': 'Asia', 'South Korea': 'Asia',
        'Taiwan': 'Asia', 'Singapore': 'Asia', 'Indonesia': 'Asia', 'Pakistan': 'Asia',
        'Philippines': 'Asia', 'Iran': 'Asia',
        'Russia': 'Europe', 'Germany': 'Europe', 'United Kingdom': 'Europe',
        'Ukraine': 'Europe', 'France': 'Europe', 'Poland': 'Europe', 'Italy': 'Europe',
        'Spain': 'Europe', 'Netherlands': 'Europe', 'Sweden': 'Europe', 'Norway': 'Europe',
        'Denmark': 'Europe', 'Romania': 'Europe', 'Belgium': 'Europe', 'Greece': 'Europe',
        'Finland': 'Europe', 'Switzerland': 'Europe', 'Czech Republic': 'Europe',
        'Turkey': 'Middle East', 'Saudi Arabia': 'Middle East', 'Israel': 'Middle East',
        'Kuwait': 'Middle East', 'Iraq': 'Middle East',
        'Algeria': 'Africa', 'Australia': 'Oceania'
    }
    sipri['Region'] = sipri['Country'].map(region_map)
    return sipri, iiss, gdp_sipri, gdp_iiss

sipri, iiss, gdp_sipri, gdp_iiss = load_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/SIPRI_logo.svg/200px-SIPRI_logo.svg.png", width=80)
    st.title("Controls")
    st.markdown("---")

    dataset = st.radio("Select Dataset", ["SIPRI 2024 (Top 40)", "IISS 2025 (Top 15)"],
                       index=0)

    top_n = st.slider("Number of Countries to Display", min_value=5, max_value=40,
                      value=10, step=5)

    chart_type = st.selectbox("Chart Type",
                              ["Bar Chart", "Horizontal Bar", "Pie Chart",
                               "Scatter Plot", "Treemap"])

    color_scheme = st.selectbox("Color Scheme",
                                ["Viridis", "Plasma", "RdYlGn_r", "Blues",
                                 "Turbo", "Spectral"])

    st.markdown("---")
    st.markdown("**Data Source**")
    st.markdown("[Wikipedia — Military Expenditures](https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures)")

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🌍 Global Military Expenditure Dashboard</div>',
            unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interactive analysis of military spending data from SIPRI & IISS | Python for Business CIA Project</div>',
            unsafe_allow_html=True)

# ── Key Metrics ──────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Global Spending", f"${sipri['Spending (US$ bn)'].sum():.0f}B",
              delta="SIPRI 2024")
with col2:
    st.metric("Highest Spender", sipri.iloc[0]['Country'],
              delta=f"${sipri.iloc[0]['Spending (US$ bn)']:.0f}B")
with col3:
    st.metric("Highest % GDP", gdp_sipri.iloc[0]['Country'],
              delta=f"{gdp_sipri.iloc[0]['% of GDP']:.1f}%")
with col4:
    st.metric("Countries Tracked", f"{len(sipri)}", delta="Top 40")

st.markdown("---")

# ── Select active data ───────────────────────────────────────────────────────
if "SIPRI" in dataset:
    df = sipri.copy()
    spending_col = "Spending (US$ bn)"
else:
    df = iiss.copy()
    spending_col = "Spending (US$ bn)"

df_display = df.nlargest(top_n, spending_col)

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(["📊 Charts", "📋 Data Table", "💰 % GDP Analysis", "🔄 Source Comparison"])

# ── Tab 1: Charts ────────────────────────────────────────────────────────────
with tab1:
    st.subheader(f"Top {top_n} Military Spenders — {dataset.split('(')[0].strip()}")

    if chart_type == "Bar Chart":
        fig = px.bar(df_display, x="Country", y=spending_col,
                     color=spending_col, color_continuous_scale=color_scheme,
                     text=spending_col, title=f"Top {top_n} Countries by Military Spending")
        fig.update_traces(texttemplate='$%{text:.0f}B', textposition='outside')
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Horizontal Bar":
        fig = px.bar(df_display.iloc[::-1], x=spending_col, y="Country",
                     orientation='h', color=spending_col,
                     color_continuous_scale=color_scheme,
                     title=f"Top {top_n} Countries by Military Spending")
        fig.update_layout(height=max(400, top_n * 35))
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pie Chart":
        fig = px.pie(df_display, values=spending_col, names="Country",
                     title=f"Military Spending Distribution — Top {top_n}",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter Plot":
        if "SIPRI" in dataset:
            fig = px.scatter(df_display, x=spending_col, y="% of GDP",
                            size="% of global spending", color="Country",
                            hover_name="Country", size_max=50,
                            title="Spending vs % of GDP (Bubble = Global Share)")
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Scatter plot requires SIPRI dataset (has % GDP column). Switch to SIPRI 2024.")

    elif chart_type == "Treemap":
        fig = px.treemap(df_display, path=["Country"], values=spending_col,
                         color=spending_col, color_continuous_scale=color_scheme,
                         title=f"Treemap — Military Spending Top {top_n}")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 2: Data Table ────────────────────────────────────────────────────────
with tab2:
    st.subheader("Full Dataset View")

    # Search filter
    search = st.text_input("Search for a country:", "")
    if search:
        filtered = df[df['Country'].str.contains(search, case=False, na=False)]
    else:
        filtered = df

    st.dataframe(filtered, use_container_width=True, height=400)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Summary Statistics")
        st.dataframe(df[spending_col].describe().round(2))
    with col2:
        st.subheader("Dataset Info")
        st.write(f"**Rows:** {df.shape[0]}")
        st.write(f"**Columns:** {df.shape[1]}")
        st.write(f"**Column Names:** {', '.join(df.columns)}")

# ── Tab 3: % GDP Analysis ───────────────────────────────────────────────────
with tab3:
    st.subheader("Military Spending as % of GDP")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### SIPRI 2024 — Top 25 by % GDP")
        fig = px.bar(gdp_sipri, x="Country", y="% of GDP",
                     color="% of GDP", color_continuous_scale="Reds",
                     title="Military Spending as % of GDP (SIPRI 2024)")
        fig.update_layout(xaxis_tickangle=-45, height=450)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### IISS 2020 — Top 15 by % GDP")
        fig = px.bar(gdp_iiss, x="Country", y="% of GDP",
                     color="% of GDP", color_continuous_scale="Oranges",
                     title="Military Spending as % of GDP (IISS 2020)")
        fig.update_layout(xaxis_tickangle=-45, height=450)
        st.plotly_chart(fig, use_container_width=True)

    # Highlight insight
    st.info(f"**Key Insight:** Ukraine has the highest military spending as % of GDP "
            f"({gdp_sipri.iloc[0]['% of GDP']}%) — largely due to the ongoing conflict.")

# ── Tab 4: Source Comparison ─────────────────────────────────────────────────
with tab4:
    st.subheader("SIPRI 2024 vs IISS 2025 — Side-by-Side")

    merged = pd.merge(
        sipri[['Country', 'Spending (US$ bn)']],
        iiss[['Country', 'Spending (US$ bn)']],
        on='Country', how='inner', suffixes=('_SIPRI', '_IISS')
    )
    merged['Difference'] = merged['Spending (US$ bn)_SIPRI'] - merged['Spending (US$ bn)_IISS']

    fig = go.Figure()
    fig.add_trace(go.Bar(name='SIPRI 2024', x=merged['Country'],
                         y=merged['Spending (US$ bn)_SIPRI'],
                         marker_color='#e74c3c'))
    fig.add_trace(go.Bar(name='IISS 2025', x=merged['Country'],
                         y=merged['Spending (US$ bn)_IISS'],
                         marker_color='#3498db'))
    fig.update_layout(barmode='group', title="SIPRI vs IISS Spending Estimates",
                      xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Difference Table (SIPRI − IISS)")
    st.dataframe(merged[['Country', 'Spending (US$ bn)_SIPRI',
                          'Spending (US$ bn)_IISS', 'Difference']].round(1),
                 use_container_width=True)

    # Regional breakdown if available
    if 'Region' in sipri.columns:
        st.subheader("Regional Spending Breakdown")
        region_agg = sipri.groupby('Region')['Spending (US$ bn)'].agg(['sum', 'mean', 'count']).round(1)
        region_agg.columns = ['Total ($bn)', 'Average ($bn)', 'Countries']
        region_agg = region_agg.sort_values('Total ($bn)', ascending=False)
        st.dataframe(region_agg, use_container_width=True)

        fig = px.pie(region_agg.reset_index(), values='Total ($bn)', names='Region',
                     title="Military Spending by Region",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#888; font-size:0.9rem'>"
    "Data Source: <a href='https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures'>Wikipedia</a> "
    "| Python for Business — CIA Project"
    "</div>",
    unsafe_allow_html=True
)
