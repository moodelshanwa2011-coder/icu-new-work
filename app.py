import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Performance Hub", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (تركيز على الوضوح التام والحدود الفخمة)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    /* مربعات الأجهزة - احترافية وبدون عنوان سفلي */
    .dev-card {
        background-color: #0d0d0d;
        border: 2px solid #1f77b4;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 12px;
    }
    .dev-label { color: #ffffff; font-size: 16px; font-weight: bold; margin-bottom: 5px; }
    .dev-value { color: #00d4ff; font-size: 38px; font-weight: 900; }
    
    /* وضوح أسماء الـ KPIs */
    .gauge-label { color: #ffffff !important; font-size: 22px !important; font-weight: 900 !important; text-shadow: 2px 2px 4px #000; }
    .bench-text { color: #888; font-size: 16px; font-weight: bold; margin-top: -10px; text-align: center; }
    
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. الداتا (نفس الداتا الدقيقة من الـ PDF)
data_cycle = [
    {
        "period": "3Q 2025",
        "falls": 0.0, "falls_m": 0.18, "injury": 0.0, "injury_m": 0.04,
        "restraint": 0.45, "restraint_m": 0.90, "hapi": 6.67, "hapi_m": 4.58, 
        "clabsi": 1.50, "clabsi_m": 3.38, "cauti": 0.0, "cauti_m": 0.44,
        "vae": 1.6, "vae_m": 3.4, "edu": 85.01, "edu_m": 70.59,
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "period": "2Q 2024",
        "falls": 0.24, "falls_m": 0.06, "injury": 0.24, "injury_m": 0.01,
        "restraint": 0.70, "restraint_m": 0.96, "hapi": 14.29, "hapi_m": 6.54, 
        "clabsi": 1.28, "clabsi_m": 2.67, "cauti": 0.70, "cauti_m": 0.99,
        "vae": 2.17, "vae_m": 2.42, "edu": 82.99, "edu_m": 70.31,
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]
d = data_cycle[st.session_state.step % len(data_cycle)]

# --- العنوان ---
st.markdown(f"<h1 style='text-align: center; color: white;'>🏥 ICU DIGITAL COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff; font-size: 20px;'>QUARTER: {d['period']}</p>", unsafe_allow_html=True)

# 4. الـ KPIs (Gauges) - النص دوائر فوق
def draw_bold_gauge(label, val, target, is_perc=False, is_edu=False):
    color = "#00CC96" if (val <= target if not is_edu else val >= target) else "#FF4B4B"
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=val,
        number={'suffix': "%" if is_perc else "", 'font': {'size': 35, 'color': 'white'}},
        title={'text': label, 'font': {'size': 22, 'color': 'white', 'family': 'Arial Black'}},
        gauge={'axis': {'range': [0, max(val, target)*1.6]}, 'bar': {'color': color},
               'bgcolor': "#111", 'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.8, 'value': target}}))
    fig.update_layout(height=180, margin=dict(l=20, r=20, t=40, b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f'<div class="bench-text">Benchmark: {target}</div>', unsafe_allow_html=True)

# صفين من الـ Gauges
c1, c2, c3, c4 = st.columns(4)
with c1: draw_bold_gauge("Total Falls", d['falls'], d['falls_m'])
with c2: draw_bold_gauge("Injury Falls", d['injury'], d['injury_m'])
with c3: draw_bold_gauge("HAPI %", d['hapi'], d['hapi_m'], True)
with c4: draw_bold_gauge("RN Education", d['edu'], d['edu_m'], True, True)

st.markdown("<br>", unsafe_allow_html=True)

c5, c6, c7, c8 = st.columns(4)
with c5: draw_bold_gauge("Restraints", d['restraint'], d['restraint_m'])
with c6: draw_bold_gauge("CLABSI Rate", d['clabsi'], d['clabsi_m'])
with c7: draw_bold_gauge("CAUTI Rate", d['cauti'], d['cauti_m'])
with c8: draw_bold_gauge("VAE/VAP", d['vae'], d['vae_m'])

st.markdown("<br><hr style='border: 1px solid #333;'><br>", unsafe_allow_html=True)

# 5. الجزء السفلي: المربعات (يسار) + البار تشارت (يمين)
col_left, col_right = st.columns([1, 2.8])

with col_left:
    # المربعات فوق بعضها بدون عنوان خارجي
    def quick_box(l, v):
        st.markdown(f'<div class="dev-card"><div class="dev-label">{l}</div><div class="dev-value">{v}</div></div>', unsafe_allow_html=True)
    quick_box("Ventilators", d['vents'])
    quick_box("Foley Catheter", d['foley'])
    quick_box("Central Line", d['cvc'])
    quick_box("Total Stay", d['stay'])

with col_right:
    # بار تشارت احترافي جداً
    labels = ['Falls', 'Injury', 'Restraint', 'CLABSI', 'CAUTI', 'VAE']
    vals = [d['falls'], d['injury'], d['restraint'], d['clabsi'], d['cauti'], d['vae']]
    benchs = [d['falls_m'], d['injury_m'], d['restraint_m'], d['clabsi_m'], d['cauti_m'], d['vae_m']]
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name='Current Unit', x=labels, y=vals,
        marker=dict(color='#00d4ff', line=dict(color='#fff', width=1)),
        text=vals, textposition='outside', textfont=dict(color='white', size=14)
    ))
    fig_bar.add_trace(go.Bar(
        name='Benchmark', x=labels, y=benchs,
        marker=dict(color='#222', line=dict(color='#444', width=1)),
        text=benchs, textposition='outside', textfont=dict(color='#888', size=12)
    ))
    
    fig_bar.update_layout(
        height=400, barmode='group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(showgrid=True, gridcolor='#111', zeroline=False),
        xaxis=dict(tickfont=dict(size=14, color='white', family='Arial Black'))
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي
time.sleep(15)
st.session_state.step += 1
st.rerun()
