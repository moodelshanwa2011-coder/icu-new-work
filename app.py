import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Comprehensive Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي مكثف
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; padding: 5px 15px; }
    .section-title { color: #666; font-size: 12px; font-weight: bold; margin-bottom: 8px; letter-spacing: 1px; text-transform: uppercase; }
    
    /* مربعات الأجهزة */
    .dev-box {
        background-color: #0a0a0a; border: 1px solid #1f77b4; border-left: 4px solid #00d4ff;
        border-radius: 8px; padding: 10px; margin-bottom: 10px; text-align: center;
    }
    .dev-label { color: #888; font-size: 12px; font-weight: bold; }
    .dev-value { color: #ffffff; font-size: 24px; font-weight: 900; }
    .stay-box { border-left: 4px solid #00d4ff; background-color: #0d0d0d; box-shadow: 0 0 10px rgba(0, 212, 255, 0.1); }
    .stay-value { color: #00d4ff; font-size: 35px; }

    /* وضوح أسماء الـ KPIs بعد التصغير */
    .gauge-header { color: #ffffff; font-size: 14px; font-weight: bold; text-align: center; margin-bottom: -10px; height: 35px; display: flex; align-items: center; justify-content: center; }
    .bench-label { color: #444; font-size: 11px; font-weight: bold; text-align: center; margin-top: -5px; }

    hr { border: 0.1px solid #222; margin: 15px 0; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات الموسعة (12 KPI)
data_cycle = [
    {
        "period": "3Q 2025",
        "falls": 0.0, "falls_m": 0.18, "injury": 0.0, "injury_m": 0.04,
        "hapi": 6.67, "hapi_m": 4.58, "restraint": 0.45, "restraint_m": 0.90,
        "clabsi": 1.50, "clabsi_m": 3.38, "cauti": 0.0, "cauti_m": 0.44,
        "vap": 1.2, "vap_m": 2.1, "vae": 1.6, "vae_m": 3.4,
        "turnover": 2.5, "turnover_m": 3.0, "nursing_hrs": 14.5, "nursing_hrs_m": 12.0,
        "edu": 85.01, "edu_m": 70.59, "cdiff": 0.0, "cdiff_m": 0.12, "mrsa": 0.0, "mrsa_m": 0.05,
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    }
]
d = data_cycle[0] # نستخدم نفس الدورة للتبسيط

# --- الهيدر ---
st.markdown(f"<h3 style='text-align: center; color: white; margin-top: -10px;'>ICU FULL CLINICAL INDICATORS | {d['period']}</h3>", unsafe_allow_html=True)

# 4. دالة الـ Gauge المصغرة
def draw_mini_gauge(label, val, target, is_perc=False, reverse=False):
    # reverse=True للمؤشرات التي يفضل فيها الرقم العالي (مثل التعليم أو ساعات التمريض)
    color = "#00CC96" if (val <= target if not reverse else val >= target) else "#FF4B4B"
    st.markdown(f'<div class="gauge-header">{label}</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=val,
        number={'suffix': "%" if is_perc else "", 'font': {'size': 20, 'color': 'white'}},
        gauge={'axis': {'range': [0, max(val, target)*2], 'visible': False},
               'bar': {'color': color, 'thickness': 0.8},
               'bgcolor': "#111",
               'threshold': {'line': {'color': "white", 'width': 2}, 'thickness': 0.8, 'value': target}}))
    fig.update_layout(height=110, margin=dict(l=20, r=20, t=5, b=5), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f'<div class="bench-label">B: {target}</div>', unsafe_allow_html=True)

# توزيع الـ 12 KPI (3 صفوف × 4 أعمدة)
row1 = st.columns(4)
with row1[0]: draw_mini_gauge("Total Falls", d['falls'], d['falls_m'])
with row1[1]: draw_mini_gauge("Injury Falls", d['injury'], d['injury_m'])
with row1[2]: draw_mini_gauge("HAPI %", d['hapi'], d['hapi_m'], True)
with row1[3]: draw_mini_gauge("Restraints", d['restraint'], d['restraint_m'])

row2 = st.columns(4)
with row2[0]: draw_mini_gauge("CLABSI Rate", d['clabsi'], d['clabsi_m'])
with row2[1]: draw_mini_gauge("CAUTI Rate", d['cauti'], d['cauti_m'])
with row2[2]: draw_mini_gauge("VAP Rate", d['vap'], d['vap_m'])
with row2[3]: draw_mini_gauge("VAE Rate", d['vae'], d['vae_m'])

row3 = st.columns(4)
with row3[0]: draw_mini_gauge("Turnover", d['turnover'], d['turnover_m'])
with row3[1]: draw_mini_gauge("Nursing Hrs", d['nursing_hrs'], d['nursing_hrs_m'], False, True)
with row3[2]: draw_mini_gauge("RN Edu %", d['edu'], d['edu_m'], True, True)
with row3[3]: draw_mini_gauge("C-Diff / MRSA", d['cdiff'], d['cdiff_m'])

st.markdown("<hr>", unsafe_allow_html=True)

# 5. الجزء السفلي: الأجهزة والبار
c_left, c_right = st.columns([1, 2.8])

with c_left:
    st.markdown('<div class="section-title">CURRENT ATTACHED DEVICES</div>', unsafe_allow_html=True)
    def dev_card(l, v, is_stay=False):
        style = "dev-box stay-box" if is_stay else "dev-box"
        val_style = "dev-value stay-value" if is_stay else "dev-value"
        st.markdown(f'<div class="{style}"><div class="dev-label">{l}</div><div class="{val_style}">{v}</div></div>', unsafe_allow_html=True)
    dev_card("Ventilators", d['vents'])
    dev_card("Foley Catheter", d['foley'])
    dev_card("Central Line", d['cvc'])
    dev_card("Total Stay", d['stay'], True)

with c_right:
    st.markdown('<div class="section-title">TREND ANALYSIS (UNIT vs BENCH)</div>', unsafe_allow_html=True)
    # اخترت أهم 6 مؤشرات للبار تشارت لمنع الازدحام
    labels = ['Falls', 'HAPI', 'CLABSI', 'CAUTI', 'VAP', 'VAE']
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name='Unit', x=labels, y=[d['falls'], d['hapi'], d['clabsi'], d['cauti'], d['vap'], d['vae']],
        marker=dict(color='#00D4FF'), text=[d['falls'], d['hapi'], d['clabsi'], d['cauti'], d['vap'], d['vae']], textposition='outside'
    ))
    fig_bar.add_trace(go.Bar(
        name='Bench', x=labels, y=[d['falls_m'], d['hapi_m'], d['clabsi_m'], d['cauti_m'], d['vap_m'], d['vae_m']],
        marker=dict(color='#E0E0E0'), text=[d['falls_m'], d['hapi_m'], d['clabsi_m'], d['cauti_m'], d['vap_m'], d['vae_m']], textposition='outside'
    ))
    fig_bar.update_layout(height=350, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font=dict(color='white'), margin=dict(l=0, r=0, t=10, b=0),
                          legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"))
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

time.sleep(15)
st.rerun()
