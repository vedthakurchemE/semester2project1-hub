import streamlit as st
import importlib
import traceback
import sys, os
import pandas as pd
import sqlite3
import io
import contextlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import matplotlib.pyplot as plt
import time
import inspect
import datetime

# ── Streamlit App Config ──────────────────────────────────────
st.set_page_config(
    page_title="⚗️ Ved Thakur — Semester 2 Engineering Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background-color: #060a10;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(0,200,150,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,120,255,0.06) 0%, transparent 60%),
        repeating-linear-gradient(0deg, transparent, transparent 60px, rgba(255,255,255,0.012) 60px, rgba(255,255,255,0.012) 61px),
        repeating-linear-gradient(90deg, transparent, transparent 60px, rgba(255,255,255,0.012) 60px, rgba(255,255,255,0.012) 61px);
    color: #d0dae8;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111f 0%, #050d18 100%);
    border-right: 1px solid rgba(0,220,160,0.12);
}
[data-testid="stSidebar"] * { color: #a8bdd4 !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.88rem !important; }

.hero-wrap {
    position: relative;
    border: 1px solid rgba(0,220,160,0.18);
    border-radius: 24px;
    padding: 70px 50px 60px;
    overflow: hidden;
    margin-bottom: 36px;
    background: linear-gradient(135deg, #050f1c 0%, #071a2e 60%, #050f1c 100%);
}
.hero-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 80% at 0% 50%, rgba(0,220,160,0.09) 0%, transparent 70%),
        radial-gradient(ellipse 50% 60% at 100% 50%, rgba(0,120,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-wrap::after {
    content: '';
    position: absolute;
    top: -1px; left: 40px; right: 40px; height: 2px;
    background: linear-gradient(90deg, transparent, #00dc9f, #0078ff, transparent);
    border-radius: 2px;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #00dc9f;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 14px;
    opacity: 0.85;
}
.hero-name {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    color: #eaf2ff;
    margin: 0 0 6px;
    letter-spacing: -1.5px;
}
.hero-name span {
    background: linear-gradient(90deg, #00dc9f, #0096ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: rgba(208,218,232,0.65);
    font-weight: 300;
    margin-bottom: 28px;
    letter-spacing: 0.3px;
}
.hero-chips { display: flex; flex-wrap: wrap; gap: 10px; }
.hero-chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    padding: 5px 14px;
    border-radius: 4px;
    border: 1px solid rgba(0,220,160,0.25);
    background: rgba(0,220,160,0.06);
    color: #00dc9f;
    letter-spacing: 0.5px;
}

.stat-box {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 22px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 10px;
}
.stat-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #00dc9f, #0078ff);
}
.stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #00dc9f;
    line-height: 1;
}
.stat-lbl {
    font-size: 0.72rem;
    color: rgba(208,218,232,0.45);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
    font-family: 'JetBrains Mono', monospace;
}

.sec-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #eaf2ff;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}
.sec-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #00dc9f;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 24px;
    opacity: 0.75;
}

.proj-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 26px 28px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
}
.proj-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0; width: 3px;
    background: linear-gradient(180deg, #00dc9f, #0078ff);
    border-radius: 3px 0 0 3px;
}
.proj-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #eaf2ff;
    margin-bottom: 4px;
}
.proj-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    padding: 3px 9px;
    border-radius: 3px;
    border: 1px solid rgba(0,150,255,0.3);
    background: rgba(0,150,255,0.08);
    color: #60a5fa;
    display: inline-block;
    margin: 2px;
    letter-spacing: 0.3px;
}

.res-item {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    background: rgba(0,220,160,0.04);
    border-left: 2px solid #00dc9f;
    border-radius: 0 8px 8px 0;
    padding: 9px 16px;
    margin: 5px 0;
    color: #b8ccdc;
}
.res-item strong { color: #00dc9f; }
.res-item code {
    background: rgba(255,255,255,0.06);
    padding: 2px 6px;
    border-radius: 4px;
    color: #7dd3fc;
}

.stButton > button {
    background: linear-gradient(135deg, #00dc9f, #0096ff) !important;
    color: #060a10 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.3px !important;
    padding: 10px 22px !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 20px rgba(0,220,160,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0,220,160,0.4) !important;
}
.stDownloadButton > button {
    background: rgba(0,220,160,0.1) !important;
    color: #00dc9f !important;
    border: 1px solid rgba(0,220,160,0.3) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
}

.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    color: #eaf2ff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.015) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 0 0 10px 10px !important;
}

.stSelectbox > div > div,
.stTextArea > div > div,
.stTextInput > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #d0dae8 !important;
    font-family: 'Outfit', sans-serif !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.02) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    color: rgba(208,218,232,0.5) !important;
    border-radius: 7px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(0,220,160,0.1) !important;
    color: #00dc9f !important;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 18px;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    color: #00dc9f !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #00dc9f, #0096ff) !important;
}
.stAlert { border-radius: 10px !important; }

.info-block {
    background: rgba(0,120,255,0.06);
    border: 1px solid rgba(0,120,255,0.18);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.info-block h3 {
    font-family: 'Syne', sans-serif;
    color: #eaf2ff;
    font-size: 1rem;
    margin-bottom: 8px;
}

.footer-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 24px;
    text-align: center;
}
.footer-card a {
    color: #00dc9f !important;
    text-decoration: none !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
}
.footer-icon { font-size: 1.8rem; margin-bottom: 8px; display: block; }

hr { border-color: rgba(255,255,255,0.06) !important; margin: 28px 0 !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,220,160,0.3); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── PROJECT METADATA ──────────────────────────────────────────
PROJECT_METADATA = {
    "⚙️ Advanced Process Control & Instrumentation": {
        "tagline": "PID tuning, transfer functions & sensor calibration",
        "problem": "Manual controller tuning was unreliable and time-consuming",
        "solution": "Automated PID design tools with real-time Bode/Nyquist plots",
        "tech": ["Python", "control", "sympy", "Matplotlib"],
        "outcome": "Reduced tuning time by 80%, improved system stability",
        "role": "Control Systems Developer",
        "users": "Process engineers & students",
        "color": "#00dc9f"
    },
    "🤖 Machine Learning for Process Systems": {
        "tagline": "Predictive modeling & anomaly detection for industrial processes",
        "problem": "Process faults detected too late, causing production losses",
        "solution": "ML pipeline with real-time anomaly detection & predictions",
        "tech": ["TensorFlow", "scikit-learn", "XGBoost", "Pandas"],
        "outcome": "94% fault detection accuracy, 60% faster predictions",
        "role": "ML Engineer",
        "users": "Plant operators & data scientists",
        "color": "#0096ff"
    },
    "📐 Process Optimization": {
        "tagline": "Mathematical optimization of industrial process variables",
        "problem": "Suboptimal process parameters wasted energy and materials",
        "solution": "Nonlinear optimization engine with constraint handling",
        "tech": ["Pyomo", "SciPy", "NumPy", "Plotly"],
        "outcome": "15% energy reduction, 20% yield improvement",
        "role": "Optimization Engineer",
        "users": "Chemical & process engineers",
        "color": "#a78bfa"
    },
    "🛡️ Process Safety & Risk Analytics": {
        "tagline": "HAZOP, fault tree analysis & Bayesian risk modeling",
        "problem": "Risk assessments were manual and lacked quantitative rigor",
        "solution": "Automated fault tree builder with probabilistic risk scoring",
        "tech": ["pgmpy", "networkx", "Pandas", "Matplotlib"],
        "outcome": "Identified 30+ hidden failure paths in test scenarios",
        "role": "Safety Systems Developer",
        "users": "HSE teams & process engineers",
        "color": "#fb923c"
    },
    "📊 Statistical Inference & Design of Experiments": {
        "tagline": "Hypothesis testing, ANOVA & DOE for process improvement",
        "problem": "Experimental design was ad-hoc with no statistical rigor",
        "solution": "Full DOE suite with response surface methodology",
        "tech": ["statsmodels", "pingouin", "pyDOE2", "SciPy"],
        "outcome": "Reduced experiments needed by 40% via optimal DOE",
        "role": "Statistician & Data Analyst",
        "users": "R&D teams & quality engineers",
        "color": "#f472b6"
    },
}

# ── Project suite → module mapping ────────────────────────────
PROJECT_SUITES = {
    "⚙️ Advanced Process Control & Instrumentation":    "Advanced_Process_Control.Modules.main1",
    "🤖 Machine Learning for Process Systems":           "Machine_Learning_for_Process_Systems.Modules.main5",
    "📐 Process Optimization":                           "Process_Optimization.Modules.main3",
    "🛡️ Process Safety & Risk Analytics":               "Process_Safety_Risk_Analytics.Modules.main4",
    "📊 Statistical Inference & Design of Experiments":  "Statistical_Inference_DOE.modules.main2",
}

# ── Project root path ─────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# ── Database Setup ────────────────────────────────────────────
DB_FILE = os.path.join(PROJECT_ROOT, "semester2_results.db")


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            project   TEXT,
            parameter TEXT,
            value     TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            project    TEXT,
            session_id TEXT,
            timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            tool          TEXT,
            feedback_text TEXT,
            rating        INTEGER DEFAULT 0,
            timestamp     DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_results_to_db(project, results: dict, input_data: dict = None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for k, v in results.items():
        c.execute("INSERT INTO results (project, parameter, value) VALUES (?,?,?)",
                  (project, str(k), str(v)))
    if input_data:
        for k, v in input_data.items():
            c.execute("INSERT INTO results (project, parameter, value) VALUES (?,?,?)",
                      (project, f"[INPUT] {k}", str(v)))
    conn.commit()
    conn.close()


def log_access(project_name):
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO analytics (project, session_id) VALUES (?,?)",
              (project_name, st.session_state['session_id']))
    conn.commit()
    conn.close()


def get_popular(limit=3):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(
        "SELECT project, COUNT(*) as n FROM analytics GROUP BY project ORDER BY n DESC LIMIT ?",
        conn, params=(limit,)
    )
    conn.close()
    return df['project'].tolist() if not df.empty else []


def get_analytics():
    conn = sqlite3.connect(DB_FILE)
    try:
        total  = pd.read_sql_query("SELECT COUNT(*) as n FROM analytics", conn).iloc[0]['n']
        fb     = pd.read_sql_query("SELECT COUNT(*) as n FROM feedback", conn).iloc[0]['n']
        res    = pd.read_sql_query("SELECT COUNT(*) as n FROM results", conn).iloc[0]['n']
        top_df = pd.read_sql_query(
            "SELECT project, COUNT(*) as n FROM analytics GROUP BY project ORDER BY n DESC LIMIT 1", conn
        )
        top = top_df.iloc[0]['project'] if not top_df.empty else "—"
    except Exception:
        total, fb, res, top = 0, 0, 0, "—"
    conn.close()
    return total, fb, res, top


def load_results(project=None):
    conn = sqlite3.connect(DB_FILE)
    if project:
        df = pd.read_sql_query(
            "SELECT parameter, value, timestamp FROM results WHERE project=? ORDER BY timestamp DESC",
            conn, params=(project,)
        )
    else:
        df = pd.read_sql_query(
            "SELECT project, parameter, value, timestamp FROM results ORDER BY timestamp DESC", conn
        )
    conn.close()
    return df


init_db()

# ── LOADING SCREEN ────────────────────────────────────────────
if "loaded" not in st.session_state:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                min-height:70vh;text-align:center;padding:40px;">
        <p style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;
                  color:#00dc9f;letter-spacing:4px;text-transform:uppercase;margin-bottom:20px;">
            INITIALIZING
        </p>
        <h1 style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;
                   color:#eaf2ff;letter-spacing:-1.5px;margin:0 0 8px;">
            Semester 2<br><span style="color:#00dc9f;">Engineering Hub</span>
        </h1>
        <p style="color:rgba(208,218,232,0.4);font-size:0.9rem;margin-bottom:40px;">
            Advanced Process Engineering &nbsp;·&nbsp; Ved Thakur &nbsp;·&nbsp; IPS Academy
        </p>
    </div>
    """, unsafe_allow_html=True)
    pb  = st.progress(0)
    txt = st.empty()
    modules_loading = [
        "Advanced Process Control",
        "Machine Learning Pipeline",
        "Optimization Engine",
        "Safety Risk Models",
        "Statistical Inference",
    ]
    for i in range(100):
        pb.progress(i + 1)
        mod_label = modules_loading[min(i // 20, len(modules_loading) - 1)]
        txt.markdown(
            f"<p style='text-align:center;font-family:JetBrains Mono,monospace;"
            f"font-size:0.75rem;color:#00dc9f;'>Loading {mod_label}... {i+1}%</p>",
            unsafe_allow_html=True
        )
        time.sleep(0.010)
    txt.empty()
    pb.empty()
    st.session_state["loaded"] = True
    time.sleep(0.3)
    st.rerun()

# ── LANDING SCREEN ────────────────────────────────────────────
if "landing_done" not in st.session_state:
    st.session_state["landing_done"] = False

if not st.session_state["landing_done"]:

    st.markdown("""
    <div class="hero-wrap">
        <p class="hero-eyebrow">// IPS Academy &nbsp;·&nbsp; Semester 2 &nbsp;·&nbsp; 2025</p>
        <h1 class="hero-name">Ved <span>Thakur</span></h1>
        <p class="hero-subtitle">
            Advanced Process Engineering Portfolio &nbsp;—&nbsp; 5 Integrated Project Suites
        </p>
        <div class="hero-chips">
            <span class="hero-chip">Process Control</span>
            <span class="hero-chip">Machine Learning</span>
            <span class="hero-chip">Optimization</span>
            <span class="hero-chip">Risk Analytics</span>
            <span class="hero-chip">Statistics &amp; DOE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    for col, (val, lbl) in zip(
        [col1, col2, col3, col4],
        [("5", "Project Suites"), ("3000+", "Lines of Code"),
         ("94%", "ML Accuracy"), ("40%", "Experiments Saved")]
    ):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val">{val}</div>
                <div class="stat-lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<p class="sec-title">Project Suites Overview</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">// Semester 2 core engineering subjects</p>', unsafe_allow_html=True)

    for name, meta in PROJECT_METADATA.items():
        tech_tags = "".join(f'<span class="proj-tag">{t}</span>' for t in meta["tech"])
        st.markdown(f"""
        <div class="proj-card">
            <p class="proj-title">{name}</p>
            <p style="color:rgba(208,218,232,0.55);font-size:0.85rem;margin:4px 0 10px;">
                {meta['tagline']}
            </p>
            <p style="font-size:0.82rem;color:rgba(208,218,232,0.4);margin-bottom:10px;">
                <strong style="color:rgba(208,218,232,0.65);">Outcome:</strong> {meta['outcome']}
            </p>
            {tech_tags}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown("""
        <div class="info-block">
        <h3>🌟 About This Portfolio</h3>
        <p style="color:rgba(208,218,232,0.65);font-size:0.9rem;line-height:1.7;">
        This Semester 2 hub integrates five advanced engineering disciplines into a single
        Streamlit platform. Each suite is independently executable and outputs structured
        results with CSV/PDF export. All runs are logged to a local SQLite database for
        session analytics and reproducibility.
        </p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        with st.expander("📖 Quick Start", expanded=True):
            st.markdown("""
            1. Click **Enter Hub** below
            2. Select a project from the sidebar
            3. Optionally upload CSV / Excel data
            4. Click **Run** to execute the module
            5. Download results as **CSV or PDF**
            6. Check **Analytics** to track usage

            > ⚡ Use **Run All** to batch-execute all 5 suites
            """)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⚡ Enter Hub", use_container_width=True):
            st.session_state["landing_done"] = True
            st.rerun()
    with col2:
        st.link_button("📧 Email Me", "mailto:vedthakursa@gmail.com", use_container_width=True)
    with col3:
        st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/ved-thakur-0b79bb36a/", use_container_width=True)

    st.stop()


# ── MAIN APPLICATION ──────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;padding-bottom:20px;
            border-bottom:1px solid rgba(255,255,255,0.06);">
    <span style="font-size:2.2rem;">⚗️</span>
    <div>
        <p style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;
                  color:#eaf2ff;margin:0;letter-spacing:-0.5px;">Semester 2 Engineering Hub</p>
        <p style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#00dc9f;
                  margin:0;letter-spacing:2px;text-transform:uppercase;opacity:0.75;">
            // 5 Advanced Project Suites &nbsp;·&nbsp; Ved Thakur &nbsp;·&nbsp; IPS Academy
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align:center;padding:18px 0 10px;">
    <p style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#00dc9f;
              letter-spacing:3px;text-transform:uppercase;margin-bottom:6px;">// SEMESTER 2</p>
    <p style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:800;
              color:#eaf2ff;margin:0;letter-spacing:-0.5px;">Engineering Hub</p>
    <p style="font-size:0.72rem;color:rgba(208,218,232,0.35);margin:4px 0 0;">
        Ved Thakur &nbsp;·&nbsp; IPS Academy</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

view_mode = st.sidebar.radio(
    "Navigate",
    ["⚡ Quick Access", "🎯 Project Gallery", "📊 Database", "📈 Analytics"],
    index=0
)
st.sidebar.markdown("---")

choice  = None
run_all = False

# ── QUICK ACCESS ──────────────────────────────────────────────
if view_mode == "⚡ Quick Access":
    st.sidebar.markdown(
        "<p style='font-size:0.72rem;color:#00dc9f;letter-spacing:2px;"
        "text-transform:uppercase;font-family:JetBrains Mono,monospace;'>Select Suite</p>",
        unsafe_allow_html=True
    )
    default_idx = 0
    if 'selected_project' in st.session_state:
        keys = list(PROJECT_SUITES.keys())
        if st.session_state['selected_project'] in keys:
            default_idx = keys.index(st.session_state['selected_project'])

    choice  = st.sidebar.selectbox("Choose a Suite", list(PROJECT_SUITES.keys()), index=default_idx)
    run_all = st.sidebar.button("▶ Run All 5 Suites", use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<p style='font-size:0.72rem;color:#00dc9f;letter-spacing:2px;"
        "text-transform:uppercase;font-family:JetBrains Mono,monospace;'>🔥 Most Visited</p>",
        unsafe_allow_html=True
    )
    popular = get_popular()
    if popular:
        for p in popular:
            st.sidebar.markdown(
                f"<p style='font-size:0.8rem;color:rgba(208,218,232,0.55);margin:3px 0;'>▸ {p}</p>",
                unsafe_allow_html=True
            )
    else:
        st.sidebar.caption("Run a project to see stats")

# ── PROJECT GALLERY ───────────────────────────────────────────
elif view_mode == "🎯 Project Gallery":
    st.markdown('<p class="sec-title">🎯 Project Gallery</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">// Browse all 5 Semester 2 project suites</p>', unsafe_allow_html=True)

    search = st.text_input("🔍 Search", placeholder="e.g. control, ML, risk, statistics...")

    filtered = {
        k: v for k, v in PROJECT_METADATA.items()
        if not search
        or search.lower() in k.lower()
        or search.lower() in v['tagline'].lower()
        or any(search.lower() in t.lower() for t in v['tech'])
    }

    if not filtered:
        st.warning("No matching projects found.")
    else:
        for idx, (name, meta) in enumerate(filtered.items()):
            with st.expander(f"{name}  ·  {meta['tagline']}", expanded=False):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**🔎 Problem:** {meta['problem']}")
                    st.markdown(f"**💡 Solution:** {meta['solution']}")
                    st.markdown(f"**📈 Outcome:** {meta['outcome']}")
                    tags = "".join(f'<span class="proj-tag">{t}</span>' for t in meta['tech'])
                    st.markdown(f"**🛠 Tech:** {tags}", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**👤 Role:** {meta['role']}")
                    st.markdown(f"**👥 Users:** {meta['users']}")
                    if name in PROJECT_SUITES:
                        if st.button("▶ Run", key=f"g_{idx}", use_container_width=True):
                            st.session_state['selected_project'] = name
                            st.rerun()

    st.sidebar.info("💡 Search or expand a card to run analysis.")

# ── DATABASE VIEWER ───────────────────────────────────────────
elif view_mode == "📊 Database":
    st.markdown('<p class="sec-title">📊 Database Viewer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">// All stored results &amp; feedback</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 All Results", "💬 Feedback", "🔍 Filter by Project"])

    with tab1:
        df_all = load_results()
        if not df_all.empty:
            st.dataframe(df_all, use_container_width=True, height=420)
            st.download_button("📥 Export CSV", df_all.to_csv(index=False).encode(),
                               "semester2_results.csv", "text/csv")
        else:
            st.info("No results yet — run a project first.")

    with tab2:
        conn = sqlite3.connect(DB_FILE)
        try:
            df_fb = pd.read_sql_query(
                "SELECT tool, rating, feedback_text, timestamp FROM feedback ORDER BY timestamp DESC", conn
            )
        except Exception:
            df_fb = pd.DataFrame()
        conn.close()
        if not df_fb.empty:
            st.dataframe(df_fb, use_container_width=True, height=300)
        else:
            st.info("No feedback yet.")

    with tab3:
        pf = st.selectbox("Project:", ["All"] + list(PROJECT_SUITES.keys()))
        if pf != "All":
            dff = load_results(project=pf)
            if not dff.empty:
                st.dataframe(dff, use_container_width=True)
                st.download_button(
                    f"📥 Export {pf}",
                    dff.to_csv(index=False).encode(),
                    f"{pf.replace(' ','_')}_results.csv",
                    "text/csv"
                )
            else:
                st.info(f"No data for '{pf}' yet.")

# ── ANALYTICS ─────────────────────────────────────────────────
elif view_mode == "📈 Analytics":
    st.markdown('<p class="sec-title">📈 Usage Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">// Platform engagement &amp; session statistics</p>', unsafe_allow_html=True)

    total, fb, res, top = get_analytics()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Accesses", total)
    m2.metric("Results Stored", res)
    m3.metric("Feedback Count", fb)
    m4.metric("Top Project", str(top)[:25] + "…" if len(str(top)) > 25 else str(top))

    conn = sqlite3.connect(DB_FILE)
    try:
        df_an = pd.read_sql_query(
            "SELECT project, COUNT(*) as visits FROM analytics GROUP BY project ORDER BY visits DESC", conn
        )
    except Exception:
        df_an = pd.DataFrame()
    conn.close()

    if not df_an.empty:
        st.markdown("#### Visit Distribution")
        fig, ax = plt.subplots(figsize=(9, 3.5))
        fig.patch.set_facecolor('#060a10')
        ax.set_facecolor('#060a10')

        bar_colors = ['#00dc9f', '#0096ff', '#a78bfa', '#fb923c', '#f472b6']
        bars = ax.barh(
            df_an['project'], df_an['visits'],
            color=bar_colors[:len(df_an)], height=0.55
        )
        ax.set_xlabel("Visits", color='#6b8099', fontsize=9)
        ax.tick_params(colors='#6b8099', labelsize=8)

        # ✅ FIX: use tuple (R,G,B,A) instead of CSS rgba() string
        for spine in ax.spines.values():
            spine.set_edgecolor((1.0, 1.0, 1.0, 0.05))

        for bar in bars:
            ax.text(
                bar.get_width() + 0.1,
                bar.get_y() + bar.get_height() / 2,
                str(int(bar.get_width())),
                va='center', color='#6b8099', fontsize=8
            )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Run some projects to populate analytics.")

# ── SIDEBAR CONTROLS ──────────────────────────────────────────
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Session", use_container_width=True):
    st.session_state.clear()
    st.rerun()
st.sidebar.markdown("""
<div style="text-align:center;padding:14px 0 6px;">
    <p style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
              color:rgba(208,218,232,0.25);line-height:1.8;">
        Semester 2 &nbsp;·&nbsp; IPS Academy<br>
        <strong style="color:rgba(208,218,232,0.4);">Ved Thakur</strong>
    </p>
</div>
""", unsafe_allow_html=True)

# ── FILE UPLOAD ───────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='font-size:0.72rem;color:#00dc9f;letter-spacing:2px;"
    "text-transform:uppercase;font-family:JetBrains Mono,monospace;margin-bottom:8px;'>📤 Upload Data</p>",
    unsafe_allow_html=True
)
uploaded_file = st.sidebar.file_uploader(
    "CSV, Excel, or Image",
    type=["csv", "xlsx", "png", "jpg", "jpeg"],
    label_visibility="collapsed"
)
uploaded_data = None
if uploaded_file:
    ftype = uploaded_file.type
    try:
        if ftype == "text/csv":
            uploaded_data = pd.read_csv(uploaded_file)
            st.sidebar.success("✅ CSV loaded")
            with st.sidebar.expander("Preview"):
                st.write(uploaded_data.head())
        elif "excel" in ftype or uploaded_file.name.endswith(".xlsx"):
            uploaded_data = pd.read_excel(uploaded_file)
            st.sidebar.success("✅ Excel loaded")
            with st.sidebar.expander("Preview"):
                st.write(uploaded_data.head())
        elif "image" in ftype:
            uploaded_data = Image.open(uploaded_file)
            st.sidebar.success("✅ Image loaded")
            st.sidebar.image(uploaded_data, use_column_width=True)
    except Exception as e:
        st.sidebar.error(f"❌ {e}")


# ── MODULE LOADER ─────────────────────────────────────────────
@st.cache_resource
def load_module(module_path):
    return importlib.import_module(module_path)


# ── PROJECT RUNNER ────────────────────────────────────────────
def run_project(display_name, module_path):
    log_access(display_name)

    with st.expander(f"📌 {display_name}", expanded=True):
        if display_name in PROJECT_METADATA:
            meta = PROJECT_METADATA[display_name]
            tags = "".join(f'<span class="proj-tag">{t}</span>' for t in meta['tech'])
            st.markdown(
                f"<div style='margin-bottom:14px;'>"
                f"<span style='color:rgba(208,218,232,0.55);font-size:0.85rem;'>{meta['tagline']}</span><br>"
                f"<div style='margin-top:6px;'>{tags}</div></div>",
                unsafe_allow_html=True
            )

        try:
            module = load_module(module_path)

            if not (hasattr(module, "run") and callable(module.run)):
                st.warning(f"⚠️ No `run()` function found in `{module_path}`")
                return

            st.markdown(
                f"<p style='font-family:JetBrains Mono,monospace;font-size:0.75rem;"
                f"color:#00dc9f;letter-spacing:1.5px;text-transform:uppercase;'>"
                f"▶ Executing {display_name}</p>",
                unsafe_allow_html=True
            )

            with st.spinner("Processing..."):
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    params = inspect.signature(module.run).parameters
                    result_data = (
                        module.run(uploaded_data=uploaded_data)
                        if "uploaded_data" in params
                        else module.run()
                    )
                printed = buf.getvalue().strip()

            input_data, results, graphs = {}, {}, []

            if isinstance(result_data, tuple):
                if len(result_data) == 2:
                    input_data, results = result_data
                elif len(result_data) == 3:
                    input_data, results, graphs = result_data
            elif isinstance(result_data, dict):
                results = result_data

            if printed:
                results["Console Output"] = printed

            if results:
                if "all_results" not in st.session_state:
                    st.session_state["all_results"] = {}
                st.session_state["all_results"][display_name] = results
                save_results_to_db(display_name, results, input_data)

                st.markdown(
                    "<p style='font-family:JetBrains Mono,monospace;font-size:0.72rem;"
                    "color:#00dc9f;letter-spacing:2px;text-transform:uppercase;"
                    "margin-top:16px;margin-bottom:8px;'>// Results</p>",
                    unsafe_allow_html=True
                )
                for key, value in results.items():
                    st.markdown(
                        f'<div class="res-item"><strong>{key}:</strong> <code>{value}</code></div>',
                        unsafe_allow_html=True
                    )

            if graphs:
                st.markdown(
                    "<p style='font-family:JetBrains Mono,monospace;font-size:0.72rem;"
                    "color:#00dc9f;letter-spacing:2px;text-transform:uppercase;"
                    "margin-top:16px;margin-bottom:8px;'>// Visualizations</p>",
                    unsafe_allow_html=True
                )
                for g in graphs:
                    if isinstance(g, plt.Figure):
                        st.pyplot(g)
                    elif isinstance(g, Image.Image):
                        st.image(g)

            # ── Downloads ─────────────────────────────────────
            if results:
                st.markdown("---")
                dl1, dl2 = st.columns(2)

                with dl1:
                    df_exp = pd.DataFrame(list(results.items()), columns=["Parameter", "Value"])
                    st.download_button(
                        "📥 Download CSV",
                        data=df_exp.to_csv(index=False).encode(),
                        file_name=f"{display_name.replace(' ','_')}_results.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                with dl2:
                    pdf_buf = io.BytesIO()
                    cv = canvas.Canvas(pdf_buf, pagesize=letter)
                    W, H = letter

                    # Header bar
                    cv.setFillColorRGB(0.0, 0.86, 0.62)
                    cv.rect(0, H - 72, W, 72, fill=True, stroke=False)
                    cv.setFillColorRGB(0.02, 0.04, 0.08)
                    cv.setFont("Helvetica-Bold", 16)
                    safe_name = display_name.encode('ascii', errors='ignore').decode().strip()
                    cv.drawString(40, H - 36, safe_name or "Project Results")
                    cv.setFont("Helvetica", 8)
                    cv.drawString(40, H - 54,
                                  f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    cv.drawString(40, H - 65,
                                  "Semester 2 Engineering Hub  |  Ved Thakur  |  IPS Academy")

                    # Results body
                    y = H - 100
                    cv.setFillColorRGB(0.12, 0.14, 0.17)
                    cv.setFont("Helvetica-Bold", 11)
                    cv.drawString(40, y, "Analysis Results")
                    y -= 18
                    cv.setFont("Helvetica", 9.5)
                    cv.setFillColorRGB(0.2, 0.25, 0.3)
                    for k, v in results.items():
                        line = f"{k}: {v}".encode('ascii', errors='ignore').decode()
                        if len(line) > 100:
                            line = line[:97] + "..."
                        cv.drawString(50, y, line)
                        y -= 16
                        if y < 60:
                            cv.showPage()
                            y = H - 60

                    # Footer bar
                    cv.setFillColorRGB(0.0, 0.86, 0.62)
                    cv.rect(0, 0, W, 24, fill=True, stroke=False)
                    cv.setFillColorRGB(0.02, 0.04, 0.08)
                    cv.setFont("Helvetica", 7.5)
                    cv.drawString(40, 8,
                                  "Developed by Ved Thakur  |  IPS Academy Semester 2  |  Advanced Process Engineering")

                    cv.save()
                    pdf_buf.seek(0)
                    st.download_button(
                        "📄 Download PDF",
                        data=pdf_buf,
                        file_name=f"{display_name.replace(' ','_')}_results.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

        except ModuleNotFoundError:
            st.error(f"❌ Module not found: `{module_path}`")
            st.info("💡 Check folder names, `__init__.py` files, and module path spelling.")
        except Exception:
            st.error(f"❌ Error in `{display_name}`")
            with st.expander("🔍 Traceback"):
                st.code(traceback.format_exc(), language="python")

    st.markdown("---")


# ── EXECUTE ───────────────────────────────────────────────────
if view_mode == "⚡ Quick Access":
    if run_all:
        st.markdown('<p class="sec-title">▶ Running All 5 Suites</p>', unsafe_allow_html=True)
        pb = st.progress(0, text="Starting...")
        total_suites = len(PROJECT_SUITES)
        for i, (dname, mpath) in enumerate(PROJECT_SUITES.items()):
            pb.progress((i + 1) / total_suites, text=f"Running: {dname}")
            run_project(dname, mpath)
        pb.empty()
        st.success("✅ All 5 suites executed successfully!")
    elif choice:
        st.session_state['selected_project'] = choice
        run_project(choice, PROJECT_SUITES[choice])


# ── FEEDBACK ──────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="sec-title">💬 Feedback</p>', unsafe_allow_html=True)
st.markdown('<p class="sec-sub">// Help improve these tools</p>', unsafe_allow_html=True)

fb_c1, fb_c2 = st.columns([3, 1])
with fb_c1:
    feedback = st.text_area(
        "Your feedback:",
        placeholder="Suggestions, bugs, improvements, or general thoughts...",
        height=100,
        label_visibility="collapsed"
    )
    rating = st.select_slider(
        "Rating",
        options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        value="⭐⭐⭐⭐⭐"
    )
with fb_c2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("📤 Submit", use_container_width=True):
        if feedback.strip():
            conn = sqlite3.connect(DB_FILE)
            c_cur = conn.cursor()
            c_cur.execute(
                "INSERT INTO feedback (tool, feedback_text, rating) VALUES (?,?,?)",
                (st.session_state.get('selected_project', 'General'), feedback, len(rating))
            )
            conn.commit()
            conn.close()
            st.success(f"✅ Thanks! ({rating})")
            time.sleep(1)
            st.rerun()
        else:
            st.warning("⚠️ Please write something first.")


# ── FOOTER ────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<p style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#00dc9f;
          letter-spacing:3px;text-transform:uppercase;text-align:center;margin-bottom:20px;">
    // Let's Connect
</p>
""", unsafe_allow_html=True)

fc1, fc2, fc3 = st.columns(3)
with fc1:
    st.markdown("""
    <div class="footer-card">
        <span class="footer-icon">📧</span>
        <strong style="color:#eaf2ff;font-size:0.85rem;">Email</strong><br>
        <a href="mailto:vedthakursa@gmail.com">vedthakursa@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)
with fc2:
    st.markdown("""
    <div class="footer-card">
        <span class="footer-icon">💼</span>
        <strong style="color:#eaf2ff;font-size:0.85rem;">LinkedIn</strong><br>
        <a href="https://www.linkedin.com/in/ved-thakur-0b79bb36a/" target="_blank">Connect &#8594;</a>
    </div>
    """, unsafe_allow_html=True)
with fc3:
    st.markdown("""
    <div class="footer-card">
        <span class="footer-icon">🔗</span>
        <strong style="color:#eaf2ff;font-size:0.85rem;">GitHub</strong><br>
        <a href="https://github.com/vedthakurchemE" target="_blank">View Projects &#8594;</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:32px;padding-bottom:10px;">
    <p style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
              color:rgba(208,218,232,0.2);letter-spacing:1px;">
        DEVELOPED BY &nbsp;
        <strong style="color:rgba(208,218,232,0.4);">VED THAKUR</strong>
        &nbsp;·&nbsp; SEMESTER 2 &nbsp;·&nbsp; IPS ACADEMY &nbsp;·&nbsp;
        BUILT WITH PYTHON &amp; STREAMLIT
    </p>
</div>
""", unsafe_allow_html=True)