import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة (شاشة عرض كاملة)
st.set_page_config(page_title="ICU Digital Wall", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS لجعل الواجهة "تنبض" بالحياة (Neon & Clean Style)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    .metric-container {
        background-color: #111111;
        border-radius: 20px;
        padding: 25px;
        border: 1px solid #222;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,212,255,0.1);
    }
    .metric-label { color: #888; font-size: 18px; font-weight: bold; }
    .metric-value { color: #00d4ff; font-size: 45px; font-weight: 900; margin: 10px 0; }
    .metric-target { color: #444; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات (كل البيانات من الـ PDF والصور)
if 'step' not in st.session_state:
    st.session_state.step = 0

all_data = [
    {
        "period": "3Q 2025",
        "falls": 0.0, "falls_target": 0.18, 
        "hapi": 6.67, "hapi_target": 8.01,
        "edu": 85.01, "edu_target": 70.59,
        "clabsi": 1.10, "clabsi_target": 1.05,
        "cauti": 0.45, "cauti_target": 0.96,
        "vap": 0.0, "vap_target": 0.25,
        "vents": 14, "foley": 15, "cvc": 8, "total": 34
    },
    {
        "period": "2Q 2024",
        "falls": 0.24, "falls_target": 0.06, 
        "hapi": 6.25, "hapi_target": 4.69,
        "edu": 71.21, "edu_target": 82.74,
        "clabsi": 0.90, "clabsi_target": 0.85,
        "cauti": 0.0, "cauti_target": 0.25,
        "vap": 0.26, "vap_target": 0.11,
        "vents": 12, "foley": 14, "cvc": 9, "total": 28
    }
]

d = all_data[st.session_state.step % len(all_data)]

# --- العنوان العلوي ---
st.markdown(f"<h1 style='text-align: center; color: white; font-family: sans-serif;'>ICU COMMAND CENTER | {d['period']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff;'>Live Update Active</p>", unsafe_allow_html=True)

# --- الجزء الأول: الدوائر الاحترافية (Gauges) ---
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

def plot_gauge(label, val, target, color, is_perc=False):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        title={'text': label, 'font': {'size': 18, 'color': 'white'}},
        number={'suffix': "%" if is_perc else "", 'font': {'size': 40, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, max(val, target)*1.3], 'tickcolor': "white"},
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

# --- الجزء الثاني: كروت الأرقام (KPI Cards) - لا جداول ولا بارات ---
st.markdown("<br>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

def kpi_card(label, value, target, unit=""):
    # تحديد لون الحالة
    status_color = "#00CC96" if value <= target else "#FF4B4B"
    if "Education" in label: status_color = "#00CC96" if value >= target else "#FF4B4B"
    
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}{unit}</div>
            <div class="metric-target" style="color:{status_color}">Benchmark: {target}{unit}</div>
        </div>
    """, unsafe_allow_html=True)

with k1: kpi_card("CAUTI Rate", d['cauti'], d['cauti_target'])
with k2: kpi_card("VAP Rate", d['vap'], d['vap_target'])
with k3: kpi_card("Ventilators", d['vents'], 20, " Patients")
with k4: kpi_card("Total Occupancy", d['total'], 40, " Patients")

# --- الجزء السفلي: عداد الثواني التلقائي ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.progress((int(time.time()) % 15) / 15.0)

# --- التحديث التلقائي كل 15 ثانية ---
time.sleep(15)
st.session_state.step += 1
st.rerun()
