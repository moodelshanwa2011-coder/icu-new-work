import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المعتمد - مسميات كاملة وتنسيق ثابت
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* المربعات العلوية */
    .kpi-card {
        position: relative; background-color: #0a0a0a; border-radius: 20px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 260px; margin-bottom: 20px;
    }
    .kpi-card::before, .circle-container::before {
        content: ''; position: absolute; width: 250%; height: 250%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .kpi-card::after, .circle-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 6px; border-radius: 16px;
    }
    
    /* الدوائر المتوهجة */
    .circle-container {
        position: relative; width: 280px; height: 280px; border-radius: 50%;
        margin: auto; overflow: hidden; display: flex; justify-content: center; align-items: center; text-align: center;
    }
    .circle-container::after { border-radius: 50%; inset: 10px; }
    
    @keyframes rotate-wave { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }
    
    .content-box { position: relative; z-index: 10; width: 100%; padding: 10px; }
    .label-full { color: #aaaaaa; font-size: 22px; font-weight: 900; text-transform: uppercase; margin-bottom: 5px; }
    .val-full { color: #00d4ff; font-size: 50px; font-weight: 900; line-height: 1; }
    .bm-full { color: #444444; font-size: 14px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }

    /* الجزء السفلي الخاص بالديفيس */
    .census-box-mini { background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; padding: 15px 25px; text-align: left; max-width: 250px; margin-bottom: 20px; }
    .census-num-mini { color: #FFD700; font-size: 40px; font-weight: 900; margin: 5px 0; }
    .gauge-label-bottom { color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase; margin-top: -20px; text-align: center; }
    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# 3. داتا الـ PDF (مقسمة كوارترات)
if 'step' not in st.session_state: st.session_state.step = 0
pdf_data = [
    {"q": "3Q 2024", "sq": [0.36, 0.36, 6.90, 2.63, 1.02, 0.00], "sq_bm": [0.28, 0.05, 4.60, 1.20, 0.40, 1.89],
     "cir": [20.69, 0.00, 4.69, 12.54, 68.25, 0.00], "cir_bm": [6.32, 1.89, 4.51, 19.20, 83.36, 0.25]},
    {"q": "1Q 2025", "sq": [1.59, 0.80, 4.17, 3.02, 0.00, 6.69], "sq_bm": [0.12, 0.03, 4.96, 1.26, 0.43, 1.91],
     "cir": [12.50, 6.69, 1.43, 12.87, 70.00, 0.00], "cir_bm": [8.23, 1.91, 3.97, 19.15, 83.78, 0.26]}
]
cur_pdf = pdf_data[st.session_state.step % len(pdf_data)]

# --- الجزء العلوي (مربعات ودواير) ---
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 50px; font-weight:900;'>ICU DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #FFD700; font-size: 20px; font-weight:bold;'>PERIOD: {cur_pdf['q']}</p>", unsafe_allow_html=True)

# المربعات (مسميات كاملة + BENCHMARK)
sq_names = ["Falls", "Injury Falls", "HAPI %", "CLABSI", "CAUTI", "VAE Rate"]
c1 = st.columns(6)
for i in range(6):
    val, bm = cur_pdf['sq'][i], cur_pdf['sq_bm'][i]
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with c1[i]:
        st.markdown(f"""<div class="kpi-card"><div class="content-box"><div class="label-full">{sq_names[i]}</div><div class="val-full" style="color:{color}">{val}</div><div class="bm-full">BENCHMARK: {bm}</div></div></div>""", unsafe_allow_html=True)

# الدوائر (مسميات كاملة + BENCHMARK)
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
cir_names = ["Restraints", "VAE Rate", "Turnover", "Nurse Hr", "RN Edu", "C-Diff"]
c2 = st.columns(6)
for i in range(6):
    val, bm = cur_pdf['cir'][i], cur_pdf['cir_bm'][i]
    is_rev = any(x in cir_names[i] for x in ["Hr", "Edu"])
    color = "#00ffaa" if (val >= bm if is_rev else val <= bm) else "#ff4b4b"
    with c2[i]:
        st.markdown(f"""<div class="circle-container"><div class="content-box"><div class="label-full" style="font-size:18px;">{cir_names[i]}</div><div class="val-full" style="color:{color}; font-size:42px;">{val}</div><div class="bm-full">BENCHMARK: {bm}</div></div></div>""", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:60px 0;'>", unsafe_allow_html=True)

# --- الجزء السفلي (Attached Devices - ثابت المسميات) ---
col_left, col_right = st.columns([2.2, 1.8])

with col_left:
    st.markdown("""<div class="census-box-mini"><div style="color:#555; font-size:12px; font-weight:bold; text-transform:uppercase;">Current Census</div><div class="census-num-mini">28</div></div>""", unsafe_allow_html=True)
    st.markdown('<div class="side-header">ATTACHED DEVICES</div>', unsafe_allow_html=True)
    
    g_cols = st.columns(4)
    dev_info = [("Pt with ETT", 11, 36, [10, 18]), ("Pt with Foley", 15, 36, [24, 30]), ("Pt with CVC", 6, 36, [16, 22]), ("Avg Stay", 4.5, 10, [4, 6])]
    for i, (name, val, mx, steps) in enumerate(dev_info):
        with g_cols[i]:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = val,
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

# تحديث كل 15 ثانية
time.sleep(15)
st.session_state.step += 1
st.rerun()
