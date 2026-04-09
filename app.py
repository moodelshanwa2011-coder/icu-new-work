import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الشاشة الكاملة
st.set_page_config(page_title="ICU Executive Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS - الحفاظ على التصميم العملاق وتنسيق العدادات الجديدة
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; overflow: hidden; }
    
    /* --- الجزء العلوي العملاق --- */
    .kpi-card {
        position: relative; background-color: #0a0a0a; border-radius: 20px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 260px; margin-bottom: 30px;
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
        position: relative; width: 240px; height: 240px; border-radius: 50%;
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
    .gray-label { color: #aaaaaa; font-size: 28px; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; }
    .cyan-val { color: #00d4ff; font-size: 65px; font-weight: 900; }
    .bm-full-text { color: #444; font-size: 14px; font-weight: bold; margin-top: 10px; }

    /* --- الجزء السفلي المتكامل --- */
    .census-box-mini {
        background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; 
        padding: 20px; text-align: left; margin-bottom: 20px;
    }
    .census-num-mini { color: #FFD700; font-size: 45px; font-weight: 900; line-height: 1; }
    
    .gauge-label-bottom {
        color: #fff; font-size: 13px; font-weight: 900; text-transform: uppercase;
        margin-top: -25px; text-align: center;
    }
    .side-header { color: #00d4ff; font-size: 24px; font-weight: 900; margin-bottom: 20px; text-transform: uppercase; }
    .week-tag { background: #FFD700; color: #000; padding: 2px 10px; border-radius: 4px; font-size: 16px; margin-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك البيانات (دورة الأسابيع)
if 'cycle' not in st.session_state: st.session_state.cycle = 0

weekly_data = [
    {"date": "March 07", "census": 31, "ett": 11, "foley": 28, "cvc": 19, "stay": 4.2},
    {"date": "March 14", "census": 33, "ett": 13, "foley": 30, "cvc": 21, "stay": 4.5},
    {"date": "March 21", "census": 29, "ett": 10, "foley": 25, "cvc": 17, "stay": 3.9},
    {"date": "March 28", "census": 35, "ett": 15, "foley": 32, "cvc": 24, "stay": 5.1},
    {"date": "April 04", "census": 32, "ett": 12, "foley": 29, "cvc": 20, "stay": 4.3}
]

curr = weekly_data[st.session_state.cycle % len(weekly_data)]

def draw_gauge(v, mx, steps):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=v,
        number={'font': {'size': 35, 'color': '#fff', 'family': 'Arial Black'}},
        gauge={
            'axis': {'range': [None, mx], 'tickvals': []},
            'bar': {'color': "#222"}, 'bgcolor': "#000", 'borderwidth': 0,
            'steps': [
                {'range': [0, steps[0]], 'color': "#00ffaa"},
                {'range': [steps[0], steps[1]], 'color': "#FFD700"},
                {'range': [steps[1], mx], 'color': "#ff4b4b"}
            ]
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, l=10, r=10), height=140)
    return fig

# --- الهيكل العام ---
st.markdown("<h1 style='text-align: center; color: #00d4ff; font-size: 55px; font-weight:900; margin-bottom:0;'>ICU COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #555; font-size: 20px; margin-bottom:40px;'>LIVE DATA STREAM • {curr['date']}, 2026</p>", unsafe_allow_html=True)

# 4. المربعات والدواير (الجزء العلوي المثبت)
c_sq = st.columns(6)
sq_data = [("Falls", 0.0, 0.18), ("Injuries", 0.0, 0.04), ("HAPI %", 6.67, 4.58), ("CLABSI", 1.5, 3.3), ("CAUTI", 0.0, 0.4), ("VAP", 1.2, 2.1)]
for i, (l, v, b) in enumerate(sq_data):
    clr = "#00ffaa" if v <= b else "#ff4b4b"
    with c_sq[i]:
        st.markdown(f'<div class="kpi-card"><div class="z-layer"><div class="gray-label">{l}</div><div class="cyan-val" style="color:{clr}">{v}</div><div class="bm-full-text">BM: {b}</div></div></div>', unsafe_allow_html=True)

st.write("") # فاصل
c_cir = st.columns(6)
cir_data = [("Restraints", 0.45, 0.9), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0), ("Nurse Hr", 14.5, 12.0), ("RN Edu", 85.0, 70.5), ("C-Diff", 0.0, 0.1)]
for i, (l, v, b) in enumerate(cir_data):
    rev = "Hr" in l or "Edu" in l
    clr = "#00ffaa" if (v >= b if rev else v <= b) else "#ff4b4b"
    with c_cir[i]:
        st.markdown(f'<div style="text-align:center;"><div class="circle-container"><div class="z-layer"><div class="cyan-val" style="font-size:48px; color:{clr}">{v}</div></div></div><div class="gray-label" style="margin-top:20px; font-size:24px;">{l}</div></div>', unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:50px 0;'>", unsafe_allow_html=True)

# 5. الجزء السفلي (العدادات + التحليل)
b1, b2 = st.columns([2.3, 1.7])

with b1:
    st.markdown(f'<div class="side-header">ATTACHED DEVICES <span class="week-tag">{curr["date"]}</span></div>', unsafe_allow_html=True)
    g_cols = st.columns(4)
    devs = [("Pt with ETT", curr['ett'], 36, [10, 18]), ("Pt with Foley", curr['foley'], 36, [24, 30]), ("Pt with CVC", curr['cvc'], 36, [16, 22]), ("Avg Stay", curr['stay'], 10, [4, 6])]
    for i, (n, v, m, s) in enumerate(devs):
        with g_cols[i]:
            st.plotly_chart(draw_gauge(v, m, s), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<div class="gauge-label-bottom">{n}</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="census-box-mini"><div style="color:#FFD700; font-size:14px; font-weight:bold; letter-spacing:1px;">CURRENT CENSUS</div><div class="census-num-mini">{curr["census"]} <span style="font-size:20px; color:#555;">/ 36</span></div></div>', unsafe_allow_html=True)

with b2:
    st.markdown('<div class="side-header">BENCHMARK COMPARISON</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[x[0] for x in sq_data], y=[x[1] for x in sq_data], name="Actual", marker_color='#00d4ff'))
    fig.add_trace(go.Bar(x=[x[0] for x in sq_data], y=[x[2] for x in sq_data], name="Benchmark", marker_color='#1a1a1a'))
    fig.update_layout(height=350, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), legend=dict(orientation="h", y=1.2, x=0.5, xanchor="center"))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# حلقة التحديث
time.sleep(15)
st.session_state.cycle += 1
st.rerun()
