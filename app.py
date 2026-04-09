import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الشاشة
st.set_page_config(page_title="ICU Performance Wall", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (أسود ملكي)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    .device-card { background-color: #111; border: 1px solid #333; padding: 20px; border-radius: 15px; text-align: center; }
    .device-label { color: #888; font-size: 16px; font-weight: bold; }
    .device-value { color: #00d4ff; font-size: 40px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. الداتا الكاملة والمفصلة من الـ PDF (شاملة الـ Restraint والـ Injury Falls وغيره)
data_cycle = [
    {
        "period": "3Q 2025",
        "falls": 0.0, "falls_m": 0.18, 
        "injury_falls": 0.0, "injury_m": 0.04,
        "restraint": 0.45, "restraint_m": 0.90, # تم إضافة Restraint
        "hapi": 6.67, "hapi_m": 4.58, 
        "clabsi": 1.50, "clabsi_m": 3.38,
        "cauti": 0.0, "cauti_m": 0.44,
        "vae": 1.6, "vae_m": 3.4,
        "edu": 85.01, "edu_m": 70.59,
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "period": "2Q 2024",
        "falls": 0.24, "falls_m": 0.06, 
        "injury_falls": 0.24, "injury_m": 0.01,
        "restraint": 0.70, "restraint_m": 0.96,
        "hapi": 14.29, "hapi_m": 6.54, 
        "clabsi": 1.28, "clabsi_m": 2.67,
        "cauti": 0.70, "cauti_m": 0.99,
        "vae": 2.17, "vae_m": 2.42,
        "edu": 82.99, "edu_m": 70.31,
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]

d = data_cycle[st.session_state.step % len(data_cycle)]

# --- العنوان ---
st.markdown(f"<h1 style='text-align: center; color: white; margin-bottom: 0;'>🏥 ICU FULL DATA MONITORING | {d['period']}</h1>", unsafe_allow_html=True)

# دالة رسم النص دائرة (Gauge)
def draw_gauge(label, val, target, color, is_perc=False):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        number={'suffix': "%" if is_perc else "", 'font': {'size': 30, 'color': 'white'}},
        title={'text': label, 'font': {'size': 14, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, max(val, target)*1.3], 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "#111",
            'threshold': {'line': {'color': "white", 'width': 3}, 'thickness': 0.8, 'value': target}
        }
    ))
    fig.update_layout(height=160, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
    return fig

# --- الصف الأول: المؤشرات الكبرى ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.plotly_chart(draw_gauge("Total Falls", d['falls'], d['falls_m'], "#FF4B4B"), use_container_width=True)
with c2: st.plotly_chart(draw_gauge("Injury Falls", d['injury_falls'], d['injury_m'], "#FF4B4B"), use_container_width=True)
with c3: st.plotly_chart(draw_gauge("HAPI %", d['hapi'], d['hapi_m'], "#00d4ff", True), use_container_width=True)
with c4: st.plotly_chart(draw_gauge("RN Education", d['edu'], d['edu_m'], "#00CC96", True), use_container_width=True)

# --- الصف الثاني: مؤشرات العدوى والقيود (Data Complete) ---
c5, c6, c7, c8 = st.columns(4)
with c5: st.plotly_chart(draw_gauge("Restraints", d['restraint'], d['restraint_m'], "#FF9F1C"), use_container_width=True)
with c6: st.plotly_chart(draw_gauge("CLABSI Rate", d['clabsi'], d['clabsi_m'], "#FF9F1C"), use_container_width=True)
with c7: st.plotly_chart(draw_gauge("CAUTI Rate", d['cauti'], d['cauti_m'], "#FF9F1C"), use_container_width=True)
with c8: st.plotly_chart(draw_gauge("VAE/VAP", d['vae'], d['vae_m'], "#FF9F1C"), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- الصف الثالث: الأجهزة (Devices) - أرقام واضحة ---
st.markdown("<h3 style='color: white; text-align: center;'>MEDICAL DEVICE CENSUS (LIVE)</h3>", unsafe_allow_html=True)
d1, d2, d3, d4 = st.columns(4)

def device_box(label, value):
    st.markdown(f'<div class="device-card"><div class="device-label">{label}</div><div class="device-value">{value}</div></div>', unsafe_allow_html=True)

with d1: device_box("Ventilators", d['vents'])
with d2: device_box("Foley Catheter", d['foley'])
with d3: device_box("Central Line", d['cvc'])
with d4: device_box("Total Occupancy", d['stay'])

# 4. التحديث التلقائي
time.sleep(15)
st.session_state.step += 1
st.rerun()
