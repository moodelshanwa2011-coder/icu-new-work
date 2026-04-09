import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- إعدادات الشاشة الكاملة ---
st.set_page_config(page_title="SGH Riyadh ICU | Live Data", layout="wide", initial_sidebar_state="collapsed")

# --- تنسيق التصميم (UI) ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #050505; }
    .stPlotlyChart { border-radius: 20px; box-shadow: 0 0 15px #00d4ff33; }
    h1, h2 { font-family: 'Arial'; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك البيانات (Data Engine) من ملفاتك ---
if 'step' not in st.session_state:
    st.session_state.step = 0

# 1. بيانات الـ PDF (أداء وحدة العناية المركزة)
# تم تفريغ البيانات الحقيقية من ملف Riyadh - Intensive Care Unit.pdf
icu_benchmarks = [
    {"period": "4Q 2023", "falls_unit": 0.0, "falls_mean": 0.04, "hapi_unit": 4.58, "hapi_mean": 5.21, "edu_unit": 67.19, "edu_mean": 83.53, "clabsi_unit": 3.38, "clabsi_mean": 0.90},
    {"period": "1Q 2024", "falls_unit": 0.24, "falls_mean": 0.09, "hapi_unit": 4.84, "hapi_mean": 4.49, "edu_unit": 82.99, "edu_mean": 70.31, "clabsi_unit": 1.50, "clabsi_mean": 0.88},
    {"period": "2Q 2024", "falls_unit": 0.24, "falls_mean": 0.06, "hapi_unit": 6.25, "hapi_mean": 4.69, "edu_unit": 71.21, "edu_mean": 82.74, "clabsi_unit": 0.90, "clabsi_mean": 0.85},
    {"period": "3Q 2025", "falls_unit": 0.0, "falls_mean": 0.18, "hapi_unit": 6.67, "hapi_mean": 8.01, "edu_unit": 85.01, "edu_mean": 70.59, "clabsi_unit": 1.10, "clabsi_mean": 1.05}
]

# 2. بيانات الصور (التعداد اليومي للأجهزة - عينة أسبوعية)
device_daily = [
    {"day": "Day 1", "vent": 14, "foley": 15, "cvc": 8, "iv": 25, "stay": 34},
    {"day": "Day 2", "vent": 13, "foley": 16, "cvc": 10, "iv": 29, "stay": 31},
    {"day": "Day 3", "vent": 11, "foley": 15, "cvc": 9, "iv": 24, "stay": 24},
    {"day": "Day 4", "vent": 12, "foley": 15, "cvc": 11, "iv": 24, "stay": 25}
]

# التبديل بين البيانات
curr_idx = st.session_state.step % len(icu_benchmarks)
d = icu_benchmarks[curr_idx]
dev = device_daily[curr_idx % len(device_daily)]

# --- الهيكل البصري ---
col_head1, col_head2 = st.columns([4, 1])
with col_head1:
    st.markdown(f"<h1 style='color: white;'>ICU COMMAND CENTER | {d['period']}</h1>", unsafe_allow_html=True)
with col_head2:
    st.progress((int(time.time()) % 15) / 15.0)
    st.caption("Auto-Syncing Data...")

st.markdown("---")

# --- الجزء الأول: الأداء المرجعي (Gauge Charts) ---
# الدوائر الآن تقارن أداء الوحدة (الإبرة) بالمتوسط المرجعي (الخلفية)
c1, c2, c3, c4 = st.columns(4)

def plot_modern_gauge(name, value, mean, color, is_percent=False):
    suffix = "%" if is_percent else ""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        delta={'reference': mean, 'relative': False, 'increasing': {'color': "red" if value > mean else "green"}},
        title={'text': name, 'font': {'size': 20, 'color': 'white'}},
        number={'suffix': suffix, 'font': {'color': 'white'}},
        gauge={
            'axis': {'range': [0, max(value, mean) * 1.5], 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "#111",
            'threshold': {'line': {'color': "yellow", 'width': 4}, 'thickness': 0.75, 'value': mean}
        }
    ))
    fig.update_layout(height=280, margin=dict(l=30, r=30, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)')
    return fig

with c1: st.plotly_chart(plot_modern_gauge("Falls Rate", d['falls_unit'], d['falls_mean'], "#FF4B4B"), use_container_width=True)
with c2: st.plotly_chart(plot_modern_gauge("HAPI %", d['hapi_unit'], d['hapi_mean'], "#00d4ff", True), use_container_width=True)
with c3: st.plotly_chart(plot_modern_gauge("RN Education", d['edu_unit'], d['edu_mean'], "#00CC96", True), use_container_width=True)
with c4: st.plotly_chart(plot_modern_gauge("CLABSI Rate", d['clabsi_unit'], d['clabsi_mean'], "#FF9F1C"), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- الجزء الثاني: بار تشارت احترافي للأجهزة (Bar Chart) ---
st.markdown(f"<h2 style='color: #888;'>Daily Device Census & Utilization</h2>", unsafe_allow_html=True)

col_bar, col_metric = st.columns([3, 1])

with col_bar:
    # رسم بياني يوضح الأجهزة المختلفة
    categories = ['Ventilators', 'Foley Cath', 'Central Lines', 'IV Sites']
    counts = [dev['vent'], dev['foley'], dev['cvc'], dev['iv']]
    
    fig_bar = go.Figure(data=[
        go.Bar(x=categories, y=counts, marker_color=['#00d4ff', '#00CC96', '#FF9F1C', '#FF4B4B'], 
               text=counts, textposition='auto', width=0.5)
    ])
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'}, height=400,
        yaxis=dict(title="Number of Patients", gridcolor="#222")
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_metric:
    # عرض إجمالي عدد المرضى (Stay) بشكل احترافي
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    st.metric(label="Total Patient Stay", value=dev['stay'], delta="-2 from yesterday")
    st.metric(label="Device Utilization Rate", value=f"{int((dev['vent']/dev['stay'])*100)}%", delta="High")

# --- التحديث التلقائي ---
time.sleep(15)
st.session_state.step += 1
st.rerun()
