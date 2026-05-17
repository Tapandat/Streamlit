
import streamlit as st, sys
sys.path.append(".")
from utils.data_loader import load_nh
import plotly.express as px

if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please sign in from the Home page.")
    st.stop()

st.title("🗓️ Monthly Patterns")
df = load_nh()

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
decade_start = st.sidebar.slider("Start from year", 1880, 2000, 1950, step=10)
fdf = df[df["Year"] >= decade_start]

# Heatmap
heat = fdf.set_index("Year")[months]
fig1 = px.imshow(heat.T, color_continuous_scale="RdBu_r",
                 color_continuous_midpoint=0, aspect="auto",
                 labels=dict(color="Anomaly (°C)"),
                 title=f"Monthly Anomalies ({decade_start}–Present)")
fig1.update_layout(height=420)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# Avg by month bar
avg = fdf[months].mean().reset_index()
avg.columns = ["Month", "Avg Anomaly"]
fig2 = px.bar(avg, x="Month", y="Avg Anomaly",
              color="Avg Anomaly", color_continuous_scale="RdBu_r",
              color_continuous_midpoint=0,
              title=f"Average Anomaly by Month ({decade_start}–Present)")
fig2.update_layout(plot_bgcolor="white", height=380)
st.plotly_chart(fig2, use_container_width=True)
