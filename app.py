import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS "الأصلي" اللي بيثبت المسميات والعناوين لكل جزء
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* الكروت العلوية (PDF Data) */
    .kpi-card, .circle-container {
        position: relative; background-color: #0a0a0a; border-radius: 20px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; margin-bottom: 20px;
    }
    .kpi-card { height: 260px; }
    .circle-container { width: 280px; height: 280px; border-radius: 50%; margin: auto; }
    
    .kpi-card::before, .circle-container::before {
        content: ''; position: absolute; width: 250%; height: 250%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .kpi-card::after, .circle-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 6px; border-radius: 16px;
    }
    .circle-container::after { border-radius: 50%; inset: 10px; }
    @keyframes rotate-wave { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }
    
    .content-box { position: relative; z-index: 10; width: 100%; padding: 10px; }
    .label-text { color: #aaaaaa; font-size: 22px; font-weight: 900; text-transform: uppercase; margin-bottom: 5px; }
    .val-text { color: #00d4ff; font-size: 50px; font-weight: 900; line-height: 1; }
    .bm-text { color: #444444; font-size: 14px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }

    /* الجزء السفلي (الخاص بالديفيس - تصميم الصور) */
    .census-box-mini { background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; padding: 15px 25px; text-align: left; max-width: 250px; margin-bottom: 20px; }
    .census-num-mini { color: #FFD700; font-size: 40px; font-weight: 900; margin: 5px 0; }
    .gauge-label-bottom { color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase; margin-top: -20px; text-align: center; }
    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; }
    .device-sub { color: #555; font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة التوقيت (Quarter للعلوي، Week للسفلي)
if 'step' not in st.session_state: st.session_state.step = 0

# داتا العلوي (PDF) - تتغير كل Quarter
pdf_quarters = [
    {"q": "3Q 2024", "sq": [0.36, 0.36, 6.90, 2.63, 1.02, 0.00], "sq_bm": [0.28, 0.05, 4.60, 1.20, 0.40, 1.89]},
    {"q": "4Q 2024", "sq": [0.00, 0.00, 9.68, 1.80, 1.13, 1.60], "sq_bm": [0.14, 0.01, 4.61, 1.21, 0.54, 2.49]},
    {"q": "1Q 2025", "sq": [1.59, 0.80, 4.17, 3.02, 0.00, 6.69], "sq_bm": [0.12, 0.03, 4.96, 1.26, 0.43, 1.91]},
    {"q": "2Q 2025", "sq": [0.18, 0.04, 4.58, 3.38, 0.44, 3.40], "sq_bm": [0.00, 0.00, 6.67, 1.50, 0.00, 1.60]}
]

# داتا السفلي (Devices) - أسبوعية حسب صورك
device_weeks = [
    {"week": "Week 1", "census": 23, "vals": [12, 16, 4, 3.5]},
    {"week": "Week 2", "census": 24, "vals": [10, 16, 3, 3.8]},
    {"week": "Week 3", "census": 28, "vals": [10, 13, 8, 4.0]}
]

cur_q = pdf_quarters[st.session_state.step % len(pdf_quarters)]
cur_w = device_weeks[st.session_state.step % len(device_weeks)]

# --- (1) الجزء العلوي: الأداء العام والبار (من الـ PDF) ---
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 50px; font-weight:900;'>ICU PERFORMANCE</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #FFD700; font-size: 20px; font-weight: bold;'>PERIOD: {cur_q['q']}</p>", unsafe_allow_html=True)

sq_names = ["Falls", "Injury Falls", "HAPI %", "CLABSI", "CAUTI", "VAE Rate"]
c_sq = st.columns(6)
for i in range(6):
    v, b = cur_q['sq'][i], cur_q['sq_bm'][i]
    color = "#00ffaa" if v <= b else "#ff4b4b"
    with c_sq[i]:
        st.markdown(f'<div class="kpi-card"><div class="content-box"><div class="label-text">{sq_names[i]}</div><div class="val-text" style="color:{color}">{v}</div><div class="bm-text">BM: {b}</div></div></div>', unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:40px 0;'>", unsafe_allow_html=True)

# --- (2) الجزء السفلي: الديفيس (ثابت المسميات، متغير أسبوعي حسب صورك) ---
c1, c2 = st.columns([2.2, 1.8])

with c1:
    # السنسس من صور الديفيس
    st.markdown(f"""<div class="census-box-mini"><div class="device-sub">CURRENT CENSUS</div><div class="census-num-mini">{cur_w['census']}</div></div>""", unsafe_allow_html=True)
    st.markdown(f'<div class="side-header">ATTACHED DEVICES <span style="color:#FFD700; font-size:16px;">({cur_w["week"]})</span></div>', unsafe_allow_html=True)
    
    g_cols = st.columns(4)
    # المسميات اللي في صورك
    dev_names = [("Pt with ETT", 36, [10, 18]), ("Pt with Foley", 36, [24, 30]), ("Pt with CVC", 36, [16, 22]), ("Avg Stay", 10, [4, 6])]
    
    def create_gauge(v, mx, s):
        fig = go.Figure(go.Indicator(
            mode = "gauge+number", value = v,
            number = {'font': {'size': 38, 'color': '#fff', 'family': 'Arial Black'}},
            gauge = {'axis': {'range': [None, mx], 'tickvals': []}, 'bar': {'color': "#222"}, 'bgcolor': "#000",
                     'steps': [{'range': [0, s[0]], 'color': "#00ffaa"}, {'range': [s[0], s[1]], 'color': "#FFD700"}, {'range': [s[1], mx], 'color': "#ff4b4b"}]}
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, l=10, r=10), height=130)
        return fig

    for i, (n, m, s) in enumerate(dev_names):
        with g_cols[i]:
            st.plotly_chart(create_gauge(cur_w['vals'][i], m, s), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<div class="gauge-label-bottom">{n}</div>', unsafe_allow_html=True)

with c2:
    # البار الخاص بالداتا العلوية (PDF) عشان يمشوا مع بعض
    st.markdown('<div class="side-header" style="margin-left:20px;">NDNQI COMPARISON</div>', unsafe_allow_html=True)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=sq_names, y=cur_q['sq'], name="Unit", marker_color='#00d4ff', text=cur_q['sq'], textposition='outside'))
    fig_bar.add_trace(go.Bar(x=sq_names, y=cur_q['sq_bm'], name="Benchmark", marker_color='#1a1a1a'))
    fig_bar.update_layout(height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          margin=dict(t=20, b=20, l=0, r=0), legend=dict(font=dict(color="#888"), orientation="h", y=1.2))
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي
time.sleep(15)
st.session_state.step += 1
st.rerun()
