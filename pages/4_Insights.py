
import streamlit as st, sys, numpy as np
sys.path.append(".")
from utils.data_loader import load_nh
import plotly.express as px

if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please sign in from the Home page.")
    st.stop()

st.title("💡 Insights")
df = load_nh()

slope, _ = np.polyfit(df["Year"], df["Annual"], 1)
rate     = round(slope * 10, 3)
top10    = df.nlargest(10, "Annual")["Year"].tolist()
last10   = df.nlargest(10, "Year")["Year"].tolist()
overlap  = len(set(top10) & set(last10))

st.markdown("### 🔑 Key Findings")
col1, col2 = st.columns(2)
col1.success( f"🌡️ Warming at **{rate} °C per decade**")
col1.info(    f"🏆 **{overlap} of the last 10 years** are in the top 10 hottest ever")
col2.error(   f"🔥 Hottest year: **{int(df.loc[df['Annual'].idxmax(),'Year'])}** "
              f"({df['Annual'].max():.2f} °C)")
col2.info(    f"❄️ Coolest year: **{int(df.loc[df['Annual'].idxmin(),'Year'])}** "
              f"({df['Annual'].min():.2f} °C)")

st.markdown("---")
st.subheader("🏆 Top 10 Hottest Years")
top_df = df.nlargest(10, "Annual")[["Year","Annual"]].rename(
            columns={"Annual":"Anomaly (°C)"}).reset_index(drop=True)
top_df.index += 1
st.dataframe(top_df, use_container_width=True)

st.markdown("---")
st.subheader("📉 Warming Trend (Linear Regression)")
df["Trend"] = np.polyval(np.polyfit(df["Year"], df["Annual"], 1), df["Year"])
fig = px.scatter(df, x="Year", y="Annual", opacity=0.4,
                 labels={"Annual":"Anomaly (°C)"})
fig.add_scatter(x=df["Year"], y=df["Trend"],
                mode="lines", line=dict(color="red", width=2),
                name="Trend Line")
fig.update_layout(plot_bgcolor="white", height=380)
st.plotly_chart(fig, use_container_width=True)

st.caption("Source: NASA GISTEMP v4 — Northern Hemisphere | Baseline: 1951–1980")
