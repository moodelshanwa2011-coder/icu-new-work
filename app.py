import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Strategic Command", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المتطور: تأثير الموجة النيونية والأسماء الرمادية المنسقة
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* حركة الموجة النيونية الدوارة */
    .wave-container {
        position: relative; background-color: #0a0a0a; border-radius: 15px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 160px; margin-bottom: 20px;
    }
    .wave-container::before {
        content: ''; position: absolute; width: 160%; height: 160%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .wave-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 4px; border-radius: 12px;
    }
    
    .wave-circle-outer {
        position: relative; width: 150px; height: 150px; border-radius: 50%;
        margin: auto; overflow: hidden; display: flex; justify-content: center; align-items: center;
    }
    .wave-circle-outer::before {
        content: ''; position: absolute; width: 160%; height: 160%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 5s linear infinite; top: 50%; left: 50%;
    }
    .wave-circle-outer::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 5px; border-radius: 50%;
    }

    @keyframes rotate-wave {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    .z-layer { position: relative; z-index: 10; }
    
    /* مسميات رمادية معدنية */
    .gray-label { color: #aaaaaa; font-size: 14px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }
    .cyan-val { color: #00d4ff; font-size: 35px; font-weight: 900; }
    .bm-val { color: #444444; font-size: 11px; font-weight: bold; }

    /* كارت Unit Census الذهبي */
    .census-card {
        background: linear-gradient(145deg, #0f0f0f, #050505);
        border-left: 6px solid #FFD700; border-radius: 10px; padding: 20px; text-align: center;
    }
    .census-val { color: #FFD700; font-size: 55px; font-weight: 900; line-height: 1; margin: 10px 0; }
    
    /* العناوين الجانبية */
    .side-title { color: #aaaaaa; font-size: 22px; font-weight: 900; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 1px; }

    .dev-card { background: #0a0a0a; border-left: 3px solid #00d4ff; border-radius: 4px; padding: 12px; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات الكاملة (12 KPIs + Devices)
data_source = [
    {
        "period": "3Q 2025 (Cycle A)",
        "squares": [("Falls", 0.0, 0.18), ("Injuries", 0.0, 0.04), ("HAPI %", 6.67, 4.58), ("CLABSI Rate", 1.50, 3.38), ("CAUTI Rate", 0.0, 0.44), ("VAP Rate", 1.2, 2.1)],
        "circles": [("Restraints", 0.45, 0.90), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0), ("Nursing Hr", 14.5, 12.0), ("RN Education", 85.0, 70.5), ("C-Diff", 0.0, 0.12)],
        "census": 32, "occupancy": "88.9%", "ett": 14, "foley": 18, "cvc": 9, "stay": 3.4
    },
    {
        "period": "2Q 2024 (Cycle B)",
        "squares": [("Falls", 0.24, 0.06), ("Injuries", 0.15, 0.01), ("HAPI %", 14.2, 6.5), ("CLABSI Rate", 1.28, 2.67), ("CAUTI Rate", 0.7, 0.99), ("VAP Rate", 2.1, 2.1)],
        "circles": [("Restraints", 0.70, 0.96), ("VAE Rate", 2.17, 3.4), ("Turnover", 3.1, 3.0), ("Nursing Hr", 12.8, 12.0), ("RN Education", 82.9, 70.5), ("C-Diff", 0.1, 0.12)],
        "census": 30, "occupancy": "83.3%", "ett": 11, "foley": 15, "cvc": 10, "stay": 2.8
    }
]
d = data_source[st.session_state.step % 2]

# العنوان الرئيسي
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 45px; font-weight:900;'>ICU STRATEGIC COMMAND HUB</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #555; font-weight: bold;'>PERIOD: {d['period']}</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 4. المربعات المتموجة (الصف العلوي)
cols1 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['squares']):
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="wave-container"><div class="z-layer">
            <div class="gray-label">{lab}</div>
            <div class="cyan-val" style="color:{color}">{val}</div>
            <div class="bm-val">Benchmark: {bm}</div>
        </div></div>""", unsafe_allow_html=True)

# 5. الدوائر المتموجة (الصف السفلي)
cols2 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['circles']):
    is_rev = any(x in lab for x in ["Hr", "Education"])
    color = "#00ffaa" if (val >= bm if is_rev else val <= bm) else "#ff4b4b"
    with cols2[i]:
        st.markdown(f"""<div class="wave-circle-outer"><div class="z-layer">
            <div class="cyan-val" style="font-size: 26px; color:{color}">{val}</div>
            <div class="bm-val" style="color:#888;">BM: {bm}</div>
        </div></div>
        <div class="gray-label" style="text-align:center; margin-top:10px; font-size:12px; font-weight:bold;">{lab}</div>""", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:40px 0;'>", unsafe_allow_html=True)

# 6. الجزء السفلي (البيانات الجانبية والرسم البياني)
c1, c2 = st.columns([1.3, 2.5])

with c1:
    st.markdown(f'<div class="side-title" style="color:#00d4ff;">36 CAPACITY STATUS</div>', unsafe_allow_html=True)
    
    # كارت Unit Census الذهبي
    st.markdown(f"""<div class="census-card">
        <div class="gray-label" style="color:#FFD700; font-size:12px;">Unit Census</div>
        <div class="census-val">{d['census']}</div>
        <div style="color:#FFD700; font-size:14px; font-weight:bold;">Occupancy: {d['occupancy']}</div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # مسميات الأجهزة الطبية بنمط Pt with
    device_data = [
        ("Pt with ETT", d['ett']), 
        ("Pt with Foley", d['foley']), 
        ("Pt with CVC", d['cvc']),
        ("Average Length of Stay", d['stay'])
    ]
    for l, v in device_data:
        st.markdown(f"""<div class="dev-card">
            <span style="float:right; color:#00d4ff; font-weight:900; font-size:22px;">{v}</span>
            <span class="gray-label" style="font-size:11px;">{l}</span>
        </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="side-title" style="margin-left:20px;">PERFORMANCE TRENDS</div>', unsafe_allow_html=True)
    
    labels = [s[0] for s in d['squares']]
    vals = [s[1] for s in d['squares']]
    bms = [s[2] for s in d['squares']]

    fig = go.Figure()
    # الأعمدة الفعلية
    fig.add_trace(go.Bar(
        x=labels, y=vals, name="Unit Actual", 
        marker=dict(color='#00d4ff'), 
        text=vals, textposition='outside'
    ))
    # أعمدة البنش مارك
    fig.add_trace(go.Bar(
        x=labels, y=bms, name="Benchmark", 
        marker=dict(color='#1a1a1a', line=dict(color='#333', width=1)), 
        text=bms, textposition='outside'
    ))

    fig.update_layout(
        height=420, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#aaaaaa'), margin=dict(t=50, b=0),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center")
    )
    fig.update_yaxes(showgrid=True, gridcolor='#111')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي
time.sleep(15)
st.session_state.step += 1
st.rerun()
