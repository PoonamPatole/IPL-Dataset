import streamlit as st
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Match Dashboard",
    page_icon="🏏",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 50%, #0d1a2e 100%);
    color: #e8e0f5;
}

/* Hero title */
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem;
    letter-spacing: 4px;
    background: linear-gradient(90deg, #f5a623, #ff6b35, #e91e8c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 0;
    line-height: 1;
}

.hero-sub {
    text-align: center;
    color: #9c88c8;
    font-size: 1rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.2rem;
    margin-bottom: 2rem;
}

/* Stat cards */
.stat-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(245,166,35,0.25);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    backdrop-filter: blur(8px);
    transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-3px); }
.stat-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    color: #f5a623;
    line-height: 1;
}
.stat-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #9c88c8;
    margin-top: 0.3rem;
}

/* Section header */
.section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 3px;
    color: #f5a623;
    border-bottom: 2px solid rgba(245,166,35,0.3);
    padding-bottom: 0.4rem;
    margin-bottom: 1.2rem;
}

/* Innings badge */
.innings-badge {
    display: inline-block;
    background: linear-gradient(90deg, #f5a623, #ff6b35);
    color: #0d0d1a;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    letter-spacing: 2px;
    padding: 0.2rem 0.8rem;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}

/* Team name */
.team-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 2px;
}

/* Player chips */
.player-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.6rem;
}
.player-chip {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.85rem;
    color: #e8e0f5;
    white-space: nowrap;
}

/* Innings card */
.innings-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}

/* Role label */
.role-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #9c88c8;
    margin-top: 0.8rem;
    margin-bottom: 0.3rem;
}

/* Venue pill */
.venue-pill {
    display: inline-block;
    background: rgba(233,30,140,0.15);
    border: 1px solid rgba(233,30,140,0.4);
    color: #e91e8c;
    border-radius: 30px;
    padding: 0.35rem 1.1rem;
    font-size: 0.9rem;
    letter-spacing: 1px;
    margin-bottom: 1.6rem;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin: 2rem 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(13,13,26,0.95);
    border-right: 1px solid rgba(245,166,35,0.15);
}
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
def parse_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    raw_df["batsmen_list"] = raw_df["batsmen"].apply(lambda x: [p.strip() for p in x.split(",")])
    raw_df["bowlers_list"] = raw_df["bowlers"].apply(lambda x: [p.strip() for p in x.split(",")])
    return raw_df

# Allow user to upload their own file
uploaded = st.sidebar.file_uploader("📂 Upload a CSV", type=["csv"])

if uploaded is not None:
    df = parse_df(pd.read_csv(uploaded))
else:
    st.info("👈 Please upload your CSV file using the sidebar to get started.")
    st.stop()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.markdown("### 🏟️ Filters")

venues = ["All"] + sorted(df["venue"].unique().tolist())
sel_venue = st.sidebar.selectbox("Venue", venues)

all_teams = sorted(set(df["batting_team"].tolist() + df["bowling_team"].tolist()))
sel_team = st.sidebar.selectbox("Team", ["All"] + all_teams)

innings_opts = ["All"] + sorted(df["innings"].unique().tolist())
sel_innings = st.sidebar.selectbox("Innings", innings_opts)

# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = df.copy()
if sel_venue != "All":
    filtered = filtered[filtered["venue"] == sel_venue]
if sel_team != "All":
    filtered = filtered[(filtered["batting_team"] == sel_team) | (filtered["bowling_team"] == sel_team)]
if sel_innings != "All":
    filtered = filtered[filtered["innings"] == sel_innings]

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🏏 IPL Match Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Indian Premier League · Match Analytics</div>', unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
all_batsmen = set(p for lst in filtered["batsmen_list"] for p in lst)
all_bowlers = set(p for lst in filtered["bowlers_list"] for p in lst)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="stat-card"><div class="stat-number">{filtered["venue"].nunique()}</div><div class="stat-label">Venues</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card"><div class="stat-number">{len(filtered)}</div><div class="stat-label">Innings</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card"><div class="stat-number">{len(all_batsmen)}</div><div class="stat-label">Batsmen</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-card"><div class="stat-number">{len(all_bowlers)}</div><div class="stat-label">Bowlers</div></div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Innings cards ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">INNINGS BREAKDOWN</div>', unsafe_allow_html=True)

if filtered.empty:
    st.warning("No data matches the selected filters.")
else:
    for _, row in filtered.iterrows():
        chips_bat = "".join(f'<span class="player-chip">🏏 {p}</span>' for p in row["batsmen_list"])
        chips_bowl = "".join(f'<span class="player-chip">🎳 {p}</span>' for p in row["bowlers_list"])
        st.markdown(f"""
        <div class="innings-card">
            <div class="innings-badge">INNINGS {row['innings']}</div>
            <div style="display:flex; gap:3rem; flex-wrap:wrap; margin-bottom:0.6rem;">
                <div>
                    <div class="role-label">🏏 Batting</div>
                    <div class="team-name" style="color:#f5a623">{row['batting_team']}</div>
                </div>
                <div>
                    <div class="role-label">🎳 Bowling</div>
                    <div class="team-name" style="color:#e91e8c">{row['bowling_team']}</div>
                </div>
            </div>
            <div class="venue-pill">📍 {row['venue']}</div>
            <div class="role-label">Batsmen</div>
            <div class="player-grid">{chips_bat}</div>
            <div class="role-label">Bowlers</div>
            <div class="player-grid">{chips_bowl}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Raw data table ────────────────────────────────────────────────────────────
with st.expander("📋 View Raw Data"):
    display_df = filtered[["venue", "innings", "batting_team", "bowling_team", "batsmen", "bowlers"]]
    st.dataframe(display_df, use_container_width=True)

# ── Player explorer ───────────────────────────────────────────────────────────
st.markdown('<div class="section-header">PLAYER EXPLORER</div>', unsafe_allow_html=True)

all_players = sorted(all_batsmen | all_bowlers)
sel_player = st.selectbox("Search for a player", ["— select —"] + all_players)

if sel_player != "— select —":
    bat_rows = filtered[filtered["batsmen_list"].apply(lambda lst: sel_player in lst)]
    bowl_rows = filtered[filtered["bowlers_list"].apply(lambda lst: sel_player in lst)]

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**🏏 Batted in {len(bat_rows)} innings**")
        if not bat_rows.empty:
            for _, r in bat_rows.iterrows():
                st.markdown(f"- Innings {r['innings']} · {r['batting_team']} vs {r['bowling_team']} @ {r['venue']}")
    with col_b:
        st.markdown(f"**🎳 Bowled in {len(bowl_rows)} innings**")
        if not bowl_rows.empty:
            for _, r in bowl_rows.iterrows():
                st.markdown(f"- Innings {r['innings']} · {r['bowling_team']} vs {r['batting_team']} @ {r['venue']}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#5a4a7a;font-size:0.8rem;letter-spacing:2px;">IPL MATCH DASHBOARD · BUILT WITH STREAMLIT</p>', unsafe_allow_html=True)
