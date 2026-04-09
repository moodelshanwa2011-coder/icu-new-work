import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard - SGH Riyadh", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المتطور (كل الكلام داخل الدوائر والمربعات)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    .kpi-card {
        position: relative; background-color: #0a0a0a; border-radius: 20px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 260px; margin-bottom: 30px;
    }
    .kpi-card::before, .circle-container::before {
        content: ''; position: absolute; width: 250%; height: 250%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .kpi-card::after, .circle-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 6px; border-radius: 16px;
    }
    .circle-container::after { border-radius: 50%; inset: 10px; }
    .circle-container {
        position: relative; width: 280px; height: 280px; border-radius: 50%;
        margin: auto; overflow: hidden; display: flex; justify-content: center; align-items: center; text-align: center;
    }
    @keyframes rotate-wave { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }
    .content-box { position: relative; z-index: 10; width: 100%; padding: 10px; }
    .label-text { color: #aaaaaa; font-size: 22px; font-weight: 900; text-transform: uppercase; margin-bottom: 5px; }
    .val-text { color: #00d4ff; font-size: 50px; font-weight: 900; line-height: 1; }
    .bm-text { color: #444444; font-size: 14px; font-weight: bold; margin-top: 10px; }
    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; text-transform: uppercase; margin-bottom: 20px; }
    .census-box { background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; padding: 15px; max-width: 200px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. البيانات المستخرجة من ملف PDF 
# الترتيب: [Falls, Injury Falls, HAPI %, CLABSI, CAUTI, VAP/VAE]
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
cur = quarters_data[st.session_state.q_idx % len(quarters_data)]

# أسماء المؤشرات 
sq_names = ["Falls", "Injury Falls", "HAPI %", "CLABSI", "CAUTI", "VAE Rate"]
cir_names = ["Restraints", "VAE Rate", "Turnover", "Nurse Hr", "RN Edu", "C-Diff"]

# --- العرض ---
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 45px; font-weight:900;'>SGH RIYADH - ICU DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #FFD700; font-size: 22px; font-weight: bold;'>FISCAL PERIOD: {cur['q']}</p>", unsafe_allow_html=True)

# 4. المربعات العلوية (Data from PDF)
cols1 = st.columns(6)
for i in range(6):
    val, bm = cur['sq'][i], cur['sq_bm'][i]
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="kpi-card"><div class="content-box"><div class="label-text">{sq_names[i]}</div><div class="val-text" style="color:{color}">{val}</div><div class="bm-text">BM: {bm}</div></div></div>""", unsafe_allow_html=True)

# 5. الدوائر العلوية (Data from PDF)
st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
cols2 = st.columns(6)
for i in range(6):
    val, bm = cur['cir'][i], cur['cir_bm'][i]
    is_rev = "Hr" in cir_names[i] or "Edu" in cir_names[i]
    color = "#00ffaa" if (val >= bm if is_rev else val <= bm) else "#ff4b4b"
    with cols2[i]:
        st.markdown(f"""<div class="circle-container"><div class="content-box"><div class="label-text" style="font-size:20px;">{cir_names[i]}</div><div class="val-text" style="color:{color}; font-size:45px;">{val}</div><div class="bm-text">BM: {bm}</div></div></div>""", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:40px 0;'>", unsafe_allow_html=True)

# 6. الجزء السفلي (مثبت كما في طلبك السابق)
c1, c2 = st.columns([2, 2])
with c1:
    st.markdown(f"""<div class="census-box"><div style="color:#FFD700; font-size:12px; font-weight:bold;">TOTAL PATIENT STAY</div><div style="color:#FFD700; font-size:40px; font-weight:900;">811</div></div>""", unsafe_allow_html=True)
    st.markdown('<div class="side-header">DEVICE CENSUS (APRIL 2026)</div>', unsafe_allow_html=True)
    # هنا يمكن وضع الـ Gauges للأجهزة من صورة الجدول (Foley: 454, Ventilator: 374...)
    st.write("Foley Catheter: 454 | Ventilators: 374 | IV Sites: 678")

with c2:
    st.markdown('<div class="side-header">QUARTERLY TREND ANALYTICS</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=sq_names, y=cur['sq'], name="Current Unit", marker_color='#00d4ff'))
    fig.add_trace(go.Bar(x=sq_names, y=cur['sq_bm'], name="NDNQI Mean", marker_color='#222'))
    fig.update_layout(height=350, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), legend=dict(font=dict(color="#888")))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# 7. التحديث التلقائي كل 15 ثانية لتمثيل الأرباع
time.sleep(15)
st.session_state.q_idx += 1
st.rerun()
