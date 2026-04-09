import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Live Command", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المتطور: تأثير "الموجة النيونية" الدوارة وألوان الأسماء الاحترافية
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    [data-testid="stHorizontalBlock"] { gap: 1rem; }

    /* المربعات الموجية */
    .kpi-wave-box {
        position: relative; background-color: #0a0a0a; border-radius: 12px;
        height: 160px; display: flex; flex-direction: column; justify-content: center;
        text-align: center; overflow: hidden; margin-bottom: 20px;
    }
    .kpi-wave-box::before {
        content: ''; position: absolute; width: 150%; height: 150%;
        background: conic-gradient(#00d4ff, #001122, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .kpi-wave-box::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 4px; border-radius: 10px;
    }
    
    /* الدوائر الموجية */
    .kpi-wave-circle-outer {
        position: relative; width: 140px; height: 140px; border-radius: 50%;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin: auto; background-color: #0a0a0a; overflow: hidden;
    }
    .kpi-wave-circle-outer::before {
        content: ''; position: absolute; width: 150%; height: 150%;
        background: conic-gradient(#00d4ff, #001122, #00d4ff);
        animation: rotate-wave 5s linear infinite; top: 50%; left: 50%;
    }
    .kpi-wave-circle-outer::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 5px; border-radius: 50%;
    }

    @keyframes rotate-wave {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    .kpi-content-layer { position: relative; z-index: 10; padding: 5px; }
    .kpi-label-text { color: #aaaaaa; font-size: 14px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value-text { color: #00d4ff; font-size: 32px; font-weight: 900; }
    .kpi-bench-text { color: #555; font-size: 11px; font-weight: bold; }

    .dev-card-dynamic {
        background-color: #0a0a0a; border-left: 4px solid #00d4ff;
        border-radius: 8px; padding: 12px; margin-bottom: 12px; text-align: center;
    }
    .dev-label-dynamic { color: #aaaaaa; font-size: 13px; font-weight: bold; }
    .dev-value-dynamic { color: #ffffff; font-size: 28px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة بيانات كاملة وديناميكية (12 KPI)
data_source = [
    {
        "period": "3Q 2025 (Cycle A)", "week": "WEEK 01",
        "squares": [
            ("Total Falls", 0.0, 0.18), ("Injury Falls", 0.0, 0.04), ("HAPI %", 6.67, 4.58),
            ("CLABSI Rate", 1.50, 3.38), ("CAUTI Rate", 0.0, 0.44), ("VAP Rate", 1.2, 2.1)
        ],
        "circles": [
            ("Restraints", 0.45, 0.90), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0),
            ("HPPD (HRS)", 14.5, 12.0), ("RN Education", 85.01, 70.59), ("C-Diff / MRSA", 0.0, 0.12)
        ],
        "devs": [("Ventilators", 14), ("Foley Cath", 15), ("Central Line", 8), ("Total Stay", 34)]
    },
    {
        "period": "2Q 2024 (Cycle B)", "week": "WEEK 02",
        "squares": [
            ("Total Falls", 0.24, 0.06), ("Injury Falls", 0.24, 0.01), ("HAPI %", 14.29, 6.54),
            ("CLABSI Rate", 1.28, 2.67), ("CAUTI Rate", 0.70, 0.99), ("VAP Rate", 2.1, 2.1)
        ],
        "circles": [
            ("Restraints", 0.70, 0.96), ("VAE Rate", 2.17, 3.4), ("Turnover", 3.1, 3.0),
            ("HPPD (HRS)", 12.8, 12.0), ("RN Education", 82.99, 70.59), ("C-Diff / MRSA", 0.1, 0.12)
        ],
        "devs": [("Ventilators", 12), ("Foley Cath", 14), ("Central Line", 9), ("Total Stay", 28)]
    }
]

# اختيار البيانات بناءً على الـ Step للتأكد من التغيير
current_data = data_source[st.session_state.step % 2]

st.markdown(f"<h2 style='text-align: center; color: white;'>ICU DYNAMIC HUB | {current_data['period']}</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 4. المربعات الموجية (العلوي)
cols_sq = st.columns(6)
for i, (lab, val, bench) in enumerate(current_data['squares']):
    color = "#00CC96" if val <= bench else "#FF4B4B"
    with cols_sq[i]:
        st.markdown(f"""
        <div class="kpi-wave-box"><div class="kpi-content-layer">
            <div class="kpi-label-text">{lab}</div>
            <div class="kpi-value-text" style="color: {color}">{val}</div>
            <div class="kpi-bench-text">Bench: {bench}</div>
        </div></div>""", unsafe_allow_html=True)

# 5. الدوائر الموجية (السفلي)
cols_ci = st.columns(6)
for i, (lab, val, bench) in enumerate(current_data['circles']):
    is_rev = any(x in lab for x in ["Hours", "Education"])
    color = "#00CC96" if (val >= bench if is_rev else val <= bench) else "#FF4B4B"
    with cols_ci[i]:
        st.markdown(f"""
        <div class="kpi-wave-circle-outer"><div class="kpi-content-layer">
            <div class="kpi-value-text" style="color: {color}; font-size: 24px; margin-top:10px;">{val}</div>
            <div class="kpi-bench-text" style="color: #fff">Target: {bench}</div>
        </div></div>
        <div class="kpi-label-text" style="text-align:center; height:30px; margin-top:8px;">{lab}</div>
        """, unsafe_allow_html=True)

st.markdown("<hr style='border-color: #1a1a1a;'>", unsafe_allow_html=True)

# 6. الجزء السفلي
c1, c2 = st.columns([1, 2.8])
with c1:
    st.markdown(f"<p style='color:#00d4ff; font-weight:bold;'>DEVICES ({current_data['week']})</p>", unsafe_allow_html=True)
    for name, val in current_data['devs']:
        st.markdown(f"""<div class="dev-card-dynamic"><span class="dev-value-dynamic">{val}</span><span class="dev-label-dynamic">{name}</span></div>""", unsafe_allow_html=True)

with c2:
    labels = [s[0] for s in current_data['squares']]
    vals = [s[1] for s in current_data['squares']]
    fig = go.Figure(go.Bar(x=labels, y=vals, marker_color='#00d4ff', text=vals, textposition='outside'))
    fig.update_layout(height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#aaaaaa'))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# التحديث الفعلي
time.sleep(15)
st.session_state.step += 1
st.rerun()
