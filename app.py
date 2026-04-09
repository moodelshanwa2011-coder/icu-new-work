import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Monitor", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS تأثير الحدود المتحركة (Loading Effect)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; padding: 10px 20px; }
    
    /* حركة الحدود للمربعات */
    .kpi-card-anim {
        position: relative; background-color: #0d0d0d; border-radius: 12px;
        padding: 20px; margin-bottom: 20px; text-align: center;
        height: 160px; display: flex; flex-direction: column; justify-content: center;
        overflow: hidden;
    }
    .kpi-card-anim::before {
        content: ''; position: absolute; width: 150%; height: 150%;
        background: conic-gradient(#00d4ff, #00CC96, #00d4ff);
        animation: rotate 3s linear infinite; top: 50%; left: 50%;
    }
    .kpi-card-anim::after {
        content: ''; position: absolute; background-color: #0d0d0d;
        inset: 4px; border-radius: 10px;
    }

    /* حركة الحدود للدوائر */
    .kpi-circle-anim {
        position: relative; width: 150px; height: 150px; border-radius: 50%;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin: auto; margin-bottom: 10px; background-color: #0d0d0d; overflow: hidden;
    }
    .kpi-circle-anim::before {
        content: ''; position: absolute; width: 150%; height: 150%;
        background: conic-gradient(#00d4ff, #FF007F, #00d4ff);
        animation: rotate 4s linear infinite; top: 50%; left: 50%;
    }
    .kpi-circle-anim::after {
        content: ''; position: absolute; background-color: #0d0d0d;
        inset: 5px; border-radius: 50%;
    }

    @keyframes rotate {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    .kpi-inner { position: relative; z-index: 10; }
    .kpi-label { color: #ffffff; font-size: 15px; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; }
    .kpi-val { font-size: 32px; font-weight: 900; }
    .kpi-bench { color: #555; font-size: 12px; font-weight: bold; }

    /* الأجهزة السفلي */
    .dev-card { background-color: #0d0d0d; border-left: 4px solid #1f77b4; padding: 10px; margin-bottom: 10px; border-radius: 5px; }
    .dev-v { color: #ffffff; font-size: 24px; font-weight: 900; float: right; }
    .dev-l { color: #888; font-size: 13px; font-weight: bold; }
    .stay-highlight { border-left: 4px solid #00CC96; background-color: #001a1a; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات بالمسميات القديمة
data_cycle = [
    {
        "q": "3Q 2025", "w": "WEEK 01",
        "squares": [
            ("Total Falls", 0.0, 0.18), ("Injury Falls", 0.0, 0.04), ("HAPI %", 6.67, 4.58),
            ("CLABSI Rate", 1.50, 3.38), ("CAUTI Rate", 0.0, 0.44), ("VAP Rate", 1.2, 2.1)
        ],
        "circles": [
            ("Restraints", 0.45, 0.90), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0),
            ("Nursing Hours", 14.5, 12.0), ("RN Education", 85.01, 70.59), ("C-Diff / MRSA", 0.0, 0.12)
        ],
        "devs": [("Ventilators", 14), ("Foley Cath", 15), ("Central Line", 8), ("Total Stay", 34)]
    },
    {
        "q": "2Q 2024", "w": "WEEK 02",
        "squares": [
            ("Total Falls", 0.24, 0.06), ("Injury Falls", 0.24, 0.01), ("HAPI %", 14.29, 6.54),
            ("CLABSI Rate", 1.28, 2.67), ("CAUTI Rate", 0.70, 0.99), ("VAP Rate", 2.1, 2.1)
        ],
        "circles": [
            ("Restraints", 0.70, 0.96), ("VAE Rate", 2.17, 3.4), ("Turnover", 3.1, 3.0),
            ("Nursing Hours", 12.8, 12.0), ("RN Education", 82.99, 70.59), ("C-Diff / MRSA", 0.1, 0.12)
        ],
        "devs": [("Ventilators", 12), ("Foley Cath", 14), ("Central Line", 9), ("Total Stay", 28)]
    }
]
d = data_cycle[st.session_state.step % 2]

st.markdown(f"<h2 style='text-align: center; color: white;'>ICU COMMAND HUB | {d['q']}</h2>", unsafe_allow_html=True)

# 4. عرض الصف العلوي (مربعات متحركة)
cols1 = st.columns(6)
for i, (lab, val, bench) in enumerate(d['squares']):
    color = "#00CC96" if val <= bench else "#FF4B4B"
    with cols1[i]:
        st.markdown(f"""
        <div class="kpi-card-anim"><div class="kpi-inner">
            <div class="kpi-label">{lab}</div>
            <div class="kpi-val" style="color:{color}">{val}</div>
            <div class="kpi-bench">Bench: {bench}</div>
        </div></div>""", unsafe_allow_html=True)

# 5. عرض الصف السفلي (دوائر متحركة)
cols2 = st.columns(6)
for i, (lab, val, bench) in enumerate(d['circles']):
    # منطق الألوان للتعليم والساعات (الأعلى أفضل)
    is_rev = "Hours" in lab or "Education" in lab
    color = "#00CC96" if (val >= bench if is_rev else val <= bench) else "#FF4B4B"
    with cols2[i]:
        st.markdown(f"""
        <div class="kpi-circle-anim"><div class="kpi-inner">
            <div class="kpi-val" style="color:{color}; font-size:26px;">{val}</div>
            <div class="kpi-bench" style="color:white">Target: {bench}</div>
        </div></div>
        <div style="text-align:center; color:#888; font-weight:bold; font-size:12px;">{lab}</div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# 6. الجزء السفلي (الأجهزة والبار)
c1, c2 = st.columns([1, 2.5])
with c1:
    st.markdown(f"<p style='color:#00d4ff; font-weight:bold;'>DEVICES ({d['w']})</p>", unsafe_allow_html=True)
    for name, val in d['devs']:
        style = "stay-highlight" if name == "Total Stay" else ""
        st.markdown(f'<div class="dev-card {style}"><span class="dev-v">{val}</span><span class="dev-l">{name}</span></div>', unsafe_allow_html=True)

with c2:
    labels = [s[0] for s in d['squares']]
    vals = [s[1] for s in d['squares']]
    benches = [s[2] for s in d['squares']]
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Unit', x=labels, y=vals, marker_color='#00d4ff'))
    fig.add_trace(go.Bar(name='Bench', x=labels, y=benches, marker_color='#222'))
    fig.update_layout(height=350, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(color='white'), margin=dict(l=0, r=0, t=10, b=0), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

time.sleep(15)
st.session_state.step += 1
st.rerun()
