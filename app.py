import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Performance Hub", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS الاحترافي (الموجة، الخطوط الكبيرة، والشرطة المائلة)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; font-family: 'Segoe UI', sans-serif; }
    
    /* حركة الموجة النيونية */
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
    
    /* الدوائر المتموجة */
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
    .gray-label { color: #888888; font-size: 14px; font-weight: 800; text-transform: uppercase; }
    .cyan-val { color: #00d4ff; font-size: 35px; font-weight: 900; }
    .bm-val { color: #444444; font-size: 12px; font-weight: bold; }

    /* تمييز Total Patients */
    .total-pt-card {
        background: linear-gradient(145deg, #0f0f0f, #050505);
        border-left: 6px solid #FFD700; border-radius: 10px; padding: 20px; text-align: center;
    }
    .total-pt-val { color: #FFD700; font-size: 55px; font-weight: 900; line-height: 1; margin: 10px 0; }
    
    /* الشرطة المائلة 36pt */
    .slash-style { color: #00d4ff; font-size: 36px; font-weight: 300; margin-right: 10px; }
    .side-title { color: #888888; font-size: 18px; font-weight: bold; display: flex; align-items: center; }

    .dev-card { background: #0a0a0a; border: 1px solid #1a1a1a; border-radius: 8px; padding: 10px; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. البيانات
data_source = [
    {
        "period": "3Q 2025", "week": "W01",
        "squares": [("Falls", 0.0, 0.18), ("Injuries", 0.0, 0.04), ("HAPI %", 6.67, 4.58), ("CLABSI", 1.50, 3.38), ("CAUTI", 0.0, 0.44), ("VAP", 1.2, 2.1)],
        "circles": [("Restraints", 0.45, 0.90), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0), ("Nursing Hr", 14.5, 12.0), ("Education", 85.01, 70.59), ("C-Diff", 0.0, 0.12)],
        "total_pt": 52, "vents": 14, "foley": 18, "cvc": 9
    },
    {
        "period": "2Q 2024", "week": "W02",
        "squares": [("Falls", 0.24, 0.06), ("Injuries", 0.24, 0.01), ("HAPI %", 14.29, 6.54), ("CLABSI", 1.28, 2.67), ("CAUTI", 0.70, 0.99), ("VAP", 2.1, 2.1)],
        "circles": [("Restraints", 0.70, 0.96), ("VAE Rate", 2.17, 3.4), ("Turnover", 3.1, 3.0), ("Nursing Hr", 12.8, 12.0), ("Education", 82.99, 70.59), ("C-Diff", 0.1, 0.12)],
        "total_pt": 46, "vents": 11, "foley": 15, "cvc": 10
    }
]
d = data_source[st.session_state.step % 2]

# العنوان الرئيسي
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 45px; margin-bottom:0;'>ICU STRATEGIC HUB</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #555; font-weight: bold;'>Data Cycle: {d['period']}</p>", unsafe_allow_html=True)

# 4. المربعات المتموجة
cols1 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['squares']):
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="wave-container"><div class="z-layer">
            <div class="gray-label">{lab}</div>
            <div class="cyan-val" style="color:{color}">{val}</div>
            <div class="bm-val">BM: {bm}</div>
        </div></div>""", unsafe_allow_html=True)

# 5. الدوائر المتموجة
cols2 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['circles']):
    is_rev = "Hr" in lab or "Education" in lab
    color = "#00ffaa" if (val >= bm if is_rev else val <= bm) else "#ff4b4b"
    with cols2[i]:
        st.markdown(f"""<div class="wave-circle-outer"><div class="z-layer">
            <div class="cyan-val" style="font-size: 26px; color:{color}">{val}</div>
            <div class="bm-val" style="color:#888;">BM: {bm}</div>
        </div></div>
        <div class="gray-label" style="text-align:center; margin-top:10px; font-size:12px;">{lab}</div>""", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:40px 0;'>", unsafe_allow_html=True)

# 6. الجزء السفلي
c1, c2 = st.columns([1, 2.5])

with c1:
    st.markdown(f'<div class="side-title"><span class="slash-style">//</span> UNIT OCCUPANCY</div>', unsafe_allow_html=True)
    # Total Patient - كبير ومميز
    st.markdown(f"""<div class="total-pt-card">
        <div class="gray-label" style="color:#FFD700;">Total Patients</div>
        <div class="total-pt-val">{d['total_pt']}</div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    for l, v in [("Ventilators", d['vents']), ("Foley Cath", d['foley']), ("Central Line", d['cvc'])]:
        st.markdown(f"""<div class="dev-card">
            <span style="float:right; color:#00d4ff; font-weight:900; font-size:20px;">{v}</span>
            <span class="gray-label" style="font-size:12px;">{l}</span>
        </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="side-title" style="margin-left:20px;"><span class="slash-style">//</span> PERFORMANCE TRENDS</div>', unsafe_allow_html=True)
    
    labels = [s[0] for s in d['squares']]
    vals = [s[1] for s in d['squares']]
    bms = [s[2] for s in d['squares']]

    fig = go.Figure()
    # بار Unit مع تأثير 3D Gradient
    fig.add_trace(go.Bar(
        x=labels, y=vals, name="Unit",
        marker=dict(color='#00d4ff', line=dict(color='#00ffff', width=1)),
        text=vals, textposition='outside'
    ))
    # بار Benchmark بلون داكن
    fig.add_trace(go.Bar(
        x=labels, y=bms, name="Benchmark",
        marker=dict(color='#1a1a1a', line=dict(color='#333', width=1)),
        text=bms, textposition='outside'
    ))

    fig.update_layout(
        height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#888'), margin=dict(t=50),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center")
    )
    fig.update_yaxes(showgrid=True, gridcolor='#111')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# تحديث تلقائي كل 15 ثانية
time.sleep(15)
st.session_state.step += 1
st.rerun()
