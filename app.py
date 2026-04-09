import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS - تثبيت العلوي وتطوير السفلي
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* --- المربعات والدواير (مثبتة كما هي) --- */
    .kpi-card {
        position: relative; background-color: #0a0a0a; border-radius: 20px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 250px; margin-bottom: 40px;
    }
    .kpi-card::before {
        content: ''; position: absolute; width: 250%; height: 250%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .kpi-card::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 6px; border-radius: 16px;
    }
    .circle-container {
        position: relative; width: 230px; height: 230px; border-radius: 50%;
        margin: auto; overflow: hidden; display: flex; justify-content: center; align-items: center;
    }
    .circle-container::before {
        content: ''; position: absolute; width: 300%; height: 300%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 5s linear infinite; top: 50%; left: 50%;
    }
    .circle-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 8px; border-radius: 50%;
    }
    @keyframes rotate-wave {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    .z-layer { position: relative; z-index: 10; width: 100%; }
    .gray-label { color: #aaaaaa; font-size: 28px; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; }
    .cyan-val { color: #00d4ff; font-size: 60px; font-weight: 900; }
    .bm-full-text { color: #555555; font-size: 14px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }

    /* --- التصميم الجديد لمنطقة الأجهزة (Devices) --- */
    .device-grid {
        display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 20px;
    }
    .device-mini-card {
        background: linear-gradient(145deg, #0f0f0f, #050505);
        border: 1px solid #1a1a1a; border-left: 4px solid #00d4ff;
        padding: 20px; border-radius: 12px; text-align: left;
    }
    .device-label { color: #666; font-size: 14px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .device-number { color: #ffffff; font-size: 32px; font-weight: 900; }

    /* كارت Census المطور */
    .census-box {
        background: #0a0a0a; border: 2px solid #FFD700; border-radius: 20px; 
        padding: 40px; text-align: center; position: relative;
    }
    .census-num { color: #FFD700; font-size: 85px; font-weight: 900; line-height: 1; }
    .occ-pill {
        display: inline-block; background: #FFD700; color: #000; 
        padding: 5px 20px; border-radius: 50px; font-weight: 900; font-size: 18px; margin-top: 15px;
    }

    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 20px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. البيانات
data_source = [
    {"period": "1Q 2026", "squares": [("Falls", 0.0, 0.18), ("Injuries", 0.0, 0.04), ("HAPI %", 6.67, 4.58), ("CLABSI", 1.5, 3.3), ("CAUTI", 0.0, 0.4), ("VAP", 1.2, 2.1)], 
     "circles": [("Restraints", 0.45, 0.9), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0), ("Nurse Hr", 14.5, 12.0), ("RN Edu", 85.0, 70.5), ("C-Diff", 0.0, 0.1)],
     "census": 32, "ett": 14, "foley": 18, "cvc": 9, "stay": 3.4},
    {"period": "4Q 2025", "squares": [("Falls", 0.2, 0.1), ("Injuries", 0.1, 0.0), ("HAPI %", 11.0, 6.0), ("CLABSI", 1.2, 2.5), ("CAUTI", 0.5, 0.8), ("VAP", 2.0, 2.1)],
     "circles": [("Restraints", 0.6, 0.9), ("VAE Rate", 2.0, 3.4), ("Turnover", 3.0, 3.0), ("Nurse Hr", 12.0, 12.0), ("RN Edu", 80.0, 70.0), ("C-Diff", 0.1, 0.1)],
     "census": 28, "ett": 10, "foley": 12, "cvc": 8, "stay": 2.9}
]
d = data_source[st.session_state.step % 2]

# حساب النسبة تلقائياً من 36
occ_percent = round((d['census'] / 36) * 100, 1)

# الهيدر
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 50px; font-weight:900; letter-spacing: 3px;'>ICU DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #444; font-weight: bold; font-size: 20px; margin-bottom: 30px;'>PERIOD: {d['period']}</p>", unsafe_allow_html=True)

# 4. المربعات الـ 6 (مثبتة)
cols1 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['squares']):
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="kpi-card"><div class="z-layer"><div class="gray-label">{lab}</div><div class="cyan-val" style="color:{color}">{val}</div><div class="bm-full-text">BENCHMARK: {bm}</div></div></div>""", unsafe_allow_html=True)

# 5. الدوائر الـ 6 (مثبتة)
st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
cols2 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['circles']):
    is_rev = any(x in lab for x in ["Hr", "Edu"])
    color = "#00ffaa" if (val >= bm if is_rev else val <= bm) else "#ff4b4b"
    with cols2[i]:
        st.markdown(f"""<div style="text-align:center;"><div class="circle-container"><div class="z-layer"><div class="cyan-val" style="font-size: 45px; color:{color}">{val}</div></div></div><div class="gray-label" style="margin-top:20px; font-size:24px;">{lab}</div><div class="bm-full-text" style="color:#333;">BENCHMARK: {bm}</div></div>""", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:60px 0;'>", unsafe_allow_html=True)

# 6. الجزء السفلي المطور (Census & Devices)
c1, c2 = st.columns([1.5, 2.5])

with c1:
    # كارت الـ Census مع النسبة التلقائية
    st.markdown(f"""
    <div class="census-box">
        <div style="color:#FFD700; font-weight:bold; letter-spacing:2px;">CURRENT CENSUS</div>
        <div class="census-num">{d['census']}</div>
        <div class="occ-pill">OCCUPANCY: {occ_percent}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # شبكة الأجهزة بتصميم جديد
    st.markdown('<div class="device-grid">', unsafe_allow_html=True)
    devs = [("Pt with ETT", d['ett']), ("Pt with Foley", d['foley']), ("Pt with CVC", d['cvc']), ("Avg Stay", d['stay'])]
    for name, val in devs:
        st.markdown(f"""
        <div class="device-mini-card">
            <div class="device-label">{name}</div>
            <div class="device-number">{val}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="side-header" style="margin-left:20px;">PERFORMANCE ANALYTICS</div>', unsafe_allow_html=True)
    labels = [s[0] for s in d['squares']]; vals = [s[1] for s in d['squares']]; bms = [s[2] for s in d['squares']]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=vals, name="Actual", marker_color='#00d4ff', text=vals, textposition='outside'))
    fig.add_trace(go.Bar(x=labels, y=bms, name="Benchmark", marker_color='#1a1a1a', text=bms, textposition='outside'))
    fig.update_layout(height=480, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=0, l=0, r=0), bargap=0.25, legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center", font=dict(color="#888")), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#111'))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

time.sleep(15)
st.session_state.step += 1
st.rerun()
