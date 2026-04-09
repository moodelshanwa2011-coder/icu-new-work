import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Elite Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS الاحترافي
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; padding: 10px 20px; }
    
    .section-title { color: #888; font-size: 14px; font-weight: bold; text-align: left; margin-bottom: 10px; letter-spacing: 1.5px; text-transform: uppercase; }

    .dev-box {
        background-color: #0a0a0a;
        border: 1px solid #1f77b4;
        border-left: 5px solid #00d4ff;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 18px;
        text-align: center;
    }
    .dev-label { color: #aaaaaa; font-size: 14px; font-weight: bold; }
    .dev-value { color: #ffffff; font-size: 32px; font-weight: 900; }
    
    .stay-box { border-left: 5px solid #00CC96; background-color: #0d0d0d; }
    .stay-value { color: #00CC96; font-size: 45px; }

    .gauge-header { color: #ffffff; font-size: 18px; font-weight: bold; text-align: center; margin-bottom: -15px; }
    .bench-label { color: #666; font-size: 14px; font-weight: bold; text-align: center; }

    hr { border: 0.1px solid #222; margin: 30px 0; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات
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

# العنوان
st.markdown(f"<h1 style='text-align: center; color: white;'>ICU COMMAND CENTER | {d['period']}</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 4. الـ KPIs (Gauges)
def draw_smart_gauge(label, val, target, is_perc=False, is_edu=False):
    color = "#00CC96" if (val <= target if not is_edu else val >= target) else "#FF4B4B"
    st.markdown(f'<div class="gauge-header">{label}</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=val,
        number={'suffix': "%" if is_perc else "", 'font': {'size': 30, 'color': 'white'}},
        gauge={'axis': {'range': [0, max(val, target)*1.8], 'visible': False},
               'bar': {'color': color, 'thickness': 0.8},
               'bgcolor': "#111",
               'threshold': {'line': {'color': "white", 'width': 3}, 'thickness': 0.8, 'value': target}}))
    fig.update_layout(height=150, margin=dict(l=35, r=35, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f'<div class="bench-label">Benchmark: {target}</div>', unsafe_allow_html=True)

cols1 = st.columns(4)
with cols1[0]: draw_smart_gauge("Total Falls", d['falls'], d['falls_m'])
with cols1[1]: draw_smart_gauge("Injury Falls", d['injury'], d['injury_m'])
with cols1[2]: draw_smart_gauge("HAPI %", d['hapi'], d['hapi_m'], is_perc=True)
with cols1[3]: draw_smart_gauge("RN Education", d['edu'], d['edu_m'], is_perc=True, is_edu=True)

st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

cols2 = st.columns(4)
with cols2[0]: draw_smart_gauge("Restraints", d['restraint'], d['restraint_m'])
with cols2[1]: draw_smart_gauge("CLABSI Rate", d['clabsi'], d['clabsi_m'])
with cols2[2]: draw_smart_gauge("CAUTI Rate", d['cauti'], d['cauti_m'])
with cols2[3]: draw_smart_gauge("VAE/VAP", d['vae'], d['vae_m'])

st.markdown("<hr>", unsafe_allow_html=True)

# 5. الجزء السفلي: الأجهزة (يسار) والبار تشارت (يمين)
col_left, col_right = st.columns([1, 2.8])

with col_left:
    st.markdown('<div class="section-title">CURRENT ATTACHED DEVICES</div>', unsafe_allow_html=True)
    def dev_card(l, v, is_stay=False):
        style = "dev-box stay-box" if is_stay else "dev-box"
        val_style = "dev-value stay-value" if is_stay else "dev-value"
        st.markdown(f'<div class="{style}"><div class="dev-label">{l}</div><div class="{val_style}">{v}</div></div>', unsafe_allow_html=True)
    
    dev_card("Ventilators", d['vents'])
    dev_card("Foley Catheter", d['foley'])
    dev_card("Central Line", d['cvc'])
    dev_card("Total Stay", d['stay'], is_stay=True)

with col_right:
    st.markdown('<div class="section-title">KPI PERFORMANCE ANALYSIS</div>', unsafe_allow_html=True)
    labels = ['Falls', 'Injury', 'Restraint', 'CLABSI', 'CAUTI', 'VAE']
    
    fig_bar = go.Figure()
    # أعمدة المستشفى الحالي (Neon Green الآن)
    fig_bar.add_trace(go.Bar(
        name='Current Unit', x=labels, y=[d['falls'], d['injury'], d['restraint'], d['clabsi'], d['cauti'], d['vae']],
        marker=dict(color='#00FF00', line=dict(color='#ffffff', width=1)), # Green
        text=[d['falls'], d['injury'], d['restraint'], d['clabsi'], d['cauti'], d['vae']], textposition='outside'
    ))
    # أعمدة الـ Benchmark (Neon Pink الآن)
    fig_bar.add_trace(go.Bar(
        name='NDNQI Benchmark', x=labels, y=[d['falls_m'], d['injury_m'], d['restraint_m'], d['clabsi_m'], d['cauti_m'], d['vae_m']],
        marker=dict(color='#FF007F', line=dict(color='#ffffff', width=1)), # Pink
        text=[d['falls_m'], d['injury_m'], d['restraint_m'], d['clabsi_m'], d['cauti_m'], d['vae_m']], textposition='outside'
    ))
    
    fig_bar.update_layout(
        height=420, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(showgrid=True, gridcolor='#222', zeroline=False)
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي
time.sleep(15)
st.session_state.step += 1
st.rerun()
