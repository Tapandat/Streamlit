

import streamlit as st
import sys
sys.path.insert(0, ".")
from utils.data_loader import load_nh
import plotly.express as px

st.set_page_config(page_title="Monthly | Climate Lens", layout="wide", page_icon="🗓️")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
[data-testid="stSidebar"] { background: rgba(255,255,255,0.05) !important; backdrop-filter: blur(10px); border-right: 1px solid rgba(255,255,255,0.1); }
[data-testid="stSidebar"] * { color: white !important; }
h1, h2, h3, p, label { color: white !important; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please sign in from the Home page.")
    st.stop()

st.markdown("<h1 style='font-size:2.2rem; font-weight:800; padding-top:1.5rem;'>🗓️ Monthly Patterns</h1>", unsafe_allow_html=True)
st.markdown("---")

df = load_nh()
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

st.sidebar.markdown("### 🔧 Controls")
decade_start = st.sidebar.slider("Start from year", 1880, 2000, 1950, step=10)
fdf = df[df["Year"] >= decade_start]

fig1 = px.imshow(
    fdf.set_index("Year")[months].T,
    color_continuous_scale="RdBu_r",
    color_continuous_midpoint=0,
    aspect="auto",
    labels=dict(color="Anomaly (°C)"),
    title=f"Monthly Temperature Anomalies ({decade_start}–Present)"
)
fig1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font_color="white", height=420,
    title_font_color="white",
    margin=dict(l=0, r=0, t=40, b=0)
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

avg = fdf[months].mean().reset_index()
avg.columns = ["Month", "Avg Anomaly"]
fig2 = px.bar(avg, x="Month", y="Avg Anomaly",
              color="Avg Anomaly", color_continuous_scale="RdBu_r",
              color_continuous_midpoint=0,
              title=f"Average Anomaly by Month ({decade_start}–Present)")
fig2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font_color="white", height=380,
    title_font_color="white",
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="white"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="white"),
    margin=dict(l=0, r=0, t=40, b=0)
)
st.plotly_chart(fig2, use_container_width=True)
