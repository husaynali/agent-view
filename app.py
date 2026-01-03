import streamlit as st
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="KEETA AGENT VIEW",
    page_icon="🐆",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():
    agents = pd.read_excel("data/main.xlsx", sheet_name="AGENTDB")
    kpis = pd.read_excel("data/main.xlsx", sheet_name="KPIDB")
    return agents, kpis

agents_df, kpis_df = load_data()

# ==================================================
# SESSION STATE
# ==================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==================================================
# KPI CARD (MOBILE SAFE)
# ==================================================
def kpi_card(title, value, unit="", color="#1f77b4"):
    st.markdown(
        f"""
        <div style="
            background-color:#ffffff;
            padding:16px;
            border-radius:16px;
            box-shadow:0 4px 14px rgba(0,0,0,0.08);
            text-align:center;
            margin-bottom:16px;
        ">
            <div style="
                font-size:15px;
                font-weight:700;
                color:#000000;
                margin-bottom:6px;
            ">
                {title}
            </div>
            <div style="
                font-size:32px;
                font-weight:800;
                color:{color};
                margin:6px 0;
            ">
                {value}
            </div>
            <div style="
                font-size:13px;
                color:#666;
            ">
                {unit}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# LOGIN PAGE
# ==================================================
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🔐 Agent Login</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Agent MIS")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            user = agents_df[
                (agents_df["AGENTMIS"] == username) &
                (agents_df["PASSWORD"] == password) &
                (agents_df["ROLE"] == "Agent")
            ]

            if not user.empty:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.name = user.iloc[0]["NAME"]
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# ==================================================
# HEADER (Centered Avatar + Profile)
# ==================================================
st.markdown(
    f"""
    <div style="
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        margin-top:20px;
        margin-bottom:20px;
    ">
        <div style="
            width:70px;
            height:70px;
            border-radius:50%;
            background-color:#1f77b4;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:32px;
            font-weight:700;
            color:white;
        ">
            👤
        </div>
        <div style="text-align:center; margin-top:10px;">
            <div style="font-size:20px; font-weight:700;">{st.session_state.name}</div>
            <div style="font-size:14px; color:#666;">{st.session_state.username}</div>
        </div>
        <div style="margin-top:10px;">
            <form action="" method="post">
                <button type="submit" style="
                    background-color:#d62728;
                    border:none;
                    color:white;
                    padding:6px 12px;
                    border-radius:8px;
                    cursor:pointer;
                ">Logout</button>
            </form>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ==================================================
# FILTER AGENT KPI DATA
# ==================================================
agent_kpi = kpis_df[kpis_df["AGENTMIS"] == st.session_state.username]

if agent_kpi.empty:
    st.error("No KPI data found for this agent.")
    st.stop()

row = agent_kpi.iloc[0]

# ==================================================
# DASHBOARD
# ==================================================
st.markdown("<h3>📊 Performance Dashboard</h3>", unsafe_allow_html=True)

# --------------------------------------------------
# VOLUME & SATISFACTION
# --------------------------------------------------
st.markdown("<h4>📞 Volume & Satisfaction</h4>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    kpi_card("Answered Volume", row["ANS_VOL"], "calls")
    kpi_card("CSAT", f"{row['CSAT_SCORE']:.0%}", "%", "#2ca02c")

with c2:
    kpi_card("Surveyed", row["SURVEYED"], "surveys")
    kpi_card("DSAT", f"{row['DSAT_SCORE']:.0%}", "%", "#d62728")

# --------------------------------------------------
# RESOLUTION & QUALITY
# --------------------------------------------------
st.markdown("<h4>✅ Resolution & Quality</h4>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    kpi_card("Solved Rate", f"{row['ISSUE_RESOLUTION']:.0%}", "%", "#9467bd")
    kpi_card("Evaluated", row["EVALUATED"], "cases")

with c2:
    kpi_card("Passed", row["PASS_EVALUATION"], "cases", "#2ca02c")
    kpi_card("Failed", row["FAIL_EVALUATION"], "cases", "#d62728")

# --------------------------------------------------
# EFFICIENCY & ATTENDANCE
# --------------------------------------------------
st.markdown("<h4>⏱ Efficiency & Attendance</h4>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    kpi_card("AHT", row["AHT_MIN"], "minutes")
    kpi_card("Absent Days", row["ABSENT"], "days", "#d62728")

with c2:
    kpi_card("ART", row["ART_MIN"], "minutes")
    kpi_card("Variable Score", row["VARIABLE"], "%", "#ff7f0e")
