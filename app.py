import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Digital Command Center", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (تركيز على وضوح الخطوط واحترافية الحدود)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    /* تحسين شكل كروت الأجهزة */
    .device-card {
        background-color: #0d0d0d;
        border-left: 5px solid #00d4ff; /* لمسة جمالية جانبية */
        border-top: 1px solid #222;
        border-right: 1px solid #222;
        border-bottom: 1px solid #222;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
    }
    .device-label { color: #ffffff; font-size: 16px; font-weight: bold; margin-bottom: 5px; }
    .device-value { color: #00d4ff; font-size: 38px; font-weight: 900; }
    /* وضوح أسماء الـ KPIs */
    .gauge-title { color: #ffffff !important; font-size: 20px !important; font-weight: bold !important; }
    .bench-label { color: #888888; font-size: 15px; font-weight: bold; text-align: center; margin-top: -10px; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات (3Q 2025 vs 2Q 2024)
data_cycle = [
    {
        "period": "3Q 2025",
        "falls": 0.0, "falls_m": 0.18, "injury": 0.0, "injury_m": 0.04,
        "restraint": 0.45, "restraint_m": 0.90, "hapi": 6.67, "hapi_m": 4.58, 
        "clabsi": 1.50, "clabsi_m": 3.38, "cauti": 0.0, "cauti_m": 0.44,
        "vae": 1.6, "vae_m": 3.4, "edu": 85.01, "edu_m": 70.59,
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "period": "2Q 2024",
        "falls": 0.24, "falls_m": 0.06, "injury": 0.24, "injury_m": 0.01,
        "restraint": 0.70, "restraint_m": 0.96, "hapi": 14.29, "hapi_m": 6.54, 
        "clabsi": 1.28, "clabsi_m": 2.67, "cauti": 0.70, "cauti_m": 0.99,
        "vae": 2.17, "vae_m": 2.42, "edu": 82.99, "edu_m": 70.31,
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]

d = data_cycle[st.session_state.step % len(data_cycle)]

# منطق الألوان
def get_status_color(val, target, reverse=False):
    if reverse: return "#00CC96" if val >= target else "#FF4B4B"
    return "#00CC96" if val <= target else "#FF4B4B"

# --- هيدر الصفحة ---
st.markdown(f"<h1 style='text-align: center; color: white;'>🏥 ICU REAL-TIME PERFORMANCE MONITOR</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff; font-weight: bold;'>Quarter: {d['period']}</p>", unsafe_allow_html=True)

# 4. قسم الـ Gauges العلوي (أوضح وأكبر)
def draw_large_gauge(label, val, target, is_perc=False, is_edu=False):
    color = get_status_color(val, target, is_edu)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=val,
        number={'suffix': "%" if is_perc else "", 'font': {'size': 35, 'color': 'white'}},
        title={'text': label, 'font': {'size': 20, 'color': 'white', 'family': 'Arial Black'}},
        gauge={'axis': {'range': [0, max(val, target)*1.5], 'tickfont': {'color': 'gray'}}, 
               'bar': {'color': color}, 'bgcolor': "#111",
               'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.8, 'value': target}}))
    fig.update_layout(height=180, margin=dict(l=20, r=20, t=40, b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f'<div class="bench-label">Target: {target}</div>', unsafe_allow_html=True)

# توزيع الـ 8 مؤشرات في صفين
r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
with r1_c1: draw_large_gauge("Total Falls", d['falls'], d['falls_m'])
with r1_c2: draw_large_gauge("Injury Falls", d['injury'], d['injury_m'])
with r1_c3: draw_large_gauge("HAPI %", d['hapi'], d['hapi_m'], True)
with r1_c4: draw_large_gauge("RN Education", d['edu'], d['edu_m'], True, True)

st.markdown("<br>", unsafe_allow_html=True)

r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
with r2_c1: draw_large_gauge("Restraints", d['restraint'], d['restraint_m'])
with r2_c2: draw_large_gauge("CLABSI Rate", d['clabsi'], d['clabsi_m'])
with r2_c3: draw_large_gauge("CAUTI Rate", d['cauti'], d['cauti_m'])
with r2_c4: draw_large_gauge("VAE/VAP", d['vae'], d['vae_m'])

st.markdown("<br><hr style='border: 1px solid #333;'>", unsafe_allow_html=True)

# 5. الجزء السفلي المدمج: الأجهزة (يسار) + البار تشارت الاحترافي (يمين)
col_left, col_right = st.columns([1, 2.5])

with col_left:
    # الأجهزة بدون عنوان مكرر وبشكل أنيق
    def quick_card(l, v):
        st.markdown(f'<div class="device-card"><div class="device-label">{l}</div><div class="device-value">{v}</div></div>', unsafe_allow_html=True)
    quick_card("Ventilators", d['vents'])
    quick_card("Foley Cath", d['foley'])
    quick_card("Central Line", d['cvc'])
    quick_card("Occupancy", d['stay'])

with col_right:
    # بار تشارت احترافي جداً (Gradient-like colors)
    kpi_labels = ['Falls', 'Injury', 'Restraint', 'CLABSI', 'CAUTI', 'VAE']
    unit_vals = [d['falls'], d['injury'], d['restraint'], d['clabsi'], d['cauti'], d['vae']]
    bench_vals = [d['falls_m'], d['injury_m'], d['restraint_m'], d['clabsi_m'], d['cauti_m'], d['vae_m']]
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name='Unit Performance', x=kpi_labels, y=unit_vals,
        marker=dict(color='#00d4ff', line=dict(color='#ffffff', width=1)),
        text=unit_vals, textposition='outside', textfont=dict(color='white')
    ))
    fig_bar.add_trace(go.Bar(
        name='NDNQI Benchmark', x=kpi_labels, y=bench_vals,
        marker=dict(color='#333333', line=dict(color='#555555', width=1)),
        text=bench_vals, textposition='outside', textfont=dict(color='gray')
    ))
    
    fig_bar.update_layout(
        height=380, barmode='group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14),
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5),
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(showgrid=True, gridcolor='#1a1a1a', zeroline=False),
        xaxis=dict(tickfont=dict(size=14, color='white'))
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# 6. التحديث التلقائي
time.sleep(15)
st.session_state.step += 1
st.rerun()
