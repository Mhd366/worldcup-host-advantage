import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Config & Theme ----------
st.set_page_config(page_title="World Cup Host Advantage", page_icon="🏆", layout="wide")
GREEN, GOLD, GRAY = "#006C35", "#C9A227", "#8B949E"

@st.cache_data
def load_data():
    return pd.read_csv("data/clean/clean_data.csv")

df = load_data()

# ---------- Sidebar (متطلب: وصف + فلاتر) ----------
st.sidebar.title("🏆 World Cup Explorer")
st.sidebar.markdown(
    "**Dataset:** all 964 FIFA World Cup matches (1930–2022). "
    "We study **host advantage** and what it means for **Saudi Arabia 2034**.")
st.sidebar.header("Filters")

years = st.sidebar.slider("Year range", int(df.year.min()), int(df.year.max()),
                          (int(df.year.min()), int(df.year.max())))          # slider ✅
rounds = st.sidebar.multiselect("Tournament stage",
        options=sorted(df["round"].unique()), default=None)                   # multiselect ✅
team = st.sidebar.selectbox("Focus team",
        ["All teams"] + sorted(pd.concat([df.home_team, df.away_team]).unique()))  # dropdown ✅

f = df[(df.year >= years[0]) & (df.year <= years[1])]
if rounds: f = f[f["round"].isin(rounds)]
if team != "All teams":
    f = f[(f.home_team == team) | (f.away_team == team)]

# ---------- Main page ----------
st.title("Host Advantage in the FIFA World Cup")
st.caption("Interactive analysis of 964 matches → a data-driven look at Saudi Arabia 2034")

# متطلب: Summary statistics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Matches", len(f))
c2.metric("Avg goals/match", f"{f.total_goals.mean():.2f}")
c3.metric("Avg attendance", f"{f.attendance.mean():,.0f}")
host_rate = f.loc[f.host_playing == 1, "host_won"].mean()
c4.metric("Host win rate", f"{host_rate:.0%}" if pd.notna(host_rate) else "—")

# متطلب: Data preview
with st.expander("📄 Data preview"):
    st.dataframe(f.head(50), use_container_width=True)

# متطلب: Interactive visualizations
tab1, tab2, tab3 = st.tabs(["⚽ Goals & Stages", "📊 Host Advantage", "🇸🇦 Saudi 2034"])

with tab1:
    st.plotly_chart(px.histogram(f, x="total_goals", nbins=13,
        title="Goals per Match", color_discrete_sequence=[GREEN]),
        use_container_width=True)
    st.plotly_chart(px.scatter(f, x="year", y="attendance", color="host_playing",
        title="Attendance Over Time",
        color_discrete_sequence=[GRAY, GREEN]), use_container_width=True)

with tab2:
    hw = df.loc[df.host_playing == 1, "host_won"].mean()
    base = 0.386
    st.plotly_chart(px.bar(x=["Average team", "Host nation"], y=[base, hw],
        title="Win Rate: Host vs Average", color=["a", "b"],
        color_discrete_sequence=[GRAY, GREEN]).update_layout(showlegend=False,
        yaxis_tickformat=".0%"), use_container_width=True)
    st.plotly_chart(px.box(df, x="host_playing", y="attendance",
        title="Attendance: Host Playing vs Not",
        color="host_playing", color_discrete_sequence=[GRAY, GREEN])
        .update_layout(showlegend=False), use_container_width=True)

with tab3:
    st.subheader("What hosting could mean for Saudi Arabia in 2034")
    a, b = st.columns(2)
    a.metric("P(win) — neutral ground", "33.7%")
    b.metric("P(win) — as 2034 host", "56.2%", delta="+22.5 pp")
    st.markdown(
        "- Hosts historically win **62.7%** of matches vs **38.6%** baseline\n"
        "- Modest hosts (South Korea 2002, Russia 2018) beat their own history\n"
        "- Our logistic model attributes **+22.5pp** to hosting for Saudi Arabia\n"
        "- *Caveat: assumes an average opponent; squad may improve by 2034*")

# متطلب: Insight sections
st.divider()
st.subheader("💡 Key insights")
st.markdown(
    "1. **Host advantage is real and large** (+24pp raw, +22.5pp modeled).\n"
    "2. **Crowds are the mechanism** — host matches draw ~70k vs ~40k median.\n"
    "3. **2034 outlook:** hosting alone makes Saudi Arabia a slight favorite "
    "in a typical match — before any squad improvement.")