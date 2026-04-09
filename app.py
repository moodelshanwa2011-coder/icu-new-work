import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS (النسخة الأصلية اللي عجبتك للجزء العلوي)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* الجزء العلوي - ثابت تماماً كما كان */
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
    .bm-full-text { color: #444444; font-size: 14px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }

    /* الجزء السفلي - الأجهزة والجداول */
    .census-box-mini {
        background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; 
        padding: 15px 25px; text-align: left; max-width: 250px; margin-bottom: 20px;
    }
    .census-num-mini { color: #FFD700; font-size: 40px; font-weight: 900; line-height: 1; margin: 5px 0; }
    .gauge-label-bottom {
        color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase;
        margin-top: -20px; text-align: center; letter-spacing: 1px;
    }
    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; }
    .week-text { color: #FFD700; font-size: 18px; font-weight: bold; margin-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة التوقيت (السيكل 7، 14، 21، 28 مارس و4 أبريل)
if 'week_index' not in st.session_state: st.session_state.week_index = 0

weekly_data = [
    {"date": "March 07", "census": 31, "ett": 11, "foley": 28, "cvc": 19, "stay": 4.2},
    {"date": "March 14", "census": 33, "ett": 13, "foley": 30, "cvc": 21, "stay": 4.5},
    {"date": "March 21", "census": 29, "ett": 10, "foley": 25, "cvc": 17, "stay": 3.9},
    {"date": "March 28", "census": 35, "ett": 15, "foley": 32, "cvc": 24, "stay": 5.1},
    {"date": "April 04", "census": 32, "ett": 12, "foley": 29, "cvc": 20, "stay": 4.3}
]
cur = weekly_data[st.session_state.week_index % len(weekly_data)]

def create_clean_gauge(v, mx, steps):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = v,
        number = {'font': {'size': 38, 'color': '#fff', 'family': 'Arial Black'}},
        gauge = {
            'axis': {'range': [None, mx], 'tickvals': []},
            'bar': {'color': "#222"}, 'bgcolor': "#000", 'borderwidth': 0,
            'steps': [
                {'range': [0, steps[0]], 'color': "#00ffaa"},
                {'range': [steps[0], steps[1]], 'color': "#FFD700"},
                {'range': [steps[1], mx], 'color': "#ff4b4b"}
            ],
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, l=10, r=10), height=130)
    return fig

# --- العرض الرئيسي ---

# العنوان العلوي (ثابت)
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 50px; font-weight:900; letter-spacing: 3px;'>ICU DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #444; font-weight: bold; font-size: 20px; margin-bottom: 30px;'>UNIT PERFORMANCE OVERVIEW</p>", unsafe_allow_html=True)

# 4. المربعات والدواير (ثابتة تماماً كما كانت)
cols1 = st.columns(6)
sqs = [("Falls", 0.0, 0.18), ("Injuries", 0.0, 0.04), ("HAPI %", 6.67, 4.58), ("CLABSI", 1.5, 3.3), ("CAUTI", 0.0, 0.4), ("VAP", 1.2, 2.1)]
for i, (lab, val, bm) in enumerate(sqs):
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="kpi-card"><div class="z-layer"><div class="gray-label">{lab}</div><div class="cyan-val" style="color:{color}">{val}</div><div class="bm-full-text">BENCHMARK: {bm}</div></div></div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
cols2 = st.columns(6)
cirs = [("Restraints", 0.45, 0.9), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0), ("Nurse Hr", 14.5, 12.0), ("RN Edu", 85.0, 70.5), ("C-Diff", 0.0, 0.1)]
for i, (lab, val, bm) in enumerate(cirs):
    is_rev = any(x in lab for x in ["Hr", "Edu"])
    color = "#00ffaa" if (val >= bm if is_rev else val <= bm) else "#ff4b4b"
    with cols2[i]:
        st.markdown(f"""<div style="text-align:center;"><div class="circle-container"><div class="z-layer"><div class="cyan-val" style="font-size: 45px; color:{color}">{val}</div></div></div><div class="gray-label" style="margin-top:20px; font-size:24px;">{lab}</div></div>""", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:60px 0;'>", unsafe_allow_html=True)

# 5. الجزء السفلي (التعديل المطلوب في منطقة الأجهزة فقط)
c1, c2 = st.columns([2.2, 1.8])
with c1:
    st.markdown(f"""<div class="census-box-mini"><div style="color:#FFD700; font-size:12px; font-weight:bold;">CURRENT CENSUS</div><div class="census-num-mini">{cur['census']}</div><div style="color:#FFD700; font-size:13px; font-weight:bold;">Occupancy: {round((cur['census']/36)*100,1)}%</div></div>""", unsafe_allow_html=True)
    
    # عنوان الأجهزة مع التاريخ المتحرك
    st.markdown(f'<div class="side-header">ATTACHED DEVICES <span class="week-text">({cur["date"]})</span></div>', unsafe_allow_html=True)
    
    g_cols = st.columns(4)
    devs = [("Pt with ETT", cur['ett'], 36, [10, 18]), ("Pt with Foley", cur['foley'], 36, [24, 30]), ("Pt with CVC", cur['cvc'], 36, [16, 22]), ("Avg Stay", cur['stay'], 10, [4, 6])]
    for i, (name, val, mx, s) in enumerate(devs):
        with g_cols[i]:
            st.plotly_chart(create_clean_gauge(val, mx, s), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<div class="gauge-label-bottom">{name}</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="side-header" style="margin-left:20px;">PERFORMANCE ANALYTICS</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[s[0] for s in sqs], y=[s[1] for s in sqs], name="Actual", marker_color='#00d4ff'))
    fig.add_trace(go.Bar(x=[s[0] for s in sqs], y=[s[2] for s in sqs], name="Benchmark", marker_color='#1a1a1a'))
    fig.update_layout(height=450, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=0, l=0, r=0), legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# حلقة التحديث كل 15 ثانية
time.sleep(15)
st.session_state.week_index += 1
st.rerun()
