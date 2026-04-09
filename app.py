import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

# --- إعدادات الصفحة الاحترافية ---
st.set_page_config(page_title="ICU Live Performance", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS مخصص لجعل الواجهة تبدو كشاشة مراقبة (Dashboard Dark Mode look)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 40px; color: #00d4ff; }
    .stPlotlyChart { border: 1px solid #30363d; border-radius: 15px; }
    h1, h2, h3 { color: #ffffff; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك الحركة (Logic for live switching) ---
if 'frame' not in st.session_state:
    st.session_state.frame = 0

# بيانات الـ PDF (أرباع السنة)
quarters = ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024", "1Q 2025", "2Q 2025", "3Q 2025"]
current_q_idx = st.session_state.frame % len(quarters)

# بيانات الصور (الأسابيع)
weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
current_w_idx = st.session_state.frame % len(weeks)

# --- العنوان العلوي المتحرك ---
st.markdown(f"<h1>🏥 ICU LIVE MONITORING: {quarters[current_q_idx]}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #888;'>Last Update: {time.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

# --- الجزء الأول: الأرقام في دوائر (Gauge Charts) مستوحاة من PDF ---
st.subheader("Key Clinical Indicators (NDNQI)")
col1, col2, col3, col4 = st.columns(4)

def create_gauge(title, value, max_val, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 18, 'color': 'white'}},
        number={'font': {'color': color}, 'suffix': "%" if "%" in title else ""},
        gauge={
            'axis': {'range': [0, max_val], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#333",
        }
    ))
    fig.update_layout(height=280, margin=dict(l=30, r=30, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)')
    return fig

# محاكاة تغير البيانات بناءً على الربع السنوي المختار
with col1:
    st.plotly_chart(create_gauge("Falls Rate", 0.18 if current_q_idx % 2 == 0 else 0.25, 1, "#FF4B4B"), use_container_width=True)
with col2:
    st.plotly_chart(create_gauge("HAPI %", 4.58 if current_q_idx < 4 else 6.67, 10, "#00D4FF"), use_container_width=True)
with col3:
    st.plotly_chart(create_gauge("RN Education", 70.59 if current_q_idx % 2 == 0 else 85.01, 100, "#00CC96"), use_container_width=True)
with col4:
    st.plotly_chart(create_gauge("CLABSI Rate", 3.38 if current_q_idx % 3 == 0 else 1.50, 5, "#FF9F1C"), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- الجزء الثاني: بار تشارت (Bar Chart) مستوحى من الصور ---
st.subheader(f"📊 Medical Device Utilization: {weeks[current_w_idx]}")

# بيانات ديناميكية تتغير مع تغير الأسبوع
device_counts = {
    'Ventilator': [14, 12, 11, 13][current_w_idx],
    'Foley Cath': [15, 16, 14, 15][current_w_idx],
    'Central Line': [8, 10, 9, 11][current_w_idx],
    'IV Site': [25, 24, 28, 26][current_w_idx]
}
df_devices = pd.DataFrame(list(device_counts.items()), columns=['Device', 'Count'])

fig_bar = px.bar(df_devices, x='Device', y='Count', color='Device',
                 text='Count', color_discrete_sequence=px.colors.qualitative.G10)

fig_bar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font={'color': 'white'},
    xaxis={'title': ''},
    yaxis={'showgrid': False},
    showlegend=False,
    height=400,
    bargap=0.
