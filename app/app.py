import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Road to 2034 — Host Advantage",
                   page_icon="🏆", layout="wide")
GREEN, GOLD, GRAY, DARK = "#006C35", "#C9A227", "#8B949E", "#0E1117"

# ---------- Theme (CSS) ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

.hero {
  background: linear-gradient(135deg, #04220f 0%, #006C35 55%, #0a3d1f 100%);
  border: 1px solid rgba(201,162,39,.35);
  border-radius: 18px; padding: 38px 44px; margin-bottom: 8px;
}
.hero h1 { color: #fff; font-size: 2.3rem; font-weight: 800; margin: 0; }
.hero .gold { color: #C9A227; }
.hero p { color: rgba(255,255,255,.85); margin: 8px 0 0; font-size: 1.05rem; }

div[data-testid="stMetric"] {
  background: linear-gradient(160deg, rgba(0,108,53,.10), rgba(201,162,39,.07));
  border: 1px solid rgba(201,162,39,.30);
  border-radius: 14px; padding: 14px 18px;
}
div[data-testid="stMetric"] label { color: #C9A227 !important; }

.stTabs [data-baseweb="tab"] { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/clean/clean_data.csv")

df = load_data()

# ---------- Hero banner ----------
st.markdown("""
<div class="hero">
  <h1>🏆 Road to <span class="gold">2034</span> — The Host Advantage</h1>
  <p>964 matches · 22 tournaments · one question: what does hosting the World Cup
  really do for a nation — and what does it mean for <b>Saudi Arabia 2034</b>?</p>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar: dataset description + filters ----------
st.sidebar.title("🏆 World Cup Explorer")
st.sidebar.markdown(
    "**Dataset:** all 964 FIFA World Cup matches (1930–2022). "
    "We study **host advantage** and what it means for **Saudi Arabia 2034**.")
st.sidebar.header("Filters")

years = st.sidebar.slider("Year range", int(df.year.min()), int(df.year.max()),
                          (int(df.year.min()), int(df.year.max())))
rounds = st.sidebar.multiselect("Tournament stage",
        options=sorted(df["round"].unique()), default=None)
team = st.sidebar.selectbox("Focus team",
        ["All teams"] + sorted(pd.concat([df.home_team, df.away_team]).unique()))

f = df[(df.year >= years[0]) & (df.year <= years[1])]
if rounds:
    f = f[f["round"].isin(rounds)]
if team != "All teams":
    f = f[(f.home_team == team) | (f.away_team == team)]

# ---------- Summary statistics ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Matches", len(f))
c2.metric("Avg goals/match", f"{f.total_goals.mean():.2f}")
c3.metric("Avg attendance", f"{f.attendance.mean():,.0f}")
host_rate = f.loc[f.host_playing == 1, "host_won"].mean()
c4.metric("Host win rate", f"{host_rate:.0%}" if pd.notna(host_rate) else "—")

# ---------- Data preview ----------
with st.expander("📄 Data preview"):
    st.dataframe(f.head(50), use_container_width=True)

# ---------- Interactive visualizations ----------
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
    st.progress(0.562, text="Modeled win probability as 2034 host: 56.2%")
    st.progress(0.337, text="Same team, neutral ground: 33.7%")
    st.markdown(
        "- Hosts historically win **62.7%** of matches vs **38.6%** baseline\n"
        "- Modest hosts (South Korea 2002, Russia 2018) beat their own history\n"
        "- Our logistic model (65.3% accuracy) attributes **+22.5pp** to hosting\n"
        "- *Caveat: assumes an average opponent; squad may improve by 2034*")

# ---------- Key insights ----------
st.divider()
st.subheader("💡 Key insights")
st.markdown(
    "1. **Host advantage is real and large** (+24pp raw, +22.5pp modeled — "
    "`is_host` coefficient +0.93 in our logistic model).\n"
    "2. **Crowds are the mechanism** — host matches draw ~70k vs ~40k median attendance.\n"
    "3. **2034 outlook:** hosting alone makes Saudi Arabia a slight favorite "
    "in a typical match — before any squad improvement.")

st.markdown(
    "<p style='text-align:center;color:#8B949E;font-size:.85rem;margin-top:30px'>"
    "Data: FIFA World Cup matches 1930–2022 (Kaggle) · Built with Streamlit & Plotly · "
    "Analysis project — Unit 3</p>", unsafe_allow_html=True)