
import streamlit as st, sys
sys.path.append(".")
from utils.data_loader import load_nh
import plotly.graph_objects as go

if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please sign in from the Home page.")
    st.stop()

st.title("📊 Overview")
st.markdown(f"Welcome back, **{st.session_state['name']}** 👋")
st.markdown("---")

df = load_nh()

latest_year   = int(df["Year"].max())
latest_val    = float(df[df["Year"] == latest_year]["Annual"].values[0])
hottest_year  = int(df.loc[df["Annual"].idxmax(), "Year"])
hottest_val   = float(df["Annual"].max())
total_warming = round(float(hottest_val - df["Annual"].min()), 2)

col1, col2, col3 = st.columns(3)
col1.metric("🌡️ Latest Anomaly",  f"{latest_val:.2f} °C",   f"Year {latest_year}")
col2.metric("🔥 Hottest Year",    str(hottest_year),          f"{hottest_val:.2f} °C")
col3.metric("📈 Total Warming",   f"{total_warming} °C",      "Since 1880")

st.markdown("---")
st.subheader("Global Trend at a Glance")

colors = ["#d73027" if v >= 0 else "#4575b4" for v in df["Annual"]]
fig = go.Figure()
fig.add_trace(go.Bar(x=df["Year"], y=df["Annual"],
                     marker_color=colors, name="Annual Anomaly", opacity=0.8))
fig.add_trace(go.Scatter(x=df["Year"], y=df["Annual"].rolling(10, center=True).mean(),
                         line=dict(color="black", width=2), name="10-Year Avg"))
fig.add_hline(y=0, line_dash="dash", line_color="gray",
              annotation_text="Baseline 1951–1980")
fig.update_layout(xaxis_title="Year", yaxis_title="Anomaly (°C)",
                  plot_bgcolor="white", height=420,
                  legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig, use_container_width=True)
st.caption("Source: NASA GISTEMP v4 — Northern Hemisphere")
