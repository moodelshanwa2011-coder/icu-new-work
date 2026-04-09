import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="ICU Clinical Intelligence", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (تركيز على هوية بصرية موحدة)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; padding: 5px 20px; }
    
    /* مربعات الأجهزة - طابع أسبوعي */
    .dev-box {
        background-color: #0a0a0a; border: 1px solid #1f77b4; border-left: 5px solid #00d4ff;
        border-radius: 12px; padding: 15px; margin-bottom: 15px; text-align: center;
    }
    .dev-label { color: #888; font-size: 13px; font-weight: bold; }
    .dev-value { color: #ffffff; font-size: 30px; font-weight: 900; }
    .week-tag { color: #00d4ff; font-size: 12px; font-weight: bold; margin-bottom: 5px; display: block; }
    
    /* تمييز Total Stay */
    .stay-box { border: 1px solid #00d4ff; background: linear-gradient(145deg, #0d0d0d, #001a1a); }
    .stay-value { color: #00d4ff; font-size: 42px; }

    /* وضوح الـ KPIs */
    .gauge-header { color: #ffffff; font-size: 15px; font-weight: 800; text-align: center; margin-bottom: -10px; height: 35px; }
    .bench-label { color: #444; font-size: 11px; font-weight: bold; text-align: center; margin-top: -5px; }

    hr { border: 0.1px solid #222; margin: 20px 0; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات المزدوجة (PDF Quarters & Weekly Images)
# هنا دمجنا بيانات الـ PDF مع بيانات الصور الأسبوعية
data_cycle = [
    {
        "quarter": "3Q 2025", "week": "WEEK 01",
        "falls": 0.0, "falls_m": 0.18, "injury": 0.0, "injury_m": 0.04,
        "hapi": 6.67, "hapi_m": 4.58, "restraint": 0.45, "restraint_m": 0.90,
        "clabsi": 1.50, "clabsi_m": 3.38, "cauti": 0.0, "cauti_m": 0.44,
        "vap": 1.2, "vae": 1.6, "turnover": 2.5, "nursing_hrs": 14.5, "edu": 85.01,
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "quarter": "2Q 2024", "week": "WEEK 02",
        "falls": 0.24, "falls_m": 0.06, "injury": 0.24, "injury_m": 0.01,
        "hapi": 14.29, "hapi_m": 6.54, "restraint": 0.70, "restraint_m": 0.96,
        "clabsi": 1.28, "clabsi_m": 2.67, "cauti": 0.70, "cauti_m": 0.99,
        "vap": 2.1, "vae": 2.17, "turnover": 3.1, "nursing_hrs": 12.8, "edu": 82.99,
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]
d = data_cycle[st.session_state.step % len(data_cycle)]

# الهيدر الأساسي (Quarterly Focus)
st.markdown(f"<h2 style='text-align: center; color: white; margin-bottom: 0;'>ICU PERFORMANCE COMMAND CENTER</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff; font-weight: bold;'>PERIOD: {d['quarter']}</p>", unsafe_allow_html=True)

# 4. توزيع 12 KPI (بيانات الـ PDF)
def draw_animated_gauge(label, val, target, is_perc=False, reverse=False):
    color = "#00CC96" if (val <= target if not reverse else val >= target) else "#FF4B4B"
    st.markdown(f'<div class="gauge-header">{label}</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=val,
        number={'suffix': "%" if is_perc else "", 'font': {'size': 24, 'color': 'white'}},
        gauge={'axis': {'range': [0, max(val, target)*2], 'visible': False},
               'bar': {'color': color, 'thickness': 0.8},
               'bgcolor': "#111",
               'threshold': {'line': {'color': "white", 'width': 3}, 'thickness': 0.8, 'value': target}}))
    fig.update_layout(height=110, margin=dict(l=20, r=20, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)',
                      transition={'duration': 1000})
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# صفوف الـ KPIs
rows = [
    [("Total Falls", d['falls'], 0.18), ("Injury Falls", d['injury'], 0.04), ("HAPI %", d['hapi'], 4.58, True), ("Restraints", d['restraint'], 0.90)],
    [("CLABSI Rate", d['clabsi'], 3.38), ("CAUTI Rate", d['cauti'], 0.44), ("VAP Rate", d['vap'], 2.1), ("VAE Rate", d['vae'], 3.4)],
    [("Turnover", d['turnover'], 3.0), ("Nursing Hrs", d['nursing_hrs'], 12.0, False, True), ("RN Edu %", d['edu'], 70.59, True, True), ("C-Diff/MRSA", 0.0, 0.12)]
]

for row in rows:
    cols = st.columns(4)
    for i, item in enumerate(row):
        with cols[i]: draw_animated_gauge(*item)

st.markdown("<hr>", unsafe_allow_html=True)

# 5. الجزء السفلي: الأجهزة (Weekly) والبار (Trends)
c_left, c_right = st.columns([1, 2.8])

with c_left:
    st.markdown(f'<p style="color:#00d4ff; font-weight:bold; font-size:12px;">CURRENT ATTACHED DEVICES ({d["week"]})</p>', unsafe_allow_html=True)
    def dev_card(l, v, is_stay=False):
        cls = "dev-box stay-box" if is_stay else "dev-box"
        val_cls = "dev-value stay-value" if is_stay else "dev-value"
        st.markdown(f'<div class="{cls}"><div class="dev-label">{l}</div><div class="{val_cls}">{v}</div></div>', unsafe_allow_html=True)
    dev_card("Ventilators", d['vents'])
    dev_card("Foley Cath", d['foley'])
    dev_card("Central Line", d['cvc'])
    dev_card("Total Stay", d['stay'], True)

with c_right:
    st.markdown(f'<p style="color:#666; font-weight:bold; font-size:12px;">QUARTERLY PERFORMANCE TRENDS</p>', unsafe_allow_html=True)
    labels = ['Falls', 'HAPI', 'CLABSI', 'CAUTI', 'VAP', 'VAE']
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name=f'Unit ({d["quarter"]})', x=labels, y=[d['falls'], d['hapi'], d['clabsi'], d['cauti'], d['vap'], d['vae']],
        marker=dict(color='#00D4FF'), text=[d['falls'], d['hapi'], d['clabsi'], d['cauti'], d['vap'], d['vae']], textposition='outside'
    ))
    fig_bar.add_trace(go.Bar(
        name='Benchmark', x=labels, y=[0.18, 4.58, 3.38, 0.44, 2.1, 3.4],
        marker=dict(color='rgba(255, 255, 255, 0.1)', line=dict(color='#444', width=1)),
        text=[0.18, 4.58, 3.38, 0.44, 2.1, 3.4], textposition='outside'
    ))
    
    fig_bar.update_layout(height=380, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font=dict(color='white'), margin=dict(l=0, r=0, t=10, b=0),
                          legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
                          transition={'duration': 1000})
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي كل 15 ثانية (Quarterly & Weekly Sync)
time.sleep(15)
st.session_state.step += 1
st.rerun()
