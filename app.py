import streamlit as st
import plotly.graph_objects as go
import time
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Live Intelligence", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS احترافي جداً لتأثيرات الإضاءة والحركة
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; padding: 5px 20px; }
    
    /* تأثير النيون للمربعات */
    .dev-box {
        background-color: #0d0d0d;
        border: 1px solid #1f77b4;
        border-radius: 15px;
        padding: 12px;
        margin-bottom: 15px;
        text-align: center;
        box-shadow: inset 0 0 10px rgba(0, 212, 255, 0.1);
    }
    .dev-label { color: #555; font-size: 13px; font-weight: bold; letter-spacing: 1px; }
    .dev-value { color: #ffffff; font-size: 28px; font-weight: 900; text-shadow: 0 0 10px rgba(255,255,255,0.2); }
    
    /* تمييز Total Stay */
    .stay-box { border: 1px solid #00d4ff; background: linear-gradient(145deg, #0d0d0d, #001a1a); }
    .stay-value { color: #00d4ff; font-size: 40px; }

    /* تحسين العناوين */
    .gauge-header { color: #ffffff; font-size: 13px; font-weight: 800; text-align: center; margin-bottom: -5px; text-transform: uppercase; letter-spacing: 0.5px; }
    .section-header { color: #00d4ff; font-size: 14px; font-weight: bold; margin-bottom: 10px; border-left: 3px solid #00d4ff; padding-left: 10px; }
    
    hr { border: 0.1px solid #222; margin: 20px 0; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات (أضفت حركة بسيطة في الأرقام لمحاكاة الواقع)
data_cycle = [
    {
        "period": "3Q 2025", "falls": 0.0, "falls_m": 0.18, "injury": 0.0, "injury_m": 0.04,
        "hapi": 6.67, "hapi_m": 4.58, "restraint": 0.45, "restraint_m": 0.90,
        "clabsi": 1.50, "clabsi_m": 3.38, "cauti": 0.0, "cauti_m": 0.44,
        "vap": 1.2, "vap_m": 2.1, "vae": 1.6, "vae_m": 3.4,
        "turnover": 2.5, "turnover_m": 3.0, "nursing_hrs": 14.5, "nursing_hrs_m": 12.0,
        "edu": 85.01, "edu_m": 70.59, "cdiff": 0.0, "cdiff_m": 0.12, "mrsa": 0.0, "mrsa_m": 0.05,
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "period": "Updating Data...", "falls": 0.12, "falls_m": 0.18, "injury": 0.02, "injury_m": 0.04,
        "hapi": 5.90, "hapi_m": 4.58, "restraint": 0.50, "restraint_m": 0.90,
        "clabsi": 1.10, "clabsi_m": 3.38, "cauti": 0.2, "cauti_m": 0.44,
        "vap": 1.0, "vap_m": 2.1, "vae": 1.4, "vae_m": 3.4,
        "turnover": 2.2, "turnover_m": 3.0, "nursing_hrs": 15.1, "nursing_hrs_m": 12.0,
        "edu": 87.5, "edu_m": 70.59, "cdiff": 0.01, "cdiff_m": 0.12, "mrsa": 0.0, "mrsa_m": 0.05,
        "vents": 16, "foley": 12, "cvc": 10, "stay": 38
    }
]
d = data_cycle[st.session_state.step % len(data_cycle)]

# الهيدر الاحترافي
st.markdown(f"<h2 style='text-align: center; color: white; margin-bottom: 0;'>SYSTEM CORE INTELLIGENCE</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff; font-weight: bold;'>LIVE FEED: {d['period']}</p>", unsafe_allow_html=True)

# 4. دالة الـ Gauge بتأثير الحركة (Animation Settings)
def draw_animated_gauge(label, val, target, is_perc=False, reverse=False):
    color = "#00CC96" if (val <= target if not reverse else val >= target) else "#FF4B4B"
    st.markdown(f'<div class="gauge-header">{label}</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=val,
        number={'suffix': "%" if is_perc else "", 'font': {'size': 24, 'color': 'white'}},
        gauge={'axis': {'range': [0, max(val, target)*2], 'visible': False},
               'bar': {'color': color, 'thickness': 1},
               'bgcolor': "#111",
               'threshold': {'line': {'color': "white", 'width': 3}, 'thickness': 0.8, 'value': target}}))
    fig.update_layout(height=120, margin=dict(l=20, r=20, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)',
                      transition={'duration': 1000, 'easing': 'cubic-in-out'}) # تأرجح الأرقام
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f'<div style="text-align:center; color:#444; font-size:10px; font-weight:bold;">BENCH: {target}</div>', unsafe_allow_html=True)

# توزيع الـ 12 KPI بشكل متناسق
for row_data in [
    [("Total Falls", d['falls'], d['falls_m']), ("Injury Falls", d['injury'], d['injury_m']), ("HAPI %", d['hapi'], d['hapi_m'], True), ("Restraints", d['restraint'], d['restraint_m'])],
    [("CLABSI Rate", d['clabsi'], d['clabsi_m']), ("CAUTI Rate", d['cauti'], d['cauti_m']), ("VAP Rate", d['vap'], d['vap_m']), ("VAE Rate", d['vae'], d['vae_m'])],
    [("Turnover", d['turnover'], d['turnover_m']), ("Nursing Hrs", d['nursing_hrs'], d['nursing_hrs_m'], False, True), ("RN Edu %", d['edu'], d['edu_m'], True, True), ("C-Diff/MRSA", d['cdiff'], d['cdiff_m'])]
]:
    cols = st.columns(4)
    for i, item in enumerate(row_data):
        with cols[i]:
            draw_animated_gauge(*item)
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# 5. الجزء السفلي: الأجهزة والبار الحديث
c_left, c_right = st.columns([1, 2.5])

with c_left:
    st.markdown('<div class="section-header">ATTACHED DEVICES</div>', unsafe_allow_html=True)
    def dev_card(l, v, is_stay=False):
        cls = "dev-box stay-box" if is_stay else "dev-box"
        val_cls = "dev-value stay-value" if is_stay else "dev-value"
        st.markdown(f'<div class="{cls}"><div class="dev-label">{l}</div><div class="{val_cls}">{v}</div></div>', unsafe_allow_html=True)
    dev_card("Ventilators", d['vents'])
    dev_card("Foley Cath", d['foley'])
    dev_card("Central Line", d['cvc'])
    dev_card("Total Stay", d['stay'], True)

with c_right:
    st.markdown('<div class="section-header">PERFORMANCE DYNAMICS</div>', unsafe_allow_html=True)
    labels = ['Falls', 'HAPI', 'CLABSI', 'CAUTI', 'VAP', 'VAE']
    
    fig_bar = go.Figure()
    # بار المستشفى بتأثير Gradient/Shadow
    fig_bar.add_trace(go.Bar(
        name='Hospital Unit', x=labels, y=[d['falls'], d['hapi'], d['clabsi'], d['cauti'], d['vap'], d['vae']],
        marker=dict(color='#00d4ff', line=dict(color='#ffffff', width=1)),
        text=[d['falls'], d['hapi'], d['clabsi'], d['cauti'], d['vap'], d['vae']],
        textposition='outside', hoverinfo='y+name'
    ))
    # بار الـ Benchmark بشكل أنيق
    fig_bar.add_trace(go.Bar(
        name='National Bench', x=labels, y=[d['falls_m'], d['hapi_m'], d['clabsi_m'], d['cauti_m'], d['vap_m'], d['vae_m']],
        marker=dict(color='rgba(255, 255, 255, 0.1)', line=dict(color='#444', width=1)),
        text=[d['falls_m'], d['hapi_m'], d['clabsi_m'], d['cauti_m'], d['vap_m'], d['vae_m']],
        textposition='outside'
    ))
    
    fig_bar.update_layout(
        height=380, barmode='group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        margin=dict(l=0, r=0, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
        xaxis=dict(showgrid=False, tickfont=dict(size=12, weight='bold')),
        yaxis=dict(showgrid=True, gridcolor='#111', zeroline=False),
        transition={'duration': 800} # حركة الأعمدة عند التحديث
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# تحديث تلقائي كل 10 ثواني لخلق حركة مستمرة
time.sleep(10)
st.session_state.step += 1
st.rerun()
