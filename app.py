import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS - تثبيت العلوي وتنسيق العدادات
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* === الجزء العلوي (مثبت) === */
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

    /* === الجزء السفلي المطور === */
    .census-box-mini {
        background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; 
        padding: 15px 25px; text-align: left; max-width: 250px; margin-bottom: 20px;
    }
    .census-label-mini { color: #FFD700; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    .census-num-mini { color: #FFD700; font-size: 40px; font-weight: 900; line-height: 1; margin: 5px 0; }
    .occ-text-mini { color: #FFD700; font-size: 13px; font-weight: bold; }

    .gauge-label-bottom {
        color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase;
        margin-top: -20px; text-align: center; letter-spacing: 1px;
    }

    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; }
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
occ_percent = round((d['census'] / 36) * 100, 1)

# دالة لإنشاء عداد نظيف (بدون عنوان داخلي)
def create_clean_gauge(value, max_val, color_scheme):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        number = {'font': {'size': 38, 'color': '#fff', 'family': 'Arial Black'}},
        gauge = {
            'axis': {'range': [None, max_val], 'tickvals': []},
            'bar': {'color': "#222"},
            'bgcolor': "#000",
            'borderwidth': 0,
            'steps': [
                {'range': [0, color_scheme[0]], 'color': "#00ffaa"},
                {'range': [color_scheme[0], color_scheme[1]], 'color': "#FFD700"},
                {'range': [color_scheme[1], max_val], 'color': "#ff4b4b"}
            ],
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      margin=dict(t=10, b=0, l=10, r=10), height=130)
    return fig

# الهيدر
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 50px; font-weight:900; letter-spacing: 3px;'>ICU DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #444; font-weight: bold; font-size: 20px; margin-bottom: 30px;'>PERIOD: {d['period']}</p>", unsafe_allow_html=True)

# 4. العلوي (مثبت)
cols1 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['squares']):
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="kpi-card"><div class="z-layer"><div class="gray-label">{lab}</div><div class="cyan-val" style="color:{color}">{val}</div><div class="bm-full-text">BENCHMARK: {bm}</div></div></div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
cols2 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['circles']):
    is_rev = any(x in lab for x in ["Hr", "Edu"])
    color = "#00ffaa" if (val >= bm if is_rev else val <= bm) else "#ff4b4b"
    with cols2[i]:
        st.markdown(f"""<div style="text-align:center;"><div class="circle-container"><div class="z-layer"><div class="cyan-val" style="font-size: 45px; color:{color}">{val}</div></div></div><div class="gray-label" style="margin-top:20px; font-size:24px;">{lab}</div><div class="bm-full-text" style="color:#333;">BENCHMARK: {bm}</div></div>""", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:60px 0;'>", unsafe_allow_html=True)

# 5. السفلي المطور (Census + Attached Devices)
c1, c2 = st.columns([2.0, 2.0])

with c1:
    st.markdown(f"""<div class="census-box-mini"><div class="census-label-mini">Current Census</div><div class="census-num-mini">{d['census']}</div><div class="occ-text-mini">Occupancy: {occ_percent}% (of 36)</div></div>""", unsafe_allow_html=True)
    
    st.markdown('<div class="side-header">ATTACHED DEVICES</div>', unsafe_allow_html=True)
    
    g_cols = st.columns(4)
    dev_info = [("Pt with ETT", d['ett'], 36, [10, 20]), ("Pt with Foley", d['foley'], 36, [15, 25]), 
                ("Pt with CVC", d['cvc'], 36, [8, 15]), ("Avg Stay", d['stay'], 10, [3, 6])]
    
    for i, (name, val, mx, clrs) in enumerate(dev_info):
        with g_cols[i]:
            st.plotly_chart(create_clean_gauge(val, mx, clrs), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<div class="gauge-label-bottom">{name}</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="side-header" style="margin-left:20px;">PERFORMANCE ANALYTICS</div>', unsafe_allow_html=True)
    labels = [s[0] for s in d['squares']]; vals = [s[1] for s in d['squares']]; bms = [s[2] for s in d['squares']]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=vals, name="Actual", marker_color='#00d4ff', text=vals, textposition='outside'))
    fig.add_trace(go.Bar(x=labels, y=bms, name="Benchmark", marker_color='#1a1a1a', text=bms, textposition='outside'))
    fig.update_layout(height=450, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=0, l=0, r=0), bargap=0.25, legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center", font=dict(color="#888")), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#111'))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

time.sleep(15)
st.session_state.step += 1
st.rerun()
