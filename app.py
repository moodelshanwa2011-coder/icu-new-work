import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الشاشة الكاملة
st.set_page_config(page_title="ICU Live Performance", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق احترافي للأرقام فقط
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    .kpi-box { background-color: #111; border: 1px solid #222; padding: 20px; border-radius: 15px; text-align: center; }
    .kpi-title { color: #888; font-size: 16px; margin-bottom: 10px; }
    .kpi-number { color: #ffffff; font-size: 35px; font-weight: bold; }
    .device-value { color: #00d4ff; font-size: 45px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. الداتا الكاملة من ملف Riyadh - Intensive Care Unit.pdf والصور المرفقة
# تشمل كافة المؤشرات: Falls, HAPI, Education, CLABSI, CAUTI, VAE, MRSA, Turnover
data_cycle = [
    {
        "period": "3Q 2025",
        "falls": 0.0, "falls_m": 0.18, "hapi": 6.67, "hapi_m": 4.58, 
        "edu": 85.01, "edu_m": 70.59, "clabsi": 1.50, "clabsi_m": 3.38,
        "cauti": 0.0, "cauti_m": 0.44, "vae": 1.6, "vae_m": 3.4,
        "mrsa": 0.22, "mrsa_m": 0.0, "turn": 3.22, "turn_m": 2.9,
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34 # بيانات من صورة WhatsApp
    },
    {
        "period": "2Q 2024",
        "falls": 0.24, "falls_m": 0.06, "hapi": 14.29, "hapi_m": 6.54, 
        "edu": 82.99, "edu_m": 70.31, "clabsi": 1.28, "clabsi_m": 2.67,
        "cauti": 0.70, "cauti_m": 0.99, "vae": 2.17, "vae_m": 2.42,
        "mrsa": 0.22, "mrsa_m": 0.0, "turn": 4.84, "turn_m": 4.49,
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]

d = data_cycle[st.session_state.step % len(data_cycle)]

# --- العنوان العلوي ---
st.markdown(f"<h1 style='text-align: center; color: white;'>🏥 ICU COMMAND CENTER | {d['period']}</h1>", unsafe_allow_html=True)

# --- الجزء الأول: مؤشرات الـ PDF الأساسية (Gauges) ---
c1, c2, c3, c4 = st.columns(4)
def draw_g(l, v, m, col, p=False):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=v, number={'suffix':"%" if p else "", 'font':{'size':35, 'color':'white'}},
        title={'text':l, 'font':{'size':16, 'color':'white'}},
        gauge={'axis':{'range':[0, max(v,m)*1.3]}, 'bar':{'color':col}, 'bgcolor':"#111",
        'threshold':{'line':{'color':"white", 'width':3}, 'thickness':0.8, 'value':m}}))
    fig.update_layout(height=180, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)')
    return fig

with c1: st.plotly_chart(draw_g("Falls Rate", d['falls'], d['falls_m'], "#FF4B4B"), use_container_width=True)
with c2: st.plotly_chart(draw_g("HAPI %", d['hapi'], d['hapi_m'], "#00d4ff", True), use_container_width=True)
with c3: st.plotly_chart(draw_g("RN Education", d['edu'], d['edu_m'], "#00CC96", True), use_container_width=True)
with c4: st.plotly_chart(draw_g("CLABSI Rate", d['clabsi'], d['clabsi_m'], "#FF9F1C"), use_container_width=True)

# --- الجزء الثاني: بقية بيانات الـ PDF (KPI Cards) ---
st.markdown("<br>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
def kpi(l, v, m, u=""):
    st.markdown(f'<div class="kpi-box"><div class="kpi-title">{l}</div><div class="kpi-number">{v}{u}</div><div style="color:#555; font-size:12px;">Benchmark: {m}{u}</div></div>', unsafe_allow_html=True)

with k1: kpi("CAUTI Rate", d['cauti'], d['cauti_m'])
with k2: kpi("VAE/VAP Rate", d['vae'], d['vae_m'])
with k3: kpi("MRSA Rate", d['mrsa'], d['mrsa_m'])
with k4: kpi("Nurse Turnover", d['turn'], d['turn_m'], "%")

# --- الجزء الثالث: بيانات الأجهزة من الصور (Devices) ---
st.markdown("<br><h3 style='color: white; text-align: center;'>Current Medical Device Census</h3>", unsafe_allow_html=True)
d1, d2, d3, d4 = st.columns(4)
def dev_card(l, v):
    st.markdown(f'<div class="kpi-box"><div class="kpi-title">{l}</div><div class="device-value">{v}</div></div>', unsafe_allow_html=True)

with d1: dev_card("Ventilators", d['vents'])
with d2: dev_card("Foley Catheter", d['foley'])
with d3: dev_card("Central Line", d['cvc'])
with d4: dev_card("Total Occupancy", d['stay'])

# تحديث تلقائي كل 15 ثانية بدون أي عناصر إضافية
time.sleep(15)
st.session_state.step += 1
st.rerun()
