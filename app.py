import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المعتمد - حدود قوية وتوهج احترافي
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* تعزيز حدود المربعات */
    .kpi-card {
        position: relative; background-color: #0a0a0a; border-radius: 20px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 260px; margin-bottom: 20px;
        border: 2px solid #1a1a1a; 
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2); 
    }
    .kpi-card::before, .circle-container::before {
        content: ''; position: absolute; width: 250%; height: 250%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .kpi-card::after, .circle-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 5px; border-radius: 16px;
    }
    
    /* تعزيز حدود الدوائر */
    .circle-container {
        position: relative; width: 280px; height: 280px; border-radius: 50%;
        margin: auto; overflow: hidden; display: flex; justify-content: center; align-items: center; text-align: center;
        border: 2px solid #1a1a1a;
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.25);
    }
    .circle-container::after { border-radius: 50%; inset: 10px; }
    
    @keyframes rotate-wave { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }
    
    .content-box { position: relative; z-index: 10; width: 100%; padding: 10px; }
    .label-full { color: #aaaaaa; font-size: 22px; font-weight: 900; text-transform: uppercase; margin-bottom: 5px; }
    .val-full { color: #00d4ff; font-size: 50px; font-weight: 900; line-height: 1; }
    .bm-full { color: #444444; font-size: 14px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }

    /* الجزء السفلي - المربعات الذهبية */
    .census-box-mini { 
        background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; 
        padding: 10px 20px; text-align: left; margin-bottom: 15px;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.1);
    }
    .census-num-mini { color: #FFD700; font-size: 38px; font-weight: 900; }
    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; }
    .gauge-label-bottom { color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase; margin-top: -20px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة حركة البيانات (تغيير كل 15 ثانية)
if 'step' not in st.session_state: st.session_state.step = 0

# داتا العلوي (Quarters من الـ PDF)
pdf_quarters = [
    {"q": "3Q 2024", "sq": [0.36, 0.36, 6.90, 2.63, 1.02, 0.00], "sq_bm": [0.28, 0.05, 4.60, 1.20, 0.40, 1.89],
     "cir": [20.69, 0.00, 4.69, 12.54, 68.25, 0.00], "cir_bm": [6.32, 1.89, 4.51, 19.20, 83.36, 0.25]},
    {"q": "1Q 2025", "sq": [1.59, 0.80, 4.17, 3.02, 0.00, 6.69], "sq_bm": [0.12, 0.03, 4.96, 1.26, 0.43, 1.91],
     "cir": [12.50, 6.69, 1.43, 12.87, 70.00, 0.00], "cir_bm": [8.23, 1.91, 3.97, 19.15, 83.78, 0.26]}
]

# داتا السفلي (Weeks من صور الديفيس) - تتغير مع الـ Step
device_weeks = [
    {"w": "Week 1", "census": 23, "occ": "78%", "vals": [12, 16, 4, 3.5]},
    {"w": "Week 2", "census": 28, "occ": "93%", "vals": [11, 15, 6, 4.5]},
    {"w": "Week 3", "census": 25, "occ": "85%", "vals": [13, 18, 5, 4.2]}
]

cur_pdf = pdf_quarters[st.session_state.step % len(pdf_quarters)]
cur_dev = device_weeks[st.session_state.step % len(device_weeks)]

# --- الجزء العلوي (مربعات ودواير) ---
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 50px; font-weight:900;'>ICU DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #FFD700; font-size: 20px; font-weight:bold;'>QUARTERLY PERFORMANCE: {cur_pdf['q']}</p>", unsafe_allow_html=True)

sq_names = ["Falls", "Injury Falls", "HAPI %", "CLABSI", "CAUTI", "VAE Rate"]
c1 = st.columns(6)
for i in range(6):
    v, b = cur_pdf['sq'][i], cur_pdf['sq_bm'][i]
    color = "#00ffaa" if v <= b else "#ff4b4b"
    with c1[i]:
        st.markdown(f'<div class="kpi-card"><div class="content-box"><div class="label-full">{sq_names[i]}</div><div class="val-full" style="color:{color}">{v}</div><div class="bm-full">BENCHMARK: {b}</div></div></div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
cir_names = ["Restraints", "VAE Rate", "Turnover", "Nurse Hr", "RN Edu", "C-Diff"]
c2 = st.columns(6)
for i in range(6):
    v, b = cur_pdf['cir'][i], cur_pdf['cir_bm'][i]
    is_rev = any(x in cir_names[i] for x in ["Hr", "Edu"])
    color = "#00ffaa" if (v >= b if is_rev else v <= b) else "#ff4b4b"
    with c2[i]:
        st.markdown(f'<div class="circle-container"><div class="content-box"><div class="label-full" style="font-size:18px;">{cir_names[i]}</div><div class="val-text" style="color:{color}; font-size:42px;">{v}</div><div class="bm-text">BENCHMARK: {b}</div></div></div>', unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:40px 0;'>", unsafe_allow_html=True)

# --- الجزء السفلي (Attached Devices - أسبوعي متحرك) ---
col_left, col_right = st.columns([2.2, 1.8])

with col_left:
    sub_c1, sub_c2 = st.columns(2)
    with sub_c1:
        st.markdown(f'<div class="census-box-mini"><div style="color:#555; font-size:12px; font-weight:bold;">CURRENT CENSUS</div><div class="census-num-mini">{cur_dev["census"]}</div></div>', unsafe_allow_html=True)
    with sub_c2:
        st.markdown(f'<div class="census-box-mini" style="border-color:#00d4ff;"><div style="color:#555; font-size:12px; font-weight:bold;">OCCUPANCY RATE</div><div class="census-num-mini" style="color:#00d4ff;">{cur_dev["occ"]}</div></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="side-header">ATTACHED DEVICES <span style="color:#FFD700; font-size:16px;">({cur_dev["w"]})</span></div>', unsafe_allow_html=True)
    
    g_cols = st.columns(4)
    dev_info = [("Pt with ETT", 36, [10, 18]), ("Pt with Foley", 36, [24, 30]), ("Pt with CVC", 36, [16, 22]), ("Avg Stay", 10, [4, 6])]
    for i, (name, mx, steps) in enumerate(dev_info):
        with g_cols[i]:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = cur_dev['vals'][i],
                number = {'font': {'size': 35, 'color': '#fff'}},
                gauge = {'axis': {'range': [None, mx], 'tickvals': []}, 'bar': {'color': "#222"}, 'bgcolor': "#000",
                         'steps': [{'range': [0, steps[0]], 'color': "#00ffaa"}, {'range': [steps[0], steps[1]], 'color': "#FFD700"}, {'range': [steps[1], mx], 'color': "#ff4b4b"}]}
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, l=10, r=10), height=120)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<div class="gauge-label-bottom">{name}</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="side-header" style="margin-left:20px;">PERFORMANCE ANALYTICS</div>', unsafe_allow_html=True)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=sq_names, y=cur_pdf['sq'], name="Current", marker_color='#00d4ff', text=cur_pdf['sq'], textposition='outside'))
    fig_bar.add_trace(go.Bar(x=sq_names, y=cur_pdf['sq_bm'], name="Benchmark", marker_color='#1a1a1a'))
    fig_bar.update_layout(height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          margin=dict(t=20, b=20, l=0, r=0), legend=dict(font=dict(color="#888"), orientation="h", y=1.2))
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي لكل 15 ثانية (يغير Quarter فوق و Week تحت)
time.sleep(15)
st.session_state.step += 1
st.rerun()
