import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="Matrix ICU", layout="wide", initial_sidebar_state="collapsed")

# 2. Matrix CSS - معالجة التداخل ومنع التصاق العناصر
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #00ff00; overflow-x: hidden; }
    
    /* منع التداخل في الأعمدة */
    [data-testid="stHorizontalBlock"] { gap: 1rem; }

    /* المربعات المتحركة (Matrix Squares) */
    .matrix-box {
        position: relative; background-color: #000; border-radius: 10px;
        height: 150px; display: flex; flex-direction: column; justify-content: center;
        text-align: center; overflow: hidden; margin: 10px 0;
    }
    .matrix-box::before {
        content: ''; position: absolute; width: 150%; height: 150%;
        background: conic-gradient(#00ff00, #001a00, #00ff00);
        animation: rotate 4s linear infinite; top: 50%; left: 50%;
    }
    .matrix-box::after {
        content: ''; position: absolute; background-color: #000;
        inset: 4px; border-radius: 8px;
    }

    /* الدوائر المتحركة (Matrix Circles) */
    .matrix-circle-outer {
        position: relative; width: 140px; height: 140px; border-radius: 50%;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin: auto; background-color: #000; overflow: hidden;
    }
    .matrix-circle-outer::before {
        content: ''; position: absolute; width: 150%; height: 150%;
        background: conic-gradient(#00ff00, #003300, #00ff00);
        animation: rotate 6s linear infinite; top: 50%; left: 50%;
    }
    .matrix-circle-outer::after {
        content: ''; position: absolute; background-color: #000;
        inset: 5px; border-radius: 50%;
    }

    @keyframes rotate {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    /* النصوص داخل العناصر */
    .content-layer { position: relative; z-index: 10; padding: 5px; }
    .label-style { color: #00ff00; font-size: 13px; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; }
    .value-style { color: #00ff00; font-size: 30px; font-weight: 900; text-shadow: 0 0 10px #00ff00; }
    .bench-style { color: #004400; font-size: 11px; font-weight: bold; }

    /* كروت الأجهزة */
    .m-device { border: 1px solid #00ff00; border-left: 5px solid #00ff00; padding: 10px; margin-bottom: 8px; border-radius: 5px; background: #000; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. البيانات بالمسميات القديمة
data = [
    {
        "period": "3Q 2025", "week": "W01",
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
        "period": "2Q 2024", "week": "W02",
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

d = data[st.session_state.step % 2]

st.markdown(f"<h1 style='text-align: center; color: #00ff00; text-shadow: 0 0 15px #00ff00;'>ICU MATRIX CORE | {d['period']}</h1>", unsafe_allow_html=True)

# 4. المربعات (العلوي)
cols1 = st.columns(6)
for i, (lab, val, bench) in enumerate(d['squares']):
    with cols1[i]:
        st.markdown(f"""
        <div class="matrix-box"><div class="content-layer">
            <div class="label-style">{lab}</div>
            <div class="value-style">{val}</div>
            <div class="bench-style">T: {bench}</div>
        </div></div>""", unsafe_allow_html=True)

st.write("") # مسافة فاصلة لمنع التداخل

# 5. الدوائر (السفلي)
cols2 = st.columns(6)
for i, (lab, val, bench) in enumerate(d['circles']):
    with cols2[i]:
        st.markdown(f"""
        <div class="matrix-circle-outer"><div class="content-layer">
            <div class="value-style" style="font-size:22px;">{val}</div>
            <div class="bench-style" style="color:#fff;">T: {bench}</div>
        </div></div>
        <div style="text-align:center; color:#00ff00; font-size:11px; font-weight:bold; margin-top:8px; text-transform:uppercase;">{lab}</div>
        """, unsafe_allow_html=True)

st.markdown("<hr style='border-color: #003300; margin: 30px 0;'>", unsafe_allow_html=True)

# 6. الجزء السفلي (الأجهزة والرسم البياني)
c1, c2 = st.columns([1, 2.5])
with c1:
    st.markdown(f"<p style='color:#00ff00; font-weight:bold; font-size:13px;'>CONNECTED SYSTEMS ({d['week']})</p>", unsafe_allow_html=True)
    for name, val in d['devs']:
        st.markdown(f"""
        <div class="m-device">
            <span style="float:right; color:#00ff00; font-size:22px; font-weight:900;">{val}</span>
            <span style="color:#00ff00; font-size:11px; font-weight:bold;">{name}</span>
        </div>""", unsafe_allow_html=True)

with c2:
    labels = [s[0] for s in d['squares']]
    vals = [s[1] for s in d['squares']]
    fig = go.Figure(go.Bar(x=labels, y=vals, marker_color='#00ff00', text=vals, textposition='outside'))
    fig.update_layout(height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(color='#00ff00', size=11), margin=dict(l=0, r=0, t=30, b=0))
    fig.update_yaxes(showgrid=True, gridcolor='#001a00', zeroline=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# تحديث تلقائي كل 15 ثانية
time.sleep(15)
st.session_state.step += 1
st.rerun()
