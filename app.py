import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الشاشة
st.set_page_config(page_title="ICU Wall - Full View", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (توسيع الحاويات وإخفاء الزوائد)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    .gauge-container { margin-bottom: 50px; text-align: center; } /* توسيع المسافة الرأسية */
    .bench-label { color: #555; font-size: 16px; margin-top: -10px; font-weight: bold; }
    .device-card { background-color: #111; border: 1px solid #333; padding: 25px; border-radius: 15px; text-align: center; }
    .device-label { color: #888; font-size: 18px; font-weight: bold; }
    .device-value { color: #00d4ff; font-size: 45px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. الداتا الكاملة من الـ PDF والصور
data_cycle = [
    {
        "period": "3Q 2025",
        "falls": 0.0, "falls_m": 0.18, 
        "injury_m": 0.04, "injury": 0.0,
        "restraint": 0.45, "restraint_m": 0.90,
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
        "injury": 0.24, "injury_m": 0.01,
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
st.markdown(f"<h1 style='text-align: center; color: white;'>🏥 ICU FULL DATA MONITORING | {d['period']}</h1>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# دالة رسم النص دائرة (Gauge) مع تحسين المساحات
def draw_gauge_with_bench(label, val, target, color, is_perc=False):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        number={'suffix': "%" if is_perc else "", 'font': {'size': 35, 'color': 'white'}},
        title={'text': label, 'font': {'size': 18, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, max(val, target)*1.5], 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "#111",
            'threshold': {'line': {'color': "white", 'width': 3}, 'thickness': 0.8, 'value': target}
        }
    ))
    fig.update_layout(height=200, margin=dict(l=30, r=30, t=50, b=0), paper_bgcolor='rgba(0,0,0,0)')
    
    # عرض الرسم وتحته الـ Benchmark مباشرة
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f'<div class="bench-label">Benchmark: {target}{"%" if is_perc else ""}</div>', unsafe_allow_html=True)

# --- توزيع المؤشرات (PDF) بمسافات واسعة ---
col_set1 = st.columns(4)
with col_set1[0]: draw_gauge_with_bench("Total Falls", d['falls'], d['falls_m'], "#FF4B4B")
with col_set1[1]: draw_gauge_with_bench("Injury Falls", d['injury'], d['injury_m'], "#FF4B4B")
with col_set1[2]: draw_gauge_with_bench("HAPI %", d['hapi'], d['hapi_m'], "#00d4ff", True)
with col_set1[3]: draw_gauge_with_bench("RN Education", d['edu'], d['edu_m'], "#00CC96", True)

st.markdown("<br><br>", unsafe_allow_html=True) # مسافة إضافية بين الصفوف

col_set2 = st.columns(4)
with col_set2[0]: draw_gauge_with_bench("Restraints", d['restraint'], d['restraint_m'], "#FF9F1C")
with col_set2[1]: draw_gauge_with_bench("CLABSI Rate", d['clabsi'], d['clabsi_m'], "#FF9F1C")
with col_set2[2]: draw_gauge_with_bench("CAUTI Rate", d['cauti'], d['cauti_m'], "#FF9F1C")
with col_set2[3]: draw_gauge_with_bench("VAE/VAP", d['vae'], d['vae_m'], "#FF9F1C")

st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- الأجهزة (Images) ---
st.markdown("<h3 style='color: white; text-align: center;'>MEDICAL DEVICE CENSUS</h3>", unsafe_allow_html=True)
d_cols = st.columns(4)

def device_box(label, value):
    st.markdown(f'<div class="device-card"><div class="device-label">{label}</div><div class="device-value">{value}</div></div>', unsafe_allow_html=True)

with d_cols[0]: device_box("Ventilators", d['vents'])
with d_cols[1]: device_box("Foley Catheter", d['foley'])
with d_cols[2]: device_box("Central Line", d['cvc'])
with d_cols[3]: device_box("Total Occupancy", d['stay'])

# 4. التحديث التلقائي
time.sleep(15)
st.session_state.step += 1
st.rerun()
