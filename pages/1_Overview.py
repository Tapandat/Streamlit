

import streamlit as st
import sys
sys.path.insert(0, ".")
from utils.data_loader import load_nh
import plotly.graph_objects as go

st.set_page_config(page_title="Overview | Climate Lens", layout="wide", page_icon="📊")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.1);
}
[data-testid="stSidebar"] * { color: white !important; }
h1, h2, h3, p, label { color: white !important; }
.metric-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-4px); }
.metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00c9ff, #92fe9d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-label {
    color: rgba(255,255,255,0.6) !important;
    font-size: 0.85rem;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.metric-sub {
    color: rgba(255,255,255,0.4) !important;
    font-size: 0.8rem;
    margin-top: 0.2rem;
}
.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: white !important;
    margin: 2rem 0 1rem 0;
    padding-left: 0.5rem;
    border-left: 4px solid #00c9ff;
}
.stButton > button {
    background: linear-gradient(90deg, #00c9ff, #92fe9d) !important;
    color: #0f2027 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please sign in from the Home page.")
    st.stop()

df = load_nh()

latest_year   = int(df["Year"].max())
latest_val    = float(df[df["Year"] == latest_year]["Annual"].values[0])
hottest_year  = int(df.loc[df["Annual"].idxmax(), "Year"])
hottest_val   = float(df["Annual"].max())
total_warming = round(float(hottest_val - df["Annual"].min()), 2)
avg_last10    = round(float(df.nlargest(10, "Year")["Annual"].mean()), 2)

st.markdown(f"""
<div style='padding: 1.5rem 0 0.5rem 0;'>
    <h1 style='font-size:2.2rem; font-weight:800; margin:0;'>
        📊 Overview
    </h1>
    <p style='color:rgba(255,255,255,0.5); margin:0.3rem 0 0 0;'>
        Welcome back, <b style='color:#00c9ff;'>{st.session_state['name']}</b> 👋
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-value'>{latest_val:+.2f}°C</div>
        <div class='metric-label'>🌡️ Latest Anomaly</div>
        <div class='metric-sub'>Year {latest_year}</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-value'>{hottest_year}</div>
        <div class='metric-label'>🔥 Hottest Year</div>
        <div class='metric-sub'>{hottest_val:+.2f}°C anomaly</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-value'>{total_warming}°C</div>
        <div class='metric-label'>📈 Total Warming</div>
        <div class='metric-sub'>Since 1880</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-value'>{avg_last10:+.2f}°C</div>
        <div class='metric-label'>📅 Last 10yr Avg</div>
        <div class='metric-sub'>Recent decade mean</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='section-title'>Temperature Anomaly Trend (1880–Present)</div>", unsafe_allow_html=True)

colors = ["#ff4e4e" if v >= 0 else "#4e9fff" for v in df["Annual"]]
fig = go.Figure()
fig.add_trace(go.Bar(x=df["Year"], y=df["Annual"],
                     marker_color=colors, name="Annual Anomaly", opacity=0.75))
fig.add_trace(go.Scatter(x=df["Year"], y=df["Annual"].rolling(10, center=True).mean(),
                         line=dict(color="#92fe9d", width=2.5), name="10-Year Avg"))
fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)",
              annotation_text="Baseline 1951–1980",
              annotation_font_color="rgba(255,255,255,0.5)")
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="white"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="white",
               title="Anomaly (°C)"),
    legend=dict(orientation="h", y=1.1,
                bgcolor="rgba(0,0,0,0)", font_color="white"),
    height=420, margin=dict(l=0, r=0, t=30, b=0)
)
st.plotly_chart(fig, use_container_width=True)
st.caption("Source: NASA GISTEMP v4 — Northern Hemisphere | Baseline: 1951–1980")
