import streamlit as st
import plotly.graph_objects as go
import time

# إعدادات الصفحة
st.set_page_config(page_title="ICU Live Dashboard", layout="wide", initial_sidebar_state="collapsed")

# تصميم الأرقام والكروت
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    .kpi-card { background-color: #111; border: 1px solid #222; padding: 15px; border-radius: 10px; text-align: center; }
    .kpi-label { color: #888; font-size: 14px; font-weight: bold; }
    .kpi-value { color: #ffffff; font-size: 28px; font-weight: bold; }
    .device-value { color: #00d4ff; font-size: 40px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# الداتا الكاملة من ملفاتك (PDF + الصور)
data = [
    {
        "period": "3Q 2025",
        "falls": 0.0, "falls_m": 0.18, "hapi": 6.67, "hapi_m": 8.01, "edu": 85.01, "edu_m": 70.59, "clabsi": 1.10, "clabsi_m": 1.05,
        "cauti": 0.45, "cauti_m": 0.96, "vap": 0.0, "vap_m": 0.25, "mrsa": 0.0, "mrsa_m": 0.14, "turnover": 2.9, "turnover_m": 3.97,
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "period": "2Q 2024",
        "falls": 0.24, "falls_m": 0.06, "hapi": 6.25, "hapi_m": 4.69, "edu": 71.21, "edu_m": 82.74, "clabsi": 0.90, "clabsi_m": 0.85,
        "cauti": 0.0, "cauti_m": 0.25, "vap": 0.26, "vap_m": 0.11, "mrsa": 0.22, "mrsa_m": 0.14, "turnover": 6.25, "turnover_m": 3.74,
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]

d = data[st.session_state.step % len(data)]

st.markdown(f"<h1 style='text-align: center; color: white;'>ICU COMMAND CENTER | {d['period']}</h1>", unsafe_allow_html=True)

# 1. الدوائر (Gauges) - أعلى الصفحة
c1, c2, c3, c4 = st.columns(4)
def plot_g(l, v, m, col, p=False):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=v, number={'suffix':"%" if p else "", 'font':{'size':35, 'color':'white'}},
        title={'text':l, 'font':{'size':16, 'color':'white'}},
        gauge={'axis':{'range':[0, max(v,m)*1.2]}, 'bar':{'color':col}, 'bgcolor':"#111",
        'threshold':{'line':{'color':"white", 'width':3}, 'thickness':0.8, 'value':m}}))
    fig.update_layout(height=200, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)')
    return fig

with c1: st.plotly_chart(plot_g("Falls Rate", d['falls'], d['falls_m'], "#FF4B4B"), use_container_width=True)
with c2: st.plotly_chart(plot_g("HAPI %", d['hapi'], d['hapi_m'], "#00d4ff", True), use_container_width=True)
with c3: st.plotly_chart(plot_g("RN Education", d['edu'], d['edu_m'], "#00CC96", True), use_container_width=True)
with c4: st.plotly_chart(plot_g("CLABSI Rate", d['clabsi'], d['clabsi_m'], "#FF9F1C"), use_container_width=True)

# 2. البيانات الناقصة (KPI Cards) - منتصف الصفحة
st.markdown("<br>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
def kpi(l, v, m, u=""):
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">{l}</div><div class="kpi-value">{v}{u}</div><div style="color:#555; font-size:12px;">Target: {m}{u}</div></div>', unsafe_allow_html=True)

with k1: kpi("CAUTI Rate", d['cauti'], d['cauti_m'])
with k2: kpi("VAP Rate", d['vap'], d['vap_m'])
with k3: kpi("MRSA Rate", d['mrsa'], d['mrsa_m'])
with k4: kpi("Turnover", d['turnover'], d['turnover_m'], "%")

# 3. الأجهزة (Devices) - أسفل الصفحة
st.markdown("<br><h3 style='color: #888; text-align: center;'>DEVICE CENSUS (LIVE)</h3>", unsafe_allow_html=True)
d1, d2, d3, d4 = st.columns(4)
def dev(l, v):
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">{l}</div><div class="device-value">{v}</div></div>', unsafe_allow_html=True)

with d1: dev("Ventilators", d['vents'])
with d2: dev("Foley Catheter", d['foley'])
with d3: dev("Central Line", d['cvc'])
with d4: dev("Total Stay", d['stay'])

# التحديث التلقائي
time.sleep(15)
st.session_state.step += 1
st.rerun()
