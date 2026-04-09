import streamlit as st
import plotly.graph_objects as go
import time
import numpy as np

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Performance Core", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (تركيز على وضوح الخطوط والحدود الاحترافية)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; padding: 5px 15px; }
    
    /* عنوان الأجهزة الأسبوعي الصغير */
    .week-title { color: #00d4ff; font-size: 13px; font-weight: bold; text-align: left; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }

    /* كروت الأجهزة (يسار) */
    .dev-box {
        background-color: #0a0a0a; border: 1px solid #111; border-left: 4px solid #1f77b4;
        border-radius: 12px; padding: 12px; margin-bottom: 12px; text-align: center;
    }
    .dev-label { color: #aaaaaa; font-size: 13px; font-weight: bold; }
    .dev-value { color: #ffffff; font-size: 30px; font-weight: 900; }
    
    /* تمييز Total Stay */
    .stay-box { border: 1px solid #1f77b4; background: linear-gradient(145deg, #0d0d0d, #001a1a); box-shadow: 0 0 10px rgba(0, 212, 255, 0.1); }
    .stay-value { color: #00CC96; font-size: 42px; }

    /* --- تنسيق الـ 12 KPI الجديد (المربعات الاحترافية) --- */
    .kpi-card {
        background-color: #0a0a0a;
        border: 1px solid #111;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        text-align: center;
        height: 180px; /* طول ثابت للكروت */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: scale(1.02); }
    
    /* وضوح الكلام (أهم نقطة) */
    .kpi-label {
        color: #ffffff; /* أبيض ناصع */
        font-size: 16px; /* خط كبير وواضح */
        font-weight: 900; /* خط عريض جداً */
        margin-bottom: 5px;
        line-height: 1.2;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
    }
    .kpi-value { color: #ffffff; font-size: 32px; font-weight: 900; margin: 10px 0; }
    .target-text { color: #666; font-size: 13px; font-weight: bold; margin-top: 5px; }

    hr { border: 0.1px solid #111; margin: 20px 0; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات الموسعة (12 KPI) - مزامنة Q و Weekly
data_cycle = [
    {
        "period": "3Q 2025 (Period A)", "week": "WEEK 01",
        "falls": 0.0, "falls_m": 0.18, "injury": 0.0, "injury_m": 0.04,
        "hapi": 6.67, "hapi_m": 4.58, "restraint": 0.45, "restraint_m": 0.90,
        "clabsi": 1.50, "clabsi_m": 3.38, "cauti": 0.0, "cauti_m": 0.44,
        "vap": 1.2, "vae": 1.6, "turnover": 2.5, "nursing_hrs": 14.5, "edu": 85.01,
        "cdiff": 0.0, "mrsa": 0.0,
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "period": "2Q 2024 (Period B)", "week": "WEEK 02",
        "falls": 0.24, "falls_m": 0.06, "injury": 0.24, "injury_m": 0.01,
        "hapi": 14.29, "hapi_m": 6.54, "restraint": 0.70, "restraint_m": 0.96,
        "clabsi": 1.28, "clabsi_m": 2.67, "cauti": 0.70, "cauti_m": 0.99,
        "vap": 2.1, "vae": 2.17, "turnover": 3.1, "nursing_hrs": 12.8, "edu": 82.99,
        "cdiff": 0.1, "mrsa": 0.05,
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]
d = data_cycle[st.session_state.step % len(data_cycle)]

# الهيدر الأساسي
st.markdown(f"<h1 style='text-align: center; color: white;'>ICU PERFORMANCE CORE MONITOR</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff; font-weight: bold;'>PERIOD Focus: {d['period']}</p>", unsafe_allow_html=True)

# 4. دالة الـ KPI Card الجديدة (مربع ودائرة)
def draw_kpi_card(label, val, target, is_perc=False, reverse=False):
    # منطق الألوان (Traffic Lights)
    is_safe = (val <= target if not reverse else val >= target)
    color = "#00CC96" if is_safe else "#FF4B4B" # أخضر للأمان، أحمر للخطر

    # رسم الدائرة (Pie progress)
    max_val = max(val, target)*2
    if max_val == 0: max_val = 1 # لتجنب القسمة على صفر
    
    fig = go.Figure(go.Pie(
        values=[val, max(0, max_val-val)],
        hole=0.8,
        sort=False,
        marker=dict(colors=[color, "#1a1a1a"], line=dict(color="#000", width=1)),
        textinfo='none',
        hoverinfo='none',
        direction='clockwise',
        rotation=90
    ))
    fig.update_layout(height=60, width=60, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)

    # عرض الكلام بوضوح
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{val}{"%" if is_perc else ""}</div>
        <div class="target-text">Bench: {target}{"%" if is_perc else ""}</div>
    </div>
    """, unsafe_allow_html=True)
    # st.plotly_chart(fig, config={'displayModeBar': False}) # يمكن تفعيل الدائرة إذا لزم الأمر

# توزيع الـ 12 KPI (صفين × 6 كروت)
row1 = st.columns(6)
with row1[0]: draw_kpi_card("Total Falls", d['falls'], 0.18)
with row1[1]: draw_kpi_card("Injury Falls", d['injury'], 0.04)
with row1[2]: draw_kpi_card("HAPI %", d['hapi'], 4.58, True)
with row1[3]: draw_kpi_card("Restraints", d['restraint'], 0.90)
with row1[4]: draw_kpi_card("CLABSI Rate", d['clabsi'], 3.38)
with row1[5]: draw_kpi_card("CAUTI Rate", d['cauti'], 0.44)

row2 = st.columns(6)
with row2[0]: draw_kpi_card("VAP Rate", d['vap'], 2.1)
with row2[1]: draw_kpi_card("VAE Rate", d['vae'], 3.4)
with row2[2]: draw_kpi_card("Nursing Hrs", d['nursing_hrs'], 12.0, False, True)
with row2[3]: draw_kpi_card("RN Education", d['edu'], 70.59, True, True)
with row2[4]: draw_kpi_card("C-Difficle", d['cdiff'], 0.12)
with row2[5]: draw_kpi_card("MRSA Rate", d['mrsa'], 0.05)

st.markdown("<hr>", unsafe_allow_html=True)

# 5. الجزء السفلي: الأجهزة (Weekly) والبار (Trends)
c_left, c_right = st.columns([1, 2.5])

with c_left:
    st.markdown(f'<div class="week-title">ATTACHED DEVICES ({d["week"]})</div>', unsafe_allow_html=True)
    def dev_card(l, v, is_stay=False):
        style = "dev-box stay-box" if is_stay else "dev-box"
        val_style = "dev-value stay-value" if is_stay else "dev-value"
        st.markdown(f'<div class="{style}"><div class="dev-label">{l}</div><div class="{val_style}">{v}</div></div>', unsafe_allow_html=True)
    dev_card("Ventilators", d['vents'])
    dev_card("Foley Cath", d['foley'])
    dev_card("Central Line", d['cvc'])
    dev_card("Total Stay", d['stay'], True)

with c_right:
    st.markdown(f'<p style="color:#666; font-weight:bold; font-size:12px;">PERFORMANCE TRENDS (Q-Sync)</p>', unsafe_allow_html=True)
    # بار تشارت احترافي بتبادل ألوان
    labels = ['Falls', 'HAPI', 'CLABSI', 'CAUTI', 'VAP', 'VAE']
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name=f'Unit ({d["period"]})', x=labels, y=[d['falls'], d['hapi'], d['clabsi'], d['cauti'], d['vap'], d['vae']],
        marker=dict(color='#00D4FF'), text=[d['falls'], d['hapi'], d['clabsi'], d['cauti'], d['vap'], d['vae']], textposition='outside'
    ))
    fig_bar.add_trace(go.Bar(
        name='Benchmark', x=labels, y=[0.18, 4.58, 3.38, 0.44, 2.1, 3.4],
        marker=dict(color='#222'), text=[0.18, 4.58, 3.38, 0.44, 2.1, 3.4], textposition='outside'
    ))
    fig_bar.update_layout(height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font=dict(color='white'), margin=dict(l=0, r=0, t=10, b=0),
                          legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),
                          xaxis=dict(tickfont=dict(size=14, weight='bold')))
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي كل 15 ثانية (Quarterly & Weekly Sync)
time.sleep(15)
st.session_state.step += 1
st.rerun()
