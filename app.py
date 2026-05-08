import streamlit as st
import pandas as pd
import joblib
import os
import random
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="CYBER-FRAUD DETECTOR | TCC VITOR", layout="wide", page_icon="🛡️")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background-color: #010b14 !important;
    color: #a8d8ea !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Scanline overlay */
.stApp::before {
    content: "";
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,255,180,0.015) 2px, rgba(0,255,180,0.015) 4px
    );
    pointer-events: none; z-index: 9999;
}

/* Grid background */
.stApp::after {
    content: "";
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(0,255,180,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,180,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none; z-index: 0;
    animation: gridScroll 20s linear infinite;
}

@keyframes gridScroll {
    0%   { background-position: 0 0; }
    100% { background-position: 40px 40px; }
}

/* ── HIDE STREAMLIT WARNINGS / DEPRECATIONS ── */
div[data-testid="stAlert"],
div[class*="stDeprecationWarning"],
div[class*="deprecation"],
[data-testid="stWarning"] {
    display: none !important;
}

/* ── HEADINGS ── */
h1 {
    font-family: 'Orbitron', monospace !important;
    font-size: 2.4rem !important; font-weight: 900 !important;
    color: #00ffe7 !important;
    text-shadow: 0 0 10px #00ffe7, 0 0 30px #00ffe7, 0 0 60px rgba(0,255,231,0.4) !important;
    letter-spacing: 0.12em !important;
    animation: flicker 6s infinite;
}
h2, h3 {
    font-family: 'Orbitron', monospace !important;
    color: #00ffe7 !important;
    text-shadow: 0 0 8px rgba(0,255,231,0.6) !important;
    letter-spacing: 0.08em !important;
}

@keyframes flicker {
    0%,95%,100%{opacity:1} 96%{opacity:0.7} 97%{opacity:1} 98%{opacity:0.5} 99%{opacity:1}
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#020f1c 0%,#010b14 100%) !important;
    border-right: 1px solid rgba(0,255,231,0.25) !important;
}
section[data-testid="stSidebar"] * {
    font-family: 'Share Tech Mono', monospace !important;
}

/* ── SIDEBAR RADIO ── */
.stRadio > div {
    gap: 8px !important;
    display: flex !important;
    flex-direction: column !important;
}
.stRadio label {
    display: flex !important;
    align-items: center !important;
    background: rgba(0,255,231,0.04) !important;
    border: 1px solid rgba(0,255,231,0.25) !important;
    border-radius: 3px !important;
    padding: 12px 14px !important;
    color: #7fffd4 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.07em !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stRadio label:hover {
    background: rgba(0,255,231,0.1) !important;
    border-color: #00ffe7 !important;
    color: #00ffe7 !important;
    text-shadow: 0 0 8px #00ffe7 !important;
    box-shadow: 0 0 12px rgba(0,255,231,0.2) !important;
}
.stRadio input[type="radio"] {
    accent-color: #00ffe7 !important;
    width: 14px !important; height: 14px !important;
    margin-right: 10px !important;
    flex-shrink: 0 !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg,#041828 0%,#021018 100%) !important;
    border: 1px solid rgba(0,255,231,0.2) !important;
    border-radius: 4px !important;
    padding: 16px 20px !important;
    position: relative !important; overflow: hidden !important;
    box-shadow: 0 0 20px rgba(0,255,231,0.06), inset 0 1px 0 rgba(0,255,231,0.1) !important;
}
[data-testid="stMetric"]::before {
    content:""; position:absolute; top:0; left:0;
    width:3px; height:100%;
    background: linear-gradient(180deg,#00ffe7,transparent);
}
[data-testid="stMetricLabel"] {
    color:#5eead4 !important;
    font-family:'Share Tech Mono',monospace !important;
    font-size:0.7rem !important; letter-spacing:0.1em !important;
}
[data-testid="stMetricValue"] {
    color:#00ffe7 !important;
    font-family:'Orbitron',monospace !important;
    font-size:1.5rem !important;
    text-shadow:0 0 12px rgba(0,255,231,0.5) !important;
}

/* ── BUTTONS (default cyan) ── */
.stButton > button {
    background: transparent !important;
    color: #00ffe7 !important;
    border: 1px solid rgba(0,255,231,0.6) !important;
    border-radius: 2px !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.72rem !important; font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    padding: 11px 10px !important;
    transition: all 0.25s !important;
    text-transform: uppercase !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: rgba(0,255,231,0.1) !important;
    box-shadow: 0 0 16px rgba(0,255,231,0.4) !important;
    text-shadow: 0 0 8px #00ffe7 !important;
    border-color: #00ffe7 !important;
}
.btn-fraud .stButton > button {
    color: #ff4466 !important;
    border-color: rgba(255,50,80,0.7) !important;
}
.btn-fraud .stButton > button:hover {
    background: rgba(255,30,60,0.12) !important;
    box-shadow: 0 0 16px rgba(255,30,60,0.45) !important;
    text-shadow: 0 0 8px #ff1e3c !important;
    border-color: #ff1e3c !important;
}
.btn-normal .stButton > button {
    color: #00e85a !important;
    border-color: rgba(0,220,90,0.6) !important;
}
.btn-normal .stButton > button:hover {
    background: rgba(0,255,100,0.1) !important;
    box-shadow: 0 0 16px rgba(0,255,100,0.4) !important;
    text-shadow: 0 0 8px #00ff64 !important;
    border-color: #00ff64 !important;
}
.btn-random .stButton > button {
    color: #ffd700 !important;
    border-color: rgba(255,215,0,0.55) !important;
}
.btn-random .stButton > button:hover {
    background: rgba(255,215,0,0.08) !important;
    box-shadow: 0 0 16px rgba(255,215,0,0.35) !important;
    text-shadow: 0 0 8px #ffd700 !important;
    border-color: #ffd700 !important;
}
/* Manual button — same cyan as default but explicit */
.btn-manual .stButton > button {
    color: #00ffe7 !important;
    border-color: rgba(0,255,231,0.6) !important;
}
.btn-manual .stButton > button:hover {
    background: rgba(0,255,231,0.1) !important;
    box-shadow: 0 0 16px rgba(0,255,231,0.4) !important;
    text-shadow: 0 0 8px #00ffe7 !important;
    border-color: #00ffe7 !important;
}

/* ── INPUTS ── */
input[type="number"], input[type="text"] {
    background: #020f1c !important;
    color: #00ffe7 !important;
    border: 1px solid rgba(0,255,231,0.3) !important;
    border-radius: 2px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
input[type="number"]:focus {
    border-color: #00ffe7 !important;
    box-shadow: 0 0 12px rgba(0,255,231,0.3) !important;
}
.stNumberInput label {
    color: #5eead4 !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ── FORM ── */
[data-testid="stForm"] {
    background: linear-gradient(135deg,#041828 0%,#020f1c 100%) !important;
    border: 1px solid rgba(0,255,231,0.15) !important;
    border-radius: 4px !important;
    padding: 24px !important;
    box-shadow: 0 0 40px rgba(0,255,231,0.04) !important;
}

/* ── RESULT CARDS ── */
.threat-card {
    background: linear-gradient(135deg,rgba(255,30,60,0.1) 0%,rgba(2,15,28,0.9) 100%);
    border: 1px solid rgba(255,30,60,0.4); border-left: 3px solid #ff1e3c;
    border-radius: 4px; padding: 24px; text-align: center;
    box-shadow: 0 0 30px rgba(255,30,60,0.15);
    animation: threatPulse 1.5s infinite;
}
.safe-card {
    background: linear-gradient(135deg,rgba(0,255,100,0.07) 0%,rgba(2,15,28,0.9) 100%);
    border: 1px solid rgba(0,255,100,0.35); border-left: 3px solid #00ff64;
    border-radius: 4px; padding: 24px; text-align: center;
    box-shadow: 0 0 30px rgba(0,255,100,0.1);
}
@keyframes threatPulse {
    0%,100%{box-shadow:0 0 30px rgba(255,30,60,0.15)}
    50%{box-shadow:0 0 50px rgba(255,30,60,0.35)}
}
.threat-title{font-family:'Orbitron',monospace;font-size:1.2rem;color:#ff1e3c;text-shadow:0 0 12px #ff1e3c;}
.safe-title{font-family:'Orbitron',monospace;font-size:1.2rem;color:#00ff64;text-shadow:0 0 12px #00ff64;}
.prob-value{font-family:'Orbitron',monospace;font-size:2.2rem;font-weight:900;margin:10px 0;}
.prob-threat{color:#ff1e3c;text-shadow:0 0 20px #ff1e3c;}
.prob-safe{color:#00ff64;text-shadow:0 0 20px #00ff64;}

/* ── MISC ── */
.section-header {
    font-family:'Orbitron',monospace; font-size:0.7rem;
    color:rgba(0,255,231,0.5); letter-spacing:0.2em; text-transform:uppercase;
    border-bottom:1px solid rgba(0,255,231,0.1); padding-bottom:8px; margin-bottom:16px;
}
.status-bar{display:flex;align-items:center;gap:8px;font-size:0.75rem;color:#5eead4;letter-spacing:0.08em;margin-bottom:4px;}
.status-dot{width:8px;height:8px;border-radius:50%;background:#00ff64;box-shadow:0 0 6px #00ff64;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{box-shadow:0 0 6px #00ff64}50%{box-shadow:0 0 14px #00ff64,0 0 28px rgba(0,255,100,0.4)}}
.cyber-badge{display:inline-block;background:rgba(0,255,231,0.08);border:1px solid rgba(0,255,231,0.3);color:#00ffe7;font-size:0.7rem;letter-spacing:0.12em;padding:3px 10px;border-radius:2px;margin-right:6px;text-shadow:0 0 6px rgba(0,255,231,0.5);}
.preset-label{font-size:0.65rem;color:rgba(0,255,231,0.45);letter-spacing:0.18em;text-transform:uppercase;margin-bottom:6px;font-family:'Share Tech Mono',monospace;}

/* ── README CARDS ── */
.readme-block {
    background: linear-gradient(135deg, #041828 0%, #021018 100%);
    border: 1px solid rgba(0,255,231,0.13);
    border-left: 3px solid #00ffe7;
    border-radius: 4px;
    padding: 20px 24px;
    margin-bottom: 14px;
    line-height: 1.85;
    font-size: 0.86rem;
    color: #a8d8ea;
}
.readme-block .block-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    color: #00ffe7;
    text-shadow: 0 0 6px rgba(0,255,231,0.5);
    margin-bottom: 10px;
}
.readme-block.red  { border-left-color: #ff1e3c; }
.readme-block.red .block-title { color: #ff4466; text-shadow: 0 0 6px rgba(255,30,60,0.5); }
.readme-block.green{ border-left-color: #00ff64; }
.readme-block.green .block-title { color: #00e85a; text-shadow: 0 0 6px rgba(0,255,100,0.5); }
.readme-block.yellow{ border-left-color: #ffd700; }
.readme-block.yellow .block-title { color: #ffd700; text-shadow: 0 0 6px rgba(255,215,0,0.5); }

.tag {
    display: inline-block;
    background: rgba(0,255,231,0.08);
    border: 1px solid rgba(0,255,231,0.25);
    color: #00ffe7;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    padding: 2px 9px;
    border-radius: 2px;
    margin: 2px 3px 2px 0;
}
.tag.red    { background:rgba(255,30,60,0.08);  border-color:rgba(255,30,60,0.3);  color:#ff4466; }
.tag.green  { background:rgba(0,255,100,0.07);  border-color:rgba(0,255,100,0.3);  color:#00e85a; }
.tag.yellow { background:rgba(255,215,0,0.07);  border-color:rgba(255,215,0,0.3);  color:#ffd700; }

.pipeline-row {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
    margin: 14px 0 4px;
}
.pipeline-step {
    background: rgba(0,255,231,0.07);
    border: 1px solid rgba(0,255,231,0.25);
    color: #00ffe7;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    padding: 6px 14px;
    border-radius: 2px;
}
.pipeline-arrow {
    color: rgba(0,255,231,0.4);
    font-size: 1rem;
}

::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:#010b14;}
::-webkit-scrollbar-thumb{background:rgba(0,255,231,0.3);border-radius:2px;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── PRESET DATA ────────────────────────────────────────────────────────────────
PRESETS = {
    "fraud": [
        {"V1":-3.0435,"V2":1.1914,"V3":-4.3012,"V4":1.9781,"V5":-2.7084,
         "V6":-0.9498,"V7":-3.8415,"V8":0.7151,"V9":-2.6898,"V10":-3.2128,
         "V11":2.0514,"V12":-5.3547,"V13":-0.4375,"V14":-9.9999,"V15":0.4182,
         "V16":-2.5965,"V17":-9.9999,"V18":-2.3887,"V19":0.8566,"V20":0.4079,
         "V21":0.9999,"V22":0.2208,"V23":-0.0865,"V24":0.1211,"V25":-0.3694,
         "V26":0.1699,"V27":0.7059,"V28":0.1285,"Amount":1.00,"Time":406.0},
        {"V1":-2.3122,"V2":1.9512,"V3":-1.6098,"V4":3.9979,"V5":-0.5220,
         "V6":-1.4265,"V7":-2.5374,"V8":1.3912,"V9":-2.7705,"V10":-2.7720,
         "V11":3.2020,"V12":-2.8990,"V13":-0.5955,"V14":-4.2894,"V15":0.3899,
         "V16":-1.1407,"V17":-2.8300,"V18":-0.0168,"V19":0.4162,"V20":0.3594,
         "V21":0.5498,"V22":-0.2261,"V23":-0.6383,"V24":-0.1287,"V25":-0.1885,
         "V26":0.0667,"V27":0.1285,"V28":0.0449,"Amount":239.93,"Time":0.0},
    ],
    "normal": [
        {"V1":1.1919,"V2":0.2662,"V3":0.1665,"V4":0.4482,"V5":0.0600,
         "V6":-0.0824,"V7":-0.0788,"V8":0.0851,"V9":-0.2552,"V10":-0.1660,
         "V11":1.6127,"V12":1.0652,"V13":0.4896,"V14":-0.1433,"V15":0.6353,
         "V16":0.4639,"V17":-0.1145,"V18":0.2397,"V19":-0.0597,"V20":0.1681,
         "V21":0.0259,"V22":-0.3658,"V23":-0.0435,"V24":-0.3201,"V25":0.0548,
         "V26":0.2040,"V27":0.0250,"V28":0.0139,"Amount":149.62,"Time":0.0},
        {"V1":1.9794,"V2":0.1161,"V3":1.4861,"V4":0.4479,"V5":0.1131,
         "V6":-0.1832,"V7":0.1458,"V8":0.1014,"V9":0.3589,"V10":0.0441,
         "V11":1.0798,"V12":0.5003,"V13":0.2488,"V14":0.5803,"V15":0.6281,
         "V16":0.4133,"V17":-0.2311,"V18":0.2613,"V19":0.0146,"V20":0.0809,
         "V21":0.0218,"V22":-0.3419,"V23":-0.0396,"V24":-0.3053,"V25":0.0485,
         "V26":0.1965,"V27":0.0211,"V28":0.0124,"Amount":2.69,"Time":1.0},
    ],
}

def get_random_preset():
    return random.choice(PRESETS["fraud"] + PRESETS["normal"])

# ── SESSION STATE ──────────────────────────────────────────────────────────────
if "preset_values" not in st.session_state:
    st.session_state.preset_values = None
if "preset_mode" not in st.session_state:
    st.session_state.preset_mode = "MANUAL"

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:4px;">
    <span class="cyber-badge">TCC II</span>
    <span class="cyber-badge">RF-v1.0</span>
    <span class="cyber-badge">SMOTE+SHAP</span>
</div>
""", unsafe_allow_html=True)

st.markdown("# 🛡️ CYBER-FRAUD DETECTOR")

st.markdown("""
<div class="status-bar">
    <div class="status-dot"></div>
    SYSTEM ONLINE &nbsp;|&nbsp; ALL NODES ACTIVE &nbsp;|&nbsp; THREAT MONITOR: RUNNING &nbsp;|&nbsp; DEVELOPER: VITOR &nbsp;|&nbsp; v1.0.4-STABLE
</div>
""", unsafe_allow_html=True)

st.divider()

# ── SIDEBAR ─────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align:center;padding:12px 0 20px;">
    <div style="font-family:'Orbitron',monospace;font-size:1rem;color:#00ffe7;text-shadow:0 0 10px #00ffe7;letter-spacing:0.15em;">◈ CONTROL PANEL ◈</div>
    <div style="font-size:0.65rem;color:rgba(0,255,231,0.4);letter-spacing:0.2em;margin-top:4px;">FRAUD DETECTION SYSTEM</div>
</div>
""", unsafe_allow_html=True)

opcao = st.sidebar.radio(
    "SELECT MODULE",
    ["🏠 SYSTEM OVERVIEW", "📊 DATA ANALYTICS", "🔍 FRAUD SCANNER"],
)

st.sidebar.markdown("""
<div style="margin-top:28px;padding-top:14px;border-top:1px solid rgba(0,255,231,0.12);font-size:0.7rem;color:rgba(0,255,231,0.35);letter-spacing:0.08em;line-height:2.1;">
    ENGINE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RANDOM FOREST<br>
    BALANCE &nbsp;&nbsp;&nbsp; SMOTE<br>
    XAI &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; SHAP<br>
    STATUS &nbsp;&nbsp;&nbsp;&nbsp; <span style="color:#00ff64;">● OPERATIONAL</span>
</div>
""", unsafe_allow_html=True)

# ── LOAD MODEL ──────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    path = "models/random_forest.pkl"
    return joblib.load(path) if os.path.exists(path) else None

model = load_model()

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 1 — OVERVIEW (README STYLE)
# ════════════════════════════════════════════════════════════════════════════════
if opcao == "🏠 SYSTEM OVERVIEW":

    # ── Métricas ──
    st.markdown('<div class="section-header">// SYSTEM METRICS</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CORE ENGINE", "RF-v1")
    col2.metric("ACCURACY",    "99.95%")
    col3.metric("RECALL",      "84.21%")
    col4.metric("AUC-ROC",     "0.9821")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Sobre o projeto ──
    st.markdown('<div class="section-header">// PROJECT README</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="readme-block">
        <div class="block-title">📋 DESCRIÇÃO GERAL</div>
        Sistema de detecção de fraudes em transações bancárias desenvolvido como
        <span style="color:#00ffe7;">Trabalho de Conclusão de Curso (TCC II)</span> por <span style="color:#00ffe7;">Vitor</span>.
        O modelo utiliza aprendizado de máquina supervisionado para classificar transações em
        <span style="color:#00ff64;">legítimas</span> ou <span style="color:#ff1e3c;">fraudulentas</span>
        em tempo real, com base em componentes PCA anonimizados do dataset público
        <span style="color:#00ffe7;">Credit Card Fraud Detection</span> (Kaggle/ULB).
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="readme-block">
            <div class="block-title">🗃️ DATASET</div>
            <span class="tag">284.807 transações</span>
            <span class="tag red">492 fraudes (0,17%)</span>
            <span class="tag green">284.315 normais</span>
            <br><br>
            Dados reais de cartões de crédito europeus coletados em setembro de 2013.
            As features <b style="color:#00ffe7;">V1–V28</b> são componentes PCA aplicados para
            preservar anonimato. Apenas <b style="color:#00ffe7;">Time</b> e <b style="color:#00ffe7;">Amount</b>
            mantêm significado original.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="readme-block yellow">
            <div class="block-title">⚖️ DESAFIO: DESBALANCEAMENTO</div>
            O dataset é <span style="color:#ffd700;">extremamente desbalanceado</span> —
            fraudes representam apenas <span style="color:#ff1e3c;font-weight:bold;">0,17%</span> dos dados.
            Para contornar isso, foi aplicado <span style="color:#ffd700;">SMOTE</span>
            (Synthetic Minority Oversampling Technique), que gera amostras sintéticas
            da classe minoritária, equilibrando o treinamento sem perda de informação real.
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="readme-block green">
            <div class="block-title">🤖 MODELO: RANDOM FOREST</div>
            Ensemble de árvores de decisão com votação majoritária.
            Escolhido por sua <span style="color:#00ff64;">robustez a outliers</span>,
            boa performance em dados desbalanceados e capacidade de capturar
            interações não-lineares entre features.<br><br>
            <span class="tag green">n_estimators: 100</span>
            <span class="tag green">max_depth: None</span>
            <span class="tag green">class_weight: balanced</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="readme-block">
            <div class="block-title">🔍 EXPLICABILIDADE: SHAP</div>
            Para garantir transparência nas predições, o modelo utiliza
            <span style="color:#00ffe7;">SHAP Values</span>
            (SHapley Additive exPlanations) — método baseado em teoria dos jogos
            que atribui a cada feature sua contribuição individual para a decisão final.
            Isso transforma o modelo de uma "caixa-preta" em um sistema
            <span style="color:#00ffe7;">auditável e interpretável</span>.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">// PIPELINE DE PROCESSAMENTO</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="readme-block">
        <div class="pipeline-row">
            <span class="pipeline-step">📥 RAW DATA</span>
            <span class="pipeline-arrow">›</span>
            <span class="pipeline-step">🔧 PRÉ-PROCESSAMENTO</span>
            <span class="pipeline-arrow">›</span>
            <span class="pipeline-step">⚖️ SMOTE BALANCING</span>
            <span class="pipeline-arrow">›</span>
            <span class="pipeline-step">🌲 RANDOM FOREST</span>
            <span class="pipeline-arrow">›</span>
            <span class="pipeline-step">🔍 SHAP ANALYSIS</span>
            <span class="pipeline-arrow">›</span>
            <span class="pipeline-step">📊 AVALIAÇÃO</span>
            <span class="pipeline-arrow">›</span>
            <span class="pipeline-step">🛡️ DEPLOY</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">// STACK TECNOLÓGICO</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="readme-block">
        <span class="tag">Python 3.11</span>
        <span class="tag">Scikit-learn</span>
        <span class="tag">Imbalanced-learn</span>
        <span class="tag">SHAP</span>
        <span class="tag">Pandas</span>
        <span class="tag">NumPy</span>
        <span class="tag">Matplotlib</span>
        <span class="tag">Seaborn</span>
        <span class="tag">Streamlit</span>
        <span class="tag">Joblib</span>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 2 — ANALYTICS
# ════════════════════════════════════════════════════════════════════════════════
elif opcao == "📊 DATA ANALYTICS":
    st.markdown("""<div class="section-header">// NETWORK TRAFFIC ANALYSIS</div>""", unsafe_allow_html=True)

    fp = "reports/figures/"

    from PIL import Image

    TARGET_H = 400

    def load_fixed(path, h=TARGET_H):
        img = Image.open(path).convert("RGB")
        w, h0 = img.size
        return img.resize((int(w * h / h0), h), Image.LANCZOS)

    def img_card(col, fname, title, tag_color_rgb, tag_label, caption):
        path = fp + fname
        with col:
            st.markdown(
                f"""<div style="background:linear-gradient(135deg,#041828,#020f1c);border:1px solid rgba(0,255,231,0.13);border-radius:4px 4px 0 0;padding:11px 16px 9px;">
                <span style="font-family:Orbitron,monospace;font-size:0.67rem;color:#00ffe7;letter-spacing:0.15em;">{title}</span>
                &nbsp;<span style="background:rgba({tag_color_rgb},0.1);border:1px solid rgba({tag_color_rgb},0.35);color:rgb({tag_color_rgb});font-size:0.61rem;letter-spacing:0.1em;padding:2px 8px;border-radius:2px;">{tag_label}</span>
                </div>""",
                unsafe_allow_html=True
            )
            if os.path.exists(path):
                st.image(load_fixed(path), use_container_width=True)
            else:
                st.markdown(
                    f"<div style='background:#041828;border-left:1px solid rgba(0,255,231,0.13);border-right:1px solid rgba(0,255,231,0.13);height:{TARGET_H}px;display:flex;align-items:center;justify-content:center;color:rgba(0,255,231,0.25);font-size:0.75rem;text-align:center;'>[ IMAGE NOT FOUND ]</div>",
                    unsafe_allow_html=True
                )
            st.markdown(
                f"""<div style="background:rgba(0,5,15,0.6);border:1px solid rgba(0,255,231,0.13);border-top:none;border-radius:0 0 4px 4px;padding:10px 16px 12px;margin-bottom:20px;font-size:0.78rem;color:#7ab8cc;line-height:1.75;">{caption}</div>""",
                unsafe_allow_html=True
            )

    col1, col2 = st.columns(2)

    img_card(
        col=col1, fname="class_distribution.png",
        title="DISTRIBUICAO DAS CLASSES",
        tag_color_rgb="255,30,60", tag_label="DESBALANCEADO",
        caption=(
            "Exibe a proporcao entre transacoes <span style='color:#00ff64;'>legitimas (0)</span> "
            "e <span style='color:#ff1e3c;'>fraudulentas (1)</span> no dataset original. "
            "Das 284.807 transacoes, apenas <b style='color:#ff1e3c;'>492 sao fraude (aprox. 0,17%)</b> - "
            "desbalanceamento extremo que justifica o uso de SMOTE."
        )
    )

    img_card(
        col=col2, fname="amount_distribution.png",
        title="DISTRIBUICAO DO VALOR (AMOUNT)",
        tag_color_rgb="255,215,0", tag_label="LONG-TAIL",
        caption=(
            "Histograma dos valores das transacoes. A distribuicao e fortemente "
            "<span style='color:#ffd700;'>assimetrica a direita</span> - a grande maioria das "
            "transacoes e de baixo valor (proximo a zero), com poucos outliers de alto valor. "
            "Transacoes fraudulentas tendem a concentrar-se em <b style='color:#ffd700;'>valores menores</b>, "
            "possivelmente para evitar deteccao."
        )
    )

    st.markdown("""<div class="section-header">// MODEL PERFORMANCE</div>""", unsafe_allow_html=True)

    roc_path = fp + "roc_curve_random_forest.png"
    st.markdown(
        """<div style="background:linear-gradient(135deg,#041828,#020f1c);border:1px solid rgba(0,255,231,0.13);border-radius:4px 4px 0 0;padding:11px 16px 9px;">
        <span style="font-family:Orbitron,monospace;font-size:0.67rem;color:#00ffe7;letter-spacing:0.15em;">CURVA ROC - RANDOM FOREST</span>
        &nbsp;<span style="background:rgba(0,255,231,0.08);border:1px solid rgba(0,255,231,0.3);color:#00ffe7;font-size:0.61rem;letter-spacing:0.1em;padding:2px 8px;border-radius:2px;">AUC = 0.9821</span>
        </div>""",
        unsafe_allow_html=True
    )
    c_roc, c_pad = st.columns([2, 1])
    with c_roc:
        if os.path.exists(roc_path):
            st.image(load_fixed(roc_path, h=380), use_container_width=True)
        else:
            st.markdown("<div style='background:#041828;border-left:1px solid rgba(0,255,231,0.13);border-right:1px solid rgba(0,255,231,0.13);height:380px;display:flex;align-items:center;justify-content:center;color:rgba(0,255,231,0.25);font-size:0.75rem;'>[ IMAGE NOT FOUND ]</div>", unsafe_allow_html=True)
    st.markdown(
        """<div style="background:rgba(0,5,15,0.6);border:1px solid rgba(0,255,231,0.13);border-top:none;border-radius:0 0 4px 4px;padding:10px 16px 12px;margin-bottom:20px;font-size:0.78rem;color:#7ab8cc;line-height:1.75;">
        A <span style='color:#00ffe7;'>Curva ROC</span> mede a capacidade do modelo de distinguir entre as duas classes em todos os limiares possiveis.
        O <b style='color:#00ffe7;'>AUC de 0.9821</b> indica que o modelo acerta a ordem de risco entre transacoes 98,21% das vezes.
        Eixo X: <span style='color:#ff1e3c;'>Taxa de Falsos Positivos (FPR)</span> | Eixo Y: <span style='color:#00ff64;'>Taxa de Verdadeiros Positivos (Recall/TPR)</span>.
        </div>""",
        unsafe_allow_html=True
    )


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 3 — FRAUD SCANNER
# ════════════════════════════════════════════════════════════════════════════════
elif opcao == "🔍 FRAUD SCANNER":
    st.markdown('<div class="section-header">// REAL-TIME TRANSACTION SCAN</div>', unsafe_allow_html=True)

    if model is None:
        st.markdown("""
        <div class="threat-card">
            <div class="threat-title">⚠ CRITICAL ERROR</div>
            <div style="color:#ff6680;margin-top:8px;font-size:0.85rem;letter-spacing:0.08em;">MODEL NOT FOUND IN /models/random_forest.pkl</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── PRESET SELECTOR ───────────────────────────────────────────────────
        st.markdown('<div class="section-header">// TRANSACTION PRESETS</div>', unsafe_allow_html=True)

        pc1, pc2, pc3, pc4 = st.columns(4)

        with pc1:
            st.markdown('<div class="preset-label">⚠ Fraudulenta</div>', unsafe_allow_html=True)
            st.markdown('<div class="btn-fraud">', unsafe_allow_html=True)
            if st.button("⚠ FRAUD SAMPLE"):
                st.session_state.preset_values = random.choice(PRESETS["fraud"])
                st.session_state.preset_mode = "FRAUD SAMPLE"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with pc2:
            st.markdown('<div class="preset-label">✓ Normal</div>', unsafe_allow_html=True)
            st.markdown('<div class="btn-normal">', unsafe_allow_html=True)
            if st.button("✓ NORMAL SAMPLE"):
                st.session_state.preset_values = random.choice(PRESETS["normal"])
                st.session_state.preset_mode = "NORMAL SAMPLE"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with pc3:
            st.markdown('<div class="preset-label">◈ Aleatória</div>', unsafe_allow_html=True)
            st.markdown('<div class="btn-random">', unsafe_allow_html=True)
            if st.button("◈ RANDOM SAMPLE"):
                st.session_state.preset_values = get_random_preset()
                st.session_state.preset_mode = "RANDOM SAMPLE"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with pc4:
            st.markdown('<div class="preset-label">✎ Manual</div>', unsafe_allow_html=True)
            st.markdown('<div class="btn-manual">', unsafe_allow_html=True)
            if st.button("✎ MANUAL INPUT"):
                st.session_state.preset_values = None
                st.session_state.preset_mode = "MANUAL"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Active mode indicator
        mode_color = {
            "FRAUD SAMPLE":  "#ff1e3c",
            "NORMAL SAMPLE": "#00ff64",
            "RANDOM SAMPLE": "#ffd700",
            "MANUAL":        "#00ffe7",
        }
        mc = mode_color.get(st.session_state.preset_mode, "#00ffe7")
        st.markdown(f"""
        <div style="margin:14px 0 4px;font-size:0.7rem;letter-spacing:0.12em;padding:8px 12px;
                    background:rgba(0,0,0,0.3);border-left:2px solid {mc};border-radius:2px;">
            ACTIVE MODE: <span style="color:{mc};text-shadow:0 0 6px {mc};font-weight:bold;">
            {st.session_state.preset_mode}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── INPUT FORM ────────────────────────────────────────────────────────
        pv = st.session_state.preset_values or {}

        st.markdown('<div class="section-header">// INPUT TRANSACTION PARAMETERS</div>', unsafe_allow_html=True)

        with st.form("scanner_form"):
            c1, c2, c3 = st.columns(3)
            v1  = c1.number_input("V1  — PCA",  value=float(pv.get("V1",  0.0)), format="%.4f")
            v14 = c2.number_input("V14 — PCA",  value=float(pv.get("V14", 0.0)), format="%.4f")
            v17 = c3.number_input("V17 — PCA",  value=float(pv.get("V17", 0.0)), format="%.4f")

            c4, c5 = st.columns(2)
            amount = c4.number_input("AMOUNT [$]",      value=float(pv.get("Amount", 10.0)), format="%.2f")
            time_  = c5.number_input("TIMESTAMP [SEC]", value=float(pv.get("Time",    0.0)), format="%.0f")

            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("⟫ INITIATE SECURITY SCAN")

        # ── RESULT ────────────────────────────────────────────────────────────
        if submit:
            input_data = {f'V{i}': [pv.get(f'V{i}', 0.0)] for i in range(1, 29)}
            input_data['V1']     = [v1]
            input_data['V14']    = [v14]
            input_data['V17']    = [v17]
            input_data['Amount'] = [amount]
            input_data['Time']   = [time_]

            cols     = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
            df_input = pd.DataFrame(input_data)[cols]

            prediction = model.predict(df_input)[0]
            prob       = model.predict_proba(df_input)[0][1]

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">// SCAN RESULT</div>', unsafe_allow_html=True)

            if prediction == 1:
                st.markdown(f"""
                <div class="threat-card">
                    <div class="threat-title">⚠ THREAT DETECTED</div>
                    <div class="prob-value prob-threat">{prob:.2%}</div>
                    <div style="color:#ff6680;font-size:0.8rem;letter-spacing:0.12em;">FRAUD PROBABILITY</div>
                    <div style="margin-top:16px;color:#ff1e3c;font-size:0.75rem;letter-spacing:0.15em;border-top:1px solid rgba(255,30,60,0.3);padding-top:12px;">
                        ◈ RECOMMENDED ACTION: BLOCK TRANSACTION IMMEDIATELY ◈
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="safe-card">
                    <div class="safe-title">✓ TRANSACTION SECURE</div>
                    <div class="prob-value prob-safe">{prob:.2%}</div>
                    <div style="color:#5eead4;font-size:0.8rem;letter-spacing:0.12em;">FRAUD PROBABILITY</div>
                    <div style="margin-top:16px;color:#00ff64;font-size:0.75rem;letter-spacing:0.15em;border-top:1px solid rgba(0,255,100,0.3);padding-top:12px;">
                        ◈ RECOMMENDED ACTION: AUTHORIZE TRANSACTION ◈
                    </div>
                </div>
                """, unsafe_allow_html=True)