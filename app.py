import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Executive Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي (منع الوميض وتحسين الحدود)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    .device-card {
        background-color: #0a0a0a;
        border: 2px solid #1f77b4;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 8px;
    }
    .device-label { color: #aaaaaa; font-size: 13px; font-weight: bold; }
    .device-value { color: #00d4ff; font-size: 28px; font-weight: 900; }
    .bench-label { color: #666; font-size: 12px; margin-top: -5px; text-align: center; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات
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

# منطق الألوان الذكي
def get_status_color(val, target, reverse=False):
    if reverse: return "#00CC96" if val >= target else "#FF4B4B"
    return "#00CC96" if val <= target else "#FF4B4B"

# --- العنوان ---
st.markdown(f"<h1 style='text-align: center; color: white; margin-bottom:0;'>🏥 ICU PERFORMANCE COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #444;'>Quarterly View: {d['period']}</p>", unsafe_allow_html=True)

# 4. الجزء العلوي: الـ Gauges (8 مؤشرات)
def draw_gauge(label, val, target, is_perc=False, is_edu=False):
    color = get_status_color(val, target, is_edu)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=val,
        number={'suffix': "%" if is_perc else "", 'font': {'size': 24, 'color': 'white'}},
        title={'text': label, 'font': {'size': 13, 'color': 'white'}},
        gauge={'axis': {'range': [0, max(val, target)*1.5]}, 'bar': {'color': color},
               'bgcolor': "#111", 'threshold': {'line': {'color': "white", 'width': 2}, 'thickness': 0.8, 'value': target}}))
    fig.update_layout(height=140, margin=dict(l=10, r=10, t=30, b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f'<div class="bench-label">Bench: {target}</div>', unsafe_allow_html=True)

# صفين من الدوائر
g_row1 = st.columns(4)
with g_row1[0]: draw_gauge("Total Falls", d['falls'], d['falls_m'])
with g_row1[1]: draw_gauge("Injury Falls", d['injury'], d['injury_m'])
with g_row1[2]: draw_gauge("HAPI %", d['hapi'], d['hapi_m'], True)
with g_row1[3]: draw_gauge("RN Education", d['edu'], d['edu_m'], True, True)

g_row2 = st.columns(4)
with g_row2[0]: draw_gauge("Restraints", d['restraint'], d['restraint_m'])
with g_row2[1]: draw_gauge("CLABSI Rate", d['clabsi'], d['clabsi_m'])
with g_row2[2]: draw_gauge("CAUTI Rate", d['cauti'], d['cauti_m'])
with g_row2[3]: draw_gauge("VAE/VAP", d['vae'], d['vae_m'])

st.markdown("<br><hr style='border: 1px solid #222;'>", unsafe_allow_html=True)

# 5. الجزء السفلي: الأجهزة يساراً والبار تشارت يميناً
col_dev, col_bar = st.columns([1, 3])

with col_dev:
    st.markdown("<p style='color: white; text-align: center; font-weight:bold;'>CURRENT ATTACHED DEVICES</p>", unsafe_allow_html=True)
    def dev_box(l, v):
        st.markdown(f'<div class="device-card"><div class="device-label">{l}</div><div class="device-value">{v}</div></div>', unsafe_allow_html=True)
    dev_box("Ventilators", d['vents'])
    dev_box("Foley Catheter", d['foley'])
    dev_box("Central Line", d['cvc'])
    dev_box("Total Occupancy", d['stay'])

with col_bar:
    st.markdown("<p style='color: white; text-align: center; font-weight:bold;'>KPI ANALYSIS BAR CHART</p>", unsafe_allow_html=True)
    kpi_names = ['Falls', 'Injury', 'Restraint', 'CLABSI', 'CAUTI', 'VAE']
    kpi_values = [d['falls'], d['injury'], d['restraint'], d['clabsi'], d['cauti'], d['vae']]
    kpi_benchs = [d['falls_m'], d['injury_m'], d['restraint_m'], d['clabsi_m'], d['cauti_m'], d['vae_m']]
    
    fig_kpi = go.Figure()
    fig_kpi.add_trace(go.Bar(name='Unit Performance', x=kpi_names, y=kpi_values, marker_color='#00d4ff'))
    fig_kpi.add_trace(go.Bar(name='Benchmark', x=kpi_names, y=kpi_benchs, marker_color='#333333'))
    
    fig_kpi.update_layout(
        height=320, barmode='group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=0, b=10),
        yaxis=dict(gridcolor='#111')
    )
    st.plotly_chart(fig_kpi, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي
time.sleep(15)
st.session_state.step += 1
st.rerun()
