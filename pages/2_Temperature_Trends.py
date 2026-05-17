%%writefile climate_lens/pages/2_Temperature_Trends.py

import streamlit as st
import sys
sys.path.insert(0, ".")
from utils.data_loader import load_nh
import plotly.graph_objects as go

st.set_page_config(page_title="Trends | Climate Lens", layout="wide", page_icon="📈")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
[data-testid="stSidebar"] { background: rgba(255,255,255,0.05) !important; backdrop-filter: blur(10px); border-right: 1px solid rgba(255,255,255,0.1); }
[data-testid="stSidebar"] * { color: white !important; }
h1, h2, h3, p, label { color: white !important; }
.section-title { font-size: 1.4rem; font-weight: 700; color: white !important; margin: 1rem 0; padding-left: 0.5rem; border-left: 4px solid #00c9ff; }
.stSlider label { color: white !important; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please sign in from the Home page.")
    st.stop()

st.markdown("<h1 style='font-size:2.2rem; font-weight:800; padding-top:1.5rem;'>📈 Temperature Trends</h1>", unsafe_allow_html=True)
st.markdown("---")

df = load_nh()

st.sidebar.markdown("### 🔧 Controls")
y_min, y_max = int(df["Year"].min()), int(df["Year"].max())
start, end   = st.sidebar.slider("Year Range", y_min, y_max, (1950, y_max))
show_roll    = st.sidebar.checkbox("5-Year Rolling Average", value=True)
show_raw     = st.sidebar.checkbox("Annual Bars", value=True)

fdf = df[(df["Year"] >= start) & (df["Year"] <= end)].copy()
fdf["Roll5"] = fdf["Annual"].rolling(5, center=True).mean()

fig = go.Figure()
if show_raw:
    colors = ["#ff4e4e" if v >= 0 else "#4e9fff" for v in fdf["Annual"]]
    fig.add_trace(go.Bar(x=fdf["Year"], y=fdf["Annual"],
                         marker_color=colors, name="Annual", opacity=0.65))
if show_roll:
    fig.add_trace(go.Scatter(x=fdf["Year"], y=fdf["Roll5"],
                             line=dict(color="#92fe9d", width=2.5), name="5-Year Avg"))

fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font_color="white", height=500,
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="white"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="white", title="Anomaly (°C)"),
    legend=dict(orientation="h", bgcolor="rgba(0,0,0,0)", font_color="white"),
    margin=dict(l=0, r=0, t=20, b=0)
)
st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Period Max", f"{fdf['Annual'].max():.2f}°C", f"{int(fdf.loc[fdf['Annual'].idxmax(),'Year'])}")
col2.metric("Period Min", f"{fdf['Annual'].min():.2f}°C", f"{int(fdf.loc[fdf['Annual'].idxmin(),'Year'])}")
col3.metric("Period Mean", f"{fdf['Annual'].mean():.2f}°C")
st.caption("🔴 Red = warmer than baseline  |  🔵 Blue = cooler than baseline")
