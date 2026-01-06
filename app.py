import streamlit as st
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="KEETA AGENT VIEW",
    page_icon="🐆",
    layout="wide",
    menu_items={}
)

# ==================================================
# GLOBAL STYLING
# ==================================================
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f0f2f6 !important;
    }
    #MainMenu, footer, header {visibility: hidden;}

    /* Input fields */
    input, textarea, select {
        color: #1f2937 !important;
        background-color: #ffffff !important;
    }
    label, [data-testid="stMarkdownContainer"] p {
        color: #1f2937 !important;
    }
    ::placeholder {
        color: #4b5563 !important;
    }

    /* Top bar */
    .top-bar {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        background-color: #f0f2f6;
        padding: 10px;
        border-bottom: 1px solid #ddd;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    .top-bar a {
        margin: 6px;
        padding: 8px 14px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        color: white;
    }
    .whatsapp-btn { background-color: #25D366; }
    .email-btn { background-color: #007bff; }
    </style>
""", unsafe_allow_html=True)

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
# KPI CARD
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
            <div style="font-size:15px; font-weight:700; color:#1f2937; margin-bottom:6px;">{title}</div>
            <div style="font-size:32px; font-weight:800; color:{color}; margin:6px 0;">{value}</div>
            <div style="font-size:13px; color:#4b5563;">{unit}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# LOGIN PAGE
# ==================================================
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center; color:#1f2937;'>🔐 Agent Login</h2>", unsafe_allow_html=True)

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
# TOP BAR WITH SUPPORT BUTTONS
# ==================================================
agent_name = st.session_state.name
agent_mis = st.session_state.username

whatsapp_url = f"https://wa.me/201012787537?text=Agent%20{agent_mis}%20({agent_name})%20reporting%20an%20issue"
email_url = f"mailto:bad-banni@proton.me?subject=Agent%20Issue%20Report&body=Agent%20{agent_mis}%20({agent_name})%20reporting%20an%20issue"

st.markdown(
    f"""
    <div class="top-bar">
        <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">📩 WhatsApp</a>
        <a href="{email_url}" target="_blank" class="email-btn">📧 Email</a>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# HEADER
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
            🐆
        </div>
        <div style="text-align:center; margin-top:10px;">
            <div style="font-size:20px; font-weight:700; color:#1f2937;">{agent_name}</div>
            <div style="font-size:14px; color:#4b5563;">{agent_mis}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ==================================================
# FILTER KPI DATA
# ==================================================
agent_kpi = kpis_df[kpis_df["AGENTMIS"] == agent_mis]

if agent_kpi.empty:
    st.error("No KPI data found for this agent.")
    st.stop()

row = agent_kpi.iloc[0]

# ==================================================
# DASHBOARD
# ==================================================
st.markdown("<h3 style='color:#1f2937;'>📊 Performance Dashboard</h3>", unsafe_allow_html=True)

# Volume & Satisfaction
st.markdown("<h4 style='color:#1f2937;'>📞 Volume & Satisfaction</h4>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    kpi_card("Answered Volume", row["ANS_VOL"], "calls")
    kpi_card("CSAT", f"{row['CSAT_SCORE']:.0%}", "%", "#2ca02c")
with c2:
    kpi_card("Surveyed", row["SURVEYED"], "surveys")
    kpi_card("DSAT", f"{row['DSAT_SCORE']:.0%}", "%", "#d62728")

# Resolution & Quality
st.markdown("<h4 style='color:#1f2937;'>✅ Resolution & Quality</h4>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    kpi_card("Solved Rate", f"{row['ISSUE_RESOLUTION']:.0%}", "%", "#9467bd")
    kpi_card("Evaluated", row["EVALUATED"], "cases")
with c2:
    kpi_card("Passed", row["PASS_EVALUATION"], "cases", "#2ca02c")
    kpi_card("Failed", row["FAIL_EVALUATION"], "cases", "#d62728")

# Efficiency & Attendance
st.markdown("<h4 style='color:#1f2937;'>⏱ Efficiency & Attendance</h4>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    kpi_card("AHT", f"{row['AHT_MIN']:.3f}", "minutes")
    kpi_card("Absent Days", row["ABSENT"], "days", "#d62728")
with c2:
    kpi_card("ART", f"{row['ART_MIN']:.3f}", "minutes")
    kpi_card("Variable Score", row["VARIABLE"], "%", "#ff7f0e")
