import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة - Mode: Wide & Dark
st.set_page_config(page_title="SGH Riyadh | ICU Command Center", layout="wide", initial_sidebar_state="collapsed")

# 2. لمسات CSS احترافية (خلفية داكنة، ظلال، وتنسيق الخطوط)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #050505; }
    .metric-card {
        background-color: #111;
        border: 1px solid #222;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .stProgress > div > div > div > div { background-color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 3. منطق التحديث والبيانات (Data Engine)
if 'step' not in st.session_state:
    st.session_state.step = 0

# أرباع السنة من الـ PDF
q_data = [
    {"q": "4Q 2023", "falls": 0.04, "hapi": 4.58, "edu": 67.19, "clabsi": 3.38},
    {"q": "1Q 2024", "falls": 0.09, "hapi": 4.84, "edu": 70.31, "clabsi": 1.50},
    {"q": "2Q 2024", "falls": 0.24, "hapi": 6.25, "edu": 82.99, "clabsi": 2.10},
    {"q": "3Q 2024", "falls": 0.06, "hapi": 3.74, "edu": 71.21, "clabsi": 0.90},
    {"q": "3Q 2025", "falls": 0.18, "hapi": 6.67, "edu": 70.59, "clabsi": 3.10}
]

# بيانات الأجهزة من الصور (مقسمة لأسابيع)
w_data = [
    {"w": "Week 1", "vents": 14, "foley": 15, "iv": 25},
    {"w": "Week 2", "vents": 13, "foley": 16, "iv": 29},
    {"w": "Week 3", "vents": 11, "foley": 15, "iv": 24},
    {"w": "Week 4", "vents": 12, "foley": 15, "iv": 24}
]

# اختيار البيانات الحالية بناءً على العداد
curr_q = q_data[st.session_state.step % len(q_data)]
curr_w = w_data[st.session_state.step % len(w_data)]

# --- العنوان العلوي ---
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.markdown(f"<h1 style='color: white; margin-bottom: 0;'>ICU PERFORMANCE COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #00d4ff; font-size: 20px;'>Live Cycle: {curr_q['q']} | {curr_w['w']}</p>", unsafe_allow_html=True)
with col_t2:
    # عداد ثواني تنازلي بصري
    st.write("")
    progress_text = "Next Update in 15s"
    st.progress((int(time.time()) % 15) / 15.0)

st.markdown("---")

# --- الجزء العلوي: دوائر الأداء (PDF Data) ---
st.markdown("<h3 style='color: #888;'>Quarterly Clinical Benchmarks</h3>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

def plot_gauge(val, target, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        number={'suffix': "%" if "Education" in title or "HAPI" in title else "", 'font': {'size': 40, 'color': 'white'}},
        title={'text': title, 'font': {'size': 18, 'color': color}},
        gauge={
            'axis': {'range': [0, target*1.5], 'tickcolor': "gray"},
            'bar': {'color': color},
            'bgcolor': "#111",
            'steps': [{'range': [0, target], 'color': "#222"}],
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': target}
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)')
    return fig

with c1: st.plotly_chart(plot_gauge(curr_q['falls'], 0.25, "Falls Rate", "#FF4B4B"), use_container_width=True)
with c2: st.plotly_chart(plot_gauge(curr_q['hapi'], 5.0, "HAPI Case %", "#00d4ff"), use_container_width=True)
with c3: st.plotly_chart(plot_gauge(curr_q['edu'], 85.0, "RN Education", "#00CC96"), use_container_width=True)
with c4: st.plotly_chart(plot_gauge(curr_q['clabsi'], 2.0, "CLABSI Rate", "#FF9F1C"), use_container_width=True)

# --- الجزء السفلي: بار تشارت احترافي (Image Data) ---
st.markdown("<br><h3 style='color: #888;'>Daily Device Census (Device/Patient)</h3>", unsafe_allow_html=True)

# تجهيز البيانات للبار تشارت
df_bar = pd.DataFrame({
    "Category": ["Ventilators", "Foley Catheters", "IV Sites"],
    "Current Count": [curr_w['vents'], curr_w['foley'], curr_w['iv']],
    "Avg Capacity": [20, 20, 35] # أرقام تقديرية للمقارنة
})

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=df_bar["Category"], y=df_bar["Current Count"],
    name='Actual Count', marker_color='#00d4ff',
    text=df_bar["Current Count"], textposition='auto',
    marker_line_width=0, opacity=0.8
))

fig_bar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font={'color': 'white'},
    height=350,
    margin=dict(l=10, r=10, t=10, b=10),
    yaxis=dict(showgrid=True, gridcolor='#222', zeroline=False)
)

st.plotly_chart(fig_bar, use_container_width=True)

# --- تذييل الصفحة وتوقيت التحديث ---
st.markdown(f"""
    <div style="text-align: center; color: #444; padding-top: 20px;">
    System Status: Active | Source: Riyadh ICU Data | Auto-Refresh: ON
    </div>
    """, unsafe_allow_html=True)

# --- منطق التحديث (15 ثانية) ---
time.sleep(15)
st.session_state.step += 1
st.rerun()
