import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS الاحترافي (تنسيق الكلام داخل الدوائر والمربعات)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* تنسيق الكروت العلوية (مربعات ودوائر) */
    .kpi-card, .circle-container {
        position: relative; background-color: #0a0a0a; border-radius: 20px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; margin-bottom: 20px;
    }
    .kpi-card { height: 260px; }
    .circle-container { width: 280px; height: 280px; border-radius: 50%; margin: auto; }
    
    .kpi-card::before, .circle-container::before {
        content: ''; position: absolute; width: 250%; height: 250%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .kpi-card::after, .circle-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 6px; border-radius: 16px;
    }
    .circle-container::after { border-radius: 50%; inset: 10px; }
    
    @keyframes rotate-wave { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }
    
    .content-box { position: relative; z-index: 10; width: 100%; padding: 10px; }
    .label-text { color: #aaaaaa; font-size: 22px; font-weight: 900; text-transform: uppercase; margin-bottom: 5px; }
    .val-text { color: #00d4ff; font-size: 50px; font-weight: 900; line-height: 1; }
    .bm-text { color: #444444; font-size: 14px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }

    /* الجزء السفلي الثابت */
    .census-box-fixed { background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; padding: 15px 25px; text-align: left; max-width: 250px; margin-bottom: 20px; }
    .census-num-fixed { color: #FFD700; font-size: 40px; font-weight: 900; margin: 5px 0; }
    .gauge-label-fixed { color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase; margin-top: -20px; text-align: center; }
    .side-header-fixed { color: #00d4ff; font-size: 26px; font-weight: 900; text-transform: uppercase; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. بيانات الـ PDF (للجزء العلوي فقط)
quarters_data = [
    {"q": "3Q 2024", "sq": [0.36, 0.36, 6.90, 2.63, 1.02, 0.00], "sq_bm": [0.28, 0.05, 4.60, 1.20, 0.40, 1.89], 
     "cir": [20.69, 0.00, 4.69, 12.54, 68.25, 0.00], "cir_bm": [6.32, 1.89, 4.51, 19.20, 83.36, 0.25]},
    {"q": "4Q 2024", "sq": [0.00, 0.00, 9.68, 1.80, 1.13, 1.60], "sq_bm": [0.14, 0.01, 4.61, 1.21, 0.54, 2.49],
     "cir": [19.35, 1.60, 4.35, 12.39, 71.83, 0.00], "cir_bm": [6.01, 2.49, 4.16, 19.82, 83.30, 0.11]},
    {"q": "1Q 2025", "sq": [1.59, 0.80, 4.17, 3.02, 0.00, 6.69], "sq_bm": [0.12, 0.03, 4.96, 1.26, 0.43, 1.91],
     "cir": [12.50, 6.69, 1.43, 12.87, 70.00, 0.00], "cir_bm": [8.23, 1.91, 3.97, 19.15, 83.78, 0.26]},
    {"q": "2Q 2025", "sq": [0.18, 0.04, 4.58, 3.38, 0.44, 3.40], "sq_bm": [0.00, 0.00, 6.67, 1.50, 0.00, 1.60],
     "cir": [13.33, 3.40, 2.90, 19.26, 70.59, 0.00], "cir_bm": [7.20, 1.60, 3.22, 13.00, 85.01, 0.45]}
]

if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
cur_q = quarters_data[st.session_state.q_idx % len(quarters_data)]

# --- الجزء العلوي (ديناميكي من PDF) ---
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 45px; font-weight:900;'>ICU PERFORMANCE DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #FFD700; font-size: 20px; font-weight: bold;'>FISCAL QUARTER: {cur_q['q']}</p>", unsafe_allow_html=True)

sq_labels = ["Falls", "Injury Falls", "HAPI %", "CLABSI", "CAUTI", "VAE Rate"]
cir_labels = ["Restraints", "VAE Rate", "Turnover", "Nurse Hr", "RN Edu", "C-Diff"]

# المربعات
c_sq = st.columns(6)
for i in range(6):
    v, b = cur_q['sq'][i], cur_q['sq_bm'][i]
    color = "#00ffaa" if v <= b else "#ff4b4b"
    with c_sq[i]:
        st.markdown(f'<div class="kpi-card"><div class="content-box"><div class="label-text">{sq_labels[i]}</div><div class="val-text" style="color:{color}">{v}</div><div class="bm-text">BM: {b}</div></div></div>', unsafe_allow_html=True)

# الدوائر
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
c_cir = st.columns(6)
for i in range(6):
    v, b = cur_q['cir'][i], cur_q['cir_bm'][i]
    is_rev = "Hr" in cir_labels[i] or "Edu" in cir_labels[i]
    color = "#00ffaa" if (v >= b if is_rev else v <= b) else "#ff4b4b"
    with c_cir[i]:
        st.markdown(f'<div class="circle-container"><div class="content-box"><div class="label-text" style="font-size:18px;">{cir_labels[i]}</div><div class="val-text" style="color:{color}; font-size:45px;">{v}</div><div class="bm-text">BM: {b}</div></div></div>', unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:40px 0;'>", unsafe_allow_html=True)

# --- الجزء السفلي (ثابت تماماً كما طلبت) ---
c1, c2 = st.columns([2.2, 1.8])

def create_gauge(v, mx, s):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = v,
        number = {'font': {'size': 38, 'color': '#fff', 'family': 'Arial Black'}},
        gauge = {'axis': {'range': [None, mx], 'tickvals': []}, 'bar': {'color': "#222"}, 'bgcolor': "#000",
                 'steps': [{'range': [0, s[0]], 'color': "#00ffaa"}, {'range': [s[0], s[1]], 'color': "#FFD700"}, {'range': [s[1], mx], 'color': "#ff4b4b"}]}
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, l=10, r=10), height=130)
    return fig

with c1:
    # Census الثابت
    st.markdown("""<div class="census-box-fixed"><div style="color:#FFD700; font-size:12px; font-weight:bold; text-transform:uppercase;">Current Census</div><div class="census-num-fixed">28</div></div>""", unsafe_allow_html=True)
    st.markdown('<div class="side-header-fixed">ATTACHED DEVICES (FIXED)</div>', unsafe_allow_html=True)
    
    g_cols = st.columns(4)
    # قيم ثابتة لا تتغير مع الـ Quarter
    fixed_dev = [("Pt with ETT", 12, 36, [10, 18]), ("Pt with Foley", 16, 36, [24, 30]), ("Pt with CVC", 8, 36, [16, 22]), ("Avg Stay", 4.0, 10, [4, 6])]
    for i, (n, v, m, s) in enumerate(fixed_dev):
        with g_cols[i]:
            st.plotly_chart(create_gauge(v, m, s), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<div class="gauge-label-fixed">{n}</div>', unsafe_allow_html=True)

with c2:
    # تشارت التحليل الثابت أو المرتبط بآخر داتا
    st.markdown('<div class="side-header-fixed" style="margin-left:20px;">TREND ANALYTICS</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=sq_labels, y=cur_q['sq'], name="Current", marker_color='#00d4ff'))
    fig.add_trace(go.Bar(x=sq_labels, y=cur_q['sq_bm'], name="Benchmark", marker_color='#1a1a1a'))
    fig.update_layout(height=450, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      margin=dict(t=20, b=20, l=0, r=0), legend=dict(font=dict(color="#888")))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي للعلوي فقط
time.sleep(15)
st.session_state.q_idx += 1
st.rerun()
