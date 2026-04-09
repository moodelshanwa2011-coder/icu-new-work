import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Performance Hub", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المطور لضمان عدم التداخل
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* حاوية المربعات العلوية */
    .wave-container {
        position: relative; background-color: #0a0a0a; border-radius: 12px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 150px; margin-bottom: 10px; padding: 10px;
    }
    .wave-container::before {
        content: ''; position: absolute; width: 200%; height: 200%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .wave-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 3px; border-radius: 10px;
    }
    
    /* حاوية الدوائر */
    .wave-circle-outer {
        position: relative; width: 130px; height: 130px; border-radius: 50%;
        margin: auto; overflow: hidden; display: flex; justify-content: center; align-items: center;
    }
    .wave-circle-outer::before {
        content: ''; position: absolute; width: 200%; height: 200%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 5s linear infinite; top: 50%; left: 50%;
    }
    .wave-circle-outer::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 4px; border-radius: 50%;
    }

    @keyframes rotate-wave {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    .z-layer { position: relative; z-index: 10; width: 100%; }
    
    /* مسميات واضحة */
    .gray-label { color: #aaaaaa; font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px; }
    .cyan-val { color: #00d4ff; font-size: 30px; font-weight: 900; }
    .bm-val { color: #444444; font-size: 10px; font-weight: bold; margin-top: 5px; }

    /* كارت Census */
    .census-card {
        background: #0a0a0a; border-left: 5px solid #FFD700; border-radius: 10px; 
        padding: 20px; text-align: center; margin-bottom: 25px;
    }
    .census-val { color: #FFD700; font-size: 50px; font-weight: 900; margin: 5px 0; }
    
    .side-title { color: #aaaaaa; font-size: 18px; font-weight: 900; margin-bottom: 20px; }
    .dev-card { background: #0a0a0a; border-left: 3px solid #00d4ff; border-radius: 4px; padding: 12px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. داتا المؤشرات (12 مؤشر)
data_source = [
    {
        "period": "CYCLE 2026-A",
        "squares": [("Falls", 0.0, 0.18), ("Injuries", 0.0, 0.04), ("HAPI %", 6.67, 4.58), ("CLABSI", 1.5, 3.3), ("CAUTI", 0.0, 0.4), ("VAP", 1.2, 2.1)],
        "circles": [("Restraints", 0.45, 0.9), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0), ("Nurse Hr", 14.5, 12.0), ("RN Edu", 85.0, 70.5), ("C-Diff", 0.0, 0.1)],
        "census": 32, "occ": "88.9%", "ett": 14, "foley": 18, "cvc": 9, "stay": 3.4
    },
    {
        "period": "CYCLE 2025-B",
        "squares": [("Falls", 0.2, 0.1), ("Injuries", 0.1, 0.0), ("HAPI %", 10.5, 6.5), ("CLABSI", 1.2, 2.6), ("CAUTI", 0.7, 1.0), ("VAP", 2.1, 2.1)],
        "circles": [("Restraints", 0.7, 0.9), ("VAE Rate", 2.1, 3.4), ("Turnover", 3.1, 3.0), ("Nurse Hr", 12.8, 12.0), ("RN Edu", 82.9, 70.5), ("C-Diff", 0.1, 0.1)],
        "census": 30, "occ": "83.3%", "ett": 11, "foley": 15, "cvc": 10, "stay": 2.8
    }
]
d = data_source[st.session_state.step % 2]

# الهيدر
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 38px; font-weight:900;'>ICU STRATEGIC COMMAND</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #555; font-weight: bold;'>{d['period']}</p>", unsafe_allow_html=True)

# 4. المربعات العلوية (6) بمسافات مضبوطة
cols1 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['squares']):
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="wave-container"><div class="z-layer">
            <div class="gray-label">{lab}</div>
            <div class="cyan-val" style="color:{color}">{val}</div>
            <div class="bm-val">BM: {bm}</div>
        </div></div>""", unsafe_allow_html=True)

# 5. الدوائر (6) بمسافات مضبوطة
cols2 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['circles']):
    is_rev = any(x in lab for x in ["Hr", "Edu"])
    color = "#00ffaa" if (val >= bm if is_rev else val <= bm) else "#ff4b4b"
    with cols2[i]:
        st.markdown(f"""<div style="margin-top:20px; margin-bottom:10px;">
            <div class="wave-circle-outer"><div class="z-layer">
                <div class="cyan-val" style="font-size: 22px; color:{color}">{val}</div>
            </div></div>
            <div class="gray-label" style="text-align:center; margin-top:8px;">{lab}</div>
            <div class="bm-val" style="text-align:center; color:#333;">BM: {bm}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:30px 0;'>", unsafe_allow_html=True)

# 6. الجزء السفلي (Census & Devices & Bar)
c1, c2 = st.columns([1.2, 2.6])

with c1:
    st.markdown('<div class="side-title">36 CAPACITY</div>', unsafe_allow_html=True)
    
    st.markdown(f"""<div class="census-card">
        <div class="gray-label" style="color:#FFD700;">Unit Census</div>
        <div class="census-val">{d['census']}</div>
        <div style="color:#FFD700; font-size:13px; font-weight:bold;">OCCUPANCY: {d['occ']}</div>
    </div>""", unsafe_allow_html=True)
    
    # قائمة الأجهزة
    devices = [("Pt with ETT", d['ett']), ("Pt with Foley", d['foley']), ("Pt with CVC", d['cvc']), ("Avg Stay", d['stay'])]
    for name, value in devices:
        st.markdown(f"""<div class="dev-card">
            <span style="float:right; color:#00d4ff; font-weight:900; font-size:20px;">{value}</span>
            <span class="gray-label" style="font-size:11px;">{name}</span>
        </div>""", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="side-title" style="margin-left:20px;">PERFORMANCE ANALYTICS</div>', unsafe_allow_html=True)
    
    labels = [s[0] for s in d['squares']]
    vals = [s[1] for s in d['squares']]
    bms = [s[2] for s in d['squares']]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=vals, name="Actual", marker_color='#00d4ff', text=vals, textposition='outside'))
    fig.add_trace(go.Bar(x=labels, y=bms, name="Target", marker_color='#1a1a1a', text=bms, textposition='outside'))

    fig.update_layout(
        height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#888'), margin=dict(t=30, b=0, l=0, r=0),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center")
    )
    fig.update_yaxes(showgrid=True, gridcolor='#111')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي
time.sleep(15)
st.session_state.step += 1
st.rerun()
