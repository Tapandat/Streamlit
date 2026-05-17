
import streamlit as st, sys
sys.path.append(".")
from utils.data_loader import load_nh
import plotly.graph_objects as go

if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please sign in from the Home page.")
    st.stop()

st.title("📈 Temperature Trends")
df = load_nh()

st.sidebar.header("🔧 Filters")
y_min, y_max = int(df["Year"].min()), int(df["Year"].max())
start, end   = st.sidebar.slider("Year Range", y_min, y_max, (1950, y_max))
show_roll    = st.sidebar.checkbox("5-Year Rolling Average", value=True)
show_raw     = st.sidebar.checkbox("Show Raw Annual Bars",   value=True)

fdf = df[(df["Year"] >= start) & (df["Year"] <= end)].copy()
fdf["Roll5"] = fdf["Annual"].rolling(5, center=True).mean()

fig = go.Figure()
if show_raw:
    colors = ["#d73027" if v >= 0 else "#4575b4" for v in fdf["Annual"]]
    fig.add_trace(go.Bar(x=fdf["Year"], y=fdf["Annual"],
                         marker_color=colors, name="Annual", opacity=0.6))
if show_roll:
    fig.add_trace(go.Scatter(x=fdf["Year"], y=fdf["Roll5"],
                             line=dict(color="black", width=2.5),
                             name="5-Year Avg"))

fig.add_hline(y=0, line_dash="dash", line_color="gray")
fig.update_layout(xaxis_title="Year", yaxis_title="Anomaly (°C)",
                  plot_bgcolor="white", height=500,
                  legend=dict(orientation="h"))
st.plotly_chart(fig, use_container_width=True)
st.caption("🔴 Red = warmer than baseline  |  🔵 Blue = cooler than baseline")
