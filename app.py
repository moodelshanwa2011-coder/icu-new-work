import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Command Center", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المتطور: توزيع الأجهزة على شكل قوس
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* تأثير الموجة النيونية */
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

    /* مسميات رمادية وقيم واضحة */
    .gray-label { color: #aaaaaa; font-size: 13px; font-weight: 800; text-transform: uppercase; }
    .cyan-val { color: #00d4ff; font-size: 35px; font-weight: 900; }
    
    /* تصميم التعداد المركزي */
    .census-center {
        background: radial-gradient(circle, #111 0%, #000 100%);
        border: 2px solid #333; border-radius: 50%;
        width: 220px; height: 220px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.1);
        margin: auto; z-index: 5; position: relative;
    }

    /* حاوية نصف الدائرة */
    .semi-circle-layout {
        position: relative; height: 450px; display: flex; justify-content: center; align-items: center;
    }

    /* وضع الأجهزة على القوس */
    .arc-item {
        position: absolute; background: rgba(10, 10, 10, 0.9);
        border-left: 4px solid #00d4ff; border-radius: 10px 40px 40px 10px;
        padding: 15px 25px; min-width: 180px;
        transition: 0.3s;
    }
    .arc-item:hover { background: #1a1a1a; transform: scale(1.05); }
    
    /* توزيع العناصر بالزوايا */
    .pos-1 { transform: translate(-220px, -120px); } /* Top Left */
    .pos-2 { transform: translate(220px, -120px); }  /* Top Right */
    .pos-3 { transform: translate(-250px, 40px); }   /* Mid Left */
    .pos-4 { transform: translate(250px, 40px); }    /* Mid Right */
    .pos-5 { transform: translate(0px, 160px); border-left: 4px solid #FFD700; } /* Bottom Center (Occupancy) */

    .dev-title { color: #888; font-size: 14px; font-weight: bold; display: block; }
    .dev-value { color: #00d4ff; font-size: 26px; font-weight: 900; }
    .occ-value { color: #FFD700; font-size: 26px; font-weight: 900; }

    .side-title { color: #00d4ff; font-size: 24px; font-weight: 900; text-align: center; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. داتا المؤشرات الـ 12
data_source = [
    {
        "period": "3Q 2025",
        "squares": [("Falls", 0.0, 0.18), ("Injuries", 0.0, 0.04), ("HAPI %", 6.67, 4.58), ("CLABSI Rate", 1.50, 3.38), ("CAUTI Rate", 0.0, 0.44), ("VAP Rate", 1.2, 2.1)],
        "circles": [("Restraints", 0.45, 0.90), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0), ("Nursing Hr", 14.5, 12.0), ("RN Education", 85.0, 70.5), ("C-Diff", 0.0, 0.12)],
        "census": 32, "occ": "88.9%", "ett": 14, "foley": 18, "cvc": 9, "stay": 3.4
    },
    {
        "period": "2Q 2024",
        "squares": [("Falls", 0.2, 0.1), ("Injuries", 0.1, 0.0), ("HAPI %", 10.0, 6.0), ("CLABSI Rate", 1.0, 2.5), ("CAUTI Rate", 0.5, 0.8), ("VAP Rate", 2.0, 2.1)],
        "circles": [("Restraints", 0.60, 0.90), ("VAE Rate", 2.0, 3.4), ("Turnover", 3.0, 3.0), ("Nursing Hr", 12.0, 12.0), ("RN Education", 80.0, 70.5), ("C-Diff", 0.1, 0.12)],
        "census": 30, "occ": "83.3%", "ett": 11, "foley": 15, "cvc": 10, "stay": 2.8
    }
]
d = data_source[st.session_state.step % 2]

# الهيدر
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 40px; font-weight: 900;'>ICU STRATEGIC COMMAND</h1>", unsafe_allow_html=True)

# صف المربعات الـ 6
cols1 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['squares']):
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="wave-container"><div class="z-layer">
            <div class="gray-label">{lab}</div>
            <div class="cyan-val" style="color:{color}">{val}</div>
            <div style="color:#444; font-size:11px; font-weight:bold;">BM: {bm}</div>
        </div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4. الجزء السفلي: توزيع نصف الدائرة والبار
c1, c2 = st.columns([1.5, 2])

with c1:
    st.markdown('<div class="side-title">36 CAPACITY STATUS</div>', unsafe_allow_html=True)
    
    # التوزيع الدائري
    st.markdown(f"""
    <div class="semi-circle-layout">
        <div class="census-center">
            <span class="gray-label" style="color:#FFD700">Unit Census</span>
            <span style="color:#FFD700; font-size:60px; font-weight:900;">{d['census']}</span>
        </div>
        
        <div class="arc-item pos-1"><span class="dev-title">Pt with ETT</span><span class="dev-value">{d['ett']}</span></div>
        <div class="arc-item pos-2"><span class="dev-title">Pt with Foley</span><span class="dev-value">{d['foley']}</span></div>
        <div class="arc-item pos-3"><span class="dev-title">Pt with CVC</span><span class="dev-value">{d['cvc']}</span></div>
        <div class="arc-item pos-4"><span class="dev-title">Avg Stay</span><span class="dev-value">{d['stay']}</span></div>
        <div class="arc-item pos-5"><span class="dev-title" style="color:#FFD700">Occupancy Rate</span><span class="occ-value">{d['occ']}</span></div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown('<div class="side-title">PERFORMANCE TRENDS</div>', unsafe_allow_html=True)
    
    # بار تشارت احترافي جداً
    labels = [s[0] for s in d['squares']]
    vals = [s[1] for s in d['squares']]
    bms = [s[2] for s in d['squares']]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels, y=vals, name="Actual",
        marker=dict(color='#00d4ff', line=dict(color='#00ffff', width=1)),
        text=vals, textposition='outside',
        textfont=dict(size=14, color='#ffffff', family="Arial Black")
    ))
    fig.add_trace(go.Bar(
        x=labels, y=bms, name="Benchmark",
        marker=dict(color='rgba(80, 80, 80, 0.3)', line=dict(color='#555', width=1)),
        text=bms, textposition='outside',
        textfont=dict(size=12, color='#aaa')
    ))

    fig.update_layout(
        height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(orientation="h", y=1.2, x=0.5, xanchor="center", font=dict(color="#fff")),
        xaxis=dict(showgrid=False, tickfont=dict(color="#888")),
        yaxis=dict(showgrid=True, gridcolor='#111', tickfont=dict(color="#444")),
        bargap=0.2
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# صف الدوائر الـ 6 في الأسفل
st.markdown("<br>", unsafe_allow_html=True)
cols3 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['circles']):
    is_rev = any(x in lab for x in ["Hr", "Education"])
    color = "#00ffaa" if (val >= bm if is_rev else val <= bm) else "#ff4b4b"
    with cols3[i]:
        st.markdown(f"""
        <div style="text-align:center;">
            <div style="color:{color}; font-size:24px; font-weight:900;">{val}</div>
            <div class="gray-label" style="font-size:11px;">{lab}</div>
            <div style="color:#333; font-size:10px;">BM: {bm}</div>
        </div>
        """, unsafe_allow_html=True)

time.sleep(15)
st.session_state.step += 1
st.rerun()
