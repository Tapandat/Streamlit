%%writefile climate_lens/pages/4_Insights.py

import streamlit as st
import sys, numpy as np
sys.path.insert(0, ".")
from utils.data_loader import load_nh
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Insights | Climate Lens", layout="wide", page_icon="💡")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
[data-testid="stSidebar"] { background: rgba(255,255,255,0.05) !important; backdrop-filter: blur(10px); border-right: 1px solid rgba(255,255,255,0.1); }
[data-testid="stSidebar"] * { color: white !important; }
h1, h2, h3, p, label { color: white !important; }
.insight-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}
.insight-card h4 { color: #00c9ff !important; margin: 0 0 0.3rem 0; font-size: 1rem; }
.insight-card p  { color: rgba(255,255,255,0.8) !important; margin: 0; font-size: 0.95rem; }
.stDataFrame { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please sign in from the Home page.")
    st.stop()

st.markdown("<h1 style='font-size:2.2rem; font-weight:800; padding-top:1.5rem;'>💡 Insights</h1>", unsafe_allow_html=True)
st.markdown("---")

df = load_nh()
slope, _    = np.polyfit(df["Year"], df["Annual"], 1)
rate        = round(slope * 10, 3)
top10_years = df.nlargest(10, "Annual")["Year"].tolist()
last10_years= df.nlargest(10, "Year")["Year"].tolist()
overlap     = len(set(top10_years) & set(last10_years))
hottest     = int(df.loc[df["Annual"].idxmax(), "Year"])
coolest     = int(df.loc[df["Annual"].idxmin(), "Year"])

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""<div class='insight-card'>
        <h4>🌡️ Warming Rate</h4>
        <p>The Northern Hemisphere is warming at <b>{rate}°C per decade</b> — a clear upward trend since industrialization.</p>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class='insight-card'>
        <h4>🏆 Recent Domination</h4>
        <p><b>{overlap} of the last 10 years</b> are among the 10 hottest years ever recorded.</p>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class='insight-card'>
        <h4>🔥 Hottest Year on Record</h4>
        <p><b>{hottest}</b> recorded the highest anomaly at <b>{df['Annual'].max():.2f}°C</b> above baseline.</p>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class='insight-card'>
        <h4>❄️ Coolest Year on Record</h4>
        <p><b>{coolest}</b> was the coolest at <b>{df['Annual'].min():.2f}°C</b> below baseline.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("#### 🏆 Top 10 Hottest Years")
    top_df = df.nlargest(10, "Annual")[["Year","Annual"]].rename(
        columns={"Annual":"Anomaly (°C)"}).reset_index(drop=True)
    top_df.index += 1
    st.dataframe(top_df, use_container_width=True)

with col_b:
    st.markdown("#### 📉 Warming Trend")
    df["Trend"] = np.polyval(np.polyfit(df["Year"], df["Annual"], 1), df["Year"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Year"], y=df["Annual"],
                             mode="markers", marker=dict(color="#4e9fff", size=4, opacity=0.5),
                             name="Annual"))
    fig.add_trace(go.Scatter(x=df["Year"], y=df["Trend"],
                             mode="lines", line=dict(color="#ff4e4e", width=2.5),
                             name="Trend"))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="white", height=320,
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="white"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="white"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_color="white"),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

st.caption("Source: NASA GISTEMP v4 — Northern Hemisphere | Baseline: 1951–1980")
