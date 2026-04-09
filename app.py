import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة (إخفاء كل القوائم للتركيز على البيانات)
st.set_page_config(page_title="ICU Command Center", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم احترافي جداً (Dark Industrial Theme)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #050505; }
    .main-title { color: white; font-size: 35px; font-weight: 800; text-align: center; margin-bottom: 20px; border-bottom: 2px solid #1f77b4; }
    .data-card { background-color: #111; border: 1px solid #222; padding: 15px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك البيانات (كل الداتا من ملف Riyadh - ICU PDF)
if 'cycle' not in st.session_state:
    st.session_state.cycle = 0

# تفريغ الداتا الكاملة (الرقم الأول: Unit، الرقم الثاني: Benchmark)
full_data = [
    {
        "period": "3Q 2025",
        "Falls": [0, 0.18], "HAPI": [6.67, 8.01], "RN_Edu": [85.01, 70.59], 
        "CLABSI": [1.10, 1.05], "CAUTI": [0.45, 0.96], "VAP": [0.0, 0.25],
        "MRSA": [0.0, 0.14], "Turnover": [2.9, 3.97]
    },
    {
        "period": "2Q 2024",
        "Falls": [0.24, 0.06], "HAPI": [6.25, 4.69], "RN_Edu": [71.21, 82.74], 
        "CLABSI": [0.90, 0.85], "CAUTI": [0, 0.25], "VAP": [0.26, 0.11],
        "MRSA": [0.22, 0.14], "Turnover": [6.25, 3.74]
    }
]

curr = full_data[st.session_state.cycle % len(full_data)]

# --- العنوان ---
st.markdown(f'<div class="main-title">🏥 ICU EXECUTIVE DASHBOARD - {curr["period"]}</div>', unsafe_allow_html=True)

# --- الصف الأول: المؤشرات الرئيسية (Gauges) ---
col1, col2, col3, col4 = st.columns(4)

def create_gauge(label, unit_val, mean_val, color, is_perc=False):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=unit_val,
        title={'text': label, 'font': {'size': 16, 'color': 'white'}},
        number={'suffix': "%" if is_perc else "", 'font': {'size': 35, 'color': color}},
        gauge={
            'axis': {'range': [0, max(unit_val, mean_val) * 1.2], 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "#111",
            'threshold': {'line': {'color': "white", 'width': 3}, 'thickness': 0.8, 'value': mean_val}
        }
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)')
    return fig

with col1: st.plotly_chart(create_gauge("Falls Rate", curr["Falls"][0], curr["Falls"][1], "#FF4B4B"), use_container_width=True)
with col2: st.plotly_chart(create_gauge("HAPI %", curr["HAPI"][0], curr["HAPI"][1], "#00d4ff", True), use_container_width=True)
with col3: st.plotly_chart(create_gauge("RN Education", curr["RN_Edu"][0], curr["RN_Edu"][1], "#00CC96", True), use_container_width=True)
with col4: st.plotly_chart(create_gauge("CLABSI Rate", curr["CLABSI"][0], curr["CLABSI"][1], "#FF9F1C"), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- الصف الثاني: مؤشرات العدوى والعمالة (KPI Cards) ---
# هنا عرضنا البيانات الناقصة بدون رسومات بيانية معقدة
c1, c2, c3, c4 = st.columns(4)

def kpi_box(label, value, benchmark, unit=""):
    color = "green" if value <= benchmark else "red"
    # لـ RN Education العكس هو الصحيح
    if "Education" in label: color = "green" if value >= benchmark else "red"
    
    st.markdown(f"""
        <div class="data-card">
            <h4 style="color: gray; margin:0;">{label}</h4>
            <h2 style="color: white; margin:5px;">{value}{unit}</h2>
            <p style="color: {color}; font-size: 12px; margin:0;">Target: {benchmark}{unit}</p>
        </div>
    """, unsafe_allow_html=True)

with c1: kpi_box("CAUTI Rate", curr["CAUTI"][0], curr["CAUTI"][1])
with c2: kpi_box("VAP Rate", curr["VAP"][0], curr["VAP"][1])
with c3: kpi_box("MRSA Rate", curr["MRSA"][0], curr["MRSA"][1])
with c4: kpi_box("Nurse Turnover", curr["Turnover"][0], curr["Turnover"][1], "%")

st.markdown("<br>", unsafe_allow_html=True)

# --- الصف الثالث: بيانات الصور (أجهزة التنفس والقسطرة) ---
# تم وضعها في مربعات بسيطة ومباشرة كما طلبت (بدون بارات لا لزوم لها)
st.markdown("<h3 style='color: white; text-align: center;'>Current Device Census</h3>", unsafe_allow_html=True)
d1, d2, d3, d4 = st.columns(4)

# هذه البيانات من صور WhatsApp المرفقة
with d1: st.metric("Ventilators", "14 Patients", "Active")
with d2: st.metric("Foley Catheter", "15 Patients", "-1")
with d3: st.metric("Central Line (CVC)", "8 Patients", "Stable")
with d4: st.metric("Total Occupancy", "34/40", "85%")

# --- منطق التحديث (15 ثانية) ---
time.sleep(15)
st.session_state.cycle += 1
st.rerun()
