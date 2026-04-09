import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Command Center", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS عصري (أسود ملكي مع ألوان فسفورية)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    .device-card {
        background-color: #111;
        border: 2px solid #222;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    .device-label { color: #888; font-size: 16px; font-weight: bold; text-transform: uppercase; }
    .device-value { color: #00d4ff; font-size: 50px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات (Data Logic)
if 'step' not in st.session_state:
    st.session_state.step = 0

# بيانات الـ PDF (KPIs) + بيانات الصور (Devices)
data_cycle = [
    {
        "period": "3Q 2025",
        "falls": 0.0, "falls_target": 0.18, 
        "hapi": 6.67, "hapi_target": 8.01,
        "clabsi": 1.10, "clabsi_target": 1.05,
        "edu": 85.01, "edu_target": 70.59,
        # بيانات الأجهزة من الصور
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "period": "2Q 2024",
        "falls": 0.24, "falls_target": 0.06, 
        "hapi": 6.25, "hapi_target": 4.69,
        "clabsi": 0.90, "clabsi_target": 0.85,
        "edu": 71.21, "edu_target": 82.74,
        # بيانات الأجهزة من الصور
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]

d = data_cycle[st.session_state.step % len(data_cycle)]

# --- العنوان ---
st.markdown(f"<h1 style='text-align: center; color: white;'>ICU MONITORING UNIT | {d['period']}</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- الجزء الأول: الـ Gauges (بيانات الـ PDF) ---
c1, c2, c3, c4 = st.columns(4)

def plot_gauge(label, val, target, color, is_perc=False):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        title={'text': label, 'font': {'size': 18, 'color': 'white'}},
        number={'suffix': "%" if is_perc else "", 'font': {'color': 'white', 'size': 40}},
        gauge={
            'axis': {'range': [0, max(val, target)*1.2], 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "#111",
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.8, 'value': target}
        }
    ))
    fig.update_layout(height=230, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
    return fig

with c1: st.plotly_chart(plot_gauge("Falls Rate", d['falls'], d['falls_target'], "#FF4B4B"), use_container_width=True)
with c2: st.plotly_chart(plot_gauge("HAPI %", d['hapi'], d['hapi_target'], "#00d4ff", True), use_container_width=True)
with c3: st.plotly_chart(plot_gauge("RN Education", d['edu'], d['edu_target'], "#00CC96", True), use_container_width=True)
with c4: st.plotly_chart(plot_gauge("CLABSI Rate", d['clabsi'], d['clabsi_target'], "#FF9F1C"), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- الجزء الثاني: الـ Devices (بيانات الصور) ---
# رجعنا الأجهزة كأرقام كبيرة بدون رسومات جانبية
st.markdown("<h3 style='color: #888; text-align: center;'>Current Device Census</h3>", unsafe_allow_html=True)
d1, d2, d3, d4 = st.columns(4)

def device_box(label, value):
    st.markdown(f"""
        <div class="device-card">
            <div class="device-label">{label}</div>
            <div class="device-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

with d1: device_box("Ventilators", d['vents'])
with d2: device_box("Foley Catheter", d['foley'])
with d3: device_box("Central Line (CVC)", d['cvc'])
with d4: device_box("Total Patient Stay", d['stay'])

# --- التحديث التلقائي ---
# حذفنا الـ Progress Bar السفلي والمربعات الزائدة
time.sleep(15)
st.session_state.step += 1
st.rerun()
